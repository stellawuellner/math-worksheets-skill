# Judging packet — run `curriculum-shardX-20260803T181926Z`

You are the independent judge for an eval of a math-worksheet generator. **You
did not produce this work and you must not be told what did.** If you know or
can infer which model generated these artifacts, say so and stop.

## What you are scoring

`tasks/<task-id>/` — 150 of them. Each contains:

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
{
  "task_id": "curr-001",
  "judge": {"agent": "<your harness>", "model": "<your model id>"},
  "verdict": "ACCEPT",
  "hard_failures": [],
  "dimension_scores": {
    "curriculum_alignment": 3,
    "problem_set_design": 3,
    "mathematical_correctness": 3,
    "answer_key_quality": 3,
    "study_guide_quality": 3,
    "clarity_and_accessibility": 3,
    "visual_and_print_quality": 3,
    "instruction_following": 3
  },
  "total_score": 30,
  "manual_items_reviewed": 0,
  "incorrect_or_ambiguous_items": [],
  "artifact_findings": [],
  "rationale": "one or two sentences"
}
```

Every dimension is an integer 0–4. `verdict` is ACCEPT only when there are no
hard failures, every dimension is at least 3, and the total is at least 27 of
32 — but do not compute the arithmetic in your head and adjust the scores to
reach a verdict you have already chosen. Score first; the verdict follows.

`judge.model` must be your real model identifier. Scoring is refused when it
matches the generator's, which the harness knows and you do not.

## When you are done

```bash
python3 evals/score_eval.py --run curriculum-shardX-20260803T181926Z
```

It re-derives every verdict from your scores, cross-checks them against
mechanical facts you were not shown, and writes `report.md`.
