Here are the three PDFs on converting between rectangular and polar
coordinates.

**Worksheet — `ws_polar_curr431.pdf` (6 pages, 10 problems).** Every problem is
a conversion, and every one comes with its own polar grid so the point gets
plotted before the angle gets written. That ordering is the whole point of the
sheet: the arithmetic is easy, and almost every lost mark on this topic comes
from the one step the calculator cannot do — deciding which of two angles with
the same tangent is the right one.

The set runs three ways through the same material. Polar to rectangular
(problems 1, 3, 6, 9), which is pure substitution into $x = r\cos\theta$ and
$y = r\sin\theta$, in radians and in degrees. Rectangular to polar (2, 4, 7),
where problem 7 is deliberately the mirror image of problem 2 — the same
3-4-5 triangle reflected into the third quadrant, so $r$ and the reference
angle are identical and only the quadrant differs. And the angle decision
itself (5, 8, 10): problem 8 asks your student to type the ratio into the
arctangent key, write down the $-45^\circ$ it returns, and then explain the
correction; problem 10 is the case on the $y$-axis where the tangent formula
does not exist at all. Problem 9 goes one level up and converts a polar
*equation*, $r = 4\cos\theta$, into the circle it really is.

**Answer key — `ak_polar_curr431.pdf` (3 pages).** Every problem worked in full,
with the quadrant reasoning written out rather than assumed, and a
$x^2 + y^2 = r^2$ check at the end of each conversion. Two problems carry a
"common wrong answer" note naming exactly which slip produces the number you
may see: the reference angle reported as if the point were in quadrant I
(problem 7, $53.13^\circ$), and the calculator's raw output copied without
adjustment (problem 8, $-45^\circ$). A quick-answer bank and a generated
Curriculum section sit at the top.

**Study guide — `ss_polar_curr431.pdf` (2 pages).** The four conversion facts up
front with a note on which direction needs a decision, then three sections —
polar to rectangular, rectangular to polar, and choosing the angle — each with
a rule box (including the quadrant placement rule spelled out for all four
quadrants), a worked example, and a distinct try-it with the answer printed
upside down inside the box. It closes on the two facts that cause the most
trouble: the arctangent key answers only between $-90^\circ$ and $90^\circ$, so
quadrants II and III always need a half turn added; and on the $y$-axis the
ratio $y/x$ does not exist.

**What was verified.** 22 of 24 checks were recomputed independently and passed
— every exact radical coordinate, every radius, every two-decimal angle, and
each of the "two candidate angles" solves, which were confirmed as *complete*
solution sets on $[0^\circ, 360^\circ)$ rather than just checked one root at a
time. All ten study-guide examples and try-its were verified too. Both declared
misconception traps were machine-checked to land on visibly different numbers
from the correct answers.

**Flagged for manual review (2 items):** problem 9(b), the derivation turning
$r = 4\cos\theta$ into $(x-2)^2 + y^2 = 4$ and naming the curve; and problem
10(c), the explanation of why the tangent formula fails on the $y$-axis. Both
are open derivations that no computer algebra system can grade as written, so
they are labelled rather than claimed — the key gives a complete model answer
for each, including the check that the part-(a) point satisfies the circle.
