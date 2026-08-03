# Coordinate Plane, Line Plots, and Numerical Patterns — Grades 4–5

Three documents, all compiled and gated: a 12-problem student worksheet, a full
step-by-step answer key, and a 2-page study guide.

## What is on the worksheet

Twelve problems on **using coordinate, data, and pattern information in combined tasks**.
Every problem needs two of the three strands at once, which is the point of the focus:

- **pattern-pairs-on-the-grid** (4 problems) — two number patterns run from the same
  start, matching terms are written as ordered pairs, and the multiplier that relates the
  two patterns is found from the step sizes;
- **line-plot-to-summary** (4 problems) — Line Plot A is read for a single column, a
  mean, a median, and a class total, with each answer also written as an ordered pair;
- **data-pattern-combined** (4 problems) — a rule stated in words is applied to a number
  the student first had to read or compute from the plot.

A two-problem blocked warm-up, then interleaved: the longest same-subskill run after the
warm-up is 2. Difficulty ramps 1, 2, 1, 2, 2, 3, 3, 3, 3, 4, 4, 5, with the only step down
being a single level. Problem 12 is the synthesis challenge: a growth pattern built on top
of the class total the student computed in problem 10, tabulated, written as ordered
pairs, and described as it would appear plotted.

**Line Plot A** and the blank **Grid A** sit in a boxed panel with the directions, before
problem 1, and are shared by several problems. Keeping them there rather than beside any
one problem is deliberate: a display carrying numbers next to problem *n* is read by a
student working problem *n+1*, so shared data belongs outside the problem list.

## What was verified, and what is flagged manual

- **10 of 12 machine-verified** by SymPy: 6 `eval` pattern/rule computations (40, 18, 35,
  6, 60, 8), 2 `stats` summaries (mean 4, median 4), and 2 `read_data` reads (a column
  count of 2, a class total of 48).
- **2 flagged manual** (problems 6 and 12): plotting four ordered pairs on Grid A with a
  written description of the relationship, and the synthesis table-plus-description. Both
  ask for a drawing and prose, which no CAS can recompute, so both are declared
  `{"type": "manual"}` and the build exits 2 listing them.
- **4 misconception traps declared and machine-checked as distinguishable**: dividing by
  the number of plot columns instead of the number of students (problem 4 → 8), using the
  tallest stack instead of the largest value (problem 5 → 15), pairing two patterns one
  step out of step (problem 9 → 45), and counting the ×-marks instead of adding the books
  (problem 10 → 12). All four print in the answer key's "Common wrong answers" block.

The study guide has one section per subskill (rule box → worked example → try-it), 6
boxes, all 6 machine-verified.

## Standards — one honest gap

`references/standards-map.md` has **no row for the grade-5 coordinate plane** (5.G.A.1 /
5.G.A.2, and 5.OA.B.3 for graphing ordered pairs generated from two patterns). Rather than
invent a code, the pattern-and-grid problems are tagged with the map's
`4.OA.B.4 / 4.OA.C.5` ("Factors, multiples, primes, number patterns") row, which really
does cover the checked mathematics in those problems — the pattern rule — while the
coordinate-plane half of them goes untagged. Line-plot and data problems are tagged
`4.MD / 5.MD`, the map's grades 4–5 measurement-and-data row, which is where 5.MD.B.2
lives. Both code strings are copied verbatim from the map.

## Gate result

`BUILD PASSED`, exit 2 with the two manual items. Worksheet 7 pages (budget 7), answer key
4 (budget 7), study guide 2 (cap 2).

**Two gates failed on the first attempt.** (1) `compile-ws`: the sheet ran 7 pages against
a 6-page ceiling, because the page budget is computed from the JSON and could not see the
hand-built display panel. Fixed by declaring the space that panel really is —
problem 6's plotting work happens on Grid A, so its `workspace_cm` is 12, and problem 3
declares the 5 cm it actually gets — rather than by shrinking anyone's work space.
(2) `compile-ak`: a 6.8 pt overfull line, from a long sentence of prose set inside an
unbreakable `\ans{}` box on problem 6. Fixed by boxing `open response` and moving the
grading note outside the box.
