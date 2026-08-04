#!/usr/bin/env python3
"""Behavioral contract for scripts/review_eval_run.py."""

import importlib.util
import json
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "review_eval_run.py"
SUITE = ROOT / "evals" / "curriculum-suite-500.json"
spec = importlib.util.spec_from_file_location("review_eval_run", SCRIPT)
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)
FAILS = []


def check(name, condition, detail=""):
    print(f"  {'ok  ' if condition else 'FAIL'} {name}")
    if not condition:
        FAILS.append(f"{name}: {detail}")


def dump(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data), encoding="utf-8")


def create_run(root, task_ids=("curr-001", "curr-002"), *, rejected=True):
    suite = json.loads(SUITE.read_text(encoding="utf-8"))
    by_id = {task["id"]: task for task in suite["tasks"]}
    dims = list(suite["judge_protocol"]["quality_dimensions"])
    root = Path(root)
    dump(root / "run.json", {
        "run_id": "author-review-test",
        "suite": "curriculum",
        "suite_file": "evals/curriculum-suite-500.json",
        "shard": "test",
        "repo_commit": "abc123",
        "condition": "skill_on",
        "generator": {"agent": "claude-code", "model": "claude-opus-5"},
        "task_ids": list(task_ids),
    })
    for task_id in task_ids:
        case = root / "tasks" / task_id
        case.mkdir(parents=True)
        task = by_id[task_id]
        (case / "prompt.txt").write_text(task["prompt"], encoding="utf-8")
        dump(case / "task.json", task)
        for name in ("worksheet.pdf", "answer_key.pdf", "study_guide.pdf"):
            (case / name).write_bytes(b"%PDF-test")
        for name in ("worksheet.tex", "answer_key.tex", "study_guide.tex"):
            (case / name).write_text("test", encoding="utf-8")
        dump(case / "verify.json", {"problem_count": task["expected"]["worksheet_problem_count"]})
        (case / "gate_log.txt").write_text("BUILD PASSED", encoding="utf-8")
        (case / "final_response.md").write_text("PDFs attached", encoding="utf-8")
        dump(root / "observations" / f"{task_id}.json", {
            "task_id": task_id,
            "generator": {"agent": "claude-code", "model": "claude-opus-5"},
            "gate_chain_passed": True,
        })
        hard = ["verification coverage is incomplete"] if rejected else []
        dump(root / "verdicts" / f"{task_id}.json", {
            "schema_version": "1.0",
            "task_id": task_id,
            "judge": {"agent": "codex", "model": "gpt-5.6"},
            "verdict": "REJECT" if rejected else "ACCEPT",
            "hard_failures": hard,
            "dimension_scores": {name: 4 for name in dims},
            "total_score": 32,
            "manual_items_reviewed": 0,
            "incorrect_or_ambiguous_items": [],
            "errors": [],
            "critical_observations": [],
            "artifact_findings": [],
            "rationale": "test verdict",
        })


def completed_review(task_id, *, issue_key="verify-all-printed-responses"):
    return {
        "schema_version": "1.0",
        "run_id": "author-review-test",
        "task_id": task_id,
        "reviewer": {
            "role": "author_system",
            "agent": "claude-code",
            "model": "claude-opus-5",
            "completed_at": "2026-08-04T12:00:00Z",
        },
        "judge_assessment": {
            "decision": "agree",
            "explanation": "The worksheet asks for responses absent from verification.",
        },
        "strengths_to_preserve": ["The mathematics and instructional progression are sound."],
        "root_causes": [{
            "category": "verification_contract",
            "description": "Generation tracked terminal answers rather than every printed response.",
            "evidence": ["The judge identifies an uncovered response in problem 2."],
            "systemic": True,
            "confidence": "high",
            "affected_files": ["SKILL.md", "scripts/verify.py"],
        }],
        "improvements": [{
            "issue_key": issue_key,
            "title": "Bind every printed response to verification or manual review",
            "priority": "p0",
            "scope": "systemic",
            "proposed_change": "Add a response inventory before worksheet rendering.",
            "affected_files": ["SKILL.md", "scripts/verify.py"],
            "regression_test": "Reject a fixture with an untracked written subresponse.",
            "expected_impact": "Eliminates false complete-verification claims.",
            "risk": "May classify more open items for manual review.",
        }],
        "case_summary": "The score is fair and exposes a reusable verification gap.",
    }


print("Packet preparation and score immutability:")
with tempfile.TemporaryDirectory() as temp:
    temp = Path(temp)
    run_dir = temp / "run"
    create_run(run_dir)
    packets = temp / "packets"
    manifest = review.prepare_run(run_dir, packets)
    check("all scored cases receive packets", manifest["task_ids"] == ["curr-001", "curr-002"])
    check("run-level author brief exists", (packets / "AUTHOR_REVIEW.md").is_file())
    packet = json.loads((packets / "tasks" / "curr-001" / "packet.json").read_text())
    check("official result is explicitly immutable",
          packet["official_result_is_immutable"] is True
          and packet["official_score"]["verdict"] == "REJECT")
    check("packet binds artifacts with hashes",
          packet["artifacts"]["worksheet.pdf"]["sha256"]
          == review.sha256_file(run_dir / "tasks" / "curr-001" / "worksheet.pdf"))
    check("author provenance is retained",
          packet["author_system"]["model"] == "claude-opus-5")
    check("response template exists",
          (packets / "tasks" / "curr-001" / "review.template.json").is_file())

    responses = temp / "responses"
    for task_id in manifest["task_ids"]:
        dump(responses / f"{task_id}.json", completed_review(task_id))
    results = temp / "results"
    rc = review.aggregate_reviews(packets, responses, results, require_complete=True)
    summary = json.loads((results / "summary.json").read_text())
    backlog = json.loads((results / "improvement-backlog.json").read_text())["items"]
    check("complete author review validates", rc == 0 and summary["counts"]["valid"] == 2)
    check("same author model is observable", summary["counts"]["author_model_matches"] == 2)
    check("stable issue keys deduplicate cases",
          len(backlog) == 1 and backlog[0]["task_ids"] == ["curr-001", "curr-002"])
    check("highest priority and systemic scope survive aggregation",
          backlog[0]["priority"] == "p0" and backlog[0]["scope"] == "systemic")
    check("all aggregate formats exist", all((results / name).is_file() for name in (
        "summary.md", "case-reviews.csv", "issues.jsonl",
    )))

    other = json.loads((results / "improvement-backlog.json").read_text())
    other["run_id"] = "author-review-test-2"
    other["items"][0]["task_ids"] = ["curr-003"]
    other_path = temp / "other-backlog.json"
    dump(other_path, other)
    global_results = temp / "global-results"
    merged = review.merge_backlogs(
        [results / "improvement-backlog.json", other_path], global_results
    )
    check("cross-run backlog keeps one systemic issue",
          len(merged) == 1 and len(merged[0]["cases"]) == 3)
    check("cross-run provenance retains both runs",
          merged[0]["run_ids"] == ["author-review-test", "author-review-test-2"])
    check("cross-run GitHub issue ledger exists",
          (global_results / "issues.jsonl").is_file())

    (responses / "curr-002.json").unlink()
    missing_results = temp / "missing-results"
    check("require-complete rejects a missing case review",
          review.aggregate_reviews(packets, responses, missing_results, require_complete=True) == 1)

    bad = completed_review("curr-002")
    bad["improvements"][0]["affected_files"] = ["../outside"]
    dump(responses / "curr-002.json", bad)
    invalid_results = temp / "invalid-results"
    check("unsafe or malformed response is invalid",
          review.aggregate_reviews(packets, responses, invalid_results) == 2)

print("Review schema branches:")
with tempfile.TemporaryDirectory() as temp:
    temp = Path(temp)
    run_dir = temp / "run"
    create_run(run_dir, ("curr-001",), rejected=False)
    packets = temp / "packets"
    review.prepare_run(run_dir, packets)
    packet = json.loads((packets / "tasks" / "curr-001" / "packet.json").read_text())
    accepted = completed_review("curr-001")
    accepted["root_causes"] = []
    accepted["improvements"] = []
    check("accepted case may preserve strengths without inventing a defect",
          review.validate_review(accepted, packet) == [])
    broken = dict(accepted)
    broken["surprise"] = True
    errors = review.validate_review(broken, packet)
    check("unknown top-level fields are rejected", any("unknown fields" in item for item in errors))

    rejected_packet = dict(packet)
    rejected_packet["official_score"] = dict(packet["official_score"], verdict="REJECT")
    errors = review.validate_review(accepted, rejected_packet)
    check("rejected cases require diagnosis and action",
          any("root cause" in item for item in errors)
          and any("improvement" in item for item in errors))

print("CI orchestration:")
with tempfile.TemporaryDirectory() as temp:
    temp = Path(temp)
    runs = temp / "runs"
    create_run(runs / "author-review-test", ("curr-001",))
    out = temp / "ci"
    rc = review.ci_runs(runs, out)
    ci = json.loads((out / "ci-manifest.json").read_text())
    check("CI prepares scored runs without requiring responses",
          rc == 0 and ci["runs"][0]["status"] == "PACKETS_READY")
    check("CI can require author responses", review.ci_runs(
        runs, temp / "strict-ci", require_author_reviews=True
    ) == 1)

print("Error paths:")
with tempfile.TemporaryDirectory() as temp:
    temp = Path(temp)
    dump(temp / "run.json", {"run_id": "bad", "suite_file": "../outside", "task_ids": ["x"]})
    try:
        review.prepare_run(temp, temp / "out")
        check("suite path traversal is rejected", False)
    except review.ReviewError:
        check("suite path traversal is rejected", True)
    try:
        review.ci_runs(temp / "missing", temp / "out")
        check("CI rejects absence of scored runs", False)
    except review.ReviewError:
        check("CI rejects absence of scored runs", True)

if FAILS:
    print(f"\nFAIL: {len(FAILS)} author-review check(s) failed")
    for failure in FAILS:
        print(f"  {failure}")
    raise SystemExit(1)

print("\nok: author-review packets, validation, aggregation, and CI orchestration")
