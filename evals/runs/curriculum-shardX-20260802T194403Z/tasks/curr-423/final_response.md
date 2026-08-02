# Solving Trigonometric Equations on Restricted Intervals — Precalculus

Three PDFs are ready: the student worksheet, a full step-by-step answer key, and
a two-page study guide.

**Worksheet (`ws_trig_interval_curr423.pdf`, 5 pages, 10 problems).** The sheet
opens with the representation that makes the whole topic make sense: a graph of
$y = \sin x$ crossed by the line $y = \tfrac{1}{2}$ on $[0, 2\pi)$, so the
student can *see* that a restricted interval is what turns infinitely many
solutions into a finite, listable answer — and that reporting one of two
crossings is half an answer.

The ten problems rotate through four methods rather than drilling one:

- **Linear equations** in a single trig function (1, 2, 3), with problem 3 set on
  $[-\pi, \pi)$ against tangent's period of $\pi$ — a different interval *and* a
  different period, which is where students lose solutions.
- **Identity-first rewrites** (4, 5, 9): verify $\cos 2x = 1 - 2\sin^2 x$, then
  use it on $\cos 2x + 3\sin x = 2$; problem 9 is $\sin 2x = \cos x$, where
  dividing by $\cos x$ silently deletes two solutions.
- **Quadratics in a trig function** (6, 10), the last one in degrees on
  $[0^\circ, 360^\circ)$.
- **A periodic model** (7, 8): a Ferris wheel with stated units — evaluate the
  height at a given time, then find every time in one full revolution at which
  the rider is at a given height. Units are declared in the data and printed on
  the answer lines.

**Answer key (`ak_trig_interval_curr423.pdf`).** Every solution shows the
isolation or rewrite, the reference angle, and the quadrant reasoning that
produces each solution — plus the interval reasoning that decides what to keep.
Several entries carry a grading note naming the specific solutions a common
error deletes (dividing by $\cos x$; using period $2\pi$ for tangent; reading a
half-open interval as closed).

**Study guide (`ss_trig_interval_curr423.pdf`, 2 pages).** Four sections, one per
method, each with a rule box, a worked example that opens by naming the
strategy, and a try-it whose answer is printed upside down inside the box. The
periodic-model section teaches the step most students skip: translating the
$t$-interval into a $u$-interval so the unit-circle count still applies.

## Verification

- **All 10 worksheet problems are machine-verified** with SymPy: eight
  `solve_interval` checks (which compare the *complete* root set on the stated
  interval, so a missing solution fails the build), one `equiv` check on the
  double-angle identity, and one `eval` for the Ferris-wheel height. Nothing is
  left to manual review — the build reported `BUILD PASSED — all gates green`.
- The two answers carrying units (13 m, and $t = 10$ s and 20 s) declare
  `answer_unit` in the data, so the unit is bound in both directions: the
  worksheet must print a matching `\answerline`, and the key must print the same
  unit inside its boxed answer.
- All 8 study-guide boxes (4 worked examples + 4 try-its) are verified the same
  way.
- Standards: `HSF-TF.A.2`, `HSF-TF.C.8`, `HSF-TF.B.5`. Difficulty ramps 1 → 5
  with no drops, and no method appears more than twice in a row after the
  warm-up.

**One transparency note.** For the two quadratics-in-a-trig-function problems,
the verify JSON states the equation in *factored* form —
$(2\cos x + 1)(\cos x - 1)$ rather than $2\cos^2 x - \cos x - 1$ — with a `note`
field saying so. The two expressions are identical on expansion, but SymPy's
solver enumerates every root of the factored form while silently dropping the
$\cos x = -\tfrac{1}{2}$ family from the expanded one. The worksheet and key
show the expanded equation, exactly as the student meets it.
