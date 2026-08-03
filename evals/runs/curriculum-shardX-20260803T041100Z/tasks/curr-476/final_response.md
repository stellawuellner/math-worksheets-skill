# Using u-Substitution in Indefinite and Definite Integrals — AP Calculus AB/BC

Three PDFs are ready: the student worksheet (5 pages, with full work space for
substitution boxes and evaluation), a step-by-step answer key, and a two-page
skills summary.

## What the worksheet contains

8 problems in a guided concept-practice format. Every problem is solved by
u-substitution — the focus is exercised by 8/8. Four subskills are tagged as
facets and interleave from the first problem:

| Facet | Problems | What it asks |
| --- | --- | --- |
| `indefinite-usub` | 1, 3, 5 | the derivative is already present; name u, swap, back-substitute |
| `usub-with-adjustment` | 2, 7 | du differs from the integrand by a constant factor |
| `definite-usub-newlimits` | 4, 6 | convert both bounds to u and never return to x |
| `improper-usub-limit` | 8 | rewrite an infinite bound as a limit, substitute, then take the limit |

The `concept-models` mode is carried by a **substitution box** — a small
four-cell table (u, du, new lower limit, new upper limit) printed value-free with
the directions and filled in by the student before every integral. The same table
makes the indefinite/definite distinction visible: indefinite integrals leave the
limit row blank and back-substitute; definite integrals fill it in and stop. Two
problems are deliberately about *choosing* rather than executing: problem 5 asks
the student to write du for both u = sin x and u = cos x and say which one strands
a leftover factor, and problem 2 asks why a constant may cross the integral sign
but a variable may not.

Difficulty ramps 1, 2, 2, 3, 3, 4, 4, 5.

Every problem is tagged `FUN-6.D–FUN-6.E`, copied verbatim from the
"u-substitution / parts (BC)" row of `references/standards-map.md` — exactly the
task's own `standard_refs` string. No code invented, none missing.

## What was verified

**All 8 worksheet problems are machine-verified by SymPy — 0 manual items**, as
9 checks: five `integrate` (each expected antiderivative is differentiated back
to the integrand), three `definite_integral`, and one `limit`. That covers all
three of the task's verification targets (`integrate`, `definite_integral`,
`limit`).

Problem 8 carries two entries under one id, which is the honest encoding of the
improper integral: part (b) is a `limit` check of
`½ − ½e^(−b²) → ½` as b → ∞, and part (c) is a `definite_integral` check of
`∫₀^∞ x e^(−x²) dx = ½`. The convergence *claim* is not asserted as verified on
its own — it is exactly what the finite limit establishes, and both the limit and
the value are checked separately. No proof or explanation anywhere on this sheet
is described as machine-verified; the "say why" parts (2b, 5b, 8c) are worked as
reasoning in the key.

No misconception traps are declared. Traps are only legal on single-comparable
types, and seven of the eight problems return a *function*, not a scalar. Rather
than manufacture a scalar problem to host a trap, the two classic errors are
taught where they actually bite: the answer key for problem 4 names evaluating a
u-antiderivative at the old x-limits as the most common error on that problem
type, and problem 5's part (b) makes the wrong substitution choice the thing the
student has to diagnose.

The study guide's 8 boxes (4 worked examples + 4 try-its) are verified by their
own JSON, including both improper-integral boxes.

## Study guide

Two pages, one section per worksheet skill: derivative already present, constant
adjustment, definite integrals with converted limits, and improper integrals as
limits. Each section is a rule box, a worked example opening with a strategy
sentence, and a distinct try-it whose answer prints upside down inside the box.
The opening box gives the three-step test the whole sheet uses — choose the inner
function, write du, and check that what remains is a *constant* multiple of it,
because a leftover x means the choice was wrong. The watch-out box was dropped to
stay inside the mechanical 2-page cap; the try-its were kept, per the skill's
priority order.

## Notes

- `workspace_cm` (7–9 cm) was declared on every problem before the first
  compile, since each stem carries a displayed integral plus a multi-part
  prompt that the page budget charges only 0.6 cm of stem for. The worksheet
  runs 5 pages against a computed 6-page budget.
- **One gate failed on the first full run**: `answer-key-ak`, on problem 7. The
  boxed answer was written `\dfrac{2}{9}(x³+1)^{3/2} + C`, and the answer-key
  binder normalizes a `\dfrac` whose parts are both plain numbers into a single
  value (0.2222), so the verified tokens 2 and 9 were no longer present in the
  box. Rewriting the box as a single fraction, `\dfrac{2(x³+1)^{3/2}}{9} + C`,
  leaves the numerals visible and the gate passes. This is a real, tested
  constraint, not an inference: I reproduced it and fixed only that one line.
  Worth knowing because it is the inverse of the usual advice — `\dfrac` is safe
  for *fraction-valued* answers precisely because it normalizes, and unsafe for
  a rational *coefficient* in front of a symbolic factor.
- All other gates passed on the first run; prose-consistency match rates are 85%
  or better, with flags on shown intermediates such as 16 − 1 = 15.
