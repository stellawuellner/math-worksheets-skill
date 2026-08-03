# Graphing basic polar curves from equations (Precalculus)

Three PDFs are ready for a precalculus student learning to graph polar curves.

**Worksheet — 12 problems, 6 pages.** Everything is in degrees on
$0^\circ \le \theta < 360^\circ$, and the four task types are interleaved after the
warm-up:

- *Evaluate r at an angle* (1, 2, 3, 5, 8) — circles, a cardioid, and two limaçons.
  Problem 5 deliberately produces $r = -2$, so the student has to confront a
  negative radius rather than assume an error.
- *Zeros of r* (4, 6, 9) — where the four-petal rose returns to the pole, the single
  cusp angle of a cardioid, and the two angles that bound a limaçon's inner loop.
- *Maximum r and orientation* (7, 10) — the three petal-tip directions of
  $r = 2\sin 3\theta$, and the one angle where $r = 4\cos\theta$ peaks, which is the
  direction the circle is offset from the pole.
- *Identify and sketch* (11, 12) — each with its own polar grid printed in the
  problem block.

Difficulty ramps 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5. Problems 11 and 12 declare extra
`workspace_cm` for the grid plus writing room rather than compressing the sheet.

**Answer key.** Every solution shows the equation being solved, not just the angle
list — including the step that actually causes errors: solving for $k\theta$ across
the widened window *before* dividing by $k$, which is why $4\sin 2\theta = 0$ has four
solutions and not two. Each answer is then connected back to the picture (four
petals, the cusp, the inner loop, the offset direction). Problem 5 carries a declared
misconception trap — taking $\cos 180^\circ = +1$ and getting 6 — printed in the key's
quick-answer bank.

**Flagged for manual review: problems 11 and 12.** Problem 11 is a hand-drawn
cardioid sketch and problem 12 asks the student to name the family, sketch it, and
justify the inner loop from the ratio of the constant to the coefficient. Neither is
CAS-checkable, so both are declared `manual`; the build exits 2 with two manual items,
which is the correct encoding. The key gives explicit grading checklists for both
(quadrantal values, symmetry, cusp placement; and for 12 the $a/b < 1$ test, the
pole-crossing evidence, and the required sketch features).

**Study guide (2 pages).** Three skill sections, each with a rule box, a worked
example, and a distinct upside-down try-it:

1. Evaluate a polar equation at an angle (including how to plot a negative $r$).
2. Pole crossings and maximum radius — and the solve-for-$k\theta$-first rule.
3. Identify the family (circle / rose / limaçon-cardioid), then sketch from four
   values plus the zeros and the maximum.

**Verification.** 10 of the 12 worksheet answers are machine-checked with SymPy
(`eval` and `solve_interval` checks, the latter confirming the *complete* root set on
the interval rather than a sampled list); the other two are the declared sketches. All
6 study-guide results are machine-checked. The full gate chain is green, including
per-problem binding of every printed boxed answer to its verified value.

**Standards note.** `references/standards-map.md` has no row for polar or parametric
coordinate systems. The task's `standard_refs` names `HSF-TF`, so every problem is
tagged `HSF-TF.A.2, HSF-TF.B.5` — the trig-functions row's code string exactly as that
file writes it, which is honest for curves defined by $\sin$ and $\cos$ of $\theta$. No
code was invented. A dedicated polar/parametric row would be a reasonable addition to
the map.
