#!/usr/bin/env python3
r"""check_artifact_health.py — is a recorded eval run still what the code produces?

Usage:
  check_artifact_health.py evals/runs/<run-id> [...]      # one or more runs
  check_artifact_health.py --all                          # every run

WHY THIS EXISTS
A recorded run is a snapshot. The code moves on: 35 fixes landed while 150 tasks
were being generated, and afterwards a third of the stored artifacts carried the
shape of a bug rather than a bug. They still compiled, every gate still passed,
and the documents were quietly worse than what the same skill would produce
today — dead workarounds for fixed faults, answer blanks printed above their
work space, headings overflowing a budget that did not exist when they were
written.

None of that is visible from a gate log, because the gate log records the run
that passed, not the run that would pass now. So this walks a stored run and
asks a different question: does this artifact still look like current output?

WHAT IT REPORTS
  workaround   a defensive edit for a fault since fixed — the artifact is
               degraded by code that no longer needs to exist
  defect       a printed fault no gate catches (answer blank above the work
               space) or one a newer gate would now catch
  gap          content a reference file could now supply (an untagged problem
               where a standards row has since been added)

Exit 0 when the run matches current output, 1 when anything is stale. Findings
are advisory in the sense that a stale artifact is not WRONG — it passed
honestly when it was made — but a run handed to a judge should represent what
the skill does now, or the score measures history.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tests"))
SUITE = os.path.join(ROOT, "evals", "curriculum-suite-500.json")
STANDARDS = os.path.join(ROOT, "references", "standards-map.md")
SKILLHEADING_BUDGET = 57


def problem_spans(tex):
    """(opt_arg, body) for each \\problem, brace-matched."""
    out = []
    for m in re.finditer(r"\\problem(\[[^\]]*\])?\{", tex):
        i, depth = m.end(), 1
        while i < len(tex) and depth:
            depth += (tex[i] == "{") - (tex[i] == "}")
            i += 1
        out.append((m.group(1), tex[m.end():i - 1]))
    return out


def visible_len(title):
    t = re.sub(r"\\[a-zA-Z]+\s*", "x", title)
    return len(t.replace("$", "").replace("{", "").replace("}", "").strip())


def check_task(d, task):
    """Findings for one recorded task directory."""
    found = []
    vp = os.path.join(d, "verify.json")
    if not os.path.isfile(vp):
        return [("defect", "no verify.json recorded")]
    try:
        problems = json.load(open(vp, encoding="utf-8")).get("problems", [])
    except json.JSONDecodeError as exc:
        return [("defect", f"verify.json will not parse: {exc}")]

    untagged = sum(1 for p in problems if "standard" not in p)
    if untagged:
        found.append(("gap", f"{untagged}/{len(problems)} problems carry no "
                             f"'standard' — check standards-map.md for a row "
                             f"added since this was recorded"))
    if task and task.get("instructional_mode") == "misconception-analysis" \
            and not sum(len(p.get("traps") or []) for p in problems):
        found.append(("gap", "a misconception-analysis task declaring no traps — "
                             "traps were once unusable; they work now"))

    for doc, label in (("worksheet", "ws"), ("answer_key", "ak"),
                       ("study_guide", "ss")):
        p = os.path.join(d, f"{doc}.tex")
        if not os.path.isfile(p):
            continue
        tex = open(p, encoding="utf-8").read()
        # A defensive edit for a fault that is fixed. Harmless to compile,
        # but it loosens lines the engine could otherwise set tightly.
        if "emergencystretch" in tex:
            found.append(("workaround", f"{label}: \\emergencystretch — added for "
                                        f"the \\commonerror overflow, since fixed"))
        if re.search(r"\{\\raggedright[^}]*qa_|\\raggedright\s*\\input\{qa_", tex):
            found.append(("workaround", f"{label}: \\raggedright around the quick-"
                                        f"answer bank — same fixed overflow"))
        # Match the ADDPLOT, not the bare phrase: a repair agent had to spell
        # "only-marks" in its explanatory comments to avoid tripping the literal
        # string, which means a comment could raise a false alarm and a
        # rephrasing could hide a real one. The option only matters inside
        # \addplot[...], so look there.
        if re.search(r"\\addplot\s*\[[^\]]*only\s+marks", tex):
            found.append(("defect", f"{label}: \\addplot[only marks] layered on a "
                                    f"function plot — types a stray 0.1pt in "
                                    f"nullfont on some `samples` values; use \\fill"))
        # \problem typesets the stem and only THEN the workspace, so an
        # \answerline inside the stem prints the blank ABOVE the blank paper.
        for opt, body in problem_spans(tex):
            if opt and "\\answerline" in body:
                found.append(("defect", f"{label}: \\answerline inside "
                                        f"\\problem[{opt[1:-1]}] — the answer blank "
                                        f"prints above the work space"))
                break
        for m in re.finditer(r"\\skillheading\{([^{}]*)\}", tex):
            n = visible_len(m.group(1))
            if n > SKILLHEADING_BUDGET:
                found.append(("defect", f"{label}: \\skillheading is {n} chars "
                                        f"(budget {SKILLHEADING_BUDGET}) — overfull"))
                break
    return found


def check_run(run_dir, suite):
    tasks_dir = os.path.join(run_dir, "tasks")
    if not os.path.isdir(tasks_dir):
        print(f"  not a run directory: {run_dir}", file=sys.stderr)
        return 1, 0
    stale = 0
    total = 0
    for tid in sorted(os.listdir(tasks_dir)):
        total += 1
        findings = check_task(os.path.join(tasks_dir, tid), suite.get(tid))
        if findings:
            stale += 1
            print(f"  {tid}")
            for kind, msg in findings:
                print(f"      [{kind}] {msg}")
    return stale, total


def main(argv):
    argv = list(argv)
    runs_root = os.path.join(ROOT, "evals", "runs")
    if "--all" in argv:
        argv.remove("--all")
        argv += [os.path.join(runs_root, d) for d in sorted(os.listdir(runs_root))
                 if os.path.isfile(os.path.join(runs_root, d, "run.json"))]
    if not argv:
        print(__doc__.strip().splitlines()[2], file=sys.stderr)
        return 2
    suite = {}
    if os.path.isfile(SUITE):
        suite = {t["id"]: t for t in
                 json.load(open(SUITE, encoding="utf-8"))["tasks"]}

    stale = total = 0
    for run in argv:
        print(f"\n{os.path.basename(run)}")
        s, t = check_run(run, suite)
        stale += s
        total += t
        if not s:
            print("  ✅ every recorded artifact matches current output")
    print()
    if stale:
        print(f"❌ {stale} of {total} recorded task(s) are stale against the "
              f"current code.\n   They passed honestly when made; they are not "
              f"what the skill produces now.\n   Repair the deterministic classes "
              f"with evals/repair_artifacts.py, and\n   regenerate the rest before "
              f"handing the run to a judge.")
        return 1
    print(f"✅ all {total} recorded artifacts match what the current code produces")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
