# Judging addendum — dual-rubric scoring (v1 + shadow v2)

This addendum extends the run's `JUDGING.md`. Nothing in it changes the
official verdict or the shape of the fields you already write.

## What to do

Score each task **once**, but record it under **both rubrics in the same
pass**:

1. **v1 (official, unchanged).** Fill `dimension_scores`, `hard_failures`,
   `total_score`, and `verdict` exactly as `curriculum-judge-rubric.md`
   directs. This block keeps the shape every earlier run used, so run-1 and
   run-2 remain directly comparable.
2. **v2 (shadow, optional but requested).** Apply
   `curriculum-judge-rubric-v2.md` — the same eight dimensions and the same
   hard-fail list, with behavioral anchors for each grade — and record the
   result in a **new `scores_v2` block with the same eight keys**, plus
   `hard_failures_v2` for any hard failure recognized under v2 wording.
   While applying v2, complete its **mandatory bank transcription**: the
   Quick Answers bank rows for the first, middle, and last problems, copied
   verbatim into `artifact_findings` as `bank row N: <what the bank prints>`.

Because both rubrics share the review procedure, one careful inspection
supports both blocks. The honest outcome when the behavioral tests reveal
something v1's adjectives let pass is a *lower* v2 score with the same v1
score — that divergence is exactly the signal the shadow column exists to
measure. Do not retrofit v1 scores to match v2.

## Verdict shape

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
  "total_score": 24,
  "scores_v2": {
    "curriculum_alignment": 3,
    "problem_set_design": 3,
    "mathematical_correctness": 3,
    "answer_key_quality": 2,
    "study_guide_quality": 3,
    "clarity_and_accessibility": 3,
    "visual_and_print_quality": 3,
    "instruction_following": 3
  },
  "hard_failures_v2": [],
  "manual_items_reviewed": 0,
  "incorrect_or_ambiguous_items": [],
  "artifact_findings": [
    "bank row 1: 5",
    "bank row 4: (-1, 1)",
    "bank row 8: (4, 3.5), (4, 3.5), ---"
  ],
  "rationale": "one or two sentences"
}
```

## How it is scored

- `evals/score_eval.py` computes the **official verdict from the v1 scores
  exactly as before**. `scores_v2` never changes it.
- When `scores_v2` is present and well-formed (the same eight dimensions,
  integers 0–4), the same acceptance arithmetic (no `hard_failures_v2`, every
  dimension ≥ 3, total ≥ 27/32) derives a **shadow v2 verdict**, and the
  report shows v1 and v2 side by side: acceptance over the verdicts that
  carry both, per-dimension means in both columns, and the tasks whose
  verdict moves.
- **A verdict without `scores_v2` is a complete, valid verdict.** The block
  is forward compatibility, not a new requirement — old verdicts and judges
  that only know v1 are scored exactly as they always were. A malformed
  `scores_v2` is reported as a non-invalidating note and simply not
  shadow-scored.
- The transcription lines in `artifact_findings` are audited like every other
  quoted value: the aggregate step looks them up in the extracted artifacts,
  so a transcription that was never read off the page surfaces in "Claims not
  found in the artifacts".
