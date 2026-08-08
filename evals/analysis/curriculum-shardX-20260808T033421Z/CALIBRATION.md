# Seeded-defect calibration — what the judge actually catches

25 cases drawn from run 2's 295 ACCEPTs: **15 seeded** (5 each of three
classes) and **10 untouched controls**. Every case rebuilt through the full
gate chain and admitted only while every gate stayed green, so nothing here is
a defect the pipeline already stops. Seeds and locations were sealed to
`seed-manifest.json`, outside the run, before judging.

This is the measurement that run 2's 295/300 ACCEPT could not supply on its
own: with no known defect count, a good judge and a blind one produce the same
number.

## Headline

| defect class | n | detected | notes |
|---|---|---|---|
| **worked-step-error** | 5 | **3** | exact: right problem, the corrupted equality quoted, the correction stated |
| **ramp-inversion** | 5 | **0** | |
| **vague-rubric** | 5 | **0** | |
| controls | 10 | — | 3 rejected, all citing specific defects (below) |

**Detection on planted defects: 3 of 15 (20%).** All three are the same class.

The three hits are unambiguous and were verified against the manifest by
locating the seeded line and counting `\problem` before it:

| case | seeded in | judge cited | what it said |
|---|---|---|---|
| curr-255 | problem 10 | problem 10 | "prints the false equality `4x² + x − 12 = 6x² + 9x − 8x − 12`; the left side should be `6x² + x − 12`" |
| curr-355 | problem 10 | problem 10 | "the second grouped factor should be `9(x − 2)`" |
| curr-373 | problem 10 | problem 10 | "changes the original radical from `√(x + 5)` to `√(x + 7)`" |

The two misses (curr-252 problem 5, curr-394 problem 7) were accepted with no
mention. Note all three hits sat in problem **10** and both misses sat earlier
— 5 and 7. Five cases cannot establish a positional effect, but a judge that
attends more closely to the last worked solution than the middle ones is a
plausible reading and worth a targeted probe before it is believed.

**A methodological correction, recorded because it nearly became the finding.**
The first scoring pass matched verdict text against a keyword list ("worked
step", "derivation", "ramp", "rubric") and reported **0 detections of 15**. That
was the matcher, not the judge: it described the defect concretely — quoting the
false equality — rather than in the vocabulary of the harness that planted it.
A detection scorer must read the citation against the manifest's location, never
grep for the seeder's own words.

## The classes it is blind to

**ramp-inversion: 0 of 5.** Reversing the declared difficulty ramp so the sheet
opens at its hardest went unremarked in every case. curr-256 *was* rejected —
for under-covering the requested explaining focus, an unrelated and pre-existing
finding — which is exactly the trap a naive scorer falls into: a rejection is
not a detection unless it cites the planted defect.

**vague-rubric: 0 of 5.** Hollowing a `manual` entry's rubric to "Grade the
student's explanation" was never mentioned. curr-075 was rejected for treating
machine-checkable equation responses as manual — again unrelated to the seed.

Both blind spots are the same shape: **defects in the JSON's pedagogical
metadata rather than in a printed mathematical statement.** The judge reads the
PDFs closely and the verification data structurally, but does not audit whether
a difficulty tag or a grading rubric is *fit for purpose*. Neither is machine
checkable either — the ramp report is deliberately exit-neutral and the
stale-rubric lint fires only on a wrong eponym — so this is currently uncovered
by gates AND by judging.

## The controls, and why "false positive" is the wrong word

3 of 10 controls were rejected. None looks like noise; each cites a specific,
locatable, plausible defect that run 2's judge accepted at 31–32/32:

- **curr-082** (run 2: 32/32 → here 23/32) — on a fractions-on-a-number-line
  sheet, "the first interior sixth tick is labelled 1 instead of the right
  endpoint". If correct that is a serious mathematical defect, and it is
  precisely the elementary number-line weakness the figure review flagged
  independently.
- **curr-482** (31 → 30) — particular-solution formulas requested in six
  problems are absent from `verify.json`; the verifier checks antiderivatives
  and evaluated values but never the requested formula.
- **curr-496** (31 → 27) — rejected on a `curriculum_alignment` score of 2,
  NOT a hard failure: two of eight problems require memorised exact zeta
  values that are not among the requested AP classification tools. (The
  p-series verification gap appears in its `errors`, but it is not what
  triggered the rejection — a distinction the first draft of this file got
  wrong.)

So the control rejections read as **findings run 2's judge missed**, not as a
false-positive rate. That inverts the usual reading: the instrument is not
noisy, the two instruments disagree about where the bar is.

## Machine cross-checks in the generated report

The scoring harness recomputes deterministic facts the judge never saw.
`bank_value_unbacked` fired 19 times and `standard_code_not_in_map` once, both
advisory. The standards flag is adjudicated here as a **false positive**: it
reports `0.08P` on curr-482, which is not a standards tag at all — the sheet
tags `FUN-7` throughout, and `0.08P` is lifted out of problem 7's stem,
`dP/dt = 0.08P`. The extractor reads `<digits>.<digits><Letter>` out of PDF
prose and cannot tell a differential equation from a CCSS code. Worth
narrowing before that flag is ever promoted past advisory.

## A correction to the rubric-v2 diagnosis this run forced

Before these verdicts arrived, run 2's constant-3 scores on
`curriculum_alignment` and `instruction_following` were diagnosed as
STRUCTURALLY unscoreable: v2's test-for-4 names a standards map absent from the
packet, and requires filenames that the harness renames after the delivery
message is written, while v2's scale forbids awarding a 4 for a test you did
not run. That reasoning was sound and the facts behind it are all true.

**The conclusion was too strong, and this run disproves it.** Scored under the
*identical frozen v2 rubric* — the copy in this run still points at
`references/standards-map.md`, which is still not in its packet — the
calibration judge produced the full range on both:

| dimension (v2) | run 2 | calibration |
|---|---|---|
| curriculum_alignment | 3 × 300 | 2 × 3, 3 × 15, **4 × 7** |
| instruction_following | 3 × 300 | 2 × 7, 3 × 6, **4 × 12** |

So the anchors are **ambiguous, not impossible**: one judge read them as
capping at 3, another did not. The repairs shipped for them — putting the map
in the packet, excluding filenames from the claim test — are still right,
because removing the ambiguity is the point. But the causal claim ("the test
could not be run", "unverifiable by construction") is corrected to: *these
anchors are read inconsistently across judges, and run 2's judge resolved that
ambiguity by refusing the 4 on every case.* A dimension constant across 300
cases remains a broken measurement; the breakage is in how the anchor is
worded, not in what the packet contains.

## The confound: this is not run 2's judge

The verdicts carry two judge models — **9 by `gpt-5`, 16 by `gpt-5.6-sol`** —
and run 2 was scored entirely by `gpt-5.6-sol`. The split is uneven across
classes (all 5 ramp-inversions went to `gpt-5.6-sol`; 4 of 5 vague-rubrics went
to `gpt-5`), so the per-class rates above are **not** clean single-model
measurements. The worked-step-error result is the least contaminated: 4 of its 5
went to `gpt-5.6-sol`, and 3 of those 4 detected.

## What this says about run 2's 295/300

On the same 25 sheets:

| | run 2 (`gpt-5.6-sol`) | calibration |
|---|---|---|
| mean | 31.32 / 32 | 29.68 / 32 |
| ACCEPT | 25 / 25 | 17 / 25 |
| verdict agreement | **17 / 25 (68%)** ||
| mean absolute score difference | **2.20 points** ||

A third of the sheets flip verdict between two passes over identical artifacts.
That is the number to carry forward: **run 2's 98.3% ACCEPT is not a property of
the worksheets, it is a property of that judging pass.** Nothing here supports
treating a single-pass ACCEPT rate as a quality measurement, and the earlier
conclusion — that the run-1/run-2 comparison shows no attributable improvement —
is strengthened, not weakened.

## What to do

1. **Seed a class the judge is blind to and see if the rubric can be taught it.**
   Both blind spots are metadata-fitness questions. A rubric line asking the
   judge to state the difficulty ramp it observed, and to quote one `manual`
   entry's rubric and say what a grader would do with it, converts both from
   inference to transcription — the same mechanism that made the bank
   transcription work.
2. **Re-run the calibration single-model.** The two-model split makes every
   per-class rate an estimate over 4–5 cases from a mixed instrument.
3. **Adjudicate the three control findings.** If curr-082's tick labelling is
   real, it is a shipped mathematical error on an elementary sheet and the
   number-line macros added this session are the fix.
4. **Stop quoting single-pass ACCEPT rates.** 68% inter-pass agreement means a
   run needs either multiple passes or a seeded denominator before its headline
   number means anything.
