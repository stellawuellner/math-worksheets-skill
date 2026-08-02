Three PDFs are ready for a Grade 3 student working on **composite rectilinear
figures** (shapes built only from rectangles, all square corners):

- **Worksheet — 12 problems, every one with its own labelled figure.** Four
  methods are interleaved after a short warm-up so the student has to *choose*
  rather than repeat: cut into rectangles and add (1, 3, 7, 12), walk around the
  edge for perimeter (2, 4, 9), fill in the missing corner and subtract (5, 8,
  11), and find a rubbed-out side length (6, 10). Difficulty ramps 1 → 5: the
  last two are challenges where a needed side is not labelled at all (11) and
  where the shape is a three-step staircase (12). Work space sits beside each
  figure, and each answer blank prints its unit (cm, cm², ft, ft²).
- **Answer key — full reasoning, not answers.** Each solution names the cut that
  was made, shows the two or three multiplications, and adds them up. Several
  problems also show the *other* method as a check (add-the-pieces vs
  subtract-the-corner), and three carry a "watch for" note naming the mistake a
  grader should expect — adding only the four outside sides on an L-shape
  (perimeter 26 instead of 34), multiplying when perimeter was asked, and using
  the step widths as heights on the staircase.
- **Study guide — 2 pages, four sections**, one per skill the worksheet tests:
  cut-and-add, subtract-the-corner, walk-around-the-perimeter, and matching
  sides for a missing length. Each section is a rule box, a worked mini-example
  with its strategy sentence first, and a try-it with the answer printed upside
  down inside the box. It closes with the area-vs-perimeter watch-out.

**Verification:** all 12 worksheet answers and all 8 study-guide answers
(4 examples + 4 try-its) were recomputed by SymPy through the build gate —
nothing is flagged manual, because every task on this sheet is a computation
rather than an open explanation. The gate chain also checked figure scope (every
problem carries its own figure, so no student can misread a neighbour's), work
space, unit binding on both the sheet and the key, and the study guide's
coverage of every tested skill and facet. Final verdict: **BUILD PASSED — all
gates green** (worksheet 6 pages, key 3, guide 2).
