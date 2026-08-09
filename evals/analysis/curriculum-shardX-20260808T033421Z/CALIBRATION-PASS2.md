# Calibration pass 2 — one instrument, and the rubric taught

The re-run pass 1's confound demanded: the same 25 sheets (15 seeded, 10
controls), byte-identical artifacts, judged blind to pass 1 by **one model
(`gpt-5.6-sol`) across all 25 verdicts**, with v2 scored under the updated
rubric that added the mandatory ramp and manual-rubric transcriptions.
Verdicts rehomed at `evals/runs/curriculum-shardX-20260808T033421Z-pass2/`;
mechanical comparison by `evals/compare_calibration_passes.py`, detection
adjudicated by reading each citation against the sealed manifest, per the
pass-1 rule: a rejection is not a detection unless it cites the planted
defect, and a citation is checked against the artifacts before it is believed.

## Headline: the two blind classes are blind no more

| defect class | pass 1 (mixed models, old rubric) | pass 2 (one model, transcribing rubric) |
|---|---|---|
| worked-step-error | 3/5 cited & rejected | **3/5** cited & rejected (the same three) |
| ramp-inversion | **0/5** | **5/5 cited** — 4 via the ramp transcription verbatim ("falls from 5 to 1 and the sheet is not declared as a drill"), 1 inside a rejection carried by a pre-existing defect |
| vague-rubric | **0/5** | **3/5 cited** ("says only 'Grade the student's explanation' and provides no criteria") — and the 2 misses are structural, below |
| controls falsely hard-failed | 1/10, on fabricated citations (curr-082) | **0/10** |

**Transcription compliance went 0/25 → 25/25** on both new sections. The
mechanism worked exactly as intended: the classes the judge could not *infer*
in pass 1 became classes it *observed* in pass 2, because the rubric made it
copy the metadata down before scoring. This is the same repair that fixed the
answer-bank blindness in run 2, now demonstrated a second time on two more
classes. Conversion of inference to transcription is, on this evidence, the
single most effective judge repair we know.

## Where the consequences landed — v1 frozen, v2 caught them

Every taught detection produced its verdict consequence in the **v2 shadow**,
not the official v1 verdict, and that is the architecture working, not a gap:
v1 has no ramp or rubric rule and stays frozen for run-to-run comparability.

| case | class | v1 (official) | v2 shadow |
|---|---|---|---|
| curr-278, 384, 419, 424 | ramp-inversion | ACCEPT (psd 4) | **REJECT** (problem_set_design capped at 2) |
| curr-051, 223, 346 | vague-rubric | ACCEPT (akq 4) | **REJECT** (answer_key_quality capped at 2) |

Seven of eight taught detections applied the cap the rubric prescribes,
7-for-7 among the cases where the citation named the planted defect. If v2 is
ever promoted to official, these become rejections outright.

## The two vague-rubric misses are a sampling artifact, not inattention

The rubric says transcribe the **first** `manual` entry. Both misses planted
the hollowed rubric elsewhere:

- curr-069: manual ids [4, 5, 7, 8]; seed in **7**; the rubric sampled 4.
- curr-075: manual ids 1–12 (all twelve); seed in **6**; the rubric sampled 1.

Where the transcription sampled the seeded entry it detected **3 of 3**.
Where it structurally could not, it detected 0 of 2. The mechanism's hit rate
is 100% conditional on looking, so the round-3 rubric fix is coverage, not
emphasis: transcribe one entry fully, then one line per remaining manual
entry stating whether a grader decision is statable from its desc.

## The worked-step position effect is now well supported

The same three hits (curr-255, 355, 373) and the same two misses (252, 394)
as pass 1, across two passes and two rubrics. Every hit sits in **problem
10** — the last worked solution; every miss sits mid-sheet (problems 5 and
7). Cumulatively: 6/6 detections at the final problem, 0/4 at interior
positions. A judge that recomputes the last worked solution and skims the
middle is no longer a hypothesis worth a probe; it is the best available
reading, and the next seeding round should plant worked-step errors at
positions 1, N/2 and N deliberately.

## Controls: the fabrication did not recur, and the real finding did

- **curr-082 flipped REJECT → ACCEPT (32/32)** — the single verdict flip of
  the entire pass. Pass 1's hard failure here was adjudicated as fabricated
  (three number-line citations, all contradicted by the TikZ source and the
  rendered page). The single-model pass does not reproduce it. One case
  cannot separate "the second model doesn't fabricate" from chance, but the
  one known fabrication vanished when the instrument was unified.
- **curr-482 REJECT again**, citing the same unverified particular-solution
  formulas — the control finding previously adjudicated as REAL (and now
  covered by the `formula_ask_notes` advisory lint). A true defect being
  re-found by an independent pass is exactly what a working judge looks like.
- **curr-496 REJECT (30/32)** on `curriculum_alignment` 2 — the same
  zeta-values judgement call as pass 1, still not a factual claim, no hard
  failure.

False hard failures on clean sheets this pass: **0 of 10** (pass 1: 1 of 10).

## Stability

| | run 2 vs pass 1 | pass 1 vs pass 2 |
|---|---|---|
| verdict agreement | 68% | **96% (24/25)** |
| mean \|score delta\| | 2.20 | **1.48** |

The comparisons are not perfectly parallel (pass 1 was itself mixed-model,
and 16 of its 25 verdicts came from the same model as pass 2), so 96% is an
upper-ish bound on same-instrument stability rather than a clean measurement.
It is still the difference between an instrument you can hillclimb with and
one you cannot: the one verdict that moved is the one that *should* have
moved.

## What changes because of this

1. **Adopted**: transcription-first rubric design. Any future dimension the
   judge scores should name the artifact lines it must copy before scoring.
2. **Round-3 rubric fix**: extend the manual-rubric transcription to cover
   every manual entry (one statability line each), closing the sampling gap.
3. **Round-3 seeding fix**: plant worked-step errors at first/middle/last
   positions to measure the position effect it can no longer hide behind
   class labels.
4. **Standing caution, unchanged**: worked-step detection is still 3/5 even
   at its best, and v1 official verdicts still pass ramp-inverted and
   rubric-hollowed sheets by design. The deterministic gates remain the only
   layer whose "pass" means pass; the judge is a survey instrument whose
   error bars are now measured — which is what makes it usable.
