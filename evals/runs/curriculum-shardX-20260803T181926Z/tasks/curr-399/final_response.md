# Conic sections — finding and fixing sign and denominator errors (Algebra 2)

Three PDFs are ready: the student worksheet, a full step-by-step answer key, and
a two-page study guide.

**What the worksheet does.** Eight problems, all of them aimed at the two errors
that account for nearly every wrong answer with conics: a sign misread out of
`(x - h)` / `(y - k)`, and a denominator (or right-hand side) copied without
taking its square root.

1. Warm-up: centre and radius of `(x+4)^2 + (y-7)^2 = 36`.
2. Find and fix: Dev's circle, with two planted errors (reversed centre signs
   and a radius of 49 instead of 7).
3. Semi-axes of `x^2/25 + y^2/9 = 1`.
4. Completing the square from general form, where the constant's sign decides
   the radius.
5. Find and fix: Rae's ellipse, where the wrong denominator was used *and* the
   square root and doubling were skipped.
6. Centre and semi-major axis of a shifted ellipse.
7. Find and fix: Sam's hyperbola, where the subtracted term was used for the
   vertices and the opening direction was reversed.
8. Open task: write a circle, an ellipse and a hyperbola about one non-origin
   centre and explain how a reader tells them apart.

Difficulty ramps 1 to 5, and the last problem is deliberately open.

**What was machine-verified.** Fourteen checks across problems 1-7 were
recomputed independently with SymPy: the centres as the solution of the two
binomials set to zero, every radius and semi-axis as a square root, and the
hyperbola's vertices by solving the equation on its own axis. Twelve
misconception traps are declared and were each proved to produce a *visibly
different* number from the correct answer — that is what makes each find-and-fix
item diagnostic rather than decorative. The traps are printed in the answer key
as a "Common wrong answers" block, so when your student writes 49, or 4, or
7.21, the key tells you which specific step they took.

**What is flagged for manual review.** Problem 8 only. It asks for equations of
the student's own choosing plus a written explanation, so no checker can mark
it; the answer key gives a model answer and a short list of what a full-credit
response must contain.

**The study guide** covers the three skills the worksheet tests — circle centre
and radius, ellipse denominators, and hyperbola orientation — each with a rule
box, a worked example, and a try-it whose answer is printed upside down inside
the box. Its six worked results are verified by the same gate chain as the
worksheet.
