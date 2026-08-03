# Converting Between Exponential and Logarithmic Forms — Algebra 2

Three PDFs are ready: the student worksheet (6 pages), a step-by-step answer
key, and a two-page skills summary.

## What the worksheet contains

10 problems in a guided concept-practice format. Every problem is a conversion
between `bʸ = x` and `log_b x = y`, or an evaluation/solution that is *done by*
converting — the focus is exercised by 10/10 problems. Four subskills are tagged
as facets and interleave:

| Facet | Problems | What it asks |
| --- | --- | --- |
| `exp-to-log` | 1, 4 | name base/exponent/result, then rewrite the power as a logarithm |
| `log-to-exp` | 2, 7 | rebuild the power from the subscript and the value |
| `evaluate-log` | 3, 6, 8 | evaluate by converting, including a fractional value and change of base |
| `solve-by-converting` | 5, 9, 10 | choose the form that isolates the unknown, then solve |

The `concept-models` mode is carried by the role-labelling model: a value-free
reference card printing both forms with base, exponent, and result named; a
powers-of-3 table the student fills in before reading `log₃ 81` off it (P3); and
a bracketing step in P5 (`2⁵ = 32 < 40 < 64 = 2⁶`, so 5 < x < 6) that ties the
symbolic answer to a size the student can check. The sheet deliberately covers
the cases where the conversion is not cosmetic: a negative logarithm (P4), a
fractional one (P6), a fractional exponent (P7), a compound argument
`log₅(2x − 3)` (P9), and a doubling-time model (P10).

Difficulty ramps 1, 1, 2, 2, 3, 3, 3, 4, 4, 5.

Every problem is tagged `HSF-LE.A.4, HSF-BF.B.5`, copied verbatim from the
"Exponentials & logs" row of `references/standards-map.md`, which is exactly the
task's own `standard_refs` string. No code was invented and none was missing.

## What was verified

**All 10 worksheet problems are machine-verified by SymPy — 0 manual items**, as
11 checks: six `eval`, three `approx`, one `solve`, and one `equiv`. That covers
all four of the task's verification targets (`eval`, `solve`, `equiv`,
`approx`). Problem 8 carries two entries under one id — the `equiv` check proves
the change-of-base identity `log₃x ≡ ln x / ln 3` symbolically, and the `approx`
check pins the decimal `log₃ 20 = 2.727` — and the key boxes both.

Three misconception traps are declared, machine-checked as distinguishable, and
printed in the answer key's "Common wrong answers" bank:

- P5 — dividing 40 by 2 instead of taking a logarithm (would give 20)
- P8 — computing `ln(20/3)` instead of `ln 20 / ln 3` (would give 1.897)
- P10 — computing `2/1.045` instead of `log₁.₀₄₅ 2` (would give 1.914)

All three are the same error at different difficulty: treating an exponent
question as a division question.

The study guide's 8 boxes (4 worked examples + 4 try-its) are verified by their
own JSON. Nothing is claimed as verified without a check behind it; the
"say why" parts (P4c on why a logarithm goes negative, P9c on why the argument
must be positive) are worked as reasoning in the key and are not presented as
machine-checked results.

## Study guide

Two pages, one section per worksheet skill: exponential to logarithmic,
logarithmic to exponential, evaluating by converting, and solving when the
unknown is the exponent. Each section is a rule box, a worked example opening
with a strategy sentence, and a distinct try-it whose answer prints upside down
inside the box. The opening box states the decision rule the whole sheet turns
on — *unknown exponent → log form; unknown inside the log → exponential form* —
and the watch-out box names the subscript-swap error and the change-of-base
error explicitly.

## Notes

- `workspace_cm` (5.5–7.5 cm) was declared on every problem before the first
  compile, because the displayed equations, the powers table, and the
  multi-part stems live in the stem region the page budget charges a flat
  0.6 cm for. The sheet runs 6 pages against a computed 6-page budget.
- The build passed on the first run of the full gate chain (all 21 gates green,
  no manual-review items). Before writing the documents I probed the four
  unfamiliar check shapes — two-argument `log`, a `log` of a decimal, an
  `equiv` against `ln(x)/ln(3)`, and a `solve` through a logarithm — against
  `run_verify.sh` in isolation, which is why no verification rewrite was needed.
- Prose-consistency match rates are 80% or better; the flagged values are
  bracketing powers (27, 81) and shown intermediates such as ln 20 = 2.995732.
