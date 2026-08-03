# Choosing a Fast Way to Add Within 10 — K/Grade 1

Three PDFs, all gated green:

- **Worksheet** (`ws_addstrategy_curr025.pdf`, 3 pages) — 10 problems. Every
  problem is an addition fact within 10 where the *choice of strategy* is the
  work: the student circles which of the three taught methods they used, then
  writes the sum. A short warm-up (problems 1–2, one count-on and one double)
  is followed by fully interleaved problems, so no two neighbours ever call for
  the same method (max same-facet run = 1).
- **Answer key** (`ak_addstrategy_curr025.pdf`, 2 pages) — every problem worked
  in numbered steps that *name the strategy first* and then execute it, plus a
  "Common wrong answers" bank generated from the declared misconception traps.
- **Study guide** (`ss_addstrategy_curr025.pdf`, 2 pages) — one section per
  strategy: when to use it, the rule/model, a worked example, and a distinct
  try-it with the answer printed upside down. A watch-out box covers the
  off-by-one count-on error.

## What the sheet actually exercises

Three facets, all planned in the JSON and tagged on every problem:

| Facet | Problems |
|---|---|
| `count-on-from-larger` | 1, 4, 9 |
| `doubles-and-near-doubles` | 2, 5, 7 |
| `partners-of-ten` | 3, 6, 8, 10 |

Difficulty ramp: `1, 1, 2, 2, 2, 3, 3, 3, 4, 5`. Problem 9 is an error-analysis
item (Sam counts on from the number he is holding and lands one short); problem
10 is the synthesis challenge — three addends, reorder to make a friendly pair.

## Verification

- **10 of 10 worksheet problems machine-verified** by SymPy — 7 `eval`
  (including the two three-addend/reordering items) and 3 `solve`
  (missing-addend forms: `7 + x = 10`, `x + x = 8`, `x + 2 = 10`).
  **0 manual.**
- **6 of 6 study-guide boxes machine-verified** (3 worked examples + 3 try-its).
- Two misconception traps are declared and machine-checked: the count-on
  off-by-one (gives 7 instead of 8) and dropping the third addend (gives 5
  instead of 10). The verifier confirmed each wrong value is *rejected* by the
  problem's own check, and both are printed in the key's "Common wrong answers"
  block so a grader can diagnose rather than just mark.
- Standard tagged on every problem: `K.OA.A / 1.OA.C.6`, taken verbatim from
  `references/standards-map.md`.

Nothing on this sheet is genuinely open-ended, so there is nothing flagged for
manual review — the "explain what Sam did wrong" line on problem 9 is written
work the key models, but the graded answer line is the verified sum.

`BUILD PASSED` on the first run: all 21 gates green, exit 0.
