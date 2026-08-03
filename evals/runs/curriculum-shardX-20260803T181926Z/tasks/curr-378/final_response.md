# Solving Exponential and Logarithmic Equations — Algebra 2

Three PDFs are ready:

- **Worksheet** (`ws_explogs_curr378.pdf`, 4 pages) — 10 problems on solving
  exponential and logarithmic equations.
- **Answer key** (`ak_explogs_curr378.pdf`, 3 pages) — a three-step solution per
  problem, a quick-answer bank, and a generated Curriculum section listing
  HSF-LE.A.4 and HSF-BF.B.5 with the difficulty range.
- **Study guide** (`ss_explogs_curr378.pdf`, 2 pages) — three sections, each with
  a rule box, a worked example, and a separate try-it.

## What is on the worksheet

The sheet is organised around the one idea that connects everything:
`log_b M = k` and `b^k = M` are the same sentence written two ways.

1. **Unknown in the exponent** (1, 2, 5, 6, 9): a yeast culture tripling hourly
   (exact, by matching powers of 3), a doubling population that needs logarithms
   because 5 is not a power of 2, a 200 g sample with a 6-year half-life, and a
   1500-dollar account growing by a factor of 1.04 a year. Problem 9 is error
   analysis: a student divided 32 by 4 on `4^(x+1) = 32`, and the student has to
   say why that is not a legal step before rewriting both sides as powers of 2.
2. **Unknown inside a logarithm** (3, 7, 10): a doubling-time model rewritten in
   exponential form, and two equations that must be condensed first and that
   produce an extraneous negative candidate the domain rejects — problems 7 and
   10 both ask explicitly which root is rejected and why.
3. **Rewriting with the logarithm laws** (4, 8): expanding `log_3(9x^4)` and
   condensing `2log_2 x − log_2 3`, presented as the enabling step that makes an
   equation solvable rather than as decoration.

Units are named where the model has them (hours, days, years), and each of those
answer blanks is labelled with its unit. Difficulty ramps 1 → 4, and the three
methods alternate so the student must choose rather than repeat.

## What was verified

All 10 problems were machine-checked with SymPy: the exponential and logarithmic
equations as `solve` checks over the reals, the two calculator answers as
`approx` checks at the precision the problems ask for (nearest thousandth,
nearest hundredth), and the two rewriting problems as `equiv` checks — which is
the honest way to verify "rewrite this", since it tests equivalence of the two
expressions rather than the look of the answer. The answer key's boxed answers
were bound problem by problem to those verified values, units included, and the
six study-guide items were verified the same way.

Two misconception traps are declared and were machine-tested to be
distinguishable from the correct answer: dividing 5 by 2 instead of dividing
their logarithms, and reporting the ratio of the two account balances instead of
the number of years. Both print in the answer key as "common wrong answers".

**Nothing is flagged for manual review.** The build finished all green. The only
consistency-report flags are the `x > 0` domain conditions written into two
stems and one study-guide example, which are conditions rather than givens.
