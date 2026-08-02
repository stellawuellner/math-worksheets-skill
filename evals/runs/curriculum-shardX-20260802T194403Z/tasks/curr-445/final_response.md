# Three Views of a Limit — Precalculus / Introduction to Limits

Three PDFs are ready:

- **Study guide** (`ss_limits_curr445.pdf`, 2 pages) — read this first.
- **Worksheet** (`ws_limits_curr445.pdf`, 7 pages, 12 problems).
- **Answer key** (`ak_limits_curr445.pdf`, 3 pages) — worked reasoning for every problem.

## What the worksheet does

The focus is the connection between the numerical, graphical and algebraic ideas
of a limit, so the sheet asks the same question through four lenses and
**interleaves** them after a single warm-up problem, which forces a choice of
method rather than repetition of one:

- **from a table** (1, 5, 10) — problem 1 reads a completed two-sided table;
  problems 5 and 10 have the student build the table (four decimal places) and
  then name the exact limit, including the end-behaviour case $x\to\infty$.
- **from algebra** (2, 6, 9) — factoring a difference of squares, a difference of
  cubes over a difference of squares, and rationalizing with a conjugate.
- **from a graph** (3, 7, 11) — a removable hole (limit exists, value does not),
  a jump (one-sided limits disagree, so the two-sided limit does not exist), and
  a horizontal asymptote read as $\lim_{x\to\infty}$. Each of the three graphs is
  printed inside its own problem and captioned, so no figure can be read as
  belonging to a neighbouring problem.
- **a series sum as a limit** (4, 8, 12) — a finite partial sum in sigma
  notation, an infinite geometric series, and the closing synthesis: compute
  $S_5$, compute the infinite sum, and explain what an "infinite sum" actually
  means.

Problems 3 and 7 are deliberately mirror images: in 3 the limit exists where the
value does not; in 7 the value exists where the limit does not. Difficulty ramps
from 1 to 5 and every problem has generous work space.

## What was verified, and what is manual

- **18 machine checks passed** across the 12 problems, using SymPy limits
  (including one-sided and at-infinity), series summation, and numeric
  evaluation. Every table cell the student is asked to fill in is itself a
  verified check — problems 5 and 10 each carry two numeric checks plus the limit
  — so nothing printed as an answer is outside the verification data. Every
  printed boxed answer in the key was bound back to its recomputed value at the
  precision it is printed with.
- **2 items are flagged for manual review**, correctly: problem 7(c) (justify why
  the two-sided limit fails) and problem 12(c) (explain what the sum of an
  infinite series really is). These are open written arguments that no CAS can
  check. The key gives a full model answer for each, plus what to accept and what
  not to accept.

The one-sentence explanations attached to problems 1, 3 and 11 are teaching
riders, not separate answers; each has a model response in the key, and the
value on every answer line is machine-checked.

## Study guide

Opens with what $\lim_{x\to a}f(x)=L$ actually claims and the existence rule for
one-sided limits, then four sections matching the worksheet's four lenses. Each
has a rule box, a worked example whose first step says *why* that method, and a
try-it with the answer printed upside down inside the box. The graph section's
example and try-it share one small graph — reading the left-hand limit, then the
right-hand limit, and noticing they disagree.

## Gate chain

Final verdict: **BUILD PASSED — 1 verification run flagged manual-review items
(exit 2)**, which is the correct outcome when a sheet contains genuinely open
explanations. All 21 gates green otherwise: template shells, both verification
files, skill and facet coverage, subtitle binding, figure scope, work space,
three compiles inside their page budgets, per-problem answer-key binding,
study-guide structure, and prose consistency.

One gate failed on the first two attempts: the study guide compiled to 3 pages
against its hard 2-page cap. The rule boxes were condensed and the example graph
resized until all four sections fit; no example, try-it or answer was dropped.
