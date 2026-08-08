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

# ── Rejection branches ──────────────────────────────────────────────────────
# The suite above proves the happy path and three refusals. Everything else in
# validate_review -- roughly a third of this module -- was untested, and a
# validator's REJECTIONS are its contract: an author-review response that
# should have been refused and was not becomes a backlog item nobody can act
# on, with the schema saying it was fine.
print("\nValidator refusals:")
with tempfile.TemporaryDirectory() as temp:
    temp = Path(temp)
    run_dir = temp / "run"
    create_run(run_dir, ("curr-001",), rejected=False)
    packets = temp / "packets"
    review.prepare_run(run_dir, packets)
    packet = json.loads((packets / "tasks" / "curr-001" / "packet.json").read_text())

    def refuses(label, mutate, needle):
        data = completed_review("curr-001")
        mutate(data)
        errors = review.validate_review(data, packet)
        check(label, any(needle in e for e in errors),
              f"expected {needle!r}, got {errors}")

    check("a non-object review is refused outright",
          review.validate_review(["not", "a", "dict"], packet)
          == ["review must be a JSON object"])

    refuses("a missing top-level field is named",
            lambda d: d.pop("case_summary"), "missing fields")
    refuses("a wrong schema_version is refused",
            lambda d: d.update(schema_version="0.0.0"), "schema_version must be")
    refuses("a run_id that is not this run is refused",
            lambda d: d.update(run_id="some-other-run"), "run_id must be")
    refuses("a task_id that is not this case is refused",
            lambda d: d.update(task_id="curr-999"), "task_id must be")
    refuses("a reviewer missing a field is refused",
            lambda d: d.update(reviewer={"role": "author_system", "agent": "a"}),
            "reviewer must contain exactly")
    refuses("a reviewer that is not the author system is refused",
            lambda d: d["reviewer"].update(role="judge"),
            "reviewer.role must be author_system")
    refuses("a blank reviewer field is refused",
            lambda d: d["reviewer"].update(model="   "),
            "reviewer.model must be a non-empty string")
    refuses("an unknown judge_assessment decision is refused",
            lambda d: d["judge_assessment"].update(decision="mostly"),
            "judge_assessment.decision must be")
    refuses("a judge_assessment with extra keys is refused",
            lambda d: d["judge_assessment"].update(extra=1),
            "judge_assessment must contain exactly")
    refuses("strengths must be a list of non-empty strings",
            lambda d: d.update(strengths_to_preserve=["", "ok"]),
            "strengths_to_preserve must be a list")
    refuses("root_causes must be a list",
            lambda d: d.update(root_causes={}), "root_causes must be a list")
    refuses("improvements must be a list",
            lambda d: d.update(improvements={}), "improvements must be a list")

    # Root-cause and improvement item shapes. Each of these is a field an
    # aggregator later groups on, so a bad value silently mis-files the item.
    def with_cause(**over):
        base = {"category": "verification-gap", "description": "d",
                "evidence": ["e"], "systemic": True, "confidence": "high",
                "affected_files": ["scripts/verify.py"]}
        base.update(over)
        return lambda d: d.update(root_causes=[base])

    refuses("an unknown root-cause category is refused",
            with_cause(category="vibes"), "category is unknown")
    refuses("a non-boolean systemic flag is refused",
            with_cause(systemic="yes"), "systemic must be a boolean")
    refuses("an unknown confidence level is refused",
            with_cause(confidence="certain"), "confidence must be low")
    refuses("empty evidence is refused",
            with_cause(evidence=[]), "evidence must not be empty")
    refuses("a root cause with a missing key is refused",
            lambda d: d.update(root_causes=[{"category": "verification-gap"}]),
            "must contain exactly")
    # An absolute path in a finding is the one that matters: the backlog is read
    # on a different machine, where /home/someone/... names nothing.
    refuses("an ABSOLUTE affected_files path is refused",
            with_cause(affected_files=["/etc/passwd"]),
            "must be repository-relative")
    refuses("a parent-escaping affected_files path is refused",
            with_cause(affected_files=["../../secrets.txt"]),
            "must be repository-relative")

    def with_improvement(**over):
        base = {"issue_key": "fix-the-thing", "title": "t", "priority": "p1",
                "scope": "systemic", "proposed_change": "c",
                "affected_files": ["scripts/verify.py"],
                "regression_test": "r", "expected_impact": "i", "risk": "k"}
        base.update(over)
        return lambda d: d.update(improvements=[base])

    refuses("a non-slug issue_key is refused",
            with_improvement(issue_key="Fix The Thing!"),
            "issue_key must be a 3-80 character lowercase slug")
    refuses("an unknown priority is refused",
            with_improvement(priority="urgent"), "priority must be p0")
    refuses("an unknown scope is refused",
            with_improvement(scope="everything"), "scope must be systemic")
    refuses("a blank required improvement field is refused",
            with_improvement(risk="  "), "risk must be a non-empty string")

    def duplicate_keys(d):
        item = {"issue_key": "same-key", "title": "t", "priority": "p1",
                "scope": "systemic", "proposed_change": "c",
                "affected_files": [], "regression_test": "r",
                "expected_impact": "i", "risk": "k"}
        d.update(improvements=[dict(item), dict(item)])
    refuses("two improvements sharing an issue_key are refused",
            duplicate_keys, "issue_key values must be unique")

# ── derive_official_result: the score is RECOMPUTED, never taken on trust ────
# This is the function that refuses to inherit a verdict's own ACCEPT. Its
# failure paths raise rather than return, so nothing above reached them.
print("\nOfficial-result derivation:")
# Eight dimensions at 4 is 32, which clears MIN_TOTAL=27 and MIN_DIMENSION=3.
# A two-dimension fixture cannot reach the accept threshold at all, so every
# case below would have derived REJECT for the wrong reason.
DIMS = [f"d{i}" for i in range(8)]
_ALL_FOUR = {name: 4 for name in DIMS}


def derive(**over):
    verdict = {"task_id": "t-1", "dimension_scores": dict(_ALL_FOUR),
               "hard_failures": [], "total_score": 32, "verdict": "ACCEPT"}
    verdict.update(over)
    return review.derive_official_result(verdict, "t-1", DIMS)


def raises(label, needle, **over):
    try:
        derive(**over)
    except review.ReviewError as exc:
        check(label, needle in str(exc), f"expected {needle!r} in {exc}")
    else:
        check(label, False, "no ReviewError raised")


status, total = derive()
check("a well-formed ACCEPT derives ACCEPT and its total",
      (status, total) == ("ACCEPT", 32))
raises("a mismatched task_id raises", "task_id must be", task_id="other")
raises("missing dimensions raise", "exactly the suite dimensions",
       dimension_scores={"d0": 4})
raises("a non-integer dimension score raises", "integers from 0 to 4",
       dimension_scores=dict(_ALL_FOUR, d1=3.5))
raises("an out-of-range dimension score raises", "integers from 0 to 4",
       dimension_scores=dict(_ALL_FOUR, d1=9))
raises("a total that does not equal the sum raises", "total_score must equal",
       total_score=99)
raises("hard_failures that are not strings raise", "hard_failures must be",
       hard_failures=[{"oops": 1}])
# The point of the whole function: a verdict claiming ACCEPT over a hard
# failure is a judging error, and it is named rather than averaged in.
raises("an ACCEPT claimed over a hard failure is refused",
       "verdict must be REJECT", hard_failures=["a PDF is missing"])
# 30 of 32 clears MIN_TOTAL comfortably; the single 2 is what rejects it, so
# this pins the floor rule specifically rather than the total rule again.
raises("an ACCEPT claimed below the dimension floor is refused",
       "verdict must be REJECT", dimension_scores=dict(_ALL_FOUR, d1=2),
       total_score=30)


# ── The CLI is the only entry point CI uses ─────────────────────────────────
# build_parser and main were entirely untested: every check above called the
# functions directly. So the dispatch that decides WHICH of them runs, and the
# ReviewError handler that turns a diagnosis into exit 2 rather than a
# traceback, were both unexercised — on the module the eval-results workflow
# invokes by command line and nothing else.
print("\nCommand-line dispatch:")
with tempfile.TemporaryDirectory() as temp:
    temp = Path(temp)
    run_dir = temp / "run"
    create_run(run_dir, ("curr-001",), rejected=False)
    packets = temp / "packets"

    rc = review.main(["prepare", "--run-dir", str(run_dir),
                      "--output-dir", str(packets)])
    check("`prepare` exits 0 and writes the packet tree", rc == 0
          and (packets / "tasks" / "curr-001" / "packet.json").is_file())

    responses = temp / "responses"
    responses.mkdir()
    (responses / "curr-001.json").write_text(
        json.dumps(completed_review("curr-001")), encoding="utf-8")
    rc = review.main(["aggregate", "--packet-dir", str(packets),
                      "--responses-dir", str(responses),
                      "--output-dir", str(temp / "agg")])
    check("`aggregate` exits 0 on a complete, valid response", rc == 0)

    backlog = temp / "agg" / "improvement-backlog.json"
    check("aggregate wrote a backlog for merge to consume", backlog.is_file())
    rc = review.main(["merge", "--backlog", str(backlog),
                      "--output-dir", str(temp / "merged")])
    check("`merge` exits 0 and writes a merged backlog", rc == 0
          and (temp / "merged" / "improvement-backlog.json").is_file())

    # Exit 2 with "no scored eval runs found", NOT a quiet 0. This test was
    # first written expecting a clean no-op and the code was right: a CI job
    # pointed at a runs root that turns out to hold nothing has almost
    # certainly been misconfigured, and reporting success would hide it.
    rc = review.main(["ci", "--runs-root", str(temp / "runs-empty"),
                      "--output-dir", str(temp / "ci-out")])
    check("`ci` over an EMPTY runs root fails loudly rather than passing",
          rc == 2)

    # A ReviewError must surface as exit 2 with a diagnosis on stderr, not as a
    # traceback: CI reads the exit code, and a human reads the line.
    rc = review.main(["prepare", "--run-dir", str(temp / "no-such-run"),
                      "--output-dir", str(temp / "nowhere")])
    check("a ReviewError becomes exit 2, not a traceback", rc == 2)

    # argparse's own refusals stay refusals: a missing required flag and an
    # unknown subcommand both exit non-zero rather than defaulting to `ci`.
    for argv, label in (([], "no subcommand"),
                        (["prepare"], "prepare without its required flags"),
                        (["nonsense"], "an unknown subcommand")):
        try:
            review.main(argv)
        except SystemExit as exc:
            check(f"{label} is refused by the parser", exc.code != 0)
        else:
            check(f"{label} is refused by the parser", False, "no SystemExit")


# ── Aggregate and merge under adverse inputs ────────────────────────────────
print("\nAggregate under adverse inputs:")
with tempfile.TemporaryDirectory() as temp:
    temp = Path(temp)
    run_dir = temp / "run"
    create_run(run_dir, ("curr-001", "curr-002"), rejected=False)
    packets = temp / "packets"
    review.prepare_run(run_dir, packets)

    responses = temp / "responses"
    responses.mkdir()
    (responses / "curr-001.json").write_text(
        json.dumps(completed_review("curr-001")), encoding="utf-8")
    # curr-002 has no response at all
    rc = review.main(["aggregate", "--packet-dir", str(packets),
                      "--responses-dir", str(responses),
                      "--output-dir", str(temp / "agg-partial")])
    check("a missing response is tolerated WITHOUT --require-complete", rc == 0)
    rc = review.main(["aggregate", "--packet-dir", str(packets),
                      "--responses-dir", str(responses),
                      "--output-dir", str(temp / "agg-strict"),
                      "--require-complete"])
    check("--require-complete makes the missing response fatal", rc != 0)

    # an INVALID response must be counted invalid, not folded into the backlog
    bad = completed_review("curr-002")
    bad["reviewer"]["role"] = "judge"
    (responses / "curr-002.json").write_text(json.dumps(bad), encoding="utf-8")
    rc = review.main(["aggregate", "--packet-dir", str(packets),
                      "--responses-dir", str(responses),
                      "--output-dir", str(temp / "agg-invalid")])
    check("an invalid response fails the aggregate", rc != 0)

    # merge: a backlog path that does not exist is a named error, exit 2
    rc = review.main(["merge", "--backlog", str(temp / "nope.json"),
                      "--output-dir", str(temp / "m")])
    check("merging a missing backlog is exit 2, not a traceback", rc == 2)

    # ci with an explicit run filter naming a run that is not there
    rc = review.main(["ci", "--runs-root", str(temp / "runs-none"),
                      "--output-dir", str(temp / "ci2"),
                      "--run-id", "does-not-exist"])
    check("ci with an unknown --run-id is exit 2", rc == 2)

if FAILS:
    print(f"\nFAIL: {len(FAILS)} author-review check(s) failed")
    for failure in FAILS:
        print(f"  {failure}")
    raise SystemExit(1)

print("\nok: author-review packets, validation, aggregation, and CI orchestration")
