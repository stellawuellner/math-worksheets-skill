# Three Views of a Limit — Precalculus / Introduction to Limits

Three PDFs are ready:

- **Study guide** (`ss_limits_curr445.pdf`, 2 pages) — read this first.
- **Worksheet** (`ws_limits_curr445.pdf`, 6 pages, 12 problems).
- **Answer key** (`ak_limits_curr445.pdf`, 4 pages) — worked reasoning for every problem.

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
  a horizontal asymptote read as $\lim_{x\to\infty}$.
- **a series sum as a limit** (4, 8, 12) — a finite partial sum in sigma
  notation, an infinite geometric series, and the closing synthesis: compute
  $S_5$, compute the infinite sum, and explain what an "infinite sum" actually
  means.

The three graphs are printed **together with the directions** as a named bank
(Graph A, Graph B, Graph C), and each graphical problem names the graph it uses.
That keeps the figure-scope rule satisfied — no problem block carries a figure of
its own, so no graph can be read as belonging to a neighbouring problem — while
the graphs stay large enough to read a limit off.

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
- **Eight misconception traps are declared and machine-checked** (problems 2, 4,
  5, 6, 8, 10, 11, 12), all reported distinguishable: reading $0/0$ as the answer
  $0$; stopping a sigma sum one term short (16); reporting $\sqrt{1}+1 = 2$
  instead of its reciprocal; dropping the middle term of the difference-of-cubes
  factor (2); taking the $n=1$ term as the first term of a geometric series
  starting at $n=0$ (3); inverting the ratio of leading coefficients at infinity
  (0.5); reading a graph's $y$-intercept instead of its end behaviour (0.5); and
  using $a=1$ in $a/(1-r)$ where the first term is $\tfrac12$ (2). Each prints in
  the key's "Common wrong answers" block, so a wrong paper names its own error.

Standards are `LIM-1`, `LIM-2` and `LIM-7`, taken from the AP Calculus rows of
`references/standards-map.md`.

## Study guide

Opens with what $\lim_{x\to a}f(x)=L$ actually claims and the existence rule for
one-sided limits, then **four** sections matching the worksheet's four lenses —
four, not five, because the graph section carries a figure and section cost is
quantised. Each has a rule box, a worked example whose first step says *why* that
method, and a try-it with the answer printed upside down inside the box. The
graph section's example and try-it share one small graph — reading the left-hand
limit, then the right-hand limit, and noticing they disagree. It compiles to
exactly 2 pages, inside the hard cap.

## Gate chain

Final verdict: **BUILD PASSED — 1 verification run flagged manual-review items
(exit 2)**, which is the correct outcome when a sheet contains genuinely open
explanations. All other gates green: template shells, both verification files,
skill and facet coverage, subtitle binding, figure scope, work space, three
compiles inside their page budgets (ws 6/7, ak 4/7, ss 2/2), per-problem
answer-key binding, study-guide structure, and prose consistency.

One gate failed on the first attempt: `layout-ws` rejected valued figures on 3 of
12 problems — the pgfplots axes count as valued because they print numeric ticks,
which is exactly the ambiguity the all-or-nothing figure rule exists to stop. The
three graphs were moved into a single named bank ahead of the first problem and
each problem now names its graph. No mathematics changed.

The answer key `\input`s the quick-answer bank plainly under the title block, with
no `\raggedright` and no `\emergencystretch`; the eight-line "Common wrong
answers" block compiles with no overfull box, and the `^` inside one trap
description was escaped for me as documented.
