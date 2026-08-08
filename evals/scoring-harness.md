# Eval-run scoring harness

`scripts/score_eval_run.py` turns a generated curriculum eval run into blind
review packets, validates judge verdicts, and calculates suite metrics. It does
not ask deterministic code to make qualitative or visual judgments it cannot
support.

## Boundary

The `prepare` stage checks artifact presence, PDF readability, page counts,
blank/sparse/edge-ink signals, verification JSON coverage, verifier reruns,
gate-log success, delivery evidence, and the declared worksheet count. It also
renders every PDF page to PNG for normal-size visual review.

A trained person or independent vision-capable agent must still independently
check the mathematics, pedagogy, curriculum alignment, problem count, answer
space, and page layout. The `aggregate` stage validates that judgment and
computes the rubric verdict; it never trusts a supplied total or ACCEPT label.

## Prerequisites

Python 3, SymPy, and Poppler (`pdfinfo`, `pdftotext`, `pdftoppm`) are required.

```bash
python3 scripts/score_eval_run.py doctor
```

On macOS, install missing PDF tools with `brew install poppler`. On
Debian/Ubuntu, use `sudo apt-get install poppler-utils`.

## Retained-run contract

The zero-configuration layout is one directory per task:

```text
RUN/
  curr-001/
    student_worksheet.pdf
    step_by_step_answer_key.pdf
    study_guide.pdf
    verify_worksheet.json
    verify_study_guide.json
    gate.log
    final_response.md
```

The harness also recognizes the skill's `ws_*.pdf`, `ak_*.pdf`, `ss_*.pdf`,
`verify.json`, `verify_*.json`, and `verify_ss_*.json` names. When the run
already has the repository's native `run.json`, its `task_ids` define the
shard automatically. The harness refuses equally plausible duplicates instead
of guessing.

For arbitrary download layouts, add `RUN/run-manifest.json`:

```json
{
  "schema_version": "1.0",
  "run_id": "claude-curriculum-2026-08-03",
  "cases": [
    {
      "task_id": "curr-001",
      "directory": "shard-01/curr-001",
      "artifacts": {
        "student_worksheet": "outputs/ws_counting.pdf",
        "step_by_step_answer_key": "outputs/ak_counting.pdf",
        "study_guide": "outputs/ss_counting.pdf",
        "worksheet_verification": "workspace/verify_counting.json",
        "study_guide_verification": "workspace/verify_ss_counting.json",
        "gate_log": "logs/build.log",
        "final_response": "final_response.md"
      },
      "surfaced_artifacts": [
        "student_worksheet",
        "step_by_step_answer_key",
        "study_guide"
      ],
      "metrics": {
        "latency_seconds": 82.4,
        "token_usage": 18450,
        "cost": 0.41
      }
    }
  ]
}
```

Artifact paths are relative to the case directory unless absolute. The
`surfaced_artifacts` field is authoritative when attachments are delivered by
the eval platform but their filenames are absent from the textual response.
For native curriculum runs, the harness also reads `run.json` and limits the
grading set to its `task_ids`; per-task `verify.json` is accepted as the
worksheet-verification artifact.

## Prepare and judge

Keep grading output outside the retained run, then prepare all 500 tasks:

```bash
python3 scripts/score_eval_run.py prepare \
  --suite evals/curriculum-suite-500.json \
  --run-dir /path/to/downloaded-run \
  --output-dir /path/to/grading
```

Use repeated `--task-id curr-NNN` options for a smoke test or shard. Each
`grading/tasks/curr-NNN/` directory contains:

- `judge-packet.json`: blind prompt, expectations, rubric, and artifact paths;
- `rendered/`: PNGs for every PDF page;
- `machine.json`: deterministic evidence and findings. Its `artifact_surfacing`
  block records, per role, **how** the delivery response was matched —
  `canonical_filename`, `original_filename`, `stem_convention` or
  `description_only`. A role matched only by description also raises
  `artifact_surfaced_without_filename`. That distinction exists because the
  check used to collapse it: the filename branch compared against the canonical
  `worksheet.pdf` while responses name the build filename
  (`ws_numbermatch_curr003.pdf`), so across 300 cases **204 responses named all
  three artifacts and none were credited** — every pass came from spotting the
  word "PDF" near a role phrase. Matching is now whitespace-tolerant, so a
  line-wrapped filename or role phrase still counts;
- `verdict.template.json`: the exact judge response shape.

The judge must inspect PDFs first, then the secondary evidence, and save a
completed copy as `verdict.json`. Record objective defects under `errors` and
important evidence or risk under `critical_observations`. Each entry may be a
concise string or an object with at least `description`; useful optional fields
are `severity`, `category`, `artifact`, `location`, and `evidence`.

## Aggregate

```bash
python3 scripts/score_eval_run.py aggregate \
  --grading-dir /path/to/grading \
  --require-complete
```

The results directory contains:

- `summary.json` and `summary.md`: completion, acceptance, hard-gate, quality,
  manual-review, latency, cost, band, and domain metrics;
- `task-scores.csv`: one row per expected task and all eight rubric scores;
- `issues.jsonl`: machine and judge errors/observations with task provenance.

Machine hard failures are automatic REJECTs and do not need a judge verdict.
All other tasks remain PENDING until a valid verdict exists. Invalid totals,
dimension sets, score ranges, or declared verdicts are INVALID and cause exit
2. `--require-complete` causes exit 1 while valid tasks remain pending. Eval
REJECTs themselves do not make the harness fail: they are the measurement.

## Feed scored cases back to the author system

Independent scoring ends when the report is written. Post-eval diagnosis is a
separate phase: `scripts/review_eval_run.py` packages every case for the system
that authored the artifacts, validates one structured diagnosis per task, and
deduplicates repeated fixes into an improvement backlog. It never changes an
official verdict or total. See `evals/author-review.md` for the response schema,
commands, and GitHub intake workflow.
