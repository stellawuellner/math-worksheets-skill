# Exponential Equations with a Common Base — three documents

Here are the three PDFs on solving exponential equations by writing both sides
over a common base (precalculus, CCSS HSF-LE.A.4 and HSF-BF.B.5).

**Study guide** (`ss_expcommon_curr411.pdf`, 2 pages) — three sections, each a
rule box, a worked example whose first step says *why* the method applies, and a
try-it with the answer printed upside down:

1. *Equating exponents when the bases match* — including why the one-to-one
   property is what licenses dropping the bases, rather than it being a trick.
2. *Rewriting both sides over a common base* — the small-powers list, the two
   exponent laws (a power of a power multiplies, a product adds), and negative
   exponents for reciprocals.
3. *Exponential models with a common base* — divide out the starting amount
   first, read the exponent as a count of doublings or half-lives, and the honest
   limit of the method (when the ratio is not a whole power, you need logs).

**Worksheet** (`ws_expcommon_curr411.pdf`, 3 pages) — 10 problems, all on the
requested focus. The directions carry a powers table (bases 2, 3, 5) so a student
can spot the shared base. Problems 1, 2 and 4 have matching bases already; 3, 5,
6, 8 and 10 need rewriting (including a reciprocal base and a product of two
powers); 7 and 9 are a doubling model and a half-life model, the doubling one
paired with a table of counts so the algebra and the pattern are visibly the same
statement. Problem 8 is a check-the-claim item, and 10 asks for the single-power
form and the solution.

**Answer key** (`ak_expcommon_curr411.pdf`) — quick-answer bank at the top, then
a full solution per problem: the rewriting line first (which is where the work
is), then the exponent equation, then a substitution check. Problem 9 also
explains why the answer came out as a whole number of half-lives and when the
method would stop working. The curriculum section (level, standards, difficulty)
prints on this document only.

**What was machine-verified:** all 11 checks behind the 10 worksheet problems and
all 6 study-guide answers were recomputed with SymPy, which re-solved each
exponential equation from the original form — not from the exponent equation the
student is meant to produce — so a mistake in the rewriting step would have been
caught. Problem 10 was checked twice: once that $9^x \cdot 27^{x+1}$ really is
$3^{5x+3}$, and once that the equation solves to $x = \tfrac{1}{5}$. Problem 8's
verification computes the difference of the two sides at $x = -2$ and confirms it
is exactly zero. Nothing is flagged for manual review.

Two short written parts are yours to grade: the "how many half-lives, and why a
whole number" explanation in problem 9, and the statement in problem 8 of what
the difference must be if the claim holds. The key says what to accept for each.
