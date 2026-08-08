#!/usr/bin/env python3
"""Prepare and aggregate post-eval reviews from the artifact author system.

This is deliberately downstream of independent scoring.  It never changes an
official verdict.  ``prepare`` turns every scored case into a self-contained
diagnostic packet for the system that authored the artifacts.  ``aggregate``
validates those responses and folds repeated issue keys into an improvement
backlog.  ``ci`` prepares every scored run and validates committed reviews.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCHEMA_VERSION = "1.0"
MIN_DIMENSION = 3
MIN_TOTAL = 27
ARTIFACT_NAMES = (
    "prompt.txt",
    "task.json",
    "worksheet.pdf",
    "answer_key.pdf",
    "study_guide.pdf",
    "worksheet.tex",
    "answer_key.tex",
    "study_guide.tex",
    "verify.json",
    "verify_study_guide.json",
    "gate_log.txt",
    "final_response.md",
    "result.json",
)
ROOT_CAUSE_CATEGORIES = {
    "skill_instructions",
    "reference_material",
    "template_or_renderer",
    "verification_contract",
    "verification_implementation",
    "generation_strategy",
    "delivery_integration",
    "eval_or_rubric",
    "case_specific_content",
    "no_defect",
    "other",
}
JUDGE_ASSESSMENTS = {"agree", "partially_agree", "disagree"}
CONFIDENCE_LEVELS = {"low", "medium", "high"}
PRIORITIES = {"p0", "p1", "p2", "p3"}
SCOPES = {"systemic", "case_specific"}
ISSUE_KEY = re.compile(r"^[a-z0-9][a-z0-9-]{2,79}$")


class ReviewError(RuntimeError):
    """Invalid input or incomplete author-review state."""


def now_utc():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def load_json(path, label="JSON"):
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise ReviewError(f"cannot read {label} {path}: {exc}") from exc


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def text(path, required=False):
    try:
        return Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        if required:
            raise ReviewError(f"cannot read required text file {path}: {exc}") from exc
        return None


def relative_display(path):
    path = Path(path).resolve()
    try:
        return path.relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path)


def require_nonempty_string(value, field, errors):
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{field} must be a non-empty string")
        return ""
    return value.strip()


def require_string_list(value, field, errors, *, nonempty=False):
    if not isinstance(value, list) or not all(
        isinstance(item, str) and item.strip() for item in value
    ):
        errors.append(f"{field} must be a list of non-empty strings")
        return []
    if nonempty and not value:
        errors.append(f"{field} must not be empty")
    return [item.strip() for item in value]


def safe_repo_paths(value, field, errors):
    paths = require_string_list(value, field, errors)
    for item in paths:
        candidate = Path(item)
        if candidate.is_absolute() or ".." in candidate.parts:
            errors.append(f"{field} entries must be repository-relative paths: {item}")
    return paths


def derive_official_result(verdict, task_id, dimensions):
    errors = []
    if verdict.get("task_id") != task_id:
        errors.append(f"task_id must be {task_id}")
    scores = verdict.get("dimension_scores")
    if not isinstance(scores, dict) or set(scores) != set(dimensions):
        errors.append("dimension_scores must contain exactly the suite dimensions")
        scores = {}
    elif not all(type(value) is int and 0 <= value <= 4 for value in scores.values()):
        errors.append("dimension scores must be integers from 0 to 4")
    hard = verdict.get("hard_failures")
    if not isinstance(hard, list) or not all(
        isinstance(item, str) and item.strip() for item in hard
    ):
        errors.append("hard_failures must be a list of non-empty strings")
        hard = []
    total = sum(scores.values()) if len(scores) == len(dimensions) else None
    if verdict.get("total_score") != total:
        errors.append(f"total_score must equal {total!r}")
    status = "REJECT"
    if not hard and total is not None:
        if total >= MIN_TOTAL and min(scores.values(), default=0) >= MIN_DIMENSION:
            status = "ACCEPT"
    if verdict.get("verdict") != status:
        errors.append(f"verdict must be {status}; it is derived from scores and hard failures")
    if errors:
        raise ReviewError(f"invalid verdict for {task_id}: {'; '.join(errors)}")
    return status, total


def artifact_inventory(case_dir):
    inventory = {}
    for name in ARTIFACT_NAMES:
        path = case_dir / name
        if path.is_file():
            inventory[name] = {
                "path": relative_display(path),
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
    return inventory


def review_template(run_id, task_id):
    return {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "task_id": task_id,
        "reviewer": {
            "role": "author_system",
            "agent": "",
            "model": "",
            "completed_at": "",
        },
        "judge_assessment": {
            "decision": "agree",
            "explanation": "",
        },
        "strengths_to_preserve": [],
        "root_causes": [
            {
                "category": "generation_strategy",
                "description": "",
                "evidence": [],
                "systemic": True,
                "confidence": "high",
                "affected_files": [],
            }
        ],
        "improvements": [
            {
                "issue_key": "short-stable-deduplication-key",
                "title": "",
                "priority": "p1",
                "scope": "systemic",
                "proposed_change": "",
                "affected_files": [],
                "regression_test": "",
                "expected_impact": "",
                "risk": "",
            }
        ],
        "case_summary": "",
    }


def review_brief(run_id, task_count):
    return f"""# Author-system post-eval review — `{run_id}`

This phase is diagnosis, not judging. The official independent verdicts are
immutable. Review all {task_count} cases, including ACCEPT cases, so fixes do
not erase strengths that already work.

For every `tasks/<task-id>/packet.json`:

1. Inspect the original prompt, task contract, generated PDFs and source files.
2. Check the judge's claims against the artifacts instead of merely agreeing.
3. Distinguish a case-specific mistake from a reusable system root cause.
4. Propose concrete repository changes and a regression test for every rejected
   case. Reuse the same stable `issue_key` when multiple cases share one fix.
5. Record at least one strength worth preserving.
6. Write the completed response to `author-reviews/<task-id>.json`, following
   `review.template.json`. Do not edit verdicts or official scores.

Root-cause categories: {', '.join(sorted(ROOT_CAUSE_CATEGORIES))}.
Priorities: p0 (invalidates trust), p1 (major systemic), p2 (bounded quality),
p3 (polish). Evidence must identify a problem, page, file, or judge claim.

After all responses are present:

```bash
python3 scripts/review_eval_run.py aggregate \\
  --packet-dir /path/to/these-packets \\
  --responses-dir evals/runs/{run_id}/author-reviews \\
  --require-complete
```

The aggregate backlog is suitable for GitHub issue triage. It does not create
issues automatically; one recurring root cause should become one issue with all
affected task IDs, not one issue per case.
"""


def prepare_run(run_dir, output_dir):
    run_dir, output_dir = Path(run_dir).resolve(), Path(output_dir)
    run = load_json(run_dir / "run.json", "run manifest")
    run_id = require_nonempty_string(run.get("run_id"), "run_id", [])
    if not run_id:
        raise ReviewError("run manifest has no run_id")
    task_ids = run.get("task_ids")
    if not isinstance(task_ids, list) or not task_ids or len(task_ids) != len(set(task_ids)):
        raise ReviewError("run task_ids must be a non-empty unique list")
    suite_rel = run.get("suite_file")
    if not isinstance(suite_rel, str) or not suite_rel:
        raise ReviewError("run manifest has no suite_file")
    suite_path = (ROOT / suite_rel).resolve()
    try:
        suite_path.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise ReviewError("suite_file must remain inside the repository") from exc
    suite = load_json(suite_path, "eval suite")
    dimensions = list(suite.get("judge_protocol", {}).get("quality_dimensions", {}))
    if len(dimensions) != 8:
        raise ReviewError("eval suite must declare eight quality dimensions")
    suite_tasks = {item.get("id"): item for item in suite.get("tasks", [])}

    output_dir.mkdir(parents=True, exist_ok=True)
    packets = []
    for task_id in task_ids:
        if task_id not in suite_tasks:
            raise ReviewError(f"{task_id} is absent from the eval suite")
        case_dir = run_dir / "tasks" / task_id
        if not case_dir.is_dir():
            raise ReviewError(f"missing task directory: {case_dir}")
        verdict = load_json(run_dir / "verdicts" / f"{task_id}.json", "judge verdict")
        status, total = derive_official_result(verdict, task_id, dimensions)
        observation_path = run_dir / "observations" / f"{task_id}.json"
        observation = load_json(observation_path, "machine observation") \
            if observation_path.is_file() else {}
        author = observation.get("generator") or run.get("generator") or {}
        task_record_path = case_dir / "task.json"
        task_record = load_json(task_record_path, "task contract") \
            if task_record_path.is_file() else suite_tasks[task_id]
        prompt = text(case_dir / "prompt.txt", required=True).strip()
        inventory = artifact_inventory(case_dir)
        required = {"prompt.txt", "task.json", "worksheet.pdf", "answer_key.pdf", "study_guide.pdf"}
        missing = sorted(required - set(inventory))
        if missing:
            raise ReviewError(f"{task_id} is missing retained author-review inputs: {', '.join(missing)}")
        packet = {
            "schema_version": SCHEMA_VERSION,
            "purpose": "post_eval_author_diagnosis",
            "official_result_is_immutable": True,
            "run": {
                "run_id": run_id,
                "repo_commit": run.get("repo_commit"),
                "condition": run.get("condition"),
                "source_directory": relative_display(run_dir),
            },
            "task_id": task_id,
            "author_system": author,
            "prompt": prompt,
            "task_contract": task_record,
            "official_score": {
                "verdict": status,
                "total": total,
                "maximum": 32,
                "dimension_scores": verdict["dimension_scores"],
                "hard_failures": verdict.get("hard_failures", []),
            },
            "judge_verdict": verdict,
            "machine_observation": observation,
            "artifacts": inventory,
            "repository_files_to_consider": [
                "SKILL.md",
                "references/problem-library.md",
                "references/manual-review-aid.md",
                "templates/worksheet-preamble.tex",
                "scripts/verify.py",
                "scripts/build.sh",
                "tests/",
            ],
            "response_path": f"author-reviews/{task_id}.json",
        }
        target = output_dir / "tasks" / task_id
        write_json(target / "packet.json", packet)
        write_json(target / "review.template.json", review_template(run_id, task_id))
        packets.append({
            "task_id": task_id,
            "official_verdict": status,
            "author_model": author.get("model"),
            "packet": relative_display(target / "packet.json"),
        })

    manifest = {
        "schema_version": SCHEMA_VERSION,
        "prepared_at": now_utc(),
        "run_id": run_id,
        "source_run_directory": relative_display(run_dir),
        "task_ids": task_ids,
        "counts": dict(Counter(item["official_verdict"] for item in packets)),
        "tasks": packets,
    }
    write_json(output_dir / "manifest.json", manifest)
    (output_dir / "AUTHOR_REVIEW.md").write_text(
        review_brief(run_id, len(task_ids)), encoding="utf-8"
    )
    print(f"Prepared {len(task_ids)} author-review packet(s) in {output_dir}")
    return manifest


def validate_review(data, packet):
    errors = []
    top_fields = {
        "schema_version", "run_id", "task_id", "reviewer", "judge_assessment",
        "strengths_to_preserve", "root_causes", "improvements", "case_summary",
    }
    if not isinstance(data, dict):
        return ["review must be a JSON object"]
    missing = sorted(top_fields - set(data))
    extra = sorted(set(data) - top_fields)
    if missing:
        errors.append("missing fields: " + ", ".join(missing))
    if extra:
        errors.append("unknown fields: " + ", ".join(extra))
    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    run_id = packet["run"]["run_id"]
    task_id = packet["task_id"]
    if data.get("run_id") != run_id:
        errors.append(f"run_id must be {run_id}")
    if data.get("task_id") != task_id:
        errors.append(f"task_id must be {task_id}")

    reviewer = data.get("reviewer")
    if not isinstance(reviewer, dict) or set(reviewer) != {
        "role", "agent", "model", "completed_at"
    }:
        errors.append("reviewer must contain exactly role, agent, model, completed_at")
    else:
        if reviewer.get("role") != "author_system":
            errors.append("reviewer.role must be author_system")
        for field in ("agent", "model", "completed_at"):
            require_nonempty_string(reviewer.get(field), f"reviewer.{field}", errors)

    assessment = data.get("judge_assessment")
    if not isinstance(assessment, dict) or set(assessment) != {"decision", "explanation"}:
        errors.append("judge_assessment must contain exactly decision and explanation")
    else:
        if assessment.get("decision") not in JUDGE_ASSESSMENTS:
            errors.append("judge_assessment.decision must be agree, partially_agree, or disagree")
        require_nonempty_string(
            assessment.get("explanation"), "judge_assessment.explanation", errors
        )

    require_string_list(
        data.get("strengths_to_preserve"), "strengths_to_preserve", errors, nonempty=True
    )
    require_nonempty_string(data.get("case_summary"), "case_summary", errors)

    causes = data.get("root_causes")
    if not isinstance(causes, list):
        errors.append("root_causes must be a list")
        causes = []
    cause_fields = {
        "category", "description", "evidence", "systemic", "confidence", "affected_files"
    }
    for index, cause in enumerate(causes):
        field = f"root_causes[{index}]"
        if not isinstance(cause, dict) or set(cause) != cause_fields:
            errors.append(f"{field} must contain exactly {', '.join(sorted(cause_fields))}")
            continue
        if cause.get("category") not in ROOT_CAUSE_CATEGORIES:
            errors.append(f"{field}.category is unknown")
        require_nonempty_string(cause.get("description"), f"{field}.description", errors)
        require_string_list(cause.get("evidence"), f"{field}.evidence", errors, nonempty=True)
        if type(cause.get("systemic")) is not bool:
            errors.append(f"{field}.systemic must be a boolean")
        if cause.get("confidence") not in CONFIDENCE_LEVELS:
            errors.append(f"{field}.confidence must be low, medium, or high")
        safe_repo_paths(cause.get("affected_files"), f"{field}.affected_files", errors)

    improvements = data.get("improvements")
    if not isinstance(improvements, list):
        errors.append("improvements must be a list")
        improvements = []
    improvement_fields = {
        "issue_key", "title", "priority", "scope", "proposed_change", "affected_files",
        "regression_test", "expected_impact", "risk",
    }
    keys = []
    for index, item in enumerate(improvements):
        field = f"improvements[{index}]"
        if not isinstance(item, dict) or set(item) != improvement_fields:
            errors.append(f"{field} must contain exactly {', '.join(sorted(improvement_fields))}")
            continue
        key = item.get("issue_key")
        if not isinstance(key, str) or not ISSUE_KEY.fullmatch(key):
            errors.append(f"{field}.issue_key must be a 3-80 character lowercase slug")
        else:
            keys.append(key)
        for name in (
            "title", "proposed_change", "regression_test", "expected_impact", "risk"
        ):
            require_nonempty_string(item.get(name), f"{field}.{name}", errors)
        if item.get("priority") not in PRIORITIES:
            errors.append(f"{field}.priority must be p0, p1, p2, or p3")
        if item.get("scope") not in SCOPES:
            errors.append(f"{field}.scope must be systemic or case_specific")
        safe_repo_paths(item.get("affected_files"), f"{field}.affected_files", errors)
    if len(keys) != len(set(keys)):
        errors.append("improvement issue_key values must be unique within a case")

    if packet["official_score"]["verdict"] == "REJECT":
        if not causes:
            errors.append("a rejected case must identify at least one root cause")
        if not improvements:
            errors.append("a rejected case must propose at least one improvement")
    return errors


def priority_rank(value):
    return {"p0": 0, "p1": 1, "p2": 2, "p3": 3}.get(value, 9)


def _unique(values):
    return sorted(set(values))


def write_aggregate_markdown(path, summary, backlog):
    counts = summary["counts"]
    lines = [
        "# Author-review improvement summary",
        "",
        f"- Run: `{summary['run_id']}`",
        f"- Reviews: {counts['valid']}/{counts['expected']} valid",
        f"- Missing: {counts['missing']}",
        f"- Invalid: {counts['invalid']}",
        f"- Reviews by the recorded author model: {counts['author_model_matches']}",
        "- Official eval scores changed: **no**",
        "",
        "## Root-cause categories",
        "",
        "| Category | Cases |",
        "|---|---:|",
    ]
    for category, count in summary["root_cause_categories"].items():
        lines.append(f"| {category} | {count} |")
    if not summary["root_cause_categories"]:
        lines.append("| None yet | 0 |")
    lines.extend([
        "",
        "## Deduplicated improvement backlog",
        "",
        "| Priority | Issue key | Cases | Scope | Title |",
        "|---|---|---:|---|---|",
    ])
    for item in backlog:
        title = item["titles"][0] if item["titles"] else ""
        lines.append(
            f"| {item['priority']} | `{item['issue_key']}` | {len(item['task_ids'])} | "
            f"{item['scope']} | {title} |"
        )
    if not backlog:
        lines.append("| — | — | 0 | — | No improvements recorded |")
    if summary["invalid_reviews"]:
        lines.extend(["", "## Invalid reviews", ""])
        for item in summary["invalid_reviews"]:
            lines.append(f"- `{item['task_id']}`: {'; '.join(item['errors'])}")
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def aggregate_reviews(packet_dir, responses_dir=None, output_dir=None, require_complete=False):
    packet_dir = Path(packet_dir)
    responses_dir = Path(responses_dir) if responses_dir else None
    output_dir = Path(output_dir or packet_dir / "results")
    manifest = load_json(packet_dir / "manifest.json", "author-review manifest")
    task_ids = manifest.get("task_ids", [])
    valid_reviews = []
    invalid_reviews = []
    missing = []
    rows = []
    cause_cases = defaultdict(set)
    backlog_groups = {}
    author_model_matches = 0

    for task_id in task_ids:
        packet = load_json(packet_dir / "tasks" / task_id / "packet.json", "review packet")
        response_path = (
            responses_dir / f"{task_id}.json" if responses_dir
            else packet_dir / "tasks" / task_id / "review.json"
        )
        if not response_path.is_file():
            missing.append(task_id)
            rows.append({
                "task_id": task_id,
                "official_verdict": packet["official_score"]["verdict"],
                "review_status": "MISSING",
                "judge_assessment": "",
                "author_model_match": "",
                "root_cause_count": 0,
                "improvement_count": 0,
            })
            continue
        try:
            review = load_json(response_path, "author review")
            errors = validate_review(review, packet)
        except ReviewError as exc:
            review, errors = {}, [str(exc)]
        if errors:
            invalid_reviews.append({"task_id": task_id, "errors": errors})
            rows.append({
                "task_id": task_id,
                "official_verdict": packet["official_score"]["verdict"],
                "review_status": "INVALID",
                "judge_assessment": "",
                "author_model_match": "",
                "root_cause_count": 0,
                "improvement_count": 0,
            })
            continue

        expected_model = str(packet.get("author_system", {}).get("model", "")).casefold()
        reviewer_model = str(review["reviewer"]["model"]).casefold()
        model_match = bool(expected_model and reviewer_model == expected_model)
        author_model_matches += model_match
        valid_reviews.append(review)
        categories = set()
        for cause in review["root_causes"]:
            categories.add(cause["category"])
            cause_cases[cause["category"]].add(task_id)
        for improvement in review["improvements"]:
            key = improvement["issue_key"]
            group = backlog_groups.setdefault(key, {
                "issue_key": key,
                "priorities": [],
                "scopes": [],
                "titles": [],
                "task_ids": set(),
                "affected_files": set(),
                "proposed_changes": set(),
                "regression_tests": set(),
                "expected_impacts": set(),
                "risks": set(),
            })
            group["priorities"].append(improvement["priority"])
            group["scopes"].append(improvement["scope"])
            group["titles"].append(improvement["title"])
            group["task_ids"].add(task_id)
            group["affected_files"].update(improvement["affected_files"])
            group["proposed_changes"].add(improvement["proposed_change"])
            group["regression_tests"].add(improvement["regression_test"])
            group["expected_impacts"].add(improvement["expected_impact"])
            group["risks"].add(improvement["risk"])
        rows.append({
            "task_id": task_id,
            "official_verdict": packet["official_score"]["verdict"],
            "review_status": "VALID",
            "judge_assessment": review["judge_assessment"]["decision"],
            "author_model_match": model_match,
            "root_cause_count": len(review["root_causes"]),
            "improvement_count": len(review["improvements"]),
        })

    backlog = []
    for group in backlog_groups.values():
        priorities = sorted(group.pop("priorities"), key=priority_rank)
        scopes = group.pop("scopes")
        backlog.append({
            **group,
            "priority": priorities[0],
            "scope": "systemic" if "systemic" in scopes else "case_specific",
            "titles": _unique(group["titles"]),
            "task_ids": sorted(group["task_ids"]),
            "affected_files": sorted(group["affected_files"]),
            "proposed_changes": sorted(group["proposed_changes"]),
            "regression_tests": sorted(group["regression_tests"]),
            "expected_impacts": sorted(group["expected_impacts"]),
            "risks": sorted(group["risks"]),
        })
    backlog.sort(key=lambda item: (
        priority_rank(item["priority"]), -len(item["task_ids"]), item["issue_key"]
    ))

    summary = {
        "schema_version": SCHEMA_VERSION,
        "aggregated_at": now_utc(),
        "run_id": manifest.get("run_id"),
        "official_scores_changed": False,
        "counts": {
            "expected": len(task_ids),
            "valid": len(valid_reviews),
            "missing": len(missing),
            "invalid": len(invalid_reviews),
            "author_model_matches": author_model_matches,
            "backlog_items": len(backlog),
        },
        "root_cause_categories": {
            key: len(value) for key, value in sorted(cause_cases.items())
        },
        "missing_reviews": missing,
        "invalid_reviews": invalid_reviews,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(output_dir / "summary.json", summary)
    write_json(output_dir / "improvement-backlog.json", {
        "schema_version": SCHEMA_VERSION,
        "run_id": manifest.get("run_id"),
        "items": backlog,
    })
    write_aggregate_markdown(output_dir / "summary.md", summary, backlog)
    with open(output_dir / "issues.jsonl", "w", encoding="utf-8") as handle:
        for item in backlog:
            handle.write(json.dumps(item, ensure_ascii=False) + "\n")
    with open(output_dir / "case-reviews.csv", "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]) if rows else ["task_id"])
        writer.writeheader()
        writer.writerows(rows)
    print(
        f"Author reviews {len(valid_reviews)}/{len(task_ids)} valid, "
        f"{len(missing)} missing, {len(invalid_reviews)} invalid; "
        f"{len(backlog)} backlog item(s)"
    )
    print(f"Results: {output_dir}")
    if invalid_reviews:
        return 2
    if require_complete and missing:
        return 1
    return 0


def merge_backlogs(backlog_paths, output_dir):
    """Merge completed per-run backlogs without losing run/task provenance."""
    output_dir = Path(output_dir)
    groups = {}
    for path in backlog_paths:
        source = load_json(path, "improvement backlog")
        run_id = require_nonempty_string(source.get("run_id"), "backlog.run_id", [])
        if not run_id:
            raise ReviewError(f"improvement backlog has no run_id: {path}")
        items = source.get("items")
        if not isinstance(items, list):
            raise ReviewError(f"improvement backlog items must be a list: {path}")
        for item in items:
            key = item.get("issue_key") if isinstance(item, dict) else None
            if not isinstance(key, str) or not ISSUE_KEY.fullmatch(key):
                raise ReviewError(f"invalid issue_key in improvement backlog {path}")
            group = groups.setdefault(key, {
                "issue_key": key,
                "priorities": [],
                "scopes": [],
                "titles": set(),
                "cases": set(),
                "affected_files": set(),
                "proposed_changes": set(),
                "regression_tests": set(),
                "expected_impacts": set(),
                "risks": set(),
            })
            group["priorities"].append(item.get("priority"))
            group["scopes"].append(item.get("scope"))
            for field in (
                "titles", "affected_files", "proposed_changes", "regression_tests",
                "expected_impacts", "risks",
            ):
                values = item.get(field, [])
                if not isinstance(values, list):
                    raise ReviewError(f"{field} must be a list in backlog item {key}")
                group[field].update(str(value) for value in values)
            task_ids = item.get("task_ids", [])
            if not isinstance(task_ids, list):
                raise ReviewError(f"task_ids must be a list in backlog item {key}")
            group["cases"].update((run_id, str(task_id)) for task_id in task_ids)

    merged = []
    for group in groups.values():
        priorities = group.pop("priorities")
        scopes = group.pop("scopes")
        cases = sorted(group["cases"])
        merged.append({
            "issue_key": group["issue_key"],
            "priority": min(priorities, key=priority_rank),
            "scope": "systemic" if "systemic" in scopes else "case_specific",
            "titles": sorted(group["titles"]),
            "run_ids": sorted({run_id for run_id, _ in cases}),
            "task_ids": sorted({task_id for _, task_id in cases}),
            "cases": [
                {"run_id": run_id, "task_id": task_id} for run_id, task_id in cases
            ],
            "affected_files": sorted(group["affected_files"]),
            "proposed_changes": sorted(group["proposed_changes"]),
            "regression_tests": sorted(group["regression_tests"]),
            "expected_impacts": sorted(group["expected_impacts"]),
            "risks": sorted(group["risks"]),
        })
    merged.sort(key=lambda item: (
        priority_rank(item["priority"]), -len(item["cases"]), item["issue_key"]
    ))
    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(output_dir / "improvement-backlog.json", {
        "schema_version": SCHEMA_VERSION,
        "source_run_count": len(backlog_paths),
        "items": merged,
    })
    with open(output_dir / "issues.jsonl", "w", encoding="utf-8") as handle:
        for item in merged:
            handle.write(json.dumps(item, ensure_ascii=False) + "\n")
    lines = [
        "# Cross-run author-review backlog",
        "",
        f"- Completed runs included: {len(backlog_paths)}",
        f"- Deduplicated improvement items: {len(merged)}",
        "- Official eval scores changed: **no**",
        "",
        "| Priority | Issue key | Cases | Runs | Scope | Title |",
        "|---|---|---:|---:|---|---|",
    ]
    for item in merged:
        lines.append(
            f"| {item['priority']} | `{item['issue_key']}` | {len(item['cases'])} | "
            f"{len(item['run_ids'])} | {item['scope']} | "
            f"{item['titles'][0] if item['titles'] else ''} |"
        )
    if not merged:
        lines.append("| — | — | 0 | 0 | — | No improvements recorded |")
    (output_dir / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Merged {len(backlog_paths)} run backlog(s) into {len(merged)} item(s)")
    return merged


def ci_runs(runs_root, output_dir, run_ids=None, require_author_reviews=False):
    runs_root, output_dir = Path(runs_root), Path(output_dir)
    if run_ids:
        runs = [runs_root / run_id for run_id in run_ids]
    else:
        runs = sorted(path.parent for path in runs_root.glob("*/run.json"))
    scored = [path for path in runs if (path / "verdicts").is_dir()]
    if not scored:
        raise ReviewError("no scored eval runs found")
    records = []
    completed_backlogs = []
    rc = 0
    for run_dir in scored:
        packet_dir = output_dir / run_dir.name
        manifest = prepare_run(run_dir, packet_dir)
        responses = run_dir / "author-reviews"
        status = "PACKETS_READY"
        if responses.is_dir():
            aggregate_rc = aggregate_reviews(
                packet_dir, responses, packet_dir / "results", require_complete=True
            )
            if aggregate_rc:
                rc = max(rc, aggregate_rc)
                status = "REVIEWS_INVALID" if aggregate_rc == 2 else "REVIEWS_INCOMPLETE"
            else:
                status = "REVIEWS_COMPLETE"
                completed_backlogs.append(packet_dir / "results" / "improvement-backlog.json")
        elif require_author_reviews:
            rc = max(rc, 1)
            status = "REVIEWS_MISSING"
        records.append({
            "run_id": manifest["run_id"],
            "task_count": len(manifest["task_ids"]),
            "status": status,
        })
    if completed_backlogs:
        merge_backlogs(completed_backlogs, output_dir / "global-results")
    write_json(output_dir / "ci-manifest.json", {
        "schema_version": SCHEMA_VERSION,
        "generated_at": now_utc(),
        "global_backlog_ready": bool(completed_backlogs),
        "runs": records,
    })
    for record in records:
        print(f"{record['run_id']}: {record['status']} ({record['task_count']} tasks)")
    return rc


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    prepare = sub.add_parser("prepare", help="create one author-review packet per scored case")
    prepare.add_argument("--run-dir", required=True)
    prepare.add_argument("--output-dir", required=True)
    aggregate = sub.add_parser("aggregate", help="validate reviews and build improvement backlog")
    aggregate.add_argument("--packet-dir", required=True)
    aggregate.add_argument("--responses-dir")
    aggregate.add_argument("--output-dir")
    aggregate.add_argument("--require-complete", action="store_true")
    merge = sub.add_parser("merge", help="deduplicate improvements across completed runs")
    merge.add_argument("--backlog", action="append", required=True)
    merge.add_argument("--output-dir", required=True)
    ci = sub.add_parser("ci", help="prepare every scored run and validate committed reviews")
    ci.add_argument("--runs-root", default=str(ROOT / "evals" / "runs"))
    ci.add_argument("--output-dir", required=True)
    ci.add_argument("--run-id", action="append", default=[])
    ci.add_argument("--require-author-reviews", action="store_true")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        if args.command == "prepare":
            prepare_run(args.run_dir, args.output_dir)
            return 0
        if args.command == "aggregate":
            return aggregate_reviews(
                args.packet_dir,
                responses_dir=args.responses_dir,
                output_dir=args.output_dir,
                require_complete=args.require_complete,
            )
        if args.command == "merge":
            merge_backlogs(args.backlog, args.output_dir)
            return 0
        return ci_runs(
            args.runs_root,
            args.output_dir,
            run_ids=args.run_id,
            require_author_reviews=args.require_author_reviews,
        )
    except ReviewError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":  # pragma: no cover — dispatch-only; main() is tested directly through all four subcommands
    sys.exit(main())
