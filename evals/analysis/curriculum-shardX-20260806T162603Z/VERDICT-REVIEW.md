# Run 2 verdict review — 300 cases, judged and read back

Verdicts merged to `main` in PR #7. Judged by `codex-independent-grader-1/2/3`
on **`gpt-5.6-sol`**, 100 cases each, with dual v1/v2 scoring as the forward
compatibility instruction asked.

Headline: **295 ACCEPT / 5 REJECT, mean 31.21 / 32.** And that number should
not be reported on its own, because most of what it says is about the
instrument rather than the worksheets.

## 1. The comparison does NOT show the fixes improved quality

Pooling every previously-judged case gives ACCEPT 65.3% → 98.3% and mean
30.02 → 31.21 (+1.19). That figure is an artifact and should not be quoted.

Broken out per prior judging pass, on the same task ids:

| prior pass | n | ACCEPT before → after | mean before → after |
|---|---|---|---|
| 20260803T181926Z (8.7% hard-fail) | 150 | 91% → 99% | 31.25 → 31.27 (**+0.01**) |
| 20260802T194403Z (10.0% hard-fail) | 50 | 90% → 98% | 31.62 → 31.04 (**−0.58**) |
| 20260803T041100Z (**86%** hard-fail) | 100 | 14% → 97% | 27.36 → 31.20 (+3.84) |

The whole of the apparent gain comes from the third row — a judging pass that
rejected 86 of 100, wildly out of line with every other pass including its own
neighbours a day either side. Pooling it in manufactures an improvement.
Against the two comparable passes the mean is **flat and slightly negative**.

**Two confounds sit on top of that, and either alone would be disqualifying:**

- **The judge changed.** Runs 1–3 were `codex` on `gpt-5.6`. Run 2 is three
  graders on `gpt-5.6-sol` — a different model. Nothing here separates "the
  worksheets got better" from "the grader got more lenient".
- **The rubric text differs by 39 lines** between the runs (additive
  improvements made while building run 2; already recorded in COMPARISON.md).

What *did* move: **hard-failure rate 8.7% / 10.0% → 1.7%** (5 of 300). That is
the one directional signal, it is consistent across both comparable baselines,
and it is still not cleanly attributable for the reasons above.

## 2. The instrument is at its ceiling

Mean 31.21 out of 32 is 97.5%. Per-dimension, v1:

| dimension | 4s | anything below 4 |
|---|---|---|
| curriculum_alignment | 297 | 3 |
| clarity_and_accessibility | 298 | 2 |
| mathematical_correctness | 297 | 3 |
| answer_key_quality | 297 | 3 |
| instruction_following | 290 | 10 |
| study_guide_quality | 282 | 18 |
| visual_and_print_quality | 213 | 87 |
| problem_set_design | 198 | 102 |

Six of eight dimensions are 4 on ~99% of cases. Only `problem_set_design` and
`visual_and_print_quality` carry usable variance. A score with this little
spread cannot register an improvement even if one happened — which is the
other half of why section 1 reads flat.

## 3. Rubric v2 is broken on two dimensions — this is our defect, not the judge's

Under v2, `curriculum_alignment` and `instruction_following` are **3 for all
300 cases**. Not one 2, not one 4. Those dimensions carry zero information and
the v2 total is really a 24-point scale plus a constant 6 (hence max 30).

v2 against v1, as a measuring instrument:

- `answer_key_quality`: **better** — 14 cases pulled off the ceiling
- `curriculum_alignment`, `instruction_following`: **dead** — constant
- `study_guide_quality` (18 → 2 below 4), `visual_and_print_quality`
  (87 → 42): **worse**, more cases pushed to the ceiling

So v2 is a net regression except on one dimension. The anchors for those two
dimensions need rewriting so a 4 is reachable and a 2 is defined; until then
the official v1 verdict stands and v2 should not be promoted.

## 4. The 5 REJECTs are all real, and two are ours

- **curr-100** — study guide teaches "a rhombus and a trapezoid have no square
  corners" as a universal rule. A square *is* a rhombus. Correct catch;
  prototypical-shape reasoning taught as classification.
- **curr-119** — worksheet asks students to refute "adds an even number each
  time", which is *true* for differences 2, 6, 18, 54; the key silently assumes
  the unprinted word "fixed". Correct catch.
- **curr-120** — study-guide try-it keyed only digit 9 where 0 also works.
- **curr-151, curr-188** — **answer-bank defects in `render_quick_answers.py`.**

The last two are one new class, and it is not one the gates model:

- curr-188: `slope` check, `expected: 6`, slot `"(a) the equation"`. The
  student is asked for `y = 6x`; the check verifies the slope; the bank prints
  "the equation = 6".
- curr-151: three entries on one problem, slots `word form` / `colon form` /
  `fraction form`, **all three `expected: "3/5"`**. Two of the three printed
  answers are wrong for the form their own label promises.

**A slot label can name a FORM that the expected value is not in.** The slot
gate checks coverage — that every printed response has an entry — and never
that the value matches the form its label advertises. Same family as the
`equiv` centre-radius fix landed this session, which is the one case that
*was* closed.

## 5. That class resists gating — measured, not assumed

Two detectors were built and measured over 2953 slotted entries across all
four runs:

- **keyword-vs-value** ("colon form" must contain `:`, "percent" must carry
  `%`, …): 49 raw hits, of which the `percent` family is **0 for 23** — "ten
  percent of the seats" asks for a count (35), not a percent. Unusable.
- **identical values across distinct slots** (the curr-151 shape): 42 hits, of
  which roughly **2 are true**. Most are the pedagogical point — curr-240's
  "slope of JK" and "slope of the image J'K'" are equal *because* rigid
  motions preserve slope.

The rules that DO hold up are narrow but real:

- a slot containing "colon form" whose value has no `:`, or "word form" whose
  value has no letters — 3 hits, 3 true (both curr-151 rows).
- a slot naming **"the equation"** whose value contains no `=` — **18 entries
  across 8 cases**: curr-188 (the one the judge caught), plus curr-190 ×5,
  curr-225 ×3, curr-338 ×3, curr-400 ×2, curr-244, curr-245, curr-373.
  Excluding "…solved for y", which names a side rather than a whole equation.

That second count is the finding worth acting on: the judge caught **1 of 8**
affected cases. It rejected curr-188 and passed the other seven, which carry
the identical defect — curr-190 five times over. So this is not a rare slip,
it is a systematic 8-case pattern that a single sampled judgement surfaced.
Worth shipping as a lint; it is cheap and its precision on this corpus is 18
for 18.

## 6. Consistency check

**0 of 295 ACCEPTs contradict a mechanical fact** — every one has a recorded
gate chain that passed and a matching problem count. The judge's ACCEPTs and
the build's own record agree.

## 7. What this run actually establishes

- No regression: 300/300 build green, 1.7% hard-failure rate, no ACCEPT
  contradicted by the record.
- Five genuine defects found, three of them in content the machine cannot
  check (a false classification rule, an ambiguous refutation task, an
  under-keyed try-it) — exactly the territory the judge exists to cover.
- It does **not** establish that the generator fixes improved quality. The
  instrument is at ceiling, the judge model changed, and the rubric moved.

The fix for that is the seeded-defect calibration run (`evals/seed_defects.py`,
task #54): plant known defects in known-clean sheets, keep controls, and
measure what the judge catches. Until that number exists, 98.3% ACCEPT and a
blind grader are indistinguishable — which is the reason the harness was built
before these verdicts landed.
