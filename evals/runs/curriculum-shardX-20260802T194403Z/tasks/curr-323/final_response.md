# Right Triangles in Elevation and Depression Problems — High School Geometry

Three PDFs are ready:

- **Study guide** (`ss_elevation_curr323.pdf`, 2 pages) — read this first.
- **Worksheet** (`ws_elevation_curr323.pdf`, 4 pages, 8 problems).
- **Answer key** (`ak_elevation_curr323.pdf`, 3 pages) — full setup-and-solve for every problem.

## What the worksheet does

Seven of the eight problems are genuine elevation or depression applications
(the eighth, problem 4, is a write-the-ratio setup inside the same surveying
context). Each states its givens and units explicitly and asks one question with
a stated rounding, so there is no ambiguity about what to write on the answer
line. The sheet rotates deliberately between four decisions rather than drilling
one:

- **finding a side from an elevation angle** (1, 5, 7). Problems 1 and 5 read
  almost identically, and that is the point: in 1 the given length is measured
  along the ground (adjacent → tangent), in 5 it is a taut kite string
  (hypotenuse → sine). Choosing the wrong one is the most common error in this
  unit.
- **finding an angle** (3, 4) — inverse tangent for the ramp, and the exact
  reduced ratio for the tower.
- **finding a side from a depression angle** (2, 6) — where the angle starts
  *outside* the triangle and has to be transferred to the object.
- **two triangles sharing a leg** (8) — the closing synthesis: two boats sighted
  from one cliff, solved as two triangles whose horizontal distances are
  subtracted. Problem 7 is the other trap: a measurement (eye height 1.6 m) that
  belongs *outside* the trig ratio, not inside it.

A value-free reference diagram printed with the directions defines how both
angles are measured; no problem carries its own labelled figure, so no figure can
be misread as belonging to a neighbouring problem.

## What was verified

**All 8 problems were machine-verified** — nothing here is flagged for manual
review. Every answer was recomputed with SymPy from the givens (problem 5 through
the triangle solver, from `C = 90°, A = 28°, c = 150 ft`), and each printed
boxed answer in the key was bound back to the verified value at its printed
precision, unit included.

**Five misconception traps were declared and machine-checked** — sine used where
tangent belongs, multiplying by the tangent instead of dividing (twice),
forgetting to add the eye height, and subtracting the two depression angles
before working the triangles. Each was proved distinguishably wrong, and each
prints in the key's "Common wrong answers" block with the number a student would
have written, so a wrong paper identifies its own error.

Every problem also declares its answer unit (ft, m, degrees); the sheet prints a
matching unit on each answer line and the key prints the same unit inside the box,
both directions gate-checked.

## Study guide

Four sections, one per skill the worksheet tests, each with a rule box, a worked
example whose first step explains *why* that ratio, and a try-it with the answer
upside down inside the box. The depression section is the one worth reading twice:
it shows why the angle of depression at the observer equals the angle of elevation
at the object, which is the step that turns every depression problem into an
ordinary one.

## Gate chain

Final verdict: **BUILD PASSED — all gates green** (exit 0), covering template
shells, both verification files, skill and facet coverage, subtitle binding,
figure scope, work space, answer-unit binding in both directions, three compiles
inside their page budgets, per-problem answer-key binding, study-guide structure,
and prose/figure consistency.

One gate failed on the first attempt: the study guide overran a line by 4.7 pt
(`Overfull \hbox`) in the first rule box; it was rephrased to give the line a
break point. No mathematics changed.
