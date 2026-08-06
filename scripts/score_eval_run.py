#!/usr/bin/env python3
"""Prepare and aggregate curriculum worksheet evaluation runs.

The harness deliberately separates deterministic evidence collection from the
qualitative judgment that requires a human or an independent vision-capable
agent.  ``prepare`` validates the retained artifacts, reruns the fixed math
verifier, renders PDFs for review, and writes a blind packet plus verdict
template per task.  ``aggregate`` validates completed verdicts and computes
the acceptance metrics without trusting judge-supplied totals or verdicts.

Run layout (an optional run-manifest.json can override every path):

    RUN/curr-001/student_worksheet.pdf
    RUN/curr-001/step_by_step_answer_key.pdf
    RUN/curr-001/study_guide.pdf
    RUN/curr-001/verify_worksheet.json
    RUN/curr-001/verify_study_guide.json
    RUN/curr-001/gate.log
    RUN/curr-001/final_response.md

See evals/scoring-harness.md for the full contract.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SUITE = ROOT / "evals" / "curriculum-suite-500.json"
PDF_ROLES = (
    "student_worksheet",
    "step_by_step_answer_key",
    "study_guide",
)
EVIDENCE_ROLES = (
    "worksheet_verification",
    "study_guide_verification",
    "gate_log",
    "final_response",
)
ALL_ROLES = PDF_ROLES + EVIDENCE_ROLES
DIMENSION_FLOOR = 3
TOTAL_FLOOR = 27
BLANK_INK_FRACTION = 0.0005
LOW_INK_FRACTION = 0.0015
EDGE_INK_FRACTION = 0.02

# build.sh names its outputs `<prefix>_<role><variant>_<stem>.pdf`; `record`
# renames them to canonical roles, so a delivery message and a retained
# artifact refer to the same file under two different names.
BUILD_ROLE_TAGS = {
    "student_worksheet": "ws",
    "step_by_step_answer_key": "ak",
    "study_guide": "ss",
}
TAG_TO_ROLE = {tag: role for role, tag in BUILD_ROLE_TAGS.items()}
ROLE_PHRASES = {
    "student_worksheet": ("worksheet",),
    "step_by_step_answer_key": ("answer key", "answer-key", "answer_key"),
    "study_guide": ("study guide", "study-guide", "skills summary", "skills-summary"),
}
# Verdict fields whose prose can quote artifact values.
CLAIM_FIELDS = (
    "hard_failures",
    "incorrect_or_ambiguous_items",
    "errors",
    "critical_observations",
    "artifact_findings",
    "rationale",
)
# A claim in one of these fields is what a REJECT rests on, so an unsupported
# value there blocks the verdict from being counted without adjudication.
BLOCKING_CLAIM_FIELDS = ("hard_failures",)


class HarnessError(RuntimeError):
    """A harness/configuration failure, distinct from a rejected eval task."""


def now_utc():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def load_json(path, label="JSON"):
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise HarnessError(f"cannot read {label} {path}: {exc}") from exc


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


def finding(code, severity, message, *, artifact=None, evidence=None,
            hard_failure=False):
    item = {
        "code": code,
        "severity": severity,
        "message": message,
        "hard_failure": bool(hard_failure),
    }
    if artifact:
        item["artifact"] = artifact
    if evidence is not None:
        item["evidence"] = evidence
    return item


def run_command(args, *, cwd=None):
    return subprocess.run(
        [str(arg) for arg in args], cwd=cwd, capture_output=True, text=True,
        errors="replace",
    )


def required_tools():
    return {
        name: shutil.which(name)
        for name in ("pdfinfo", "pdftotext", "pdftoppm")
    }


def doctor():
    tools = required_tools()
    checks = {
        "python": sys.executable,
        "pdfinfo": tools["pdfinfo"],
        "pdftotext": tools["pdftotext"],
        "pdftoppm": tools["pdftoppm"],
        "run_verify": str(ROOT / "scripts" / "run_verify.sh")
        if (ROOT / "scripts" / "run_verify.sh").is_file() else None,
    }
    for name, value in checks.items():
        print(f"{'ok' if value else 'MISSING':7} {name:12} {value or ''}")
    return 0 if all(checks.values()) else 2


def parse_pdfinfo(text):
    result = {}
    for line in text.splitlines():
        if ":" not in line:
            continue
        key, value = (part.strip() for part in line.split(":", 1))
        if key == "Pages":
            try:
                result["page_count"] = int(value)
            except ValueError:
                pass
        elif key == "Page size":
            match = re.search(r"([\d.]+)\s+x\s+([\d.]+)\s+pts", value)
            if match:
                result["page_size_points"] = [
                    round(float(match.group(1)), 2),
                    round(float(match.group(2)), 2),
                ]
            result["page_size_label"] = value
        elif key == "Encrypted":
            result["encrypted"] = value.lower().startswith("yes")
    return result


def read_pgm(path):
    data = Path(path).read_bytes()
    fields = []
    index = 0
    while len(fields) < 4:
        while index < len(data) and data[index:index + 1].isspace():
            index += 1
        if data[index:index + 1] == b"#":
            while index < len(data) and data[index:index + 1] != b"\n":
                index += 1
            continue
        start = index
        while index < len(data) and not data[index:index + 1].isspace():
            index += 1
        fields.append(data[start:index])
    if fields[0] != b"P5" or fields[3] != b"255":
        raise HarnessError(f"unsupported PGM raster in {path}")
    index += 1
    width, height = int(fields[1]), int(fields[2])
    pixels = data[index:index + width * height]
    if len(pixels) != width * height:
        raise HarnessError(f"truncated PGM raster in {path}")
    return width, height, pixels


def raster_page_stats(page):
    width, height, pixels = page
    ink_pixels = sum(value < 245 for value in pixels)
    total = max(1, len(pixels))
    bx = max(1, width // 100)
    by = max(1, height // 100)
    border_ink = border_total = 0
    for y in range(height):
        row = y * width
        for x in range(width):
            if x < bx or x >= width - bx or y < by or y >= height - by:
                border_total += 1
                border_ink += pixels[row + x] < 245
    return {
        "width": width,
        "height": height,
        "ink_fraction": round(ink_pixels / total, 6),
        "edge_ink_fraction": round(border_ink / max(1, border_total), 6),
    }


def _natural_page_key(path):
    match = re.search(r"-(\d+)\.[^.]+$", Path(path).name)
    return int(match.group(1)) if match else 0


def inspect_pdf(path, role, rendered_dir, render_dpi=110):
    """Return (metadata, findings), using Poppler for structural and visual evidence."""
    path = Path(path)
    findings = []
    meta = {
        "role": role,
        "path": str(path),
        "size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }
    info = run_command(["pdfinfo", path])
    if info.returncode:
        findings.append(finding(
            "pdf_unreadable", "critical", "PDF cannot be read by pdfinfo.",
            artifact=role, evidence=(info.stderr or info.stdout).strip(),
            hard_failure=True,
        ))
        return meta, findings
    meta.update(parse_pdfinfo(info.stdout))
    if meta.get("encrypted"):
        findings.append(finding(
            "pdf_encrypted", "critical", "PDF is encrypted and cannot be reliably judged.",
            artifact=role, hard_failure=True,
        ))
    if meta.get("page_count", 0) < 1:
        findings.append(finding(
            "pdf_zero_pages", "critical", "PDF contains no pages.", artifact=role,
            hard_failure=True,
        ))

    extracted = run_command(["pdftotext", "-layout", path, "-"])
    if extracted.returncode:
        findings.append(finding(
            "pdf_text_extract_failed", "error", "PDF text extraction failed.",
            artifact=role, evidence=extracted.stderr.strip(), hard_failure=True,
        ))
        text = ""
    else:
        text = extracted.stdout
    page_text = text.split("\f")
    if page_text and not page_text[-1].strip():
        page_text.pop()
    meta["text_character_count"] = len(text.strip())
    meta["page_text_character_counts"] = [len(page.strip()) for page in page_text]
    meta["extracted_text"] = text

    with tempfile.TemporaryDirectory(prefix="mws-score-") as scratch:
        prefix = str(Path(scratch) / "page")
        raster = run_command(["pdftoppm", "-r", "36", "-gray", path, prefix])
        pgms = sorted(Path(scratch).glob("page-*.pgm"), key=_natural_page_key)
        if raster.returncode or not pgms:
            findings.append(finding(
                "pdf_raster_failed", "critical", "PDF could not be rasterized for visual checks.",
                artifact=role, evidence=(raster.stderr or raster.stdout).strip(),
                hard_failure=True,
            ))
        else:
            stats = [raster_page_stats(read_pgm(page)) for page in pgms]
            meta["raster_pages"] = stats
            for index, stat in enumerate(stats, 1):
                text_count = (meta["page_text_character_counts"][index - 1]
                              if index <= len(meta["page_text_character_counts"]) else 0)
                if stat["ink_fraction"] < BLANK_INK_FRACTION and text_count == 0:
                    findings.append(finding(
                        "blank_page", "critical", f"Page {index} appears blank.",
                        artifact=role, evidence=stat, hard_failure=True,
                    ))
                elif stat["ink_fraction"] < LOW_INK_FRACTION:
                    findings.append(finding(
                        "sparse_page", "warning", f"Page {index} has unusually little ink; inspect it.",
                        artifact=role, evidence=stat,
                    ))
                if stat["edge_ink_fraction"] > EDGE_INK_FRACTION:
                    findings.append(finding(
                        "edge_ink", "warning",
                        f"Page {index} has substantial ink in the outer 1% margin; inspect for clipping.",
                        artifact=role, evidence=stat,
                    ))

    rendered_dir = Path(rendered_dir)
    rendered_dir.mkdir(parents=True, exist_ok=True)
    for stale in rendered_dir.glob("page-*.png"):
        stale.unlink()
    rendered = run_command([
        "pdftoppm", "-r", str(render_dpi), "-png", path,
        str(rendered_dir / "page"),
    ])
    pages = sorted(rendered_dir.glob("page-*.png"), key=_natural_page_key)
    if rendered.returncode or not pages:
        findings.append(finding(
            "judge_render_failed", "critical", "Judge PNG rendering failed.",
            artifact=role, evidence=(rendered.stderr or rendered.stdout).strip(),
            hard_failure=True,
        ))
    meta["rendered_pages"] = [str(page) for page in pages]
    return meta, findings


def candidate_score(path, role):
    name = path.name.lower().replace("-", "_").replace(" ", "_")
    exact = {
        "student_worksheet": {"student_worksheet.pdf", "worksheet.pdf"},
        "step_by_step_answer_key": {
            "step_by_step_answer_key.pdf", "answer_key.pdf", "answerkey.pdf",
        },
        "study_guide": {"study_guide.pdf", "skills_summary.pdf", "skill_summary.pdf"},
        "worksheet_verification": {
            "verify.json", "verify_worksheet.json", "worksheet_verification.json",
        },
        "study_guide_verification": {
            "verify_study_guide.json", "study_guide_verification.json",
        },
        "gate_log": {"gate.log", "build.log", "gate_chain.log"},
        "final_response": {"final_response.md", "final_response.txt", "response.md", "response.txt"},
    }
    if name in exact[role]:
        return 100
    if role == "student_worksheet" and path.suffix.lower() == ".pdf":
        if name.startswith("ws_") or ("worksheet" in name and "answer" not in name):
            return 50
    if role == "step_by_step_answer_key" and path.suffix.lower() == ".pdf":
        if name.startswith("ak_") or "answer_key" in name or "answerkey" in name:
            return 50
    if role == "study_guide" and path.suffix.lower() == ".pdf":
        if name.startswith("ss_") or "study_guide" in name or "skills_summary" in name:
            return 50
    if role == "worksheet_verification" and path.suffix.lower() == ".json":
        if name.startswith("verify_") and not name.startswith("verify_ss_"):
            return 50
    if role == "study_guide_verification" and path.suffix.lower() == ".json":
        if name.startswith("verify_ss_"):
            return 50
    if role == "gate_log" and path.suffix.lower() in {".log", ".txt"}:
        if "gate" in name or "build" in name:
            return 40
    if role == "final_response" and path.suffix.lower() in {".md", ".txt"}:
        if "final" in name or "response" in name:
            return 40
    return 0


def discover_artifact(case_dir, role):
    files = [path for path in Path(case_dir).rglob("*") if path.is_file()]
    scored = [(candidate_score(path, role), path) for path in files]
    scored = [(score, path) for score, path in scored if score]
    if not scored:
        return None, []
    top = max(score for score, _ in scored)
    choices = sorted(path for score, path in scored if score == top)
    if len(choices) > 1:
        return None, choices
    return choices[0], []


def resolve_path(case_dir, value):
    if value is None:
        return None
    path = Path(value)
    return path if path.is_absolute() else Path(case_dir) / path


def resolve_artifacts(case_dir, case_record):
    case_dir = Path(case_dir)
    local = {}
    local_record = {}
    local_manifest = case_dir / "artifacts.json"
    if local_manifest.is_file():
        local_record = load_json(local_manifest, "task artifact manifest")
        local = local_record.get("artifacts", local_record)
    mapping = dict(local)
    mapping.update(case_record.get("artifacts", {}))
    resolved = {}
    ambiguities = {}
    for role in ALL_ROLES:
        if role in mapping:
            resolved[role] = resolve_path(case_dir, mapping[role])
        else:
            resolved[role], ambiguous = discover_artifact(case_dir, role)
            if ambiguous:
                ambiguities[role] = [str(path) for path in ambiguous]
    surfaced = case_record.get("surfaced_artifacts")
    if surfaced is None:
        surfaced = local_record.get("surfaced_artifacts")
    metrics = dict(local_record.get("metrics", {}))
    metrics.update(case_record.get("metrics", {}))
    originals = {}
    for source in (local_record, case_record):
        declared = source.get("original_filenames") or {}
        if isinstance(declared, dict):
            for role, names in declared.items():
                if isinstance(names, str):
                    names = [names]
                originals.setdefault(role, [])
                originals[role].extend(
                    name for name in names if name not in originals[role]
                )
    return resolved, ambiguities, surfaced, metrics, originals


def find_case_directory(run_dir, task_id):
    direct = [Path(run_dir) / task_id, Path(run_dir) / "tasks" / task_id]
    found = [path for path in direct if path.is_dir()]
    if found:
        return found[0], found[1:]
    matches = [path for path in Path(run_dir).rglob(task_id) if path.is_dir()]
    return (matches[0], matches[1:]) if matches else (None, [])


def load_run_cases(run_dir):
    manifest_path = Path(run_dir) / "run-manifest.json"
    if not manifest_path.is_file():
        native_path = Path(run_dir) / "run.json"
        if native_path.is_file():
            native = load_json(native_path, "native run manifest")
            if not isinstance(native.get("task_ids"), list):
                raise HarnessError("run.json must contain a task_ids list")
            return {}, native
        return {}, {"schema_version": "1.0", "run_id": Path(run_dir).name}
    manifest = load_json(manifest_path, "run manifest")
    if manifest.get("schema_version") != "1.0" or not isinstance(manifest.get("cases"), list):
        raise HarnessError("run-manifest.json must have schema_version 1.0 and a cases list")
    cases = {}
    for record in manifest["cases"]:
        task_id = record.get("task_id")
        if not isinstance(task_id, str) or task_id in cases:
            raise HarnessError(f"invalid or duplicate task_id in run manifest: {task_id!r}")
        cases[task_id] = record
    return cases, manifest


def read_text_file(path):
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        raise HarnessError(f"cannot read {path}: {exc}") from exc


def rerun_verifier(path):
    proc = run_command(["bash", ROOT / "scripts" / "run_verify.sh", path])
    return {
        "exit_code": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def inspect_verification(path, role, rerun=True):
    findings = []
    try:
        data = load_json(path, role)
    except HarnessError as exc:
        return {}, [finding(
            "verification_invalid", "critical", str(exc), artifact=role,
            hard_failure=True,
        )]
    problems = data.get("problems")
    declared = data.get("problem_count")
    meta = {
        "path": str(path),
        "sha256": sha256_file(path),
        "problem_count": declared,
        "listed_problem_count": len(problems) if isinstance(problems, list) else None,
        "manual_item_count": sum(
            problem.get("type") == "manual" for problem in problems
        ) if isinstance(problems, list) else 0,
    }
    if not isinstance(problems, list) or not isinstance(declared, int):
        findings.append(finding(
            "verification_schema", "critical",
            "Verification JSON must declare integer problem_count and a problems list.",
            artifact=role, hard_failure=True,
        ))
    # problem_count is the numbered worksheet-item count, while `problems`
    # contains verification checks. One numbered item may legitimately have
    # multiple checks/subparts, so their lengths need not match. verify.py's
    # coverage gate below is authoritative for missing numbered items.
    if rerun:
        rerun_result = rerun_verifier(path)
        meta["verifier_rerun"] = rerun_result
        if rerun_result["exit_code"] not in (0, 2):
            findings.append(finding(
                "verifier_rerun_failed", "critical",
                f"Deterministic verifier rerun exited {rerun_result['exit_code']}.",
                artifact=role,
                evidence=(rerun_result["stdout"] + rerun_result["stderr"])[-4000:],
                hard_failure=True,
            ))
    return meta, findings


def extract_problem_numbers(text):
    values = []
    for line in text.splitlines():
        match = re.match(r"^\s*(\d{1,3})(?:[.)]|\s{2,})", line)
        if match:
            values.append(int(match.group(1)))
    return sorted(set(values))


def wrap_tolerant(literal):
    """Regex for ``literal`` that survives line wrapping inside the token.

    A delivery message is prose: the filename it names can be broken across a
    line, and a role phrase can be split by the same wrap. Matching the raw
    string misses both, so every character is separated by optional space.
    """
    return r"\s*".join(re.escape(char) for char in literal)


def build_name_pattern(role):
    """Match build.sh's own output naming for ``role``, wrap tolerantly.

    The retained artifact is `worksheet.pdf`; the response names
    `ws_addstories_curr023.pdf`. Nothing records that mapping, so the role tag
    plus the stem convention is what identifies the file.
    """
    tag = BUILD_ROLE_TAGS[role]
    return (rf"(?<![a-z0-9])(?:[a-z]+\s*_\s*)*{tag}\s*[scx]?\s*_\s*"
            rf"[a-z0-9_][a-z0-9_\s]*\.\s*pdf")


BUILD_NAME_RE = re.compile(
    r"(?<![A-Za-z0-9])((?:[a-z]+_)*(ws|ak|ss)[scx]?_[A-Za-z0-9_]+\.pdf)"
)


def discover_original_names(texts):
    """Recover per-role build filenames from recorded evidence (e.g. gate logs)."""
    names = defaultdict(list)
    for text in texts:
        for match in BUILD_NAME_RE.finditer(text or ""):
            role = TAG_TO_ROLE[match.group(2)]
            if match.group(1) not in names[role]:
                names[role].append(match.group(1))
    return dict(names)


def surfacing_evidence(response, role, path=None, original_names=()):
    """How — not merely whether — the delivery message surfaces ``role``.

    Naming the file is the only evidence that an artifact was handed over;
    saying the word "worksheet" near the word "PDF" is vocabulary. Both are
    reported, distinguishably, so the gate can be read for what it measured.
    """
    lower = (response or "").lower()
    collapsed = re.sub(r"\s+", " ", lower)
    candidates = []
    if path:
        candidates.append(Path(path).name)
    candidates.extend(original_names or ())
    for name in candidates:
        name = str(name).strip().lower()
        if not name:
            continue
        match = re.search(rf"(?<![a-z0-9]){wrap_tolerant(name)}", lower)
        if match:
            return {"surfaced": True, "basis": "declared_filename",
                    "match": re.sub(r"\s+", "", match.group(0))}
    if role in BUILD_ROLE_TAGS:
        match = re.search(build_name_pattern(role), lower)
        if match:
            return {"surfaced": True, "basis": "build_filename",
                    "match": re.sub(r"\s+", "", match.group(0))}
    if re.search(r"(?:\.pdf\b|\bpdfs?\b)", collapsed):
        for phrase in ROLE_PHRASES[role]:
            if phrase in collapsed:
                return {"surfaced": True, "basis": "description", "match": phrase}
    return {"surfaced": False, "basis": None, "match": None}


def response_surfaces(response, role, path=None, original_names=()):
    return surfacing_evidence(response, role, path, original_names)["surfaced"]


# ---------------------------------------------------------------------------
# Claim auditing: a finding that quotes a value must quote one the artifact has
#
# pdftotext flattens `\frac{3}{5}` to "35", splits a display fraction across
# lines, and mangles radicals, so a literal comparison would flag correct
# findings constantly. Every check below therefore normalises first, accepts
# every plausible extraction of the same value, and reports "not found" as a
# review flag — never as an automatic overturn of the judge.

DASHES = "−–—‐‑‒"
NUMBER_RE = re.compile(r"(?<![\w.])-?\d+(?:\.\d+)?")
REF_WORDS = (r"problems?|items?|questions?|pages?|steps?|parts?|sections?|rows?|"
             r"columns?|lines?|tasks?|figures?|standards?|grades?|dimensions?|"
             r"scores?|totals?|facets?|boxes?|examples?|entry|entries|no|number|"
             r"factor(?: of)?")
REF_BEFORE_RE = re.compile(rf"(?:{REF_WORDS})\W{{0,3}}$", re.I)
COMPOUND_BEFORE_RE = re.compile(r"[A-Za-z]-$")
RADICAL_BEFORE_RE = re.compile(r"(?:√|sqrt|root)\s*\(?$", re.I)
COUNT_AFTER_RE = re.compile(
    r"^\s*(?:manual|problems?|items?|questions?|pages?|steps?|examples?|"
    r"dimensions?|facets?|boxes?|sections?|figures?|rows?|columns?)\b", re.I)
FRACTION_RE = re.compile(r"(?<![\d/])(-?\d+)\s*/\s*(\d+)(?![\d/])")
PAIR_RE = re.compile(
    r"\(\s*((?<![\w.])-?\d+(?:\.\d+)?(?:\s*/\s*\d+)?)\s*,"
    r"\s*(-?\d+(?:\.\d+)?(?:\s*/\s*\d+)?)\s*\)")
RELATION_RE = re.compile(
    r"(-?\d+(?:\.\d+)?)\s*(<=|>=|!=|<|>|=)\s*(-?\d+(?:\.\d+)?)")
ASSIGN_RE = re.compile(
    r"\b([A-Za-z][A-Za-z0-9_']{0,7}(?:\([^)]{0,6}\))?)\s*=\s*"
    r"(-?\d+(?:\.\d+)?(?:\s*/\s*\d+)?)")


def normalize_math_text(text):
    """Fold the characters PDF extraction varies on, so matching is stable."""
    text = str(text or "")
    for dash in DASHES:
        text = text.replace(dash, "-")
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", " ", text)
    return text


def artifact_value_index(texts):
    """Every numeric token the artifacts contain, plus their joined text."""
    numbers = set()
    parts = []
    for text in texts:
        if not text:
            continue
        normalized = normalize_math_text(text)
        parts.append(normalized)
        for match in NUMBER_RE.finditer(normalized):
            numbers.add(match.group(0))
            numbers.add(match.group(0).lstrip("-"))
    return {"numbers": numbers, "text": "\n".join(parts)}


def extract_claim_values(claim):
    """Pull the checkable values a finding quotes, ignoring artifact references.

    "problem 7" and "four pages" describe where to look; "36" and "12 < 16"
    assert what is printed there. Only the second kind is checkable.
    """
    text = normalize_math_text(claim)
    values = []
    spans = []

    def covered(match):
        return any(start <= match.start() and match.end() <= end
                   for start, end in spans)

    for kind, pattern, parts in (
        ("pair", PAIR_RE, lambda m: [m.group(1), m.group(2)]),
        ("relation", RELATION_RE, lambda m: [m.group(1), m.group(3)]),
        ("assignment", ASSIGN_RE, lambda m: [m.group(2)]),
        ("fraction", FRACTION_RE, lambda m: [m.group(1), m.group(2)]),
    ):
        for match in pattern.finditer(text):
            if covered(match):
                continue
            values.append({"kind": kind, "value": match.group(0).strip(),
                           "components": parts(match)})
            spans.append(match.span())
    for match in NUMBER_RE.finditer(text):
        if covered(match):
            continue
        before = text[max(0, match.start() - 24):match.start()]
        after = text[match.end():match.end() + 20]
        if (REF_BEFORE_RE.search(before) or COMPOUND_BEFORE_RE.search(before)
                or RADICAL_BEFORE_RE.search(before) or COUNT_AFTER_RE.match(after)):
            continue
        values.append({"kind": "number", "value": match.group(0),
                       "components": [match.group(0)]})
    unique = []
    seen = set()
    for item in values:
        key = (item["kind"], item["value"].replace(" ", ""))
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return unique


def number_present(value, index):
    value = value.replace(" ", "")
    if value in index["numbers"] or value.lstrip("-") in index["numbers"]:
        return True
    try:
        number = float(value)
    except ValueError:
        return False
    return number == int(number) and str(int(number)) in index["numbers"]


def fraction_present(numerator, denominator, index):
    numerator = numerator.replace(" ", "")
    denominator = denominator.replace(" ", "")
    # `\frac{a}{b}` extracts as "a/b", as "ab", or as "a" and "b" on two lines.
    if re.search(rf"(?<![\d.]){re.escape(numerator)}\s*/?\s*{re.escape(denominator)}"
                 r"(?![\d.])", index["text"]):
        return True
    if (numerator.lstrip("-") + denominator) in index["numbers"]:
        return True
    # "115/65" is as often two values written with a slash as it is a fraction,
    # so both parts being present is enough to keep the claim out of the ledger.
    return (number_present(numerator, index)
            and number_present(denominator, index))


def _pair_alternatives(component):
    component = component.replace(" ", "")
    if "/" in component:
        numerator, denominator = component.split("/", 1)
        return [re.escape(numerator) + r"\s*/?\s*" + re.escape(denominator),
                re.escape(denominator + numerator.lstrip("-"))]
    return [re.escape(component)]


def claim_value_supported(item, index):
    kind, components = item["kind"], item["components"]
    if kind == "fraction":
        return fraction_present(components[0], components[1], index)
    if kind == "assignment" and "/" in components[0]:
        numerator, denominator = components[0].replace(" ", "").split("/", 1)
        return fraction_present(numerator, denominator, index)
    if kind == "pair":
        left, right = (_pair_alternatives(part) for part in components)
        pattern = (r"(?<![\w.\-])(?:" + "|".join(left)
                   + r")\s*[,;]\s*(?:[A-Za-z][A-Za-z0-9_]{0,3}\s*=\s*)?(?:"
                   + "|".join(right) + r")(?![\d.])")
        return bool(re.search(pattern, index["text"]))
    return all(number_present(part, index) for part in components)


def audit_claim(claim, index):
    """Values this finding quotes that no artifact contains."""
    return [item for item in extract_claim_values(claim)
            if not claim_value_supported(item, index)]


def iter_verdict_claims(verdict):
    for field in CLAIM_FIELDS:
        value = (verdict or {}).get(field)
        if isinstance(value, str):
            if value.strip():
                yield field, value, None
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, str) and item.strip():
                    yield field, item, None
                elif isinstance(item, dict) and isinstance(item.get("description"), str):
                    yield field, item["description"], item.get("severity")


def audit_verdict_claims(verdict, index):
    """Findings for verdict claims quoting values absent from the artifacts.

    A blocking claim is one a REJECT rests on. It is flagged for adjudication,
    never silently dropped and never silently believed: PDF extraction is lossy
    enough that "not found" means "a person has to look", not "the judge lied".
    """
    findings = []
    if not index["text"].strip():
        # Nothing was extracted, so nothing can be looked up. A task with no
        # readable artifacts already fails on its own evidence; flagging every
        # value in its verdict would bury that under noise.
        return findings
    for field, claim, severity in iter_verdict_claims(verdict):
        unsupported = audit_claim(claim, index)
        if not unsupported:
            continue
        blocking = field in BLOCKING_CLAIM_FIELDS or severity == "critical"
        for item in unsupported:
            findings.append({
                "code": "claim_value_not_in_artifact",
                "severity": "critical" if blocking else "review",
                "field": field,
                "value": item["value"],
                "value_kind": item["kind"],
                "blocking": blocking,
                "claim": claim,
                "message": (
                    f"{field} quotes {item['value']!r}, which does not appear in "
                    "the artifacts' extracted text or verification data."
                ),
            })
    return findings


def machine_artifact_index(machine):
    """Build a value index from a prepared task's recorded artifacts."""
    texts = []
    artifacts = (machine or {}).get("artifacts", {})
    for role in PDF_ROLES:
        texts.append(artifacts.get(role, {}).get("extracted_text", ""))
    for role in ("worksheet_verification", "study_guide_verification"):
        path = artifacts.get(role, {}).get("path")
        if path and Path(path).is_file():
            try:
                texts.append(Path(path).read_text(encoding="utf-8", errors="replace"))
            except OSError:
                pass
    return artifact_value_index(texts)


def case_record_for(task_id, run_dir, run_cases):
    record = dict(run_cases.get(task_id, {}))
    if record:
        directory = resolve_path(run_dir, record.get("directory", task_id))
        return record, directory, []
    directory, duplicates = find_case_directory(run_dir, task_id)
    return record, directory, duplicates


def prepare_task(task, run_dir, run_cases, output_dir, *, render_dpi=110,
                 rerun=True, pdf_inspector=inspect_pdf):
    task_id = task["id"]
    task_out = Path(output_dir) / "tasks" / task_id
    task_out.mkdir(parents=True, exist_ok=True)
    findings = []
    artifacts = {}
    record, case_dir, duplicate_dirs = case_record_for(task_id, run_dir, run_cases)
    if duplicate_dirs:
        findings.append(finding(
            "duplicate_task_directories", "error",
            "Multiple task directories were found; use run-manifest.json to select one.",
            evidence=[str(path) for path in [case_dir] + duplicate_dirs], hard_failure=True,
        ))
    metrics = dict(record.get("metrics", {}))
    if not case_dir or not Path(case_dir).is_dir():
        findings.append(finding(
            "missing_task_directory", "critical",
            f"No retained artifact directory exists for {task_id}.", hard_failure=True,
        ))
        resolved = {}
        surfaced = None
        original_names = {}
        surfacing = {}
    else:
        resolved, ambiguities, surfaced, discovered_metrics, original_names = (
            resolve_artifacts(case_dir, record)
        )
        metrics.update(discovered_metrics)
        for role, choices in ambiguities.items():
            findings.append(finding(
                "ambiguous_artifact", "critical",
                f"Multiple equally likely files map to {role}; declare the path in run-manifest.json.",
                artifact=role, evidence=choices, hard_failure=True,
            ))

        for role in ALL_ROLES:
            path = resolved.get(role)
            if not path or not Path(path).is_file():
                findings.append(finding(
                    "missing_artifact", "critical", f"Required artifact {role} is missing.",
                    artifact=role, hard_failure=True,
                ))
                continue
            if role in PDF_ROLES:
                meta, pdf_findings = pdf_inspector(
                    path, role, task_out / "rendered" / role, render_dpi,
                )
                artifacts[role] = meta
                findings.extend(pdf_findings)
            elif role.endswith("verification"):
                meta, verify_findings = inspect_verification(path, role, rerun=rerun)
                artifacts[role] = meta
                findings.extend(verify_findings)
            else:
                text = read_text_file(path)
                artifacts[role] = {
                    "path": str(path), "sha256": sha256_file(path),
                    "size_bytes": Path(path).stat().st_size, "text": text,
                }

        expected_count = task.get("expected", {}).get("worksheet_problem_count")
        declared_count = artifacts.get("worksheet_verification", {}).get("problem_count")
        if isinstance(expected_count, int) and declared_count != expected_count:
            findings.append(finding(
                "worksheet_count_mismatch", "critical",
                f"Expected {expected_count} worksheet problems; verification declares {declared_count!r}.",
                artifact="worksheet_verification", hard_failure=True,
            ))
        worksheet_text = artifacts.get("student_worksheet", {}).get("extracted_text", "")
        if worksheet_text:
            numbers = extract_problem_numbers(worksheet_text)
            artifacts["student_worksheet"]["extracted_problem_numbers"] = numbers
            if expected_count and numbers != list(range(1, expected_count + 1)):
                findings.append(finding(
                    "problem_count_needs_visual_confirmation", "warning",
                    "Text extraction did not recover the exact expected problem-number sequence; judge must count visually.",
                    artifact="student_worksheet", evidence=numbers,
                ))
        study_pages = artifacts.get("study_guide", {}).get("page_count")
        if study_pages is not None and not 1 <= study_pages <= 2:
            findings.append(finding(
                "study_guide_page_count", "critical",
                f"Study guide has {study_pages} pages; prompt requires 1-2.",
                artifact="study_guide", hard_failure=True,
            ))

        gate_text = artifacts.get("gate_log", {}).get("text", "")
        if gate_text:
            if "BUILD FAILED" in gate_text or "BUILD PASSED" not in gate_text:
                findings.append(finding(
                    "gate_chain_not_passed", "critical",
                    "Gate log does not end in a successful BUILD PASSED verdict.",
                    artifact="gate_log", evidence="\n".join(gate_text.splitlines()[-25:]),
                    hard_failure=True,
                ))
        response = artifacts.get("final_response", {}).get("text", "")
        surfaced_set = set(surfaced or [])
        # `record` renames build outputs to canonical roles, so the response
        # and the retained file disagree by construction. Recover the build
        # names from the evidence that kept them before matching.
        for role, names in discover_original_names([gate_text]).items():
            original_names.setdefault(role, [])
            original_names[role].extend(
                name for name in names if name not in original_names[role]
            )
        surfacing = {}
        for role in PDF_ROLES:
            if surfaced is not None:
                evidence = {"surfaced": role in surfaced_set,
                            "basis": "declared_surfaced_list" if role in surfaced_set else None,
                            "match": None}
            else:
                evidence = surfacing_evidence(
                    response, role, resolved.get(role), original_names.get(role, ()),
                )
            surfacing[role] = evidence
            if not evidence["surfaced"]:
                findings.append(finding(
                    "artifact_not_surfaced", "critical",
                    f"Final delivery evidence does not surface {role}.", artifact=role,
                    hard_failure=True,
                ))
            elif evidence["basis"] == "description":
                findings.append(finding(
                    "artifact_surfaced_without_filename", "warning",
                    f"Final delivery evidence describes {role} but never names a file; "
                    "surfacing is inferred from wording alone.",
                    artifact=role, evidence=evidence["match"],
                ))

    manual_count = sum(
        artifact.get("manual_item_count", 0)
        for role, artifact in artifacts.items() if role.endswith("verification")
    )
    hard_failures = [item["message"] for item in findings if item["hard_failure"]]
    status = ("FAIL" if hard_failures else
              "PASS_WITH_OBSERVATIONS" if findings else "PASS")
    machine = {
        "schema_version": "1.0",
        "task_id": task_id,
        "prepared_at": now_utc(),
        "case_directory": str(case_dir) if case_dir else None,
        "machine_status": status,
        "machine_hard_failures": hard_failures,
        "manual_item_count": manual_count,
        "artifact_surfacing": surfacing,
        "metrics": metrics,
        "artifacts": artifacts,
        "findings": findings,
    }
    write_json(task_out / "machine.json", machine)

    rubric = task.get("_judge_protocol", {})
    packet_artifacts = {}
    for role in PDF_ROLES:
        meta = artifacts.get(role, {})
        packet_artifacts[role] = {
            "pdf": meta.get("path"),
            "rendered_pages": meta.get("rendered_pages", []),
            "page_count": meta.get("page_count"),
        }
    packet = {
        "schema_version": "1.0",
        "task": {key: task.get(key) for key in (
            "id", "band", "band_label", "domain", "topic", "focus",
            "instructional_mode", "standard_refs", "review_mode", "prompt", "expected",
        )},
        "review_order": rubric.get("review_order", []),
        "hard_fail_conditions": rubric.get("hard_fail_conditions", []),
        "score_scale": rubric.get("score_scale", {}),
        "quality_dimensions": rubric.get("quality_dimensions", {}),
        "acceptance_rule": rubric.get("acceptance_rule", ""),
        "artifacts": packet_artifacts,
        "secondary_evidence": {
            role: artifacts.get(role, {}).get("path") for role in EVIDENCE_ROLES
        },
        "machine_evidence": str(task_out / "machine.json"),
        "judge_instruction": (
            "Inspect the PDFs/rendered pages before opening secondary evidence. "
            "Independently check every answer and record evidence-backed errors and observations."
        ),
    }
    write_json(task_out / "judge-packet.json", packet)
    template = {
        "schema_version": "1.0",
        "task_id": task_id,
        "judge": {"type": None, "id": None, "completed_at": None},
        "verdict": None,
        "hard_failures": [],
        "dimension_scores": {
            name: None for name in rubric.get("quality_dimensions", {})
        },
        "total_score": None,
        "manual_items_reviewed": 0,
        "incorrect_or_ambiguous_items": [],
        "errors": [],
        "critical_observations": [],
        "artifact_findings": [],
        "rationale": "",
    }
    write_json(task_out / "verdict.template.json", template)
    return machine


def select_tasks(suite, task_ids):
    tasks = suite.get("tasks", [])
    by_id = {task.get("id"): task for task in tasks}
    if not task_ids:
        return tasks
    unknown = sorted(set(task_ids) - set(by_id))
    if unknown:
        raise HarnessError(f"unknown task id(s): {', '.join(unknown)}")
    return [by_id[task_id] for task_id in task_ids]


def prepare_run(suite_path, run_dir, output_dir, *, task_ids=None,
                render_dpi=110, rerun=True, pdf_inspector=inspect_pdf):
    suite_path, run_dir, output_dir = map(Path, (suite_path, run_dir, output_dir))
    suite = load_json(suite_path, "eval suite")
    rubric = suite.get("judge_protocol")
    if not isinstance(rubric, dict) or len(rubric.get("quality_dimensions", {})) != 8:
        raise HarnessError("suite has no valid eight-dimension judge_protocol")
    if not run_dir.is_dir():
        raise HarnessError(f"run directory does not exist: {run_dir}")
    missing_tools = [name for name, path in required_tools().items() if not path]
    if missing_tools and pdf_inspector is inspect_pdf:
        raise HarnessError("missing PDF prerequisites: " + ", ".join(missing_tools))
    run_cases, run_manifest = load_run_cases(run_dir)
    tasks = select_tasks(suite, task_ids or run_manifest.get("task_ids"))
    output_dir.mkdir(parents=True, exist_ok=True)
    machines = []
    for task in tasks:
        enriched = dict(task)
        enriched["_judge_protocol"] = rubric
        machines.append(prepare_task(
            enriched, run_dir, run_cases, output_dir, render_dpi=render_dpi,
            rerun=rerun, pdf_inspector=pdf_inspector,
        ))
        print(f"{task['id']}: {machines[-1]['machine_status']}")
    suite_snapshot = dict(suite)
    suite_snapshot["tasks"] = tasks
    write_json(output_dir / "suite-snapshot.json", suite_snapshot)
    manifest = {
        "schema_version": "1.0",
        "prepared_at": now_utc(),
        "suite_path": str(suite_path.resolve()),
        "suite_sha256": sha256_file(suite_path),
        "run_directory": str(run_dir.resolve()),
        "run_id": run_manifest.get("run_id", run_dir.name),
        "task_ids": [task["id"] for task in tasks],
        "render_dpi": render_dpi,
        "verifier_rerun": rerun,
        "machine_status_counts": dict(Counter(m["machine_status"] for m in machines)),
    }
    write_json(output_dir / "manifest.json", manifest)
    with open(output_dir / "issues.jsonl", "w", encoding="utf-8") as handle:
        for machine in machines:
            for item in machine["findings"]:
                handle.write(json.dumps({"task_id": machine["task_id"], **item}, ensure_ascii=False) + "\n")
    print(f"Prepared {len(tasks)} judge packet(s) in {output_dir}")
    return manifest


def normalize_note_list(value, field, errors):
    if not isinstance(value, list):
        errors.append(f"{field} must be a list")
        return []
    normalized = []
    for index, item in enumerate(value):
        if isinstance(item, str) and item.strip():
            normalized.append({"description": item.strip()})
        elif (isinstance(item, dict) and isinstance(item.get("description"), str)
              and item["description"].strip()):
            normalized.append({**item, "description": item["description"].strip()})
        else:
            errors.append(f"{field}[{index}] must be a string or object with description")
    return normalized


def validate_verdict(data, task_id, dimensions, machine_hard_failures):
    errors = []
    if data.get("task_id") != task_id:
        errors.append(f"task_id must be {task_id}")
    hard = data.get("hard_failures")
    if not isinstance(hard, list) or not all(isinstance(item, str) and item.strip() for item in hard):
        errors.append("hard_failures must be a list of non-empty strings")
        hard = []
    scores = data.get("dimension_scores")
    if not isinstance(scores, dict) or set(scores) != set(dimensions):
        errors.append("dimension_scores must contain exactly the rubric dimensions")
        scores = {}
    elif not all(type(value) is int and 0 <= value <= 4 for value in scores.values()):
        errors.append("every dimension score must be an integer from 0 to 4")
    calculated_total = sum(scores.values()) if len(scores) == len(dimensions) and all(
        type(value) is int for value in scores.values()
    ) else None
    if data.get("total_score") != calculated_total:
        errors.append(f"total_score must equal the calculated total {calculated_total!r}")
    manual = data.get("manual_items_reviewed")
    if type(manual) is not int or manual < 0:
        errors.append("manual_items_reviewed must be a non-negative integer")
    lists = {}
    for field in ("incorrect_or_ambiguous_items", "artifact_findings"):
        value = data.get(field)
        if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
            errors.append(f"{field} must be a list of non-empty strings")
            value = []
        lists[field] = value
    normalized_errors = normalize_note_list(data.get("errors"), "errors", errors)
    normalized_observations = normalize_note_list(
        data.get("critical_observations"), "critical_observations", errors,
    )
    if not isinstance(data.get("rationale"), str) or not data.get("rationale", "").strip():
        errors.append("rationale must be non-empty")
    combined_hard = list(machine_hard_failures) + list(hard)
    if lists["incorrect_or_ambiguous_items"] and not hard:
        errors.append("incorrect_or_ambiguous_items requires a corresponding judge hard failure")
    if any(item.get("severity") == "critical" for item in normalized_errors) and not hard:
        errors.append("a critical judge error requires a corresponding judge hard failure")
    computed = "REJECT"
    if not combined_hard and calculated_total is not None:
        if min(scores.values(), default=0) >= DIMENSION_FLOOR and calculated_total >= TOTAL_FLOOR:
            computed = "ACCEPT"
    if data.get("verdict") != computed:
        errors.append(f"verdict must be {computed}; the harness computes it from hard failures and scores")
    return {
        "valid": not errors,
        "validation_errors": errors,
        "computed_verdict": computed,
        "calculated_total": calculated_total,
        "combined_hard_failures": combined_hard,
        "errors": normalized_errors,
        "critical_observations": normalized_observations,
    }


def rate(numerator, denominator):
    return round(numerator / denominator, 4) if denominator else None


def group_metrics(rows, key):
    grouped = defaultdict(list)
    for row in rows:
        grouped[row[key] or "unknown"].append(row)
    output = {}
    for name, items in sorted(grouped.items()):
        accepted = sum(item["status"] == "ACCEPT" for item in items)
        output[name] = {
            "expected": len(items),
            "completed": sum(item["status"] in {"ACCEPT", "REJECT"} for item in items),
            "accepted": accepted,
            "acceptance_rate": rate(accepted, len(items)),
        }
    return output


def numeric_metric(rows, name):
    values = [row["metrics"].get(name) for row in rows]
    values = [value for value in values if isinstance(value, (int, float)) and not isinstance(value, bool)]
    return round(statistics.median(values), 4) if values else None


def write_summary_markdown(path, summary):
    counts = summary["counts"]
    metrics = summary["metrics"]
    lines = [
        "# Eval run score summary", "",
        f"- Run: `{summary['run_id']}`",
        f"- Completion: {counts['completed']}/{counts['expected']}",
        f"- Accepted: {counts['accepted']}",
        f"- Rejected: {counts['rejected']}",
        f"- Pending: {counts['pending']}",
        f"- Invalid verdicts: {counts['invalid']}",
        f"- Verdicts quoting values absent from the artifacts: "
        f"{counts.get('verdicts_with_unsupported_claims', 0)}",
        f"- Verdicts needing adjudication: {counts.get('needs_adjudication', 0)}",
        f"- Acceptance rate: {metrics['acceptance_rate']}",
        f"- Hard-gate pass rate: {metrics['hard_gate_pass_rate']}",
        f"- Mean quality score among hard-gate passes: {metrics['mean_quality_score_among_hard_gate_passes']}",
        "", "## Acceptance by band", "",
        "| Band | Accepted | Completed | Expected | Rate |",
        "|---|---:|---:|---:|---:|",
    ]
    for name, item in summary["by_band"].items():
        lines.append(
            f"| {name} | {item['accepted']} | {item['completed']} | {item['expected']} | {item['acceptance_rate']} |"
        )
    claims = summary.get("unsupported_claims", [])
    if claims:
        lines.extend([
            "", "## Claims not found in the artifacts", "",
            "A finding is evidence only if the value it quotes is printed in the",
            "artifact it cites. PDF extraction is lossy, so these are flagged for a",
            "person to adjudicate, not counted as judge errors.", "",
            "| Task | Field | Value | Blocking |", "|---|---|---|---|",
        ])
        for item in claims[:100]:
            lines.append(
                f"| `{item['task_id']}` | {item['field']} | `{item['value']}` | "
                f"{'yes' if item['blocking'] else 'no'} |"
            )
    lines.extend(["", "## Errors", ""])
    errors = summary.get("errors", [])
    lines.extend(
        f"- `{item['task_id']}` [{item.get('source', 'machine')}]: {item['description']}"
        for item in errors[:100]
    )
    if not errors:
        lines.append("- None recorded.")
    lines.extend(["", "## Critical observations", ""])
    observations = summary.get("critical_observations", [])
    lines.extend(
        f"- `{item['task_id']}` [{item.get('source', 'judge')}]: {item['description']}"
        for item in observations[:100]
    )
    if not observations:
        lines.append("- None recorded.")
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def aggregate_run(grading_dir, output_dir=None, require_complete=False):
    grading_dir = Path(grading_dir)
    output_dir = Path(output_dir or grading_dir / "results")
    manifest = load_json(grading_dir / "manifest.json", "grading manifest")
    suite = load_json(grading_dir / "suite-snapshot.json", "suite snapshot")
    rubric = suite["judge_protocol"]
    dimensions = list(rubric["quality_dimensions"])
    tasks = {task["id"]: task for task in suite["tasks"]}
    rows = []
    issues = []
    invalid_details = []
    unsupported_claims = []
    needs_adjudication = []
    for task_id in manifest["task_ids"]:
        task = tasks[task_id]
        task_dir = grading_dir / "tasks" / task_id
        machine = load_json(task_dir / "machine.json", "machine evidence")
        machine_hard = machine.get("machine_hard_failures", [])
        for item in machine.get("findings", []):
            issues.append({"task_id": task_id, "source": "machine", "kind": "machine_finding", **item})
        verdict_path = task_dir / "verdict.json"
        verdict = None
        validation = None
        if verdict_path.is_file():
            verdict = load_json(verdict_path, "judge verdict")
            validation = validate_verdict(verdict, task_id, dimensions, machine_hard)
            if not validation["valid"]:
                invalid_details.append({
                    "task_id": task_id,
                    "errors": validation["validation_errors"],
                })
            else:
                for item in validation["errors"]:
                    issues.append({
                        "task_id": task_id, "source": "judge", "kind": "error",
                        "severity": item.get("severity", "major"),
                        "code": item.get("category", "judge_error"), "description": item["description"],
                        **{key: value for key, value in item.items() if key != "description"},
                    })
                for item in validation["critical_observations"]:
                    issues.append({
                        "task_id": task_id, "source": "judge", "kind": "critical_observation",
                        "severity": "critical_observation",
                        "code": item.get("category", "judge_observation"), "description": item["description"],
                        **{key: value for key, value in item.items() if key != "description"},
                    })

        if machine_hard and verdict is None:
            status = "REJECT"
            source = "machine"
            score = None
            scores = {}
            combined_hard = machine_hard
        elif validation and validation["valid"]:
            status = validation["computed_verdict"]
            source = "judge"
            score = validation["calculated_total"]
            scores = verdict["dimension_scores"]
            combined_hard = validation["combined_hard_failures"]
        elif validation:
            status, source, score, scores, combined_hard = "INVALID", "judge", None, {}, machine_hard
        else:
            status, source, score, scores, combined_hard = "PENDING", None, None, {}, machine_hard

        # A judge's finding is evidence only if the value it quotes is in the
        # artifact it cites. Audited here rather than in validate_verdict,
        # because only aggregation has the extracted text to check against.
        claim_findings = []
        if verdict is not None:
            index = machine_artifact_index(machine)
            claim_findings = audit_verdict_claims(verdict, index)
            for item in claim_findings:
                unsupported_claims.append({"task_id": task_id, **item})
                issues.append({
                    "task_id": task_id, "source": "harness", "kind": "unsupported_claim",
                    **item,
                })
        blocking_claims = [item for item in claim_findings if item["blocking"]]
        if blocking_claims:
            needs_adjudication.append({
                "task_id": task_id,
                "status": status,
                "values": sorted({item["value"] for item in blocking_claims}),
            })
        row = {
            "task_id": task_id,
            "band": task.get("band"),
            "domain": task.get("domain"),
            "topic": task.get("topic"),
            "status": status,
            "decision_source": source,
            "hard_gate_pass": status in {"ACCEPT", "REJECT"} and not combined_hard,
            "total_score": score,
            "dimension_scores": scores,
            "machine_status": machine.get("machine_status"),
            "manual_review": bool(machine.get("manual_item_count")) or bool(
                verdict and verdict.get("manual_items_reviewed", 0)
            ),
            "hard_failures": combined_hard,
            "unsupported_claim_count": len(claim_findings),
            "hard_failure_claims_unverified": bool(blocking_claims),
            "metrics": machine.get("metrics", {}),
        }
        rows.append(row)

    expected = len(rows)
    accepted = sum(row["status"] == "ACCEPT" for row in rows)
    rejected = sum(row["status"] == "REJECT" for row in rows)
    invalid = sum(row["status"] == "INVALID" for row in rows)
    pending = sum(row["status"] == "PENDING" for row in rows)
    hard_passes = [row for row in rows if row["hard_gate_pass"]]
    scored_hard_passes = [row["total_score"] for row in hard_passes if row["total_score"] is not None]
    errors = []
    observations = []
    for item in issues:
        if item.get("kind") == "critical_observation":
            observations.append({
                "task_id": item["task_id"], "source": item.get("source"),
                "description": item.get("description", item.get("message", "")),
                "code": item.get("code"),
            })
        elif item.get("kind") == "error" or item.get("hard_failure"):
            errors.append({
                "task_id": item["task_id"], "source": item.get("source"),
                "description": item.get("description", item.get("message", "")),
                "code": item.get("code"), "severity": item.get("severity"),
            })
    summary = {
        "schema_version": "1.0",
        "aggregated_at": now_utc(),
        "run_id": manifest.get("run_id"),
        "counts": {
            "expected": expected,
            "completed": accepted + rejected,
            "accepted": accepted,
            "rejected": rejected,
            "pending": pending,
            "invalid": invalid,
            "machine_rejected": sum(
                row["status"] == "REJECT" and row["decision_source"] == "machine" for row in rows
            ),
            "verdicts_with_unsupported_claims": len(
                {item["task_id"] for item in unsupported_claims}
            ),
            "needs_adjudication": len(needs_adjudication),
        },
        "metrics": {
            "completion_rate": rate(accepted + rejected, expected),
            "acceptance_rate": rate(accepted, expected),
            "hard_gate_pass_rate": rate(len(hard_passes), expected),
            "mean_quality_score_among_hard_gate_passes": (
                round(statistics.mean(scored_hard_passes), 4) if scored_hard_passes else None
            ),
            "manual_review_rate": rate(sum(row["manual_review"] for row in rows), expected),
            "unsupported_claim_rate": rate(
                len({item["task_id"] for item in unsupported_claims}), expected,
            ),
            "median_latency_seconds": numeric_metric(rows, "latency_seconds"),
            "median_cost": numeric_metric(rows, "cost"),
        },
        "by_band": group_metrics(rows, "band"),
        "by_domain": group_metrics(rows, "domain"),
        "invalid_verdicts": invalid_details,
        "unsupported_claims": unsupported_claims,
        "needs_adjudication": needs_adjudication,
        "errors": errors,
        "critical_observations": observations,
        "task_results": rows,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(output_dir / "summary.json", summary)
    write_summary_markdown(output_dir / "summary.md", summary)
    with open(output_dir / "issues.jsonl", "w", encoding="utf-8") as handle:
        for item in issues:
            handle.write(json.dumps(item, ensure_ascii=False) + "\n")
    fieldnames = [
        "task_id", "band", "domain", "topic", "status", "decision_source",
        "machine_status", "hard_gate_pass", "total_score", "manual_review",
        *dimensions, "hard_failure_count",
    ]
    with open(output_dir / "task-scores.csv", "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            flat = {key: row.get(key) for key in fieldnames}
            flat.update(row["dimension_scores"])
            flat["hard_failure_count"] = len(row["hard_failures"])
            writer.writerow(flat)
    with open(output_dir / "unsupported-claims.jsonl", "w", encoding="utf-8") as handle:
        for item in unsupported_claims:
            handle.write(json.dumps(item, ensure_ascii=False) + "\n")
    print(
        f"Scored {accepted + rejected}/{expected}: {accepted} ACCEPT, {rejected} REJECT, "
        f"{pending} PENDING, {invalid} INVALID"
    )
    if unsupported_claims:
        print(
            f"⚠️  {len(unsupported_claims)} judge claim(s) across "
            f"{len({item['task_id'] for item in unsupported_claims})} task(s) quote values "
            "absent from the artifacts; see unsupported-claims.jsonl"
        )
    if needs_adjudication:
        print(
            f"❌ {len(needs_adjudication)} verdict(s) rest on a hard failure whose cited "
            "value is not in the artifact — adjudicate before using these scores"
        )
    print(f"Results: {output_dir}")
    if invalid:
        return 2
    if require_complete and (pending or accepted + rejected != expected
                             or needs_adjudication):
        return 1
    return 0


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor", help="check local PDF/verifier prerequisites")
    prepare = sub.add_parser("prepare", help="inspect artifacts and create blind judge packets")
    prepare.add_argument("--suite", default=str(DEFAULT_SUITE))
    prepare.add_argument("--run-dir", required=True)
    prepare.add_argument("--output-dir", required=True)
    prepare.add_argument("--task-id", action="append", default=[])
    prepare.add_argument("--render-dpi", type=int, default=110)
    prepare.add_argument("--no-rerun-verifier", action="store_true")
    aggregate = sub.add_parser("aggregate", help="validate verdicts and calculate run scores")
    aggregate.add_argument("--grading-dir", required=True)
    aggregate.add_argument("--output-dir")
    aggregate.add_argument("--require-complete", action="store_true")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        if args.command == "doctor":
            return doctor()
        if args.command == "prepare":
            if not 72 <= args.render_dpi <= 200:
                raise HarnessError("--render-dpi must be between 72 and 200")
            prepare_run(
                args.suite, args.run_dir, args.output_dir,
                task_ids=args.task_id, render_dpi=args.render_dpi,
                rerun=not args.no_rerun_verifier,
            )
            return 0
        return aggregate_run(
            args.grading_dir, args.output_dir, require_complete=args.require_complete,
        )
    except HarnessError as exc:
        print(f"scoring harness error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
