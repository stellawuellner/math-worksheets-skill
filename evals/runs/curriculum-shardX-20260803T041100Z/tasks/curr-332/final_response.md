# Interior and exterior polygon angle sums (High-school Geometry)

Three PDFs are ready for a geometry student practising polygon angle sums.

**Worksheet — 10 problems, 5 pages.** A single value-free reference figure sits
with the directions (a convex pentagon $ABCDE$ with one interior angle and one
exterior angle marked, captioned "no values are shown"), so the naming convention
is visible without any figure being mistakable for a problem's givens. Four task
types are interleaved after the warm-up:

- *Interior angle sum* (1, 2, 9) — hexagon, 15-gon, and the reverse direction:
  a sum of $1980^\circ$, find $n$.
- *Missing angle inside a polygon* (5, 8) — four given angles of a pentagon, and a
  quadrilateral whose angles are in the ratio $1:2:3:4$.
- *Exterior angle sum* (4, 6, 10) — one exterior angle of a regular 12-gon, and the
  reverse: $24^\circ$ exterior implies 15 sides.
- *Regular-polygon angles* (3, 7) — one interior angle of a regular octagon, and
  $150^\circ$ interior implies 12 sides, set up from the interior sum rather than guessed.

Difficulty ramps 1, 1, 2, 2, 2, 3, 3, 3, 4, 5. Angle answers carry unit-labelled
answer lines (degrees); side-count answers deliberately do not.

**Answer key.** Each solution names the theorem before substituting, and several
carry an independent cross-check — problem 7 is solved from the interior sum and
then re-checked via the exterior angle, and problem 8 lists all four resulting
angles and confirms they total $360^\circ$.

**Flagged for manual review: problem 10** asks the student to prove that the
exterior angles of *every* convex polygon total $360^\circ$. That is open written
justification, so it is declared `manual` — the build exits 2 with one manual item,
which is the correct encoding, not a defect. The key supplies a full model argument
(interior + exterior $= 180n$, minus the interior sum $180n - 360$, leaving 360 with
the $n$-terms cancelling), the alternative "walk once around the polygon" argument,
and explicit guidance to reject a single worked example.

**Study guide (2 pages).** Three skill sections, each with a rule box, a worked
example, and a distinct upside-down try-it:

1. Interior angle sum $(n-2)180^\circ$, including running it backwards to find $n$.
2. Exterior angles total $360^\circ$ for every convex polygon.
3. Angles of a regular polygon, and the supplementary relationship between them.

A watch-out box flags the most common error: dividing $360^\circ$ by $n$ and calling
the result an interior angle.

**Verification.** 9 of the 10 worksheet answers are machine-checked with SymPy
(`solve` checks over the stated angle equations); the tenth is the declared manual
proof. All 6 study-guide results are machine-checked. The full gate chain is green,
including the declared-unit binding in both directions (sheet answer line ↔ JSON ↔
key box) and the per-problem binding of every printed boxed answer.

**Standards note.** `references/standards-map.md` has no dedicated row for polygon
interior/exterior angle sums. The task's `standard_refs` names `HSG-CO.C`, which
falls inside the map's congruence row, so every problem is tagged
`HSG-CO.A–HSG-CO.D` — the code string exactly as that file writes it. No code was
invented. A dedicated row (the polygon angle-sum theorems) would be a reasonable
addition to the map.
