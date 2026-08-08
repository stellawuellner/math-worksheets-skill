#!/usr/bin/env python3
"""run_eval.py — scaffold, capture and package an eval run for an OUTSIDE judge.

Usage:
  run_eval.py start   --suite curriculum --shard 1 [--shard-size 25]
                      --generator-agent NAME --generator-model NAME [--label TEXT]
  run_eval.py next    [--run ID]                 # next unrecorded task + prompt
  run_eval.py record  TASK_ID --from DIR [--run ID] [--response-file F]
                      [--latency-seconds N] [--notes TEXT]
  run_eval.py status  [--run ID]
  run_eval.py package [--run ID]                 # validate + write the judge brief

WHY A HARNESS AND NOT A FOLDER CONVENTION
The suite's own execution block asks for a clean workspace per task, retention of
nine specific things, and a judge kept blind to model identity and the generation
transcript. Every one of those is a rule someone forgets at task 40 of 500. Here
they are mechanical: `record` captures the retention list or fails, `package`
refuses to hand over a run with gaps, and the generator's identity is written to
the run root — never into the directory the judge is given.

THE INDEPENDENCE RULE
The point of this harness is that the model which produced a worksheet must not
be the model that scores it. That is enforced in score_eval.py by comparing the
generator recorded here against the judge recorded in the verdicts, and refusing
to aggregate when they match. It is a declaration, not a proof: it catches the
accident of pointing the same agent at both halves, which is the realistic
failure, and it cannot stop someone determined to lie about who they are.

HARNESS OBSERVATIONS ARE NOT VERDICTS
`record` computes what can be known mechanically — are three PDFs present, does
the printed problem count match the task, did the gate chain pass. These are
kept OUT of the judge packet on purpose: telling a judge "the harness thinks the
count is wrong" anchors the judgement it was asked to make independently. They
are used afterwards, in scoring, to cross-check the judge: a verdict of ACCEPT on
a task whose PDFs are missing says something about the judge, not the worksheet.
"""
import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, "evals", "runs")
SUITES = {
    "curriculum": os.path.join(ROOT, "evals", "curriculum-suite-500.json"),
    "capability": os.path.join(ROOT, "evals", "capability-suite.json"),
}
RUBRIC = os.path.join(ROOT, "evals", "curriculum-judge-rubric.md")

# The suite's retention list, as filenames in the task directory. Anything
# required and absent makes `package` refuse: a run with holes in it produces a
# score that quietly means something else.
REQUIRED = ("prompt.txt", "task.json", "worksheet.pdf", "answer_key.pdf",
            "study_guide.pdf", "verify.json", "gate_log.txt")
OPTIONAL = ("verify_study_guide.json", "final_response.md",
            "worksheet.tex", "answer_key.tex", "study_guide.tex")


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def die(msg, code=2):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def load(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        die(f"cannot read {path}: {exc}")


def save(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def git_commit():
    try:
        r = subprocess.run(["git", "-C", ROOT, "rev-parse", "HEAD"],
                           capture_output=True, text=True)
        return r.stdout.strip() or "unknown"
    except OSError:
        return "unknown"


def latest_run():
    if not os.path.isdir(RUNS):
        die("no runs yet — start one with `run_eval.py start`")
    runs = sorted(d for d in os.listdir(RUNS)
                  if os.path.isfile(os.path.join(RUNS, d, "run.json")))
    if not runs:
        die("no runs yet — start one with `run_eval.py start`")
    return runs[-1]


def run_dir(run_id):
    d = os.path.join(RUNS, run_id or latest_run())
    if not os.path.isfile(os.path.join(d, "run.json")):
        die(f"not a run directory: {d}")
    return d


# ----------------------------------------------------------------- start

def write_task_files(out, task):
    """prompt.txt + task.json — the two files that describe the ASK, not the answer.

    Written by `start` as well as by `record`, because a run driven by several
    agents at once has no other collision-free way for an agent to read its own
    assignment: `next` returns the next UNRECORDED task, so two agents starting
    within a minute of each other are handed the same one. Nothing here depends
    on the artifacts, and `record` rewrites both from the same source, so a
    pre-written pair cannot drift from the recorded one.

    Deliberately excludes anything about the generator — the rubric requires the
    judge be blind to model identity, and this is the directory the judge gets.
    """
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "prompt.txt"), "w", encoding="utf-8") as fh:
        fh.write(task["prompt"] + "\n")
    save(os.path.join(out, "task.json"), {
        k: task[k] for k in ("id", "band", "band_label", "domain", "topic", "focus",
                             "instructional_mode", "standard_refs",
                             "verification_targets", "review_mode", "expected")
        if k in task})


def cmd_start(a):
    if a.suite not in SUITES:
        die(f"unknown suite {a.suite!r} — one of {', '.join(sorted(SUITES))}")
    suite = load(SUITES[a.suite])
    tasks = suite["tasks"]
    if a.tasks:
        wanted = [t.strip() for t in a.tasks.split(",") if t.strip()]
        by_id = {t["id"]: t for t in tasks}
        missing = [t for t in wanted if t not in by_id]
        if missing:
            die(f"no such task(s): {', '.join(missing)}")
        selected = [by_id[t] for t in wanted]
        shard_label = "custom"
    else:
        size = a.shard_size
        lo = (a.shard - 1) * size
        if lo >= len(tasks):
            die(f"shard {a.shard} is past the end of {len(tasks)} tasks")
        selected = tasks[lo:lo + size]
        shard_label = f"{a.shard}/{-(-len(tasks) // size)}"

    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_id = f"{a.suite}-shard{a.shard if not a.tasks else 'X'}-{stamp}"
    d = os.path.join(RUNS, run_id)
    if os.path.exists(d):
        die(f"run {run_id} already exists")
    os.makedirs(os.path.join(d, "tasks"))
    os.makedirs(os.path.join(d, "verdicts"))

    save(os.path.join(d, "run.json"), {
        "run_id": run_id,
        "started": now(),
        "suite": a.suite,
        "suite_file": os.path.relpath(SUITES[a.suite], ROOT),
        "shard": shard_label,
        "repo_commit": git_commit(),
        "label": a.label or "",
        # Recorded at the run ROOT, deliberately never copied into tasks/:
        # the rubric requires the judge be blind to model identity.
        "generator": {"agent": a.generator_agent, "model": a.generator_model},
        "condition": "skill_on",
        "task_ids": [t["id"] for t in selected],
    })
    for t in selected:
        write_task_files(os.path.join(d, "tasks", t["id"]), t)

    print(f"run {run_id}")
    print(f"  {len(selected)} task(s): {selected[0]['id']}..{selected[-1]['id']}")
    print(f"  each task's prompt.txt and task.json are written now, so parallel "
          f"agents can read their own assignment without racing on `next`")
    print(f"  dir: {os.path.relpath(d, ROOT)}")
    print(f"\nNext: python3 evals/run_eval.py next")
    return 0


# ------------------------------------------------------------------ next

def suite_tasks(run):
    suite = load(os.path.join(ROOT, run["suite_file"]))
    by_id = {t["id"]: t for t in suite["tasks"]}
    return [by_id[i] for i in run["task_ids"]]


def cmd_next(a):
    d = run_dir(a.run)
    run = load(os.path.join(d, "run.json"))
    for task in suite_tasks(run):
        if not os.path.isfile(os.path.join(d, "tasks", task["id"], "result.json")):
            print(f"TASK {task['id']}  ({task['band']} · {task['topic']})")
            print(f"EXPECTED PROBLEMS: {task['expected']['worksheet_problem_count']}")
            print(f"VERIFY TARGETS: {', '.join(task.get('verification_targets', []))}")
            print(f"\n{task['prompt']}\n")
            return 0
    print("all tasks in this run are recorded — next: run_eval.py package")
    return 0


# ---------------------------------------------------------------- record

def find_one(d, pattern, what):
    hits = sorted(f for f in os.listdir(d) if re.fullmatch(pattern, f))
    if len(hits) != 1:
        return None, (f"expected exactly one {what} in {d}, found "
                      f"{len(hits)}{': ' + ', '.join(hits) if hits else ''}")
    return os.path.join(d, hits[0]), None


# A build directory holding two `verify_<stem>.json` files — the usual cause is a
# stale stem from an earlier attempt in a reused /tmp dir — used to be recorded as
# a WARNING: discovery returned nothing, no artifact was copied, `result.json` was
# written anyway with only `task_id` and `recorded`, and the run still printed a
# line beginning "recorded". Three agents in the 2026-08-06 run hit it and had to
# catch it by eye; one nearly did not. `package` would have failed the task later
# as missing-artifact, far from the cause. Discovery that cannot name the artifact
# is now fatal: nothing is written, nothing is claimed, and the exit code says so.
def record_abort(task_id, headline, detail=""):
    print(f"❌ NOT recorded: {task_id} — {headline}", file=sys.stderr)
    if detail:
        print(f"   {detail}", file=sys.stderr)
    print("   Nothing was written: no artifact copied, no observation, no\n"
          "   result.json — so this capture cannot be mistaken for a success\n"
          "   later. Build each task in its own EMPTY directory (or delete the\n"
          "   stale files), then re-run `record`.", file=sys.stderr)
    return 2


def copy_artifact(src_path, dest_path, landed, problems):
    """Copy, then CONFIRM the destination exists and is non-empty.

    `record` reports what it copied; it must not report a copy it did not make.
    A silently truncated or unwritten artifact reads downstream as a generator
    that produced nothing.
    """
    try:
        shutil.copy(src_path, dest_path)
    except OSError as exc:
        problems.append(f"copy failed: {os.path.basename(dest_path)} ({exc})")
        return False
    if not os.path.isfile(dest_path) or os.path.getsize(dest_path) == 0:
        problems.append(f"copy did not land on disk: {os.path.basename(dest_path)}")
        return False
    landed.append(os.path.basename(dest_path))
    return True


def pdf_page_count(path):
    try:
        r = subprocess.run(["pdfinfo", path], capture_output=True, text=True)
        m = re.search(r"^Pages:\s+(\d+)", r.stdout, re.M)
        return int(m.group(1)) if m else None
    except OSError:
        return None


def cmd_record(a):
    d = run_dir(a.run)
    run = load(os.path.join(d, "run.json"))
    if a.task_id not in run["task_ids"]:
        die(f"{a.task_id} is not part of run {run['run_id']}")
    task = next(t for t in suite_tasks(run) if t["id"] == a.task_id)
    src = os.path.abspath(a.source)
    if not os.path.isdir(src):
        die(f"not a directory: {src}")

    out = os.path.join(d, "tasks", a.task_id)
    problems = []
    landed = []

    # DISCOVERY FIRST, and before anything is written. Every artifact name is
    # derived from the stem of the one verify_<stem>.json in the build dir, so an
    # ambiguous stem means the whole retention list is unresolvable — there is no
    # partial record worth keeping, and writing one hides the fault.
    stem_json, err = find_one(src, r"verify_(?!ss_).+\.json", "verify_<stem>.json")
    if err:
        return record_abort(
            a.task_id, "cannot tell which verify JSON is this task's", err)

    stem = re.sub(r"^verify_|\.json$", "", os.path.basename(stem_json))
    plan = []          # (source path, destination name)
    for role, dest in (("ws", "worksheet"), ("ak", "answer_key"), ("ss", "study_guide")):
        for ext in ("pdf", "tex"):
            hits = sorted(f for f in os.listdir(src)
                          if re.fullmatch(rf"(?:[a-z]+_)?{role}[SCX]?_{re.escape(stem)}\.{ext}", f))
            if len(hits) > 1:
                return record_abort(
                    a.task_id, f"more than one {role} {ext} matches stem {stem!r}",
                    f"candidates: {', '.join(hits)}")
            if len(hits) == 1:
                plan.append((os.path.join(src, hits[0]), f"{dest}.{ext}"))
            elif ext == "pdf":
                problems.append(f"{role} pdf: found no {role}_{stem}.pdf")

    os.makedirs(out, exist_ok=True)

    # Copy the retention list, following build.sh's own naming convention so a
    # task directory is whatever the gate chain actually produced.
    copy_artifact(stem_json, os.path.join(out, "verify.json"), landed, problems)
    for src_path, dest_name in plan:
        copy_artifact(src_path, os.path.join(out, dest_name), landed, problems)
    ss_json = os.path.join(src, f"verify_ss_{stem}.json")
    if os.path.isfile(ss_json):
        copy_artifact(ss_json, os.path.join(out, "verify_study_guide.json"),
                      landed, problems)

    log = os.path.join(src, a.gate_log) if a.gate_log else None
    if log and os.path.isfile(log):
        copy_artifact(log, os.path.join(out, "gate_log.txt"), landed, problems)
    elif os.path.isfile(os.path.join(src, "gate_log.txt")):
        copy_artifact(os.path.join(src, "gate_log.txt"),
                      os.path.join(out, "gate_log.txt"), landed, problems)
    else:
        problems.append("no gate_log.txt — capture build.sh output with `| tee gate_log.txt`")

    if a.response_file:
        if not os.path.isfile(a.response_file):
            die(f"no such response file: {a.response_file}")
        copy_artifact(a.response_file, os.path.join(out, "final_response.md"),
                      landed, problems)

    # The judge gets the prompt and the task's own expectations — nothing about
    # who or what generated the artifacts.
    write_task_files(out, task)

    # Mechanical observations, kept at the run root, never in tasks/.
    verify = None
    vpath = os.path.join(out, "verify.json")
    if os.path.isfile(vpath):
        try:
            verify = json.load(open(vpath, encoding="utf-8"))
        except json.JSONDecodeError as exc:
            problems.append(f"verify.json is not parseable: {exc}")
    declared = verify.get("problem_count") if verify else None
    unique = len({p.get("id") for p in verify.get("problems", [])}) if verify else None
    expected = task["expected"]["worksheet_problem_count"]
    gate_text = ""
    gpath = os.path.join(out, "gate_log.txt")
    if os.path.isfile(gpath):
        gate_text = open(gpath, encoding="utf-8", errors="replace").read()

    # Per task, not just per run. A run may be authored by several agents, and
    # the question "how much does the driving model change the result" is only
    # answerable if every artifact carries the model that actually made it —
    # a run-level field silently averages a mixed fleet into one label.
    obs = {
        "task_id": a.task_id,
        "recorded": now(),
        "generator": {
            "agent": a.generator_agent or run["generator"]["agent"],
            "model": a.generator_model or run["generator"]["model"],
        },
        "latency_seconds": a.latency_seconds,
        "notes": a.notes or "",
        "artifacts_present": {name: os.path.isfile(os.path.join(out, name))
                              for name in REQUIRED + OPTIONAL},
        "expected_problem_count": expected,
        "declared_problem_count": declared,
        "unique_verified_problems": unique,
        "problem_count_matches": declared == expected,
        "gate_chain_passed": "BUILD PASSED" in gate_text,
        "gate_chain_manual_flags": "flagged manual-review" in gate_text,
        "worksheet_pages": pdf_page_count(os.path.join(out, "worksheet.pdf")),
        "capture_problems": problems,
    }
    save(os.path.join(out, "result.json"), {"task_id": a.task_id, "recorded": obs["recorded"]})
    obs_dir = os.path.join(d, "observations")
    save(os.path.join(obs_dir, f"{a.task_id}.json"), obs)

    flag = "⚠️ " if problems or not obs["gate_chain_passed"] or not obs["problem_count_matches"] else "✅ "
    print(f"{flag}recorded {a.task_id} [{obs['generator']['model']}]: "
          f"{declared}/{expected} problems, "
          f"gates {'passed' if obs['gate_chain_passed'] else 'DID NOT PASS'}, "
          f"{obs['worksheet_pages']} ws page(s)")
    # Name the files that are actually on disk, not the ones a copy was attempted
    # for. "copied 11 artifacts" is a claim; this is the check behind it.
    if landed:
        print(f"   {len(landed)} artifact(s) copied and confirmed on disk: "
              f"{', '.join(sorted(landed))}")
    else:
        print("   NO artifacts landed on disk")
    for p in problems:
        print(f"   • {p}")
    return 0


# ---------------------------------------------------------------- status

def cmd_status(a):
    d = run_dir(a.run)
    run = load(os.path.join(d, "run.json"))
    done, pending = [], []
    for tid in run["task_ids"]:
        (done if os.path.isfile(os.path.join(d, "tasks", tid, "result.json"))
         else pending).append(tid)
    print(f"run {run['run_id']}  ({run['suite']} shard {run['shard']})")
    print(f"  generator : {run['generator']['agent']} / {run['generator']['model']}")
    print(f"  recorded  : {len(done)}/{len(run['task_ids'])}")
    fleet = {}
    for tid in done:
        m = load(os.path.join(d, "observations", f"{tid}.json")) \
            .get("generator", {}).get("model", "?")
        fleet[m] = fleet.get(m, 0) + 1
    if fleet:
        print("  by model  : " + ", ".join(f"{m} ×{n}" for m, n in sorted(fleet.items())))
    clean = flagged = 0
    for tid in done:
        o = load(os.path.join(d, "observations", f"{tid}.json"))
        if o["capture_problems"] or not o["gate_chain_passed"] or not o["problem_count_matches"]:
            flagged += 1
        else:
            clean += 1
    print(f"  clean     : {clean}")
    if flagged:
        print(f"  flagged   : {flagged}  (see observations/, these still go to the judge)")
    if pending:
        print(f"  pending   : {', '.join(pending[:8])}{' …' if len(pending) > 8 else ''}")
    return 0


# --------------------------------------------------------------- package

JUDGE_BRIEF = """# Judging packet — run `{run_id}`

You are the independent judge for an eval of a math-worksheet generator. **You
did not produce this work and you must not be told what did.** If you know or
can infer which model generated these artifacts, say so and stop.

## What you are scoring

`tasks/<task-id>/` — {count} of them. Each contains:

| File | What it is |
| --- | --- |
| `prompt.txt` | the original request, verbatim |
| `task.json` | the task's declared expectations (problem count, focus, level) |
| `worksheet.pdf` `answer_key.pdf` `study_guide.pdf` | the delivered artifacts |
| `verify.json` (`verify_study_guide.json`) | the generator's verification data |
| `gate_log.txt` | the repository gate chain's output |
| `final_response.md` | what the generator told the user, when captured |

## Procedure

Follow `rubric.md` in this directory exactly, in the order it gives. In
particular: **inspect the PDFs before you read the gate logs**, and recompute
every final answer yourself. A verifier PASS is supporting evidence, not your
correctness oracle — a run where you never disagreed with the verifier is a
sign you deferred to it.

## What to write

One file per task: `verdicts/<task-id>.json`, matching this shape.

```json
{{
  "task_id": "curr-001",
  "judge": {{"agent": "<your harness>", "model": "<your model id>"}},
  "verdict": "ACCEPT",
  "hard_failures": [],
  "dimension_scores": {{
{dimensions}
  }},
  "total_score": 30,
  "manual_items_reviewed": 0,
  "incorrect_or_ambiguous_items": [],
  "artifact_findings": [],
  "rationale": "one or two sentences"
}}
```

Every dimension is an integer 0–4. `verdict` is ACCEPT only when there are no
hard failures, every dimension is at least 3, and the total is at least 27 of
32 — but do not compute the arithmetic in your head and adjust the scores to
reach a verdict you have already chosen. Score first; the verdict follows.

`judge.model` must be your real model identifier. Scoring is refused when it
matches the generator's, which the harness knows and you do not.

## When you are done

```bash
python3 evals/score_eval.py --run {run_id}
```

It re-derives every verdict from your scores, cross-checks them against
mechanical facts you were not shown, and writes `report.md`.
"""


def generator_identities(d, run):
    """Every agent/model string that authored any task in this run."""
    out = {run["generator"]["model"], run["generator"]["agent"]}
    obs_dir = os.path.join(d, "observations")
    for name in sorted(os.listdir(obs_dir)) if os.path.isdir(obs_dir) else []:
        gen = load(os.path.join(obs_dir, name)).get("generator", {})
        out |= {gen.get("model"), gen.get("agent")}
    return {x for x in out if x}


def cmd_package(a):
    d = run_dir(a.run)
    run = load(os.path.join(d, "run.json"))
    suite = load(os.path.join(ROOT, run["suite_file"]))
    dims = suite["judge_protocol"]["quality_dimensions"]

    missing, leaked = [], []
    recorded = 0
    for tid in run["task_ids"]:
        t = os.path.join(d, "tasks", tid)
        if not os.path.isfile(os.path.join(t, "result.json")):
            missing.append(f"{tid}: not recorded")
            continue
        recorded += 1
        for name in REQUIRED:
            if not os.path.isfile(os.path.join(t, name)):
                missing.append(f"{tid}: missing {name}")
        # Blindness is a property of the packet, so check it rather than trust it.
        for name in os.listdir(t):
            if name in ("observations", "result.json"):
                continue
            path = os.path.join(t, name)
            if not name.endswith((".txt", ".json", ".md", ".tex")):
                continue
            body = open(path, encoding="utf-8", errors="replace").read().lower()
            for ident in generator_identities(d, run):
                if ident and ident.lower() in body:
                    leaked.append(f"{tid}/{name} names the generator ({ident})")

    if missing:
        print(f"❌ this run is not ready to judge ({len(missing)} problem(s)):")
        for m in missing[:20]:
            print(f"  • {m}")
        if len(missing) > 20:
            print(f"  … and {len(missing) - 20} more")
        print("\n  A partial run scores as though the missing tasks never existed,\n"
              "  which reads as a better result than it is. Record them, or start\n"
              "  a run whose task list is the work you actually intend to do.")
        return 1
    if leaked:
        print("❌ the judge packet names the generator — blindness is part of the rubric:")
        for l in leaked[:10]:
            print(f"  • {l}")
        return 1

    shutil.copy(RUBRIC, os.path.join(d, "rubric.md"))
    dim_block = ",\n".join(f'    "{k}": 3' for k in dims)
    with open(os.path.join(d, "JUDGING.md"), "w", encoding="utf-8") as fh:
        fh.write(JUDGE_BRIEF.format(run_id=run["run_id"], count=recorded,
                                    dimensions=dim_block))
    print(f"✅ {recorded} task(s) packaged for judging")
    print(f"   brief : {os.path.relpath(os.path.join(d, 'JUDGING.md'), ROOT)}")
    print(f"   rubric: {os.path.relpath(os.path.join(d, 'rubric.md'), ROOT)}")
    print(f"\n   Hand the judge this directory and nothing else. The generator's\n"
          f"   identity lives in run.json at the run root, which the judge does\n"
          f"   not need and must not read.")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("start")
    s.add_argument("--suite", default="curriculum")
    s.add_argument("--shard", type=int, default=1)
    s.add_argument("--shard-size", type=int, default=25)
    s.add_argument("--tasks", help="explicit comma-separated task ids")
    s.add_argument("--generator-agent", required=True)
    s.add_argument("--generator-model", required=True)
    s.add_argument("--label", default="")
    s.set_defaults(fn=cmd_start)

    for name, fn in (("next", cmd_next), ("status", cmd_status), ("package", cmd_package)):
        q = sub.add_parser(name)
        q.add_argument("--run")
        q.set_defaults(fn=fn)

    r = sub.add_parser("record")
    r.add_argument("task_id")
    r.add_argument("--from", dest="source", required=True)
    r.add_argument("--run")
    r.add_argument("--gate-log")
    r.add_argument("--response-file")
    r.add_argument("--generator-agent", help="defaults to the run's generator")
    r.add_argument("--generator-model", help="defaults to the run's generator")
    r.add_argument("--latency-seconds", type=float)
    r.add_argument("--notes")
    r.set_defaults(fn=cmd_record)

    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
