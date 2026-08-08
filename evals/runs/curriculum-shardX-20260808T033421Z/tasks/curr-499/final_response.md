# Find and Fix: Inconclusive Tests and Forgotten Endpoints — AP Calculus BC

Three PDFs are ready:

- **`ws_serfix_curr499.pdf`** — the student worksheet, 8 error-analysis problems.
- **`ak_serfix_curr499.pdf`** — the full step-by-step answer key.
- **`ss_serfix_curr499.pdf`** — a 2-page study guide.

## What the worksheet does

Every problem shows student work that is wrong in one specific way, asks for the
corrected value, and then asks what rule was broken. The eight errors are the
two the focus names, plus the near neighbours that produce them:

- **Treating an inconclusive test as a conclusion** (1, 5): using the nth-term
  test to *prove* convergence of $\sum 1/n$, and reading a ratio-test limit of
  $1$ as "converges" — when for rational terms that limit was guaranteed to be
  $1$ and was never going to settle anything.
- **Stopping before the endpoints** (2, 6, 8): reporting the open interval the
  ratio test produced. Problem 6 stacks a second fault on it — the coefficient
  in $(2x-6)^n$ is never factored out, so the radius is twice too large as well.
- **Reading a formula off the wrong term** (3, 4, 7): the alternating remainder
  bound taken from the last term kept instead of the first omitted; a geometric
  sum starting at $n=2$ summed as though it started at $n=0$; and an integral
  test where the exponent is decreased instead of increased *and* the integral's
  value is mistaken for the series' sum.

## Verification — and the traps

The answer key's "What is verified" note reports the same split.

- **11 of the 19 checks are machine-verified with SymPy**: every corrected value,
  including the exact bound $\tfrac{1}{81}$, the geometric sum $\tfrac{1}{12}$,
  the radius $\tfrac12$, the improper integral $2$, and the alternating harmonic
  value $-\ln 2$.
- **4 problems carry a machine-checked misconception trap.** Every wrong number
  printed in a stem — $\tfrac{1}{64}$, $\tfrac43$, a radius of $1$, and
  $\tfrac25$ — was *computed* from the wrong method and confirmed by SymPy to be
  distinguishable from the correct answer. Those appear in the key as "Common
  wrong answers" lines, so a paper showing 0.0156 is instantly diagnosable as the
  off-by-one in the remainder bound rather than an arithmetic slip.
- **8 are instructor-judged** — the diagnosis on every problem. That is the
  whole point of an error-analysis sheet: the graded skill is naming the broken
  rule, and no CAS reads prose. Each has a rubric in the key.

Nothing is marked `[unchecked]`: every printed answer slot has an entry.

## Notes

- Problem 8 is worth doing aloud. Its right endpoint gives $\sum 1/n$, whose
  terms *do* go to zero — so the nth-term test is silent there and the harmonic
  series has to be recognised directly. That is the two errors of this sheet
  meeting in one place.
- Problem 7 asks for *both* errors in one sentence of student work; the key
  scores them separately.
- The grade level and the LIM-7/LIM-8 tagging print on the answer key only.
