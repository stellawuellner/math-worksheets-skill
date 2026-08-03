Here are the three PDFs on slope fields.

**Worksheet — `ws_slopefields_curr481.pdf` (5 pages, 8 problems).** Every
problem is about reading or drawing a slope field, and each one comes with its
own picture: four problems give a blank lattice grid to build the field on,
four print a finished field to read. The set works through three moves in turn
and then mixes them — computing the slope at a lattice point by substitution
(problems 1, 2, 7), reading structure off a printed field and identifying which
equation made it (3, 5), and sketching the solution curve through a given point
then confirming it with an antiderivative (4, 6, 8). Problem 5 hands back the
same equation the student started building in problem 1, now fully drawn, so
they can see their own four segments inside the finished picture. The closing
problem (8) is the AP-style one: find the equilibrium solution, sketch the
curves above and below it, and explain from the field alone why neither can
ever reach it.

**Answer key — `ak_slopefields_curr481.pdf` (4 pages).** Every problem worked
in full — substitution first, then the structural reading ("no $x$ on the right,
so each row is one repeated segment"), then the algebra where there is any. The
top of the key carries a quick-answer bank for fast grading plus a Curriculum
section built from the tagged standards and difficulty range. Two problems
carry a "common wrong answer" note: subtracting in the wrong order on problem 1,
and evaluating the antiderivative without ever using the initial condition on
problem 6.

**Study guide — `ss_slopefields_curr481.pdf` (2 pages).** An opening box on
what a slope field actually is and the two structural tells (no $y$ means
columns repeat; no $x$ means rows repeat and roots give constant solutions),
then three teaching sections: slope at a lattice point (with a small printed
field and the example point marked on it), finding the zero-slope isocline, and
following the flow from a given point. Each section has a rule box, a worked
example with the strategy named before any computation, and a separate try-it
whose answer is printed upside down inside the box. It ends with the two
mistakes that cost the most marks: reading the field's number as a height
instead of a slope, and letting a curve cross an equilibrium line.

**What was verified.** 27 of the 30 checks were recomputed by SymPy and passed:
every lattice-point slope, every zero-slope isocline (solved symbolically, so
"$y = x$" and "$y = -x$" are checked as equations, not as text), both
antiderivatives, and the two-decimal value of the particular solution in
problem 6 — plus all six study-guide examples and try-its. Both declared
misconception traps were machine-checked to land on a visibly different number
from the correct answer.

**Flagged for manual review (3 items), all in the parts that ask for words or a
drawing:** problem 3(c), the sentence naming the equation and ruling the other
two out; problem 5(c), describing what the solution curve does for large $x$;
and problem 8(c), the two sketches plus the argument for why a curve cannot
reach the equilibrium. No computer algebra system can grade those, so they are
labelled rather than claimed — the answer key spells out what full credit
contains for each.
