# Multi-Theorem Circle Configurations — High-School Geometry

Three PDFs are ready:

- **`ws_circles_curr340.pdf`** — the student worksheet, 10 problems, 6 pages.
- **`ak_circles_curr340.pdf`** — the full step-by-step answer key, 3 pages.
- **`ss_circles_curr340.pdf`** — a 2-page skills summary.

## What the worksheet covers

The focus is configurations that need **more than one theorem**. Four families are
interleaved after a short warm-up, so the student has to decide which theorem opens
the problem rather than apply the same one ten times:

1. **Inscribed and central angles** (problems 1, 2, 6) — inscribed-angle theorem,
   cyclic quadrilaterals, and the angle in a semicircle.
2. **Arcs and sectors** (3, 5, 9) — arc length, sector area, and a circular segment.
3. **Segment relationships** (4, 8) — intersecting chords, and tangent-secant power
   of a point.
4. **Circle equations** (7, 10) — completing the square for the centre and radius.

Six of the ten problems chain two theorems together. Problem 3 needs the
inscribed-angle theorem *before* the arc-length formula; problem 6 needs the angle in
a semicircle *before* the triangle sum; problem 9 needs the sector formula *and* the
triangle area; problem 10 needs completing the square *before* the sector formula.
The answer key names each theorem beside the line where it is used.

Each configuration problem carries its own diagram. The diagrams are deliberately
**value-free** — they show the points, chords and tangents with letter labels only,
and every measurement lives in the words of the problem. That prevents the commonest
worksheet defect, where a labelled figure sitting between two problems gets applied
to the wrong one.

## What was verified

Every machine-checkable answer was recomputed with SymPy before the PDFs were built:
17 checks across the 10 problems (the multi-part problems carry one check per part —
the centre coordinates, the radius and the intercepts of problem 7 are checked
separately, not as one lump). All 17 passed.

One **misconception trap** is declared and machine-checked: on problem 6, a student
who forgets that an angle inscribed in a semicircle is a right angle gets 146°
instead of 56°. That value is printed in the key's **Common wrong answers** block, so
the specific missing theorem is diagnosable from the wrong answer alone.

Answer units are verified in both directions — the unit printed on the worksheet's
answer line (degrees, cm, cm², m, m²) has to match the unit inside the key's boxed
answer and the verification data.

**Flagged for manual review (1 item):** problem 10(c) asks the student to explain
*why* the watered region is that fraction of the fountain's area. That is genuinely
open reasoning, so it is labelled for a human to read; the key carries a full model
answer.

## The study guide

Four sections — inscribed/central angles, arc length and sector area, chords and
tangents and secants, and the equation of a circle. Each has the rules stated
compactly, one worked example whose first line says *why* that theorem is the one to
use, and a try-it problem with the answer printed upside down.
