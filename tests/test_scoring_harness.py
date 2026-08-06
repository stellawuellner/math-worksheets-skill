#!/usr/bin/env python3
"""Behavioral contract for scripts/score_eval_run.py."""

import importlib.util
import json
import os
import shutil
import tempfile
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "score_eval_run.py"
SUITE = ROOT / "evals" / "curriculum-suite-500.json"
spec = importlib.util.spec_from_file_location("score_eval_run", SCRIPT)
score = importlib.util.module_from_spec(spec)
spec.loader.exec_module(score)
FAILS = []


def check(name, condition, detail=""):
    print(f"  {'ok  ' if condition else 'FAIL'} {name}")
    if not condition:
        FAILS.append(f"{name}: {detail}")


def dump(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(data), encoding="utf-8")


def tiny_suite(path):
    source = json.loads(SUITE.read_text(encoding="utf-8"))
    source["tasks"] = source["tasks"][:1]
    source["suite"]["task_count"] = 1
    dump(path, source)
    return source


def create_case(run_dir):
    case = Path(run_dir) / "curr-001"
    case.mkdir(parents=True)
    for name in ("student_worksheet.pdf", "step_by_step_answer_key.pdf", "study_guide.pdf"):
        (case / name).write_bytes(b"%PDF-fake-for-injected-inspector")
    verify = {
        "topic": "counting", "problem_count": 8,
        "problems": [{"id": index, "type": "eval", "expr": "1", "expected": 1}
                     for index in range(1, 9)],
    }
    dump(case / "verify_worksheet.json", verify)
    dump(case / "verify_study_guide.json", {
        "topic": "counting guide", "problem_count": 1,
        "problems": [{"id": 1, "type": "manual", "prompt": "review"}],
        "allow_all_manual": True,
    })
    (case / "gate.log").write_text("gate summary\nBUILD PASSED — all gates green\n", encoding="utf-8")
    (case / "final_response.md").write_text(
        "Attached: student_worksheet.pdf, step_by_step_answer_key.pdf, study_guide.pdf",
        encoding="utf-8",
    )
    return case


def fake_pdf_inspector(path, role, rendered_dir, render_dpi):
    rendered = Path(rendered_dir) / "page-1.png"
    rendered.parent.mkdir(parents=True, exist_ok=True)
    rendered.write_bytes(b"png")
    page_count = 2 if role == "study_guide" else 1
    return {
        "role": role,
        "path": str(path),
        "size_bytes": Path(path).stat().st_size,
        "sha256": score.sha256_file(path),
        "page_count": page_count,
        "text_character_count": 64,
        "page_text_character_counts": [64] * page_count,
        "extracted_text": "\n".join(f"{index}. problem" for index in range(1, 9)),
        "rendered_pages": [str(rendered)],
        "render_dpi": render_dpi,
    }, []


def completed_verdict(template_path, *, scores=None, verdict="ACCEPT"):
    data = json.loads(Path(template_path).read_text(encoding="utf-8"))
    scores = scores or {name: 4 for name in data["dimension_scores"]}
    data.update({
        "judge": {"type": "independent agent", "id": "judge-a", "completed_at": "2026-08-03T00:00:00Z"},
        "verdict": verdict,
        "dimension_scores": scores,
        "total_score": sum(scores.values()),
        "manual_items_reviewed": 1,
        "errors": [],
        "critical_observations": [
            {"description": "Clear progression", "category": "pedagogy"}
        ],
        "artifact_findings": ["All pages inspected"],
        "incorrect_or_ambiguous_items": [],
        "rationale": "All hard gates and score thresholds are satisfied.",
    })
    return data


print("Core parsing and raster evidence:")
info = score.parse_pdfinfo("Pages: 2\nPage size: 612 x 792 pts (letter)\nEncrypted: no\n")
check("pdfinfo parser", info == {
    "page_count": 2, "page_size_points": [612.0, 792.0],
    "page_size_label": "612 x 792 pts (letter)", "encrypted": False,
})
with tempfile.TemporaryDirectory() as temp:
    pgm = Path(temp) / "p.pgm"
    pgm.write_bytes(b"P5\n# c\n4 3\n255\n" + bytes([255] * 11 + [0]))
    page = score.read_pgm(pgm)
    stats = score.raster_page_stats(page)
    check("PGM dimensions", page[:2] == (4, 3))
    check("raster ink fraction", stats["ink_fraction"] == round(1 / 12, 6))
    try:
        pgm.write_bytes(b"P2\n1 1\n255\n0")
        score.read_pgm(pgm)
        check("unsupported PGM rejected", False)
    except score.HarnessError:
        check("unsupported PGM rejected", True)
    pgm.write_bytes(b"P5\n2 2\n255\n\x00")
    try:
        score.read_pgm(pgm)
        check("truncated PGM rejected", False)
    except score.HarnessError:
        check("truncated PGM rejected", True)
check("garbage pdfinfo fields are ignored",
      score.parse_pdfinfo("no colon\nPages: nope\nEncrypted: yes\n") == {"encrypted": True})

original_tools = score.required_tools
score.required_tools = lambda: {"pdfinfo": "/p", "pdftotext": "/t", "pdftoppm": "/r"}
check("doctor succeeds with prerequisites", score.doctor() == 0)
score.required_tools = lambda: {"pdfinfo": None, "pdftotext": "/t", "pdftoppm": "/r"}
check("doctor reports missing prerequisite", score.doctor() == 2)
score.required_tools = original_tools

print("Real inspector orchestration with injected Poppler output:")
original_runner = score.run_command
with tempfile.TemporaryDirectory() as temp:
    pdf = Path(temp) / "a.pdf"
    pdf.write_bytes(b"pdf")
    render_dir = Path(temp) / "rendered"

    def fake_runner(args, cwd=None):
        args = [str(arg) for arg in args]
        if args[0] == "pdfinfo":
            return SimpleNamespace(returncode=0, stdout="Pages: 1\nPage size: 612 x 792 pts\nEncrypted: no\n", stderr="")
        if args[0] == "pdftotext":
            return SimpleNamespace(returncode=0, stdout="1. Count the dots.\f", stderr="")
        prefix = args[-1]
        if "-gray" in args:
            Path(prefix + "-1.pgm").write_bytes(b"P5\n10 10\n255\n" + bytes([255] * 95 + [0] * 5))
        else:
            Path(prefix + "-1.png").write_bytes(b"png")
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    score.run_command = fake_runner
    meta, findings = score.inspect_pdf(pdf, "student_worksheet", render_dir, 96)
    check("inspector collects pages/text/render", meta["page_count"] == 1 and meta["rendered_pages"])
    check("inspector emits no hard failure for valid fake PDF",
          not any(item["hard_failure"] for item in findings))

    def failed_runner(args, cwd=None):
        return SimpleNamespace(returncode=1, stdout="", stderr="broken")

    score.run_command = failed_runner
    _, broken = score.inspect_pdf(pdf, "student_worksheet", render_dir, 96)
    check("unreadable PDF is hard failure", broken[0]["code"] == "pdf_unreadable" and broken[0]["hard_failure"])

    calls = {"ppm": 0}
    stale = render_dir / "page-99.png"
    stale.write_bytes(b"stale")

    def fault_runner(args, cwd=None):
        args = [str(arg) for arg in args]
        if args[0] == "pdfinfo":
            return SimpleNamespace(returncode=0, stdout="Pages: 0\nEncrypted: yes\n", stderr="")
        if args[0] == "pdftotext":
            return SimpleNamespace(returncode=1, stdout="", stderr="no text")
        calls["ppm"] += 1
        return SimpleNamespace(returncode=1, stdout="", stderr="no render")

    score.run_command = fault_runner
    _, faults = score.inspect_pdf(pdf, "student_worksheet", render_dir, 96)
    codes = {item["code"] for item in faults}
    check("inspector captures encryption/zero/text/raster/judge faults",
          {"pdf_encrypted", "pdf_zero_pages", "pdf_text_extract_failed",
           "pdf_raster_failed", "judge_render_failed"} <= codes)
    check("stale judge renders are removed", not stale.exists())

    def visual_runner(args, cwd=None):
        args = [str(arg) for arg in args]
        if args[0] == "pdfinfo":
            return SimpleNamespace(returncode=0, stdout="Pages: 3\nEncrypted: no\n", stderr="")
        if args[0] == "pdftotext":
            return SimpleNamespace(returncode=0, stdout="\ftext\ftext\f", stderr="")
        prefix = args[-1]
        if "-gray" in args:
            blank = bytes([255] * 1000)
            sparse = bytes([255] * 999 + [0])
            edge = bytes([0] * 1000)
            for index, pixels in enumerate((blank, sparse, edge), 1):
                Path(f"{prefix}-{index}.pgm").write_bytes(b"P5\n20 50\n255\n" + pixels)
        else:
            Path(prefix + "-1.png").write_bytes(b"png")
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    score.run_command = visual_runner
    _, visual = score.inspect_pdf(pdf, "student_worksheet", render_dir, 96)
    visual_codes = {item["code"] for item in visual}
    check("blank/sparse/edge raster signals are emitted",
          {"blank_page", "sparse_page", "edge_ink"} <= visual_codes)
score.run_command = original_runner

print("Artifact discovery:")
with tempfile.TemporaryDirectory() as temp:
    case = Path(temp)
    (case / "ws_demo.pdf").write_bytes(b"x")
    (case / "ak_demo.pdf").write_bytes(b"x")
    (case / "ss_demo.pdf").write_bytes(b"x")
    path, ambiguous = score.discover_artifact(case, "student_worksheet")
    check("skill filename discovered", path.name == "ws_demo.pdf" and not ambiguous)
    (case / "ws_second.pdf").write_bytes(b"x")
    path, ambiguous = score.discover_artifact(case, "student_worksheet")
    check("equally plausible artifacts are ambiguous", path is None and len(ambiguous) == 2)
    check("natural page sort", score._natural_page_key("page-12.png") == 12)
    check("unknown artifact is absent", score.discover_artifact(case, "gate_log") == (None, []))
    recognized = {
        "step_by_step_answer_key": "ak_demo.pdf",
        "study_guide": "ss_demo.pdf",
        "worksheet_verification": "verify_demo.json",
        "study_guide_verification": "verify_ss_demo.json",
        "gate_log": "build-output.log",
        "final_response": "agent-response.txt",
    }
    check("all fallback filename families score",
          all(score.candidate_score(Path(name), role) > 0 for role, name in recognized.items()))
    check("irrelevant filename scores zero", score.candidate_score(Path("notes.md"), "final_response") == 0)
    check("None path resolves to None", score.resolve_path(case, None) is None)
    check("absolute path remains absolute", score.resolve_path(case, case / "x") == case / "x")

with tempfile.TemporaryDirectory() as temp:
    case = Path(temp)
    target = case / "nested" / "ws.pdf"
    target.parent.mkdir()
    target.write_bytes(b"x")
    dump(case / "artifacts.json", {
        "artifacts": {"student_worksheet": "nested/ws.pdf"},
        "surfaced_artifacts": list(score.PDF_ROLES),
    })
    resolved, ambiguities, surfaced, metrics, originals = score.resolve_artifacts(
        case, {"metrics": {"cost": 1}})
    check("per-task artifact manifest overrides discovery",
          resolved["student_worksheet"] == target and not ambiguities)
    check("per-task surfaced list and metrics load", surfaced == list(score.PDF_ROLES) and metrics["cost"] == 1)
    check("no declared original filenames by default", originals == {})
    dump(case / "artifacts.json", {
        "artifacts": {"student_worksheet": "nested/ws.pdf"},
        "original_filenames": {"student_worksheet": "ws_addstories_curr023.pdf"},
    })
    _, _, _, _, originals = score.resolve_artifacts(case, {})
    check("declared original build filenames load",
          originals == {"student_worksheet": ["ws_addstories_curr023.pdf"]})

print("Prepare + aggregate end to end:")
with tempfile.TemporaryDirectory() as temp:
    temp = Path(temp)
    suite_path = temp / "suite.json"
    tiny_suite(suite_path)
    run_dir = temp / "run"
    create_case(run_dir)
    grading = temp / "grading"
    manifest = score.prepare_run(
        suite_path, run_dir, grading, rerun=False, pdf_inspector=fake_pdf_inspector,
    )
    task_dir = grading / "tasks" / "curr-001"
    machine = json.loads((task_dir / "machine.json").read_text(encoding="utf-8"))
    check("prepare emits packet/template/manifest",
          (task_dir / "judge-packet.json").is_file()
          and (task_dir / "verdict.template.json").is_file()
          and manifest["task_ids"] == ["curr-001"])
    check("prepare recognizes manual review", machine["manual_item_count"] == 1)
    check("clean prepared task has no hard failures", not machine["machine_hard_failures"])
    check("prepare records how each artifact was surfaced",
          all(machine["artifact_surfacing"][role]["basis"] == "declared_filename"
              for role in score.PDF_ROLES), repr(machine.get("artifact_surfacing")))

    verdict = completed_verdict(task_dir / "verdict.template.json")
    dump(task_dir / "verdict.json", verdict)
    results = temp / "results"
    rc = score.aggregate_run(grading, results, require_complete=True)
    summary = json.loads((results / "summary.json").read_text(encoding="utf-8"))
    check("accepted verdict aggregates", rc == 0 and summary["counts"]["accepted"] == 1)
    check("acceptance arithmetic", summary["metrics"]["acceptance_rate"] == 1.0)
    check("manual review metric", summary["metrics"]["manual_review_rate"] == 1.0)
    check("all report formats exist",
          all((results / name).is_file() for name in (
              "summary.md", "task-scores.csv", "issues.jsonl",
          )))

    bad = dict(verdict)
    bad["total_score"] = 31
    dump(task_dir / "verdict.json", bad)
    bad_results = temp / "bad-results"
    rc = score.aggregate_run(grading, bad_results)
    check("judge total is never trusted", rc == 2)
    invalid = json.loads((bad_results / "summary.json").read_text(encoding="utf-8"))
    check("invalid verdict is reported", invalid["counts"]["invalid"] == 1)

    (task_dir / "verdict.json").unlink()
    pending_results = temp / "pending-results"
    rc = score.aggregate_run(grading, pending_results, require_complete=True)
    check("strict aggregation rejects pending review", rc == 1)

    machine["machine_hard_failures"] = ["worksheet missing"]
    machine["machine_status"] = "FAIL"
    dump(task_dir / "machine.json", machine)
    auto_results = temp / "auto-results"
    rc = score.aggregate_run(grading, auto_results, require_complete=True)
    auto = json.loads((auto_results / "summary.json").read_text(encoding="utf-8"))
    check("machine hard failure auto-rejects", rc == 0 and auto["counts"]["machine_rejected"] == 1)

    # Objective machine findings plus structured judge errors must retain task provenance.
    machine["machine_hard_failures"] = []
    machine["machine_status"] = "PASS_WITH_OBSERVATIONS"
    machine["findings"] = [score.finding("edge_ink", "warning", "inspect edge")]
    machine["metrics"] = {"latency_seconds": 4, "cost": 2}
    dump(task_dir / "machine.json", machine)
    reject_scores = {name: 3 for name in verdict["dimension_scores"]}
    rejected = completed_verdict(
        task_dir / "verdict.template.json", scores=reject_scores, verdict="REJECT",
    )
    rejected["errors"] = [{"description": "Wrong notation", "severity": "major", "category": "math"}]
    dump(task_dir / "verdict.json", rejected)
    reject_results = temp / "reject-results"
    rc = score.aggregate_run(grading, reject_results)
    rejected_summary = json.loads((reject_results / "summary.json").read_text(encoding="utf-8"))
    check("quality reject can still pass hard gates",
          rc == 0 and rejected_summary["task_results"][0]["hard_gate_pass"])
    check("judge errors and observations retain separate ledgers",
          rejected_summary["errors"][0]["source"] == "judge"
          and rejected_summary["critical_observations"][0]["source"] == "judge")
    check("latency/cost medians aggregate",
          rejected_summary["metrics"]["median_latency_seconds"] == 4
          and rejected_summary["metrics"]["median_cost"] == 2)
    check("clean verdicts produce no unsupported-claim ledger",
          rejected_summary["unsupported_claims"] == []
          and rejected_summary["counts"]["needs_adjudication"] == 0)

    # A REJECT whose hard failure quotes a value the artifacts never print is
    # held for adjudication instead of being counted as a decided task.
    fabricating = completed_verdict(task_dir / "verdict.template.json", verdict="REJECT")
    fabricating["hard_failures"] = [
        "The answer key prints 36 for item 10; the worksheet's own value is 27."
    ]
    dump(task_dir / "verdict.json", fabricating)
    claim_results = temp / "claim-results"
    rc = score.aggregate_run(grading, claim_results, require_complete=True)
    claim_summary = json.loads((claim_results / "summary.json").read_text(encoding="utf-8"))
    flagged_values = sorted(item["value"] for item in claim_summary["unsupported_claims"])
    check("aggregate flags hard-failure claims absent from the artifacts",
          flagged_values == ["27", "36"], repr(claim_summary["unsupported_claims"]))
    check("an unsupported hard failure is held for adjudication",
          [item["task_id"] for item in claim_summary["needs_adjudication"]] == ["curr-001"]
          and claim_summary["task_results"][0]["hard_failure_claims_unverified"])
    check("a run needing adjudication is not complete", rc == 1)
    check("unsupported claims get their own ledger file",
          (claim_results / "unsupported-claims.jsonl").is_file()
          and "Claims not found in the artifacts"
          in (claim_results / "summary.md").read_text(encoding="utf-8"))

print("Verdict validation branches:")
dimensions = [f"d{index}" for index in range(8)]
base = {
    "task_id": "curr-001", "verdict": "REJECT", "hard_failures": [],
    "dimension_scores": {name: 3 for name in dimensions}, "total_score": 24,
    "manual_items_reviewed": 0, "incorrect_or_ambiguous_items": [],
    "errors": ["minor notation concern"],
    "critical_observations": [{"description": "needs review"}],
    "artifact_findings": ["inspected"], "rationale": "Below total threshold.",
}
validated = score.validate_verdict(base, "curr-001", dimensions, [])
check("below-threshold reject validates", validated["valid"] and validated["computed_verdict"] == "REJECT")
base["hard_failures"] = ["wrong answer"]
validated = score.validate_verdict(base, "curr-001", dimensions, [])
check("judge hard failure remains reject", validated["valid"] and validated["combined_hard_failures"])
broken = dict(base)
broken.update({"hard_failures": "bad", "errors": [{}], "rationale": ""})
validated = score.validate_verdict(broken, "curr-999", dimensions, [])
check("malformed verdict accumulates validation errors", len(validated["validation_errors"]) >= 4)
bad_scores = dict(base)
bad_scores["hard_failures"] = []
bad_scores["dimension_scores"] = {name: 5 for name in dimensions}
bad_scores["total_score"] = 40
validated = score.validate_verdict(bad_scores, "curr-001", dimensions, [])
check("out-of-range scores are invalid", not validated["valid"])
critical_without_hard = dict(base)
critical_without_hard["hard_failures"] = []
critical_without_hard["errors"] = [{"description": "fatal", "severity": "critical"}]
validated = score.validate_verdict(critical_without_hard, "curr-001", dimensions, [])
check("critical error cannot be averaged away", not validated["valid"])
incorrect_without_hard = dict(base)
incorrect_without_hard["hard_failures"] = []
incorrect_without_hard["incorrect_or_ambiguous_items"] = ["problem 2 is wrong"]
validated = score.validate_verdict(incorrect_without_hard, "curr-001", dimensions, [])
check("incorrect item requires hard failure", not validated["valid"])
check("non-list observation field is invalid",
      score.normalize_note_list("no", "notes", [])[0:] == [])

print("Run-manifest contract and helper metrics:")
with tempfile.TemporaryDirectory() as temp:
    temp = Path(temp)
    dump(temp / "run-manifest.json", {
        "schema_version": "1.0", "run_id": "r1",
        "cases": [{"task_id": "curr-001", "directory": "x"}],
    })
    cases, run_manifest = score.load_run_cases(temp)
    check("run manifest parsed", run_manifest["run_id"] == "r1" and "curr-001" in cases)
    dump(temp / "run-manifest.json", {"schema_version": "0", "cases": []})
    try:
        score.load_run_cases(temp)
        check("bad run manifest rejected", False)
    except score.HarnessError:
        check("bad run manifest rejected", True)
    dump(temp / "run-manifest.json", {
        "schema_version": "1.0", "cases": [
            {"task_id": "curr-001"}, {"task_id": "curr-001"},
        ],
    })
    try:
        score.load_run_cases(temp)
        check("duplicate run-manifest task rejected", False)
    except score.HarnessError:
        check("duplicate run-manifest task rejected", True)

with tempfile.TemporaryDirectory() as temp:
    temp = Path(temp)
    (temp / "tasks" / "curr-001").mkdir(parents=True)
    found, duplicates = score.find_case_directory(temp, "curr-001")
    check("tasks/ fallback directory discovered", found == temp / "tasks" / "curr-001" and not duplicates)
    cases, default_manifest = score.load_run_cases(temp)
    check("run manifest is optional", cases == {} and default_manifest["run_id"] == temp.name)
    dump(temp / "run.json", {"run_id": "native-run", "task_ids": ["curr-001"]})
    cases, native_manifest = score.load_run_cases(temp)
    check("native run manifest is supported",
          cases == {} and native_manifest["task_ids"] == ["curr-001"])
    dump(temp / "run.json", {"run_id": "bad-native-run"})
    try:
        score.load_run_cases(temp)
        check("native run requires task ids", False)
    except score.HarnessError:
        check("native run requires task ids", True)
    try:
        score.read_text_file(temp / "missing")
        check("unreadable text evidence rejected", False)
    except score.HarnessError:
        check("unreadable text evidence rejected", True)

print("Verification and bad-run evidence:")
with tempfile.TemporaryDirectory() as temp:
    temp = Path(temp)
    invalid_json = temp / "invalid.json"
    invalid_json.write_text("{", encoding="utf-8")
    _, findings = score.inspect_verification(invalid_json, "worksheet_verification", rerun=False)
    check("invalid verification JSON is hard failure", findings[0]["code"] == "verification_invalid")
    dump(temp / "schema.json", {"problem_count": "one", "problems": {}})
    _, findings = score.inspect_verification(temp / "schema.json", "worksheet_verification", rerun=False)
    check("verification schema is enforced", findings[0]["code"] == "verification_schema")
    dump(temp / "count.json", {"problem_count": 2, "problems": [{"id": 1, "type": "manual"}]})
    _, findings = score.inspect_verification(temp / "count.json", "worksheet_verification", rerun=False)
    check("verification subpart counts may differ from worksheet count", not findings)
    original_rerun = score.rerun_verifier
    score.rerun_verifier = lambda path: {"exit_code": 1, "stdout": "FAIL", "stderr": ""}
    _, findings = score.inspect_verification(temp / "count.json", "worksheet_verification", rerun=True)
    check("failed verifier rerun is hard failure",
          any(item["code"] == "verifier_rerun_failed" for item in findings))
    score.rerun_verifier = original_rerun

check("response needs PDF evidence", not score.response_surfaces("worksheet attached", "student_worksheet", None))
check("role phrase can prove surfacing",
      score.response_surfaces("The answer key is in key.pdf", "step_by_step_answer_key", None))
check("plural PDF label can prove surfacing",
      score.response_surfaces("Three PDFs: worksheet, answer key, and study guide.",
                              "study_guide", None))
check("problem number extraction deduplicates",
      score.extract_problem_numbers("1. a\n2) b\n2) repeat\nnot a problem") == [1, 2])

# --------------------------------------------------------------------------
# Regression: artifact-surfacing-check-tests-vocabulary-not-surfacing
#
# `record` renames build outputs to canonical roles, so the response names
# `ws_addstories_curr023.pdf` while the retained file is `worksheet.pdf`. The
# filename branch compared against the canonical name only, so across a 300-case
# run it credited zero of the 204 responses that did name their artifacts, and
# every pass came from the word "pdf" plus a role phrase.
print("Artifact surfacing is measured by filename, not vocabulary:")
CANONICAL = {
    "student_worksheet": "/run/curr-023/worksheet.pdf",
    "step_by_step_answer_key": "/run/curr-023/answer_key.pdf",
    "study_guide": "/run/curr-023/study_guide.pdf",
}
build_named = (
    "Three PDFs are ready:\n"
    "- **`ws_addstories_curr023.pdf`** - the student worksheet\n"
    "- **`ak_addstories_curr023.pdf`** - the answer key\n"
    "- **`ss_addstories_curr023.pdf`** - the study guide\n"
)
check("original build filename surfaces its role",
      all(score.response_surfaces(build_named, role, path)
          for role, path in CANONICAL.items()))
check("original build filename is credited as filename evidence, not vocabulary",
      score.surfacing_evidence(build_named, "student_worksheet",
                               CANONICAL["student_worksheet"])["basis"] == "build_filename")
# The role phrases are deliberately absent here: only the filename can prove it.
bare_name = "Attached: ak_addstories_curr023.pdf"
check("build filename alone proves surfacing without any role vocabulary",
      score.response_surfaces(bare_name, "step_by_step_answer_key",
                              CANONICAL["step_by_step_answer_key"]))
check("a build filename only credits its own role",
      not score.response_surfaces(bare_name, "study_guide", CANONICAL["study_guide"]))
# No role vocabulary here either: only the wrapped filename can prove it.
wrapped_name = "Delivered in the build directory: `ws_addstories_\ncurr023.pdf`."
check("a filename split by line wrapping still matches",
      score.response_surfaces(wrapped_name, "student_worksheet",
                              CANONICAL["student_worksheet"]))
wrapped_phrase = (
    "Three PDFs: the student worksheet (10 problems, 5 pages), a step-by-step answer\n"
    "key, and a two-page study guide.\n"
)
check("a role phrase split by line wrapping still matches",
      score.response_surfaces(wrapped_phrase, "step_by_step_answer_key",
                              CANONICAL["step_by_step_answer_key"]))
check("recorded original filename is matched when it breaks the build convention",
      score.response_surfaces("Delivered: handout-final.pdf", "student_worksheet",
                              CANONICAL["student_worksheet"], ["handout-final.pdf"]))
check("gate logs recover the build names the response uses",
      score.discover_original_names([
          "compiled ws_addstories_curr023.pdf\nwrote ak_addstories_curr023.pdf\n"
      ]) == {"student_worksheet": ["ws_addstories_curr023.pdf"],
             "step_by_step_answer_key": ["ak_addstories_curr023.pdf"]})
check("prose is not mistaken for a build filename",
      not score.response_surfaces("The sheet draws_shapes.pdf-style figures.",
                                  "student_worksheet", None))
unsurfaced = (
    "Three documents, all compiled and gated: a 10-problem student worksheet, a full\n"
    "step-by-step answer key, and a 2-page study guide.\n"
)
check("naming no file and no PDF still fails the gate",
      not any(score.response_surfaces(unsurfaced, role, path)
              for role, path in CANONICAL.items()))
check("description-only surfacing is recorded as the weak evidence it is",
      score.surfacing_evidence("Three PDFs: worksheet, answer key, and study guide.",
                               "study_guide", None)["basis"] == "description")

# The frozen 300-case run is the corpus the defect was measured on: 11 cases
# failed, and the 10 that name neither a file nor a PDF must keep failing.
RUNS = ROOT / "evals" / "runs"
UNSURFACED_TASKS = [
    "curr-050", "curr-051", "curr-150", "curr-173", "curr-250",
    "curr-295", "curr-350", "curr-373", "curr-412", "curr-450",
]
corpus = {}
for task_id in UNSURFACED_TASKS + ["curr-406", "curr-003"]:
    hits = sorted(RUNS.glob(f"*/tasks/{task_id}/final_response.md"))
    if hits:
        corpus[task_id] = hits[0].read_text(encoding="utf-8", errors="replace")
if len(corpus) == len(UNSURFACED_TASKS) + 2:
    still_failing = [
        task_id for task_id in UNSURFACED_TASKS
        if not all(score.response_surfaces(corpus[task_id], role, path)
                   for role, path in CANONICAL.items())
    ]
    check("the genuinely unsurfaced responses still fail",
          still_failing == UNSURFACED_TASKS, f"passing now: "
          f"{sorted(set(UNSURFACED_TASKS) - set(still_failing))}")
    check("curr-406's wrapped role phrase no longer fails the gate",
          all(score.response_surfaces(corpus["curr-406"], role, path)
              for role, path in CANONICAL.items()))
    check("a response naming build filenames is credited by filename",
          all(score.surfacing_evidence(corpus["curr-003"], role, path)["basis"]
              == "build_filename" for role, path in CANONICAL.items()))
else:
    print("  skip  frozen eval run corpus is not present")

with tempfile.TemporaryDirectory() as temp:
    temp = Path(temp)
    suite_path = temp / "suite.json"
    suite = tiny_suite(suite_path)
    bad_suite = dict(suite)
    bad_suite["judge_protocol"] = {}
    dump(temp / "bad-suite.json", bad_suite)
    try:
        score.prepare_run(temp / "bad-suite.json", temp, temp / "out", pdf_inspector=fake_pdf_inspector)
        check("missing rubric rejected", False)
    except score.HarnessError:
        check("missing rubric rejected", True)
    try:
        score.prepare_run(suite_path, temp / "no-run", temp / "out", pdf_inspector=fake_pdf_inspector)
        check("missing run directory rejected", False)
    except score.HarnessError:
        check("missing run directory rejected", True)
    try:
        score.select_tasks(suite, ["curr-999"])
        check("unknown selected task rejected", False)
    except score.HarnessError:
        check("unknown selected task rejected", True)

    missing_run = temp / "missing-run"
    missing_run.mkdir()
    missing_grading = temp / "missing-grading"
    score.prepare_run(
        suite_path, missing_run, missing_grading, rerun=False,
        pdf_inspector=fake_pdf_inspector,
    )
    missing_machine = json.loads(
        (missing_grading / "tasks" / "curr-001" / "machine.json").read_text(encoding="utf-8")
    )
    check("missing task directory becomes machine reject",
          missing_machine["machine_status"] == "FAIL"
          and missing_machine["findings"][0]["code"] == "missing_task_directory")

# --------------------------------------------------------------------------
# Regression: hard-failure-claims-must-cite-verified-artifact-values
#
# curr-131 was rejected on "4/5 of 45 is 36" for a problem that asks for 3/5 of
# 45; 36 is printed nowhere in the packet, and four rubric points moved on it.
# Nothing required a finding to quote a string the artifact actually contains.
print("Judge claims are checked against the artifact values:")
audit = getattr(score, "audit_verdict_claims", None)
build_index = getattr(score, "artifact_value_index", None)
if not (audit and build_index):
    check("harness audits verdict claims against artifact values", False,
          "score_eval_run has no audit_verdict_claims/artifact_value_index")
else:
    # As pdftotext renders it: \frac{3}{5} flattens to "35" and the display
    # fraction in the key splits its numerator and denominator across lines.
    worksheet_text = (
        "10. Sam is asked for 35 of 45 counters. He splits the 45 counters into five\n"
        "equal groups, points at one group, and says the answer is 9.\n"
    )
    key_text = (
        "1. 6    4. 24    7. 0.3    10. 27\n"
        "Step 3. Finish the job: 3 x 9.\n"
        "                                     27 counters\n"
        "Step 4. Check on the picture: 27 + 18 = 45\n"
    )
    index = build_index([worksheet_text, key_text])
    fabricated = {
        "hard_failures": [
            "The Quick Answers bank prints 27 for item 10, which is Sam's planted wrong "
            "result; the requested correct value is 36 because 4/5 of 45 is 36."
        ],
        "errors": [],
        "critical_observations": [],
        "artifact_findings": [],
        "incorrect_or_ambiguous_items": [],
        "rationale": "",
    }
    findings = audit(fabricated, index)
    check("a hard failure quoting a value no artifact prints is flagged",
          [item["value"] for item in findings] == ["36"], repr(findings))
    check("an unsupported hard-failure claim blocks rather than passes silently",
          bool(findings) and findings[0]["blocking"]
          and findings[0]["code"] == "claim_value_not_in_artifact")
    check("values the artifact does print are not flagged",
          not audit({"hard_failures": [
              "Item 10's quick answer is 27, and the worked solution shades 27 of the 45."
          ]}, index), repr(audit({"hard_failures": [
              "Item 10's quick answer is 27, and the worked solution shades 27 of the 45."
          ]}, index)))
    check("a flattened fraction still counts as present",
          not audit({"artifact_findings": ["Item 10 asks for 3/5 of 45."]}, index))
    check("artifact references are not treated as quoted values",
          not audit({"artifact_findings": [
              "Exactly 10 readable problems over 5 pages; item 7 is the hardest."
          ]}, index))

    # curr-005: the relation is right, the numbers recited are not.
    compare_index = build_index([
        "Quick answers: 1. 8   2. 14   4. 3   6. 5\n"
        "5. Jar A is a full ten frame and 2 loose, so 12. Jar B is a ten frame and 5, so 15.\n",
        '{"problems": [{"id": 5, "type": "compare", "values": ["10+2", "10+5"]}]}',
    ])
    flagged = audit({"critical_observations": [
        "Verified totals and relations 8, 14, difference 3, 12<16, and difference 5."
    ]}, compare_index)
    check("a recited relation citing an absent number is flagged",
          [item["value"] for item in flagged] == ["12<16"], repr(flagged))
    check("a recitation flag is review-only, not a block on the verdict",
          bool(flagged) and not flagged[0]["blocking"]
          and flagged[0]["severity"] == "review")

    # curr-369: the hole is at x = -2, the asymptote at x = 2. Both values are
    # in the key, so only the pair as a unit shows the swap.
    hole_index = build_index([
        "The factor x + 2 cancels completely, so it produces the hole.\n"
        "                     hole at -2, 54\n"
        "                                           and vertical asymptote x = 2\n"
    ])
    swapped = audit({"artifact_findings": ["Independent factoring gives the hole (2, 5/4)."]},
                    hole_index)
    check("a coordinate pair the artifact never prints together is flagged",
          [item["value"] for item in swapped] == ["(2, 5/4)"], repr(swapped))
    check("the pair the artifact does print is not flagged",
          not audit({"artifact_findings": ["The hole is (-2, 5/4)."]}, hole_index))

    # False-positive guards: mangled radicals and the judge's own arithmetic.
    radical_index = build_index(["The exact value is 2 3 after rationalising.\n"])
    check("a mangled radical is not reported as a fabricated value",
          not audit({"artifact_findings": ["The exact value is 2√3."]}, radical_index))
    check("an asserted correction is not read as a transcription",
          not audit({"hard_failures": [
              "The key omits the required factor of 100 in the accumulation formula."
          ]}, build_index(["C'(x) is measured in dollars per unit.\n"])))

    check("a critical judge error is treated as blocking",
          audit({"errors": [{"description": "The key prints 36.", "severity": "critical"}]},
                index)[0]["blocking"])
    check("claim extraction ignores wrapped-artifact noise",
          score.extract_claim_values("Problem 4 on page 2 lists 6 items.") == [])
    check("nothing extractable means nothing to flag",
          audit({"hard_failures": ["The key prints 36."]}, build_index([])) == [])

rows = [
    {"band": "a", "domain": "x", "status": "ACCEPT", "metrics": {"cost": 1.0}},
    {"band": "a", "domain": "y", "status": "REJECT", "metrics": {"cost": 3.0}},
]
check("group metrics", score.group_metrics(rows, "band")["a"]["acceptance_rate"] == 0.5)
check("median metric", score.numeric_metric(rows, "cost") == 2.0)
check("zero denominator rate", score.rate(1, 0) is None)

print("CLI dispatch:")
original_doctor = score.doctor
score.doctor = lambda: 7
check("main dispatches doctor", score.main(["doctor"]) == 7)
score.doctor = original_doctor
check("main rejects unsafe render DPI", score.main([
    "prepare", "--run-dir", "/tmp", "--output-dir", "/tmp/x", "--render-dpi", "20",
]) == 2)

if FAILS:
    print(f"\nFAIL: {len(FAILS)} scoring-harness check(s)")
    for failure in FAILS:
        print("  " + failure)
    raise SystemExit(1)
print("\nPASS: scoring harness")
