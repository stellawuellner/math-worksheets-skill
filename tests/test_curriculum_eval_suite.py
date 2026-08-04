#!/usr/bin/env python3
"""Contract checks for the generated 500-prompt curriculum eval suite."""

import importlib.util
import json
import os
import re
import sys
from collections import Counter, defaultdict


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MANIFEST_PATH = os.path.join(ROOT, "evals", "curriculum-suite-500.json")
GENERATOR_PATH = os.path.join(ROOT, "evals", "generate_curriculum_suite.py")
RUBRIC_PATH = os.path.join(ROOT, "evals", "curriculum-judge-rubric.md")

EXPECTED_TYPES = {
    "solve", "zeros", "factor", "expand", "eval", "diff", "integrate",
    "limit", "equiv", "solve_interval", "approx", "distance", "midpoint",
    "slope", "polygon_area", "triangle", "system", "series", "inequality",
    "stats", "probability", "read_data", "definite_integral", "estimate",
    "compare", "manual",
}
EXPECTED_BANDS = {
    "foundations-k1", "elementary-2-3", "upper-elementary-4-5",
    "middle-grades-6-7", "grade8-prealgebra", "algebra-1", "geometry",
    "algebra-2", "precalculus-statistics", "calculus-ab-bc",
}
EXPECTED_MODES = {
    "concept-models", "procedural-fluency", "representations-applications",
    "misconception-analysis", "interleaved-synthesis",
}
FAILS = []


def check(name, condition, detail=""):
    print(f"  {'✅' if condition else '❌'} {name}")
    if not condition:
        FAILS.append(f"{name}{': ' + detail if detail else ''}")


def load_json(path):
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"❌ cannot load {path}: {exc}")
        sys.exit(1)


def load_generator():
    spec = importlib.util.spec_from_file_location("curriculum_eval_generator", GENERATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


manifest = load_json(MANIFEST_PATH)
generator = load_generator()
generated = generator.build_suite()
tasks = manifest.get("tasks", [])
task_ids = [task.get("id") for task in tasks]

print("Generated-manifest integrity:")
check("manifest exactly matches deterministic generator", manifest == generated)
check("schema version is declared", manifest.get("schema_version") == "1.0")
check("suite declares exactly 500 tasks", manifest.get("suite", {}).get("task_count") == 500)
check("manifest contains exactly 500 tasks", len(tasks) == 500)
check("ids are contiguous curr-001..curr-500",
      task_ids == [f"curr-{i:03d}" for i in range(1, 501)])
check("standalone judge rubric exists", os.path.isfile(RUBRIC_PATH))
check("scoring harness is declared",
      manifest.get("scoring_harness", {}).get("script") == "scripts/score_eval_run.py"
      and manifest.get("scoring_harness", {}).get("stages") == [
          "prepare", "independent_judgment", "aggregate",
      ])
check("post-eval author review is declared",
      manifest.get("author_review", {}).get("script") == "scripts/review_eval_run.py"
      and manifest.get("author_review", {}).get("stages") == [
          "prepare", "author_system_diagnosis", "aggregate",
      ]
      and manifest.get("author_review", {}).get("official_score_is_immutable") is True)

print("Prompt and curriculum uniqueness:")
names = [task.get("curriculum_key") for task in tasks]
prompts = [task.get("prompt", "") for task in tasks]
normalized = [" ".join(prompt.lower().split()) for prompt in prompts]
check("all 500 curriculum keys are unique", len(set(names)) == 500)
check("all 500 prompt strings are unique", len(set(prompts)) == 500)
check("all prompts remain unique after case/whitespace normalization",
      len(set(normalized)) == 500)
check("all 500 curriculum focus strings are distinct",
      len({task.get("focus") for task in tasks}) == 500)
check("no prompt has leading or trailing whitespace",
      all(prompt == prompt.strip() for prompt in prompts))
check("all prompts are substantive", min(map(len, prompts), default=0) >= 350)

print("Curriculum distribution:")
band_counts = Counter(task.get("band") for task in tasks)
check("the ten declared curriculum bands are exact", set(band_counts) == EXPECTED_BANDS)
check("every curriculum band has exactly 50 prompts",
      set(band_counts.values()) == {50}, str(dict(band_counts)))
topic_modes = defaultdict(set)
for task in tasks:
    topic_modes[(task.get("band"), task.get("topic"))].add(task.get("instructional_mode"))
check("there are exactly 100 topic families", len(topic_modes) == 100)
check("all 100 topic-family names are distinct",
      len({task.get("topic") for task in tasks}) == 100)
check("every topic family has all five distinct instructional modes",
      all(modes == EXPECTED_MODES for modes in topic_modes.values()))
check("suite begins with counting foundations",
      tasks and tasks[0].get("band") == "foundations-k1"
      and "counting" in tasks[0].get("topic", "").lower())
check("suite ends with Calculus BC series",
      tasks and tasks[-1].get("band") == "calculus-ab-bc"
      and "Taylor" in tasks[-1].get("topic", ""))

print("Artifact-generation contract:")
bad_contract = []
for task in tasks:
    prompt = task.get("prompt", "").lower()
    expected = task.get("expected", {})
    artifacts = expected.get("required_pdf_artifacts")
    assertions = expected.get("assertions")
    if not all(term in prompt for term in ("student worksheet", "answer key", "study guide", "pdf")):
        bad_contract.append(f"{task.get('id')}: prompt does not request trio")
    if artifacts != ["student_worksheet", "step_by_step_answer_key", "study_guide"]:
        bad_contract.append(f"{task.get('id')}: artifact contract")
    match = re.search(r"containing (\d+) problems", prompt)
    if not match or int(match.group(1)) != expected.get("worksheet_problem_count"):
        bad_contract.append(f"{task.get('id')}: problem count")
    if not isinstance(assertions, list) or len(assertions) != 4:
        bad_contract.append(f"{task.get('id')}: assertions")
    elif task.get("focus", "") not in assertions[0]:
        bad_contract.append(f"{task.get('id')}: focus assertion")
    if task.get("profile") != "artifact_trio_acceptance":
        bad_contract.append(f"{task.get('id')}: profile")
    if task.get("review_mode") not in {"machine_first", "manual_allowed"}:
        bad_contract.append(f"{task.get('id')}: review mode")
check("every task requests and specifies the same three-PDF contract",
      not bad_contract, "; ".join(bad_contract[:8]))

print("Verifier and judge coverage:")
coverage = manifest.get("verifier_type_coverage", {})
check("coverage map names all 26 public verifier types", set(coverage) == EXPECTED_TYPES)
derived = defaultdict(list)
unknown_targets = []
for task in tasks:
    targets = task.get("verification_targets", [])
    unknown_targets.extend(set(targets) - EXPECTED_TYPES)
    for target in targets:
        derived[target].append(task["id"])
check("every task verification target is public", not unknown_targets)
check("coverage references exactly match task metadata",
      all(coverage.get(kind) == derived[kind] for kind in EXPECTED_TYPES))
check("every verifier type appears in multiple curriculum prompts",
      min(map(len, coverage.values()), default=0) >= 2)

judge = manifest.get("judge_protocol", {})
dimensions = judge.get("quality_dimensions", {})
hard_fails = judge.get("hard_fail_conditions", [])
check("human and independent-agent judges are both supported",
      len(judge.get("eligible_judges", [])) == 2)
check("judge must independently recompute every answer",
      any("every final answer" in step for step in judge.get("review_order", [])))
check("seven non-negotiable hard-fail rules are present", len(hard_fails) == 7)
check("eight quality dimensions are scored", len(dimensions) == 8)
check("acceptance threshold is explicit",
      "27 of 32" in judge.get("acceptance_rule", "")
      and "every quality dimension" in judge.get("acceptance_rule", ""))
check("structured judge verdict schema is present",
      set(judge.get("verdict_schema", {})) >= {
          "task_id", "verdict", "hard_failures", "dimension_scores",
          "total_score", "errors", "critical_observations", "rationale",
      })

if FAILS:
    print(f"\n❌ {len(FAILS)} curriculum-eval contract check(s) failed:")
    for failure in FAILS:
        print(f"   {failure}")
    sys.exit(1)

print("\n✅ Curriculum eval suite valid — 500 unique prompts · "
      "10 bands · 100 topic families · 26 verifier types")
