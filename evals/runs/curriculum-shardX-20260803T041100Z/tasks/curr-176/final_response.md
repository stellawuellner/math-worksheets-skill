# Solving One-Step Equations with Rational Coefficients — Grades 6–7

Three PDFs are ready: the student worksheet (6 pages, with full work space), a
step-by-step answer key, and a two-page skills summary.

## What the worksheet contains

10 problems in a guided concept-practice format. Every one of them is a
*one-step* equation whose coefficient is rational — a unit fraction, a non-unit
fraction (positive and negative), or a decimal — so the requested focus is
exercised by 10/10 problems, not merely most of them. Four subskills are tagged
as facets and rotate from the first problem, so no two consecutive problems use
the same undo:

| Facet | Problems | The undo being practised |
| --- | --- | --- |
| `fraction-coefficient` | 1, 4, 8 | unit-fraction coefficient: multiply by the denominator |
| `decimal-coefficient` | 2, 7 | divide both sides; clear the decimal by scaling by 10 or 100 |
| `reciprocal-multiply` | 3, 6, 9 | non-unit fraction: multiply by the reciprocal, sign included |
| `check-and-fix` | 5, 10 | substitute into the original equation to test a claimed solution |

The `concept-models` mode is carried by tape diagrams: a value-free reference bar
sits with the directions, problems 1 and 3 read their equations *off* a bar cut
into equal parts (one part is 7; two starred parts are 8), and problem 4 asks the
student to draw the bar themselves. Each diagram is explicitly connected to the
notation the problem then solves. Problems 6, 7, and 9 add the cases students
most often get backwards: a negative rational coefficient, a coefficient greater
than 1 (so the solution is *smaller* than the constant), and a fraction
coefficient with a decimal constant.

Difficulty ramps 1, 2, 2, 2, 3, 3, 3, 3, 4, 5. Every problem is tagged
`6.EE.B.7 / 7.EE.B.4`, which is the row `references/standards-map.md` gives for
"One/two-step equations" and matches the task's own `standard_refs` string
exactly — no code invented, none missing.

## What was verified

**All 10 worksheet problems are machine-verified by SymPy — 0 manual items**, as
11 checks: eight `solve` checks and three `eval` checks. Problem 10 (the
error-analysis challenge) carries two verify entries under one problem id, which
is the encoding for a multi-part problem: part (a) is an `eval` of Devon's value
(8) and part (c) is the `solve` of the corrected equation (27). Both are boxed
separately in the key. That matches the task's `solve` + `eval` verification
targets.

Two misconception traps are declared, machine-checked as distinguishable, and
printed in the answer key's "Common wrong answers" bank:

- P5 — using the reciprocal while *checking* instead of substituting as written
  (would give 33.33)
- P10 — substituting into 3/2 instead of 2/3 (would give 18 and wrongly confirm
  Devon's error)

Both target the same misconception the focus lives on: when the reciprocal
belongs in the work and when it does not.

The study guide's 8 boxes (4 worked examples + 4 try-its) are verified by their
own JSON. Nothing is claimed as verified without a check behind it; the
one-sentence explanations asked for in parts (a) of several problems are worked
in the key as reasoning, not scored as separate answers.

## Study guide

Two pages, one section per worksheet skill: unit-fraction coefficient, decimal
coefficient, reciprocal for a non-unit fraction, and checking by substitution.
Each section is a rule box, a worked example opening with a strategy sentence,
and a distinct try-it whose answer prints upside down inside the box. Sections 3
and 4 are deliberately linked — section 4 checks section 3's answer — so the
student sees solving and checking as two different moves on one equation. The
opening box gives the size prediction (coefficient below 1 means a bigger
solution) that catches most errors before arithmetic starts.

## Notes

- `workspace_cm` (6–8 cm) is declared on every problem and was set before the
  first compile: the tape diagrams and displayed equations sit in the *stem*,
  which the page budget charges a flat 0.6 cm for. The sheet runs 6 pages
  against a computed 6-page budget; nothing was compressed.
- The build passed on the first run — all 21 gates green, no manual-review
  items. Prose-consistency match rates are 93.5% (worksheet) and 87.9% (study
  guide); the flagged values are intermediate products such as 60/3 and 90/6
  that appear inside the shown work.
