# Diagnosing Quadrant and Parameter-Orientation Errors — Precalculus

Three PDFs are ready.

**Worksheet (`ws_polarerr_curr434.pdf`, 4 pages, 8 problems).** An error-analysis set built
entirely around the two places students lose points on polar and parametric work: where the point
actually is, and how far around the curve the parameter runs. Five problems are explicit
find-and-fix items — a student's wrong work is shown and must be diagnosed in a sentence before
the correct value is given:

- 1: $\arctan$ used raw on $(-3,4)$, giving a Quadrant IV angle for a Quadrant II point.
- 2: $180^\circ$ added to $-45^\circ$ instead of $360^\circ$ (direction reversed, not renamed).
- 3: a negative $r$ dropped when converting $(-4, 60^\circ)$ to rectangular coordinates.
- 5: only one parameter value reported where an ellipse reaches $y = 1$ twice.
- 6: the reference angle reported for the Quadrant III point $(-5,-12)$, because the two minus
  signs cancelled inside $\arctan$.

Problem 4 diagnoses a swapped parametrization ($x = 3\sin t$ vs $x = 3\cos t$) and asks how
starting point and direction differ; problem 7 renames $(-6, 200^\circ)$ with a positive $r$ inside
$[0^\circ, 360^\circ)$; problem 8 is the open synthesis — show $x = 2+3\cos(\pm t)$,
$y = -1+3\sin(\pm t)$ trace the same circle in opposite directions, sketch it with arrows, and
explain why the Cartesian equation cannot carry orientation. Difficulty ramps 2 to 5 and the four
methods interleave (no run longer than one).

**Answer key (`ak_polarerr_curr434.pdf`, 3 pages).** Quick-answer bank, then a **Common wrong
answers** block generated from the verification data — each planted error printed with the number
it produces ($-53.13$, $135$, $3.46$, $1.5$, $67.38$, $380$), so a grader can read the
misconception straight off the student's answer. Every solution is written as *diagnosis first,
repair second*, and problem 8 carries a full model answer with a $t$-table and explicit grading
criteria.

**Study guide (`ss_polarerr_curr434.pdf`, 2 pages).** Four sections: the quadrant-placement rule
for rectangular-to-polar (with the QI–QIV table and why $\arctan$ can never place a QII/QIII
point), negative $r$ and equivalent names, reading parametric orientation from a $t$-table, and
finding *every* parameter value rather than the one the inverse function returns. Each section has
a rule box, a two-step worked example with the strategy stated first, and a try-it whose answer is
printed upside down inside the box.

## Verification

7 of 8 worksheet answers are machine-checked with SymPy: 4 `approx` (the quadrant-corrected
angles $126.87^\circ$, $315^\circ$, the negative-$r$ coordinate $-3.46$, and the parametric
$x = 2.60$), 1 `solve_interval` (both parameter values $30^\circ$ and $150^\circ$, with the
solver confirming completeness on $[0^\circ,360^\circ)$), and 1 `eval` (the $20^\circ$ rename).
**Problem 8 is flagged `manual`** — it is an explain-and-sketch task with no single checkable
value, and no verification is claimed for it.

**All six planted wrong results are declared as machine-checked misconception traps.** SymPy
evaluates each wrong method and the build fails unless the problem's own check rejects it, so
every find-and-fix item provably discriminates the error it targets, and each printed wrong number
is derived from its trap expression rather than typed by hand. All 8 study-guide boxes are
verified as well (4 `approx`, 2 `approx` try-its, 2 `solve_interval`). Every other gate is green:
skill and facet coverage, layout, unit binding on the answer lines, page budgets, per-problem
answer-key binding, worked-example structure, and prose consistency.

Standards codes are taken verbatim from the skill's standards map; that map has no polar/vector
entry, so the trigonometric-function and trig-equation codes closest to this content are used.
