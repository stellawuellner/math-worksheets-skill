#!/usr/bin/env python3
"""Contract checks for the end-to-end capability and smoke eval manifests."""

import json
import os
import sys


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

if FAILS:
    print(f"\n❌ {len(FAILS)} eval-suite contract check(s) failed")
    sys.exit(1)

print(f"\n✅ Eval manifests valid — {len(tasks)} capability tasks · "
      f"{len(coverage)} verifier types · {len(smoke_evals)} smoke tasks")
