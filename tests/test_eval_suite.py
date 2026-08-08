#!/usr/bin/env python3
"""Contract checks for the end-to-end capability and smoke eval manifests, plus
the `run_eval.py record` capture contract."""

import contextlib
import io
import json
import os
import shutil
import sys
import tempfile


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FULL_PATH = os.path.join(ROOT, "evals", "capability-suite.json")
SMOKE_PATH = os.path.join(ROOT, "evals", "evals.json")

EXPECTED_TYPES = {
    "solve", "zeros", "factor", "expand", "eval", "diff", "integrate",
    "limit", "equiv", "solve_interval", "approx", "distance", "midpoint",
    "slope", "polygon_area", "triangle", "system", "series", "inequality",
    "stats", "probability", "read_data", "definite_integral", "estimate",
    "compare", "manual",
}
EXPECTED_PROFILES = {
    "standard_trio", "manual_trio", "worksheet_only", "multi_set",
    "routing_no_artifact",
}
EXPECTED_CADENCES = {"pr", "nightly", "weekly"}
FAILS = []


def check(name, condition):
    print(f"  {'✅' if condition else '❌'} {name}")
    if not condition:
        FAILS.append(name)


def load(path):
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"  ❌ cannot load {path}: {exc}")
        sys.exit(1)


full = load(FULL_PATH)
smoke = load(SMOKE_PATH)
tasks = full.get("tasks", [])
task_by_name = {task.get("name"): task for task in tasks}
task_ids = {task.get("id") for task in tasks}

print("Capability-suite structure:")
check("schema version is declared", full.get("schema_version") == "1.0")
check("target is this skill", full.get("suite", {}).get("target_repository")
      == "stellawuellner/math-worksheets-skill")
check("initial suite has 20-50 tasks", 20 <= len(tasks) <= 50)
check("task ids are unique", len(task_ids) == len(tasks))
check("task names are unique", len(task_by_name) == len(tasks))
check("ids are contiguous mw-001..mw-N",
      [task.get("id") for task in tasks]
      == [f"mw-{i:03d}" for i in range(1, len(tasks) + 1)])
check("all five outcome profiles are defined",
      set(full.get("profiles", {})) == EXPECTED_PROFILES)

print("Per-task contract:")
for task in tasks:
    label = task.get("id", "<missing-id>")
    mode = task.get("mode")
    has_prompt = isinstance(task.get("prompt"), str) and bool(task["prompt"].strip())
    has_turns = (isinstance(task.get("turns"), list)
                 and len(task["turns"]) >= 2
                 and all(isinstance(turn, str) and turn.strip()
                         for turn in task["turns"]))
    check(f"{label}: exactly one prompt shape",
          has_turns != has_prompt and (mode == "multi_turn") == has_turns)
    check(f"{label}: known profile", task.get("profile") in EXPECTED_PROFILES)
    check(f"{label}: known cadence", task.get("cadence") in EXPECTED_CADENCES)
    check(f"{label}: capability tags", bool(task.get("capabilities")))
    assertions = task.get("expected", {}).get("assertions")
    check(f"{label}: explicit assertions",
          isinstance(assertions, list) and len(assertions) >= 2
          and all(isinstance(item, str) and item.strip() for item in assertions))
    for asset in task.get("assets", []):
        rel = asset.get("repository_path", "")
        check(f"{label}: asset exists ({rel})",
              bool(rel) and os.path.isfile(os.path.join(ROOT, rel)))

print("Verifier-family coverage:")
coverage = full.get("verifier_type_coverage", {})
check("coverage keys exactly match verify.py's 26 public types",
      set(coverage) == EXPECTED_TYPES)
for verify_type, refs in coverage.items():
    check(f"{verify_type}: has valid task references",
          isinstance(refs, list) and bool(refs)
          and all(ref in task_ids for ref in refs))

print("Evaluation balance:")
profile_counts = {
    profile: sum(task.get("profile") == profile for task in tasks)
    for profile in EXPECTED_PROFILES
}
check("at least two negative-routing tasks",
      profile_counts["routing_no_artifact"] >= 2)
check("manual-review boundary is exercised",
      profile_counts["manual_trio"] >= 1)
check("single-document exception is exercised",
      profile_counts["worksheet_only"] >= 1)
check("multi-set behavior is exercised", profile_counts["multi_set"] >= 1)
check("multi-turn behavior is exercised",
      any(task.get("mode") == "multi_turn" for task in tasks))
check("asset-backed behavior is exercised",
      any(task.get("assets") for task in tasks))
check("stress cadence is exercised",
      any(task.get("cadence") == "weekly" for task in tasks))

print("Quick smoke subset:")
smoke_evals = smoke.get("evals", [])
check("smoke manifest names this skill", smoke.get("skill_name") == "math-worksheets")
check("smoke ids are contiguous integers",
      [item.get("id") for item in smoke_evals] == list(range(len(smoke_evals))))
check("smoke subset has three focused tasks", len(smoke_evals) == 3)
for item in smoke_evals:
    full_task = task_by_name.get(item.get("eval_name"))
    check(f"{item.get('eval_name')}: exists in full suite", full_task is not None)
    check(f"{item.get('eval_name')}: prompt is synchronized",
          full_task is not None and item.get("prompt") == full_task.get("prompt"))
    check(f"{item.get('eval_name')}: expected output is actionable",
          isinstance(item.get("expected_output"), str)
          and "zero incorrect answers" in item["expected_output"])

print("Record capture contract (run_eval.py):")
# WHAT WENT WRONG. A build directory holding two `verify_<stem>.json` files — a
# stale stem from an earlier attempt in a reused /tmp dir — made discovery return
# nothing. `record` then copied NO artifact, wrote a `result.json` containing only
# `task_id` and `recorded`, and still printed a line beginning "recorded", so the
# task looked captured and only failed much later, in `package`, as
# missing-artifact. Three agents in the 2026-08-06 run hit it and caught it by
# hand. A partial record must never be reported as success.
sys.path.insert(0, os.path.join(ROOT, "evals"))
import run_eval  # noqa: E402


def _build_dir(stems):
    """A build directory as build.sh leaves it, one artifact set per stem."""
    d = tempfile.mkdtemp()
    for stem in stems:
        json.dump({"problem_count": 8, "problems": [{"id": i} for i in range(1, 9)]},
                  open(os.path.join(d, f"verify_{stem}.json"), "w"))
        for role in ("ws", "ak", "ss"):
            with open(os.path.join(d, f"{role}_{stem}.pdf"), "w") as fh:
                fh.write("%PDF-1.4\n")
    with open(os.path.join(d, "gate_log.txt"), "w") as fh:
        fh.write("BUILD PASSED\n")
    return d


def _record(run_id, task_id, source):
    """Run `record`, returning (exit code, everything it printed)."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = run_eval.main(["record", task_id, "--run", run_id, "--from", source])
    return code, out.getvalue() + err.getvalue()


real_runs = run_eval.RUNS
sandbox = tempfile.mkdtemp()
builds = []
try:
    # Never touch evals/runs: a judge may be reading a real run right now.
    run_eval.RUNS = os.path.join(sandbox, "runs")
    task_id = load(os.path.join(ROOT, "evals", "curriculum-suite-500.json"))["tasks"][0]["id"]
    with contextlib.redirect_stdout(io.StringIO()):
        run_eval.main(["start", "--suite", "curriculum", "--tasks", task_id,
                       "--generator-agent", "test", "--generator-model", "test-model"])
    run_id = os.listdir(run_eval.RUNS)[0]
    result = os.path.join(run_eval.RUNS, run_id, "tasks", task_id, "result.json")
    observation = os.path.join(run_eval.RUNS, run_id, "observations", f"{task_id}.json")

    clean = _build_dir(["good_curr001"])
    builds.append(clean)
    code, said = _record(run_id, task_id, clean)
    check("record: an unambiguous build dir is recorded", code == 0)
    check("record: it writes result.json", os.path.isfile(result))
    check("record: it confirms the artifacts landed on disk",
          "confirmed on disk" in said and "worksheet.pdf" in said)

    os.remove(result)
    os.remove(observation)
    colliding = _build_dir(["good_curr001", "stale_curr001"])
    builds.append(colliding)
    code, said = _record(run_id, task_id, colliding)
    check("record: two verify_<stem>.json files is a HARD failure", code != 0)
    check("record: the collision is reported with ❌, never as 'recorded'",
          "❌" in said and "NOT recorded" in said)
    check("record: both colliding stems are named",
          "verify_good_curr001.json" in said and "verify_stale_curr001.json" in said)
    check("record: no partial result.json is left behind",
          not os.path.isfile(result))
    check("record: no observation is left behind", not os.path.isfile(observation))
    check("record: the task stays pending, so `next` hands it out again",
          not os.path.isfile(result))

    # Same class: a stem that resolves but whose PDFs are ambiguous cannot name
    # the artifact either, and must not be captured as a guess.
    two_pdfs = _build_dir(["good_curr001"])
    builds.append(two_pdfs)
    shutil.copy(os.path.join(two_pdfs, "ws_good_curr001.pdf"),
                os.path.join(two_pdfs, "draft_ws_good_curr001.pdf"))
    code, said = _record(run_id, task_id, two_pdfs)
    check("record: two candidate worksheet PDFs is a HARD failure", code != 0)
    check("record: no partial result.json from an ambiguous PDF",
          not os.path.isfile(result))
finally:
    run_eval.RUNS = real_runs
    shutil.rmtree(sandbox, ignore_errors=True)
    for d in builds:
        shutil.rmtree(d, ignore_errors=True)

if FAILS:
    print(f"\n❌ {len(FAILS)} eval-suite contract check(s) failed")
    sys.exit(1)

print(f"\n✅ Eval manifests valid — {len(tasks)} capability tasks · "
      f"{len(coverage)} verifier types · {len(smoke_evals)} smoke tasks")
