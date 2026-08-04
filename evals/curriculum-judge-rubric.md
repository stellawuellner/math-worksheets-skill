# Curriculum-suite acceptance rubric

Use this rubric for `curriculum-suite-500.json`. A trained person or an
independent second agent with PDF vision may judge a run. Keep the judge blind
to model identity, skill-on/off labels, and the generation transcript until
after the verdict.

## Inputs

Give the judge only:

1. the original eval prompt;
2. the rendered worksheet, answer-key, and study-guide PDFs;
3. the two verification JSON files;
4. the gate-chain logs and final delivery response.

## Review procedure

1. Read the prompt and inspect the rendered PDFs before reading gate logs.
2. Confirm that all three PDFs are present and readable, then count the
   worksheet problems. Study-guide examples and try-it items do not count.
3. Independently solve or recompute every final answer. A verifier PASS is
   supporting evidence, not the judge's sole correctness oracle.
4. Check every worked solution, study-guide rule, example, try-it, diagram,
   unit, and genuinely manual response.
5. Inspect every page at normal reading size for clipping, overlap, missing
   glyphs, tiny type, poor page flow, and inadequate work or answer space.
6. Apply the hard-fail rules. If none applies, score all eight dimensions.
7. Record every objective defect under `errors`, and capture important
   evidence, risks, or unusually strong/weak patterns under
   `critical_observations`. Identify the artifact and page/problem when known.

## Hard failures

Reject the run if any of these is true:

- A requested PDF is missing, unreadable, or not surfaced to the user.
- The worksheet problem count differs from the task expectation.
- Any problem is wrong, ambiguous, internally inconsistent, or mismatched
  with its answer.
- Any machine-checkable printed item is absent from verification data, or a
  required repository gate fails.
- An open proof, construction, graph, or explanation is falsely described as
  machine-verified.
- A severe layout defect causes clipping, overlap, missing glyphs, unusably
  small type, or insufficient answer/work space.
- The requested curriculum focus appears materially in fewer than 70% of the
  worksheet problems.

## Quality scoring

Score each dimension from 0 to 4: 0 missing/unusable; 1 major defects; 2
material revision needed; 3 good and acceptance-ready; 4 excellent.

- Curriculum alignment
- Problem-set design
- Mathematical correctness
- Answer-key quality
- Study-guide quality
- Clarity and accessibility
- Visual and print quality
- Instruction following

Accept only when there are no hard failures, every dimension scores at least
3, and the total is at least 27/32. Return the structured verdict described in
the manifest's `judge_protocol.verdict_schema`. Do not copy a supplied total or
ACCEPT label: the scoring harness recalculates both from the dimension scores
and combined machine/judge hard failures.

Run `scripts/score_eval_run.py prepare` before judgment and
`scripts/score_eval_run.py aggregate --require-complete` afterward. The full
artifact layout and commands are in `evals/scoring-harness.md`.
