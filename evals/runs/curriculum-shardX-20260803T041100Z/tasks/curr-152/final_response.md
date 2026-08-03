# Building Equivalent Ratio Tables (Grade 6–7)

Three PDFs are ready.

- **Worksheet** (`ws_ratio_tables_curr152.pdf`, 6 pages) — 12 problems in a
  procedural-fluency format, most of them printed as an actual ratio table with
  cells to fill in. A directions box states the one governing idea (multiply
  both entries of a column by the same number) and the one error that breaks it
  (adding the same amount to both). Problems 1–4 are the warm-up; after that
  the four methods are interleaved so the student has to decide which one a
  table calls for: complete a missing entry, find the scale factor between two
  columns, add the unit-rate column, or judge whether two tables are
  equivalent. No skeleton repeats — problem 3 scales from the *second* row,
  problem 6 has a non-integer scale factor, problem 7 has two blanks pulling in
  opposite directions, problems 10 and 11 ask for an equation rather than
  arithmetic, and the closing challenge adds a "total" row and splits 66 ounces
  into 11 equal parts.
- **Answer key** (`ak_ratio_tables_curr152.pdf`, 3 pages) — a quick-answer bank
  for fast grading, then a reasoned solution per problem: which row reveals the
  scale factor, why that factor applies to the partner entry, the arithmetic,
  and the boxed answer. Five problems carry a grading note naming the exact
  wrong number a specific misconception produces.
- **Study guide** (`ss_ratio_tables_curr152.pdf`, 2 pages) — four sections, each
  with a rule box, a worked example whose first line explains *why* that method
  applies, and a try-it with the answer printed upside down inside the box.

## Verification

Every worksheet answer is machine-verified with SymPy — 21 checks across the
12 problems (several problems have more than one blank, so they carry more than
one verify entry under the same problem id): 16 `eval` checks that recompute
each table entry, scale factor, or unit rate from the problem's own givens,
2 `compare` checks for the equivalent/stronger judgements, and 3 `solve` checks
for the problems that ask for an equation. Nothing is flagged manual — every
problem on this sheet has an exactly checkable answer.

Three misconception traps are declared and machine-checked, so each planted
wrong answer is provably distinguishable from the right one and each is printed
in the key's "common wrong answers" block:

- problem 1: 13 instead of 25 — added the difference instead of multiplying;
- problem 6: 24 instead of 30 — the same additive error with a non-integer
  scale factor, where it is hardest to spot;
- problem 12: 16.5 instead of 24 — divided the total by each ratio number
  instead of by the 11 total parts.

All 8 study-guide items (4 worked examples + 4 try-its) are verified the same
way, and each of the four worksheet facets has a matching worked example.

**Standards used:** `6.RP.A.2` (unit rate) and `6.RP.A.3` (ratio tables), both
taken verbatim from `references/standards-map.md`.

## Build

Green on the first build — all 21 gates pass, including the per-problem
answer-key binding, the `mph` unit binding on problem 8 (declared in the JSON,
printed on the worksheet's answer line and inside the key's box), and the page
budget (worksheet 6 pages, key 3, guide 2 against its hard 2-page cap).
