# Classifying Quadrilaterals from Defining Properties — High School Geometry

Three PDFs are ready: the student worksheet, a full step-by-step answer key,
and a two-page study guide.

## What the worksheet covers

Eight problems, and every one of them turns on the same question: *what name do
these properties force?* The algebra is there to make the classification pay
off — a student who names the shape wrong picks the wrong property and cannot
finish. Each problem carries its own marked figure.

1. **Naming from the marks** (problems 1, 2, 3) — chevrons for parallel, ticks
   for congruent, a small square for a right angle. Problem 2 is deliberately
   unmarked: the honest answer is that nothing beyond "quadrilateral" is
   forced, and only the $360^\circ$ angle sum is available. Recognising when
   *not* to classify is part of the skill.
2. **Naming from the diagonals** (4, 5) — the diagonal tests are a second,
   independent route into the same families: bisecting gives a parallelogram,
   bisecting plus congruent gives a rectangle, bisecting plus perpendicular
   gives a rhombus.
3. **Naming from coordinates** (6) — slopes decide parallel and perpendicular,
   distances decide congruent. This one looks like a rectangle and turns out to
   be a square, which is the point.
4. **Justifying** (7, 8) — an always/sometimes/never on "is a rhombus a
   rectangle", and a proof that one pair of sides both congruent and parallel
   forces a parallelogram.

Two figures are marked *not to scale* on purpose, so the reasoning has to come
from the marks rather than from how the drawing looks.

## What was verified

Six of the eight problems have machine-checkable answers, and all ten of their
individual checks were recomputed by SymPy before anything was typeset — the
four solve-for-$x$ equations, the back-substituted diagonal length in problem 4,
and the two slopes plus two distances in problem 6. The answer key was then
bound to that verified data problem by problem, so no printed answer can drift
from the value that was checked.

Problems 7 and 8 are open written arguments, so they are **flagged for manual
review** — a justification cannot be machine-checked. The key gives a full model
answer for each, including what a full-credit response has to contain and the
common shortfall (answering "never" on problem 7 forgets the square; asserting
the parallelogram conclusion in problem 8 without naming reasons).

## The study guide

Two pages, three sections — reading the marks, reading the diagonals, reading
coordinates — each with a rule box, a worked example (two of them with their own
figure), and a try-it whose answer prints upside down inside the box. The
definition ladder in the first box is the piece worth keeping in front of the
student: each family adds exactly one condition to the one above it, which is
what makes "most specific" a decidable question.

## Notes

The grade level is not printed on the worksheet or the study guide by design —
it appears on the answer key, along with a generated curriculum section listing
the standards covered (HSG-CO.A–HSG-CO.D for the classification work,
HSG-GPE.B.4–B.7 for the coordinate problem) and the difficulty range.
