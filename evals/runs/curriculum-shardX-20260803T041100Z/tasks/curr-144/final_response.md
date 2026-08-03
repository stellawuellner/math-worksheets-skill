# Square or Cubic? Finding the Unit Mistake — Grade 4/5

Three PDFs are ready:

- **Worksheet** (`ws_sqcube_curr144.pdf`, 4 pages) — 8 problems, every one of them about
  the same diagnosis: *how many lengths were multiplied, and does the label agree?* A
  value-free reference panel with the directions shows unit squares tiling a flat surface
  next to unit cubes filling a solid, so the vocabulary has a picture behind it.
- **Answer key** (`ak_sqcube_curr144.pdf`, 2 pages) — generated quick-answer bank
  (including a "common wrong answers" line per declared trap), then full reasoning for
  every problem: layers and rows are counted out, not just multiplied, and each solution
  ends by naming the wrong answer that problem is built to catch.
- **Study guide** (`ss_sqcube_curr144.pdf`, 2 pages) — three sections, each a rule box, a
  worked example and a distinct try-it with the answer printed upside down: read the unit
  off the formula, find and fix a squared-for-cubed mistake, convert square and cubic
  units.

## What was verified

7 of 8 problems are machine-checked with SymPy (`verify_sqcube_curr144.json`):

| # | Check | Answer |
|---|---|---|
| 1 | area 8 × 5 | 40 cm² |
| 2 | volume 8 × 5 × 3 | 120 cm³ |
| 3 | find-and-fix: cube edge 6, volume 6³ | 216 cm³ |
| 4 | surface area 6 × 4² | 96 cm² |
| 5 | square centimeter to square millimeters, 10² | 100 mm² |
| 6 | find-and-fix: cubic centimeter to cubic millimeters, 10³ | 1000 mm³ |
| 7 | find-and-fix: pool floor area 12 × 5 (depth is a distractor) | 60 m² |

Each declared unit is bound in both directions: the worksheet's answer blank prints it
and the key's boxed answer must repeat it, so a volume answered in square units cannot
pass.

**Problem 8 is flagged `manual`** — the student draws tiles on a flat rectangle and cubes
in a box and writes why two multiplied lengths give square units while three give cubic
units. That is an explanation plus a drawing, so it is labelled for manual review rather
than claimed as verified; the build exits 2 and says so. The key states what full credit
looks like and what falls short.

**Seven misconception traps are declared and machine-checked** as distinguishable, and
they print in the key's common-wrong-answers block. The important ones:

- problem 2 — 40, the base layer only (a flat area handed in as a volume);
- problem 3 — 36, the edge squared instead of cubed (the target misconception);
- problem 4 — 64, the volume handed in as surface area;
- problem 5 — 10, the length factor used once on an area;
- problem 6 — 10 *and* 100, the length factor used once, and the factor squared as if a
  cubic unit converted like a square one (both wrong answers are printed in the stem, so
  the student must diagnose two different errors);
- problem 7 — 120, the depth multiplied in and the result labelled in square meters.

Three problems (3, 6, 7) are explicit find-and-fix items — one more than requested.

Standards: every problem is tagged `4.MD / 5.MD`, taken verbatim from
`references/standards-map.md`.

## Gate chain

`BUILD PASSED` (exit 2 — one manual-review item, the open explanation). All 21 gates
green, including both verification runs, skill/facet coverage, unit binding in both
directions, the three page-budget compiles (worksheet 4, key 2, guide 2), per-problem
answer-key binding and prose consistency (worksheet 15/15; study guide 17/18, the single
flag being the intermediate 15 = 5 × 3 printed inside a worked example).
