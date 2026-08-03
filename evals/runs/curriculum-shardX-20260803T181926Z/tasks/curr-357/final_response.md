# Polynomial Long Division — Algebra 2

Three PDFs are ready: the student worksheet, a full step-by-step answer key,
and a two-page study guide.

## What's in the worksheet (12 problems)

All twelve problems are polynomial long division, the skill in CCSS
**HSA-APR.A.1**. The set ramps from difficulty 1 to 5, and no two problems
share the same skeleton — each one adds something the previous one did not
have:

- **Linear divisors (7 problems)** — starting with a quadratic that divides
  exactly, then a first remainder, then cubics, then a divisor whose leading
  coefficient is not 1 (2x − 1), where each quotient term is a genuine
  division rather than a copy.
- **A missing power in the dividend (3 problems)** — x³ − 8, then
  2x³ + 5x − 3, then a quartic missing two powers. This is where the algorithm
  most often collapses, because a skipped column shifts everything after it.
- **Quadratic divisors (2 problems)** — including one that has a missing power
  as well, so the student meets both complications at once.

Two problems build in their own checks. Problem 4 and problem 7 ask for the
dividend to be evaluated at the divisor's zero, which must reproduce the
remainder; problem 10 asks for the multiply-back check written out in full.
Problem 12 closes the set by using a zero remainder to factor a cubic
completely, which is what division is actually *for*.

## What was verified

All 16 machine-checkable answers were recomputed independently with SymPy —
each division as an algebraic identity (dividend over divisor really does
equal the printed quotient plus remainder over divisor, checked symbolically,
not at sample points), plus the two substitution checks, the multiply-back
expansion in problem 10, and the complete factorization in problem 12. Every
boxed answer in the key matches its own problem's verified value.

Two misconception traps were machine-checked as distinguishably wrong: on both
substitution checks, using +3 or +1 instead of the value that makes the
divisor zero. Those print in the answer key as "common wrong answers", so a
student who writes 70 instead of −8 gets a diagnosis rather than a cross.

Nothing on this sheet is flagged for manual review — every problem asks for a
polynomial or a number, and all of them were checked by machine.

## The study guide

Two pages, three sections matching the three worksheet strands. Each carries a
rule box, a worked example whose first step names the stopping rule or the
setup issue *before* any dividing, and a separate try-it with the answer
printed upside down. The opening box states the identity the whole method
rests on — dividend equals divisor times quotient plus remainder — which is
also why the multiply-back check works.

The watch-out box names the two errors that cost the most: subtracting only
the first term of the product, and misjudging when to stop.
