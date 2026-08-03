# Compositions of rigid motions and symmetry — Geometry practice set

Three PDFs are ready:

- **Study guide** — `ss_transformations_curr347.pdf` (2 pages)
- **Worksheet** — `ws_transformations_curr347.pdf` (6 pages, 10 problems)
- **Answer key** — `ak_transformations_curr347.pdf` (5 pages)

## What's on the worksheet

Ten problems that build one argument in three stages. Every problem has its own
coordinate grid (or figure) to work on.

- **Problems 1–3 — carry out a composition.** A point, then a segment, then a
  triangle, each through a two-step composition. Problems 2 and 3 close with a
  distance or midpoint calculation on the image, so the student proves for
  themselves that the rigid motion left the length alone.
- **Problems 4–6 — name the single transformation.** Two reflections in parallel
  mirrors (a translation of twice the gap), two in perpendicular mirrors (a half
  turn about the crossing point), and two in mirrors meeting at 45° (a quarter
  turn). Each asks for a written description, and each has a computed part —
  distance travelled, midpoint, or the areas before and after — that pins the
  image down before the description is attempted.
- **Problem 7** returns to applying a composition and asks whether the two steps
  can be swapped. They cannot, and the key shows the counterexample.
- **Problems 8–10 — symmetry.** The lines and rotational symmetry of a regular
  hexagon; why a parallelogram has a half turn but no line of symmetry (using the
  shared midpoint of its diagonals); and finally a proof-style question asking why
  two perpendicular mirrors *always* compose to a half turn about their crossing
  point.

Difficulty ramps 1 → 5. All ten problems sit inside the requested focus.

## What was verified

Seventeen separate checks were run through the skill's SymPy verification gate
and all passed: the image coordinates in problems 1 and 7, the two equal
segment lengths in problem 2, the length and midpoint in problem 3, the distance
travelled in problem 4, the midpoints in problems 5, 9 and 10, the two triangle
areas in problem 6 (equal, as an isometry requires), and both symmetry counts for
the regular hexagon. The answer key's boxed answers are bound to those verified
values.

Two **misconception traps** were declared and proved distinguishable: giving the
gap between the mirror lines (3) instead of the distance the point travels (6),
and giving 180° instead of 60° for the hexagon's smallest angle of rotational
symmetry — a rotation that does work, but is not the smallest one. Both print in
the key as "if they got N…" lines.

## What is flagged for manual review

Five parts of the sheet are written descriptions or justifications, labelled
`manual` in the verification data and reported as manual-review items by the
build. No machine graded them:

- **4(c), 5(c), 6(c)** — name the single transformation equivalent to each
  composition.
- **9(c)** — why the parallelogram has rotational symmetry of order 2 but no line
  of symmetry.
- **10(c)** — why perpendicular mirrors always compose to a half turn.

Each has a model answer in the key plus an explicit marking guide. Two of those
guides are worth reading before grading: on 6(c) a 90° *counterclockwise* answer
is genuinely wrong rather than a slip (it is the composition taken in the other
order), and on 10(c) re-checking the single point from part (a) does not earn full
credit, because the question asks for an argument covering every point.

Everything computational on the sheet is machine-verified.
