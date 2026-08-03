# Convergence: Geometric Series, p-Series, and the nth-Term Test (AP Calculus BC)

Three PDFs are ready:

- **Worksheet** (`ws_series_curr496.pdf`, 7 pages) — 8 problems, opening with a
  full-width panel showing two pictures of "adding infinitely many terms": a
  table and graph of the partial sums of a convergent geometric series climbing
  toward its limit, and a table of the harmonic series' partial sums that never
  settle. Those two models are referenced by name in the problems, so the
  arithmetic has something concrete underneath it.
- **Answer key** (`ak_series_curr496.pdf`, 4 pages) — a full worked solution per
  problem, a quick-answer bank at the top, a generated curriculum section, and a
  grading note on each problem saying what a full-credit justification has to
  contain.
- **Study guide** (`ss_series_curr496.pdf`, 2 pages) — three sections (geometric
  series, p-series, nth-term test), each with a rule box, one short worked
  example, and a try-it whose answer is printed upside down in the box.

## What the sheet practises

Every problem is a classification: name the family, name the parameter that
decides it, state the conclusion as a consequence.

- **Geometric series** (1, 4, 7): read off $a$ and $r$ — including the case where
  the index starts at $n=1$ so the first term already carries a factor of $r$,
  and the case of a negative ratio. Problem 7 is a bouncing-ball model whose
  total travel distance is finite even though the ball bounces forever.
- **p-series** (3, 6): the whole test is one comparison of $p$ with 1, so both
  problems ask for that comparison in writing before the verdict.
- **nth-term test** (2, 5, 8): the test detects divergence and nothing else.
  Problem 6 is the deliberate collision — the nth-term test is inconclusive there
  while the p-series test settles it — and problem 8 asks the student to write
  out why "the terms go to zero, so it converges" is the test read backwards.

Difficulty ramps from 1 to 5 and the three families rotate rather than block, so
the student has to choose the test rather than repeat one.

## What was checked by machine, and what wasn't

Nine machine checks cover problems 1 through 7 — every infinite sum recomputed
symbolically by SymPy (including $\sum 3(2/5)^n = 5$, $\sum 6(-1/3)^{n-1} = 9/2$,
and the ball's $72$ ft of bouncing), every limit evaluated independently, and both
$p$-versus-1 comparisons. Problem 5 also declares the wrong answer it is designed
to catch — a student who assumes any ratio of polynomials tends to zero — and the
checker confirmed that wrong value really is rejected by the problem's own answer.

**Problem 8 is flagged for manual review.** It asks for a paragraph rebutting a
classmate's argument, which no computer algebra system can grade. The answer key
gives a complete model paragraph, states the three moves a full-credit answer
makes, and says what should not earn credit (a correct verdict with no reason —
which the classmate could have guessed).

## A note on length

The worksheet is 7 pages for 8 problems. That is deliberate: series work needs
room for a limit computation and a written justification underneath each part,
and roughly a page goes to the two partial-sum models on the front. The page
budget was declared against that content rather than the sheet being squeezed to
fit a smaller number.

## Suggested order

Study guide first, then the worksheet with the guide beside it, then the key.
