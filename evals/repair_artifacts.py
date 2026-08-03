#!/usr/bin/env python3
"""repair_artifacts.py — re-gate stored eval artifacts after a checker fix.

Usage:
  repair_artifacts.py --run RUN_ID TASK_ID [TASK_ID ...] [--dry-run]

WHY THIS AND NOT ANOTHER AGENT
Some faults leave a deterministic mark on the artifact, and a deterministic mark
takes a deterministic fix. Re-asking an agent to rewrite the whole worksheet
would re-roll every unrelated choice it made — different problems, different
numbers, different prose — so the regenerated set would no longer be comparable
with the rest of the run, and the diff would hide the repair inside a rewrite.
These transforms change exactly the thing the bug caused and nothing else, then
put the result back through the full gate chain, which is the same standard the
original had to meet.

Agent regeneration is still right when the repair needs judgement — choosing a
standards code, redesigning a figure. This handles the cases where it does not.

TRANSFORMS
  answerline-in-problem
      \\problem[Ncm]{stem ... \\answerline{u}}  ->
      \\problem{stem ... \\par\\vspace*{Ncm}\\answerline{u}}
      \\problem typesets the stem and only THEN emits the workspace, so an
      \\answerline written inside the stem printed the answer blank ABOVE the
      blank paper. No gate sees it; an agent found it by rendering a page.
  overlong-skillheading
      Drops the parenthesised JSON slug from a \skillheading over the
      57-character budget. Sheets built before that gate existed carry real
      overfull hboxes in the study guide; the coverage gate reads the JSON tag,
      never the printed title, so nothing bound to it changes.
  dead-emergencystretch
      Drops \\setlength{\\emergencystretch}{...} from an answer key. It was added
      to survive the \\commonerror overflow, which is fixed; left in place it
      loosens lines the engine could set tightly.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, "evals", "runs")
WORK = "/tmp/evalrepair2"
DOCS = {"worksheet": "ws", "answer_key": "ak", "study_guide": "ss"}


def problem_spans(tex):
    """(start, opt_arg, body_start, body_end) for each \\problem, brace-matched."""
    out = []
    for m in re.finditer(r"\\problem(\[[^\]]*\])?\{", tex):
        i, depth = m.end(), 1
        while i < len(tex) and depth:
            depth += (tex[i] == "{") - (tex[i] == "}")
            i += 1
        out.append((m.start(), m.group(1), m.end(), i - 1))
    return out


def fix_answerline(tex):
    """Move the workspace ahead of an \\answerline written inside the stem."""
    changed = 0
    for start, opt, b0, b1 in reversed(problem_spans(tex)):
        if not opt or "\\answerline" not in tex[b0:b1]:
            continue
        dim = opt[1:-1]
        body = tex[b0:b1]
        # Put the space immediately before the answer line, and drop the
        # optional argument so \problem does not ALSO emit it afterwards.
        body = re.sub(r"(\s*)(\\answerline)", r"\\par\\vspace*{%s}\1\2" % dim,
                      body, count=1)
        tex = tex[:start] + "\\problem{" + body + "}" + tex[b1 + 1:]
        changed += 1
    return tex, changed


def fix_emergencystretch(tex):
    new = re.sub(r"^.*\\setlength\{\\emergencystretch\}\{[^}]*\}.*\n", "",
                 tex, flags=re.M)
    # drop an orphaned explanatory comment block left behind above it
    new = re.sub(r"^% [^\n]*[Cc]ommon wrong answers[^\n]*\n"
                 r"(?:^% [^\n]*\n)*", "", new, flags=re.M)
    return new, int(new != tex)


def fix_skillheading(tex):
    """Drop the parenthesised JSON slug from an over-length \skillheading.

    Sheets built before the 57-character budget gate existed carry headings that
    overflow the study-guide text block — a real overfull hbox that shipped
    because nothing checked it. The documented cause is echoing the JSON skill
    slug in parentheses, and the coverage gate reads the tag rather than the
    printed title, so removing it changes nothing the gates bind to.
    """
    changed = 0

    def shorten(m):
        nonlocal changed
        title = m.group(1)
        if len(re.sub(r"\\[a-zA-Z]+\s*", "x", title).strip()) <= 57:
            return m.group(0)
        stripped = re.sub(r"\s*\([a-z0-9-]+\)\s*$", "", title)
        if stripped != title:
            changed += 1
            return "\\skillheading{" + stripped + "}"
        return m.group(0)

    return re.sub(r"\\skillheading\{([^{}]*)\}", shorten, tex), changed


TRANSFORMS = {"worksheet": [("answerline-in-problem", fix_answerline)],
              "answer_key": [("dead-emergencystretch", fix_emergencystretch)],
              "study_guide": [("overlong-skillheading", fix_skillheading)]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("tasks", nargs="+")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--rebuild", action="store_true",
                    help="rebuild and re-record even when no transform applies "
                         "— use after a change to the shared preamble, which "
                         "alters every document without touching any .tex")
    a = ap.parse_args()
    run_dir = os.path.join(RUNS, a.run)
    if not os.path.isfile(os.path.join(run_dir, "run.json")):
        print(f"error: not a run: {run_dir}", file=sys.stderr)
        return 2

    ok, failed, skipped = [], [], []
    for tid in a.tasks:
        src = os.path.join(run_dir, "tasks", tid)
        if not os.path.isfile(os.path.join(src, "verify.json")):
            skipped.append((tid, "no stored verify.json"))
            continue
        d = os.path.join(WORK, tid)
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
        stem = f"r_{tid.replace('-', '')}"
        shutil.copy(os.path.join(src, "verify.json"), f"{d}/verify_{stem}.json")
        ss = os.path.join(src, "verify_study_guide.json")
        if os.path.isfile(ss):
            shutil.copy(ss, f"{d}/verify_ss_{stem}.json")

        applied = []
        for doc, role in DOCS.items():
            p = os.path.join(src, f"{doc}.tex")
            if not os.path.isfile(p):
                skipped.append((tid, f"missing {doc}.tex"))
                break
            tex = open(p, encoding="utf-8").read()
            for name, fn in TRANSFORMS[doc]:
                tex, n = fn(tex)
                if n:
                    applied.append(f"{name}×{n}")
            # the quick-answer bank is regenerated per build under the new stem
            tex = re.sub(r"\\input\{qa_[^}]*\}", f"\\\\input{{qa_{stem}}}", tex)
            open(f"{d}/{role}_{stem}.tex", "w", encoding="utf-8").write(tex)
        else:
            if not applied and not a.rebuild:
                skipped.append((tid, "nothing to repair"))
                continue
            if not applied:
                applied = ["rebuild (shared preamble changed)"]
            if a.dry_run:
                ok.append((tid, ", ".join(applied) + " (dry run)"))
                continue
            log = f"{d}/gate_log.txt"
            with open(log, "w") as fh:
                r = subprocess.run(
                    ["bash", os.path.join(ROOT, "scripts", "build.sh"),
                     f"{d}/verify_{stem}.json", "--outdir", d],
                    stdout=fh, stderr=subprocess.STDOUT, cwd=ROOT)
            # build.sh exits 2 when a verification run flagged manual-review
            # items — that is a PASS with honest manual encoding, not a failure.
            if r.returncode not in (0, 2):
                failed.append((tid, f"build exit {r.returncode} — see {log}"))
                continue
            # Carry the original delivery response into the BUILD dir first:
            # recording reads it from there and writes it back into the task
            # dir, and passing the task dir's own copy makes source and
            # destination the same file.
            resp = os.path.join(src, "final_response.md")
            staged = os.path.join(d, "final_response.md")
            if os.path.isfile(resp):
                shutil.copy(resp, staged)
            cmd = ["python3", os.path.join(ROOT, "evals", "run_eval.py"), "record",
                   tid, "--run", a.run, "--from", d,
                   "--generator-model", "claude-opus-5",
                   "--notes", "artifact repair: " + ", ".join(applied)]
            if os.path.isfile(staged):
                cmd += ["--response-file", staged]
            rec = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
            if rec.returncode != 0:
                failed.append((tid, f"record failed: {rec.stderr.strip()[:120]}"))
            else:
                ok.append((tid, ", ".join(applied)))

    for tid, what in ok:
        print(f"  ✅ {tid}: {what}")
    for tid, why in skipped:
        print(f"  ·  {tid}: {why}")
    for tid, why in failed:
        print(f"  ❌ {tid}: {why}")
    print(f"\nrepaired {len(ok)} · skipped {len(skipped)} · failed {len(failed)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
