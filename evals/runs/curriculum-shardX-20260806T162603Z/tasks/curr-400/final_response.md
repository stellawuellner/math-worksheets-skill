# Modeling Loci and Intersections with Conic Sections — three PDFs

A 12-problem Algebra 2 synthesis review, plus the worked answer key and a
two-page study guide.

| File | What it is |
|---|---|
| `ss_conicloci_curr400.pdf` | Study guide (2 pages) |
| `ws_conicloci_curr400.pdf` | Student worksheet, 12 problems (6 pages) |
| `ak_conicloci_curr400.pdf` | Step-by-step answer key (4 pages) |

**How the sheet is arranged.** Problems 1–3 are a short warm-up, one on each
idea and labelled as such in the directions. From problem 4 on the three ideas
are shuffled, so the student has to decide which tool a problem wants before
picking up a pencil. Difficulty runs 1 to 5 and the last problem is the
synthesis challenge.

The three interleaved strands:

* **A circle from a distance condition** (#1, #4, #7, #10) — the locus problems.
  #7 is the good one: "twice as far from A as from B" produces a circle centred
  at neither point and at neither midpoint. #10 uses a sum-of-squared-distances
  condition in which both fixed points cancel out entirely.
* **Parabola from focus and directrix** (#2, #5, #9) — the equidistance
  definition, not just the formula. #5 has the focal chord come out at exactly
  |4p|; #9 asks for the locus argument in words.
* **Conic intersections** (#3, #6, #8, #11, #12) — parabola/line, circle/line,
  and circle/parabola with four solutions. #12 asks for the values of k that
  make a line tangent to a circle, via the discriminant.

Everything stays inside Algebra 2: no trigonometry, no calculus, no rotated
conics, no ellipse or hyperbola standard forms.

**How much is machine-checked — honestly.** There are 17 responses across the 12
problems. **14 were recomputed with SymPy** — every simplified locus equation,
every radius, and every intersection set, including all four points of #11
(the verifier confirms the solution set is complete, not just that the listed
points work). **3 are instructor-judged** and marked `---` in the Quick Answers
bank: #9(b), #10(b) and #12(b), which ask for arguments rather than values. The
key's "What is verified" note names those three.

Each of the three carries a grading note. On #9(b), for example, a student who
substitutes into y² = 8x has checked the algebra rather than the equidistance
definition the question asked about, and the note says that earns no credit for
that part.

All six study-guide items are fully machine-verified.
