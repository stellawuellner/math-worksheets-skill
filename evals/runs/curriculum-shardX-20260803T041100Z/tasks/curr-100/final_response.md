# Graphs, Line Plots, and Shape Sorting (Grade 2–3)

Three PDFs are ready.

- **Worksheet** (`ws_datashapes_curr100.pdf`, 5 pages) — 12 problems in an
  interleaved-synthesis format. Three shared displays sit above the problem
  list so no problem carries its own labelled figure: **Graph A** (a bar graph
  of books read by four students), **Line Plot B** (twelve pencil lengths in
  inches), and **Shape Set C** (six unlabelled shapes P–U). The directions box
  tells the student to decide *what the question wants* — read one bar, add
  every bar, compare two, or sort shapes first — before writing anything.
  Problems 1–4 are the blocked warm-up (read one bar, add the bars, read one
  stack, add the stacks); after that the four methods rotate, with no
  same-method run longer than two. Problem 5 makes the student classify the six
  shapes and build a tally chart, problem 6 asks for the spread of the pencil
  lengths, problem 8 is an open "why is Dev wrong" about four-sided shapes,
  problem 11 compares the distance around a square with the distance around a
  rectangle, and problem 12 adds a seventh shape and asks whether more than half
  the set now has four sides.
- **Answer key** (`ak_datashapes_curr100.pdf`, 3 pages) — the generated
  quick-answer bank, then a worked solution per problem showing which numbers
  were used and why. Five problems carry a "common wrong answer" note naming
  the exact number a specific misconception produces (26 from skipping a bar,
  10 from starting the X-count at the second label, 1 inch from reading the
  tallest stack as the longest pencil, 17 from adding instead of comparing,
  13 cm from giving a rectangle only one length and one width).
- **Study guide** (`ss_datashapes_curr100.pdf`, 2 pages) — four sections
  matching the four worksheet skills (reading a bar graph, reading a line plot,
  comparing and measuring a data set, sorting shapes by sides and corners). Each
  has a rule box, a worked example whose first step says *why* that method
  applies, and a try-it with the answer printed upside down inside the box.

## Verification

14 of the 16 checks are machine-verified with SymPy: 9 `read_data` checks
(value / total / difference queries against the same data arrays that draw the
bar graph and the line plot, so the display and the answer cannot disagree),
2 `stats` checks (range and mode of the twelve pencil lengths), and 3 `eval`
checks (counting the X marks past 4 inches, the perimeter comparison, and the
seventh-shape count). Problem 5 carries four verify entries — one per row of
the tally chart — under one problem id. Three answers carry a verified
measurement unit (`inches`, `inches`, `cm`) bound to the sheet's
`\answerline` and to the key's boxed answer in both directions.

Two items are labelled for manual review and the key says so at the point of
use:

- problem 8 — "explain why *every shape with 4 sides is a square* is wrong".
  A written explanation; the key gives a full model answer and tells the grader
  what to credit.
- problem 12(b) — "is more than half of the set now four-sided? use numbers".
  Part (a) (the count, 5) is machine-checked; the reasoning is prose.

Both are encoded as `{"type": "manual", ...}` rather than claimed as verified,
which is why the build exits 2. All 8 study-guide items (4 worked examples +
4 try-its) are fully machine-verified, and each of the four worksheet facets
has a matching worked example.

Five misconception traps are declared and machine-proved distinguishable from
the correct answers; the key prints each as a named wrong answer.

**Standards used:** `3.MD` for the data-display problems (row "Measurement &
data (length, mass, time) | 2.MD / 3.MD"), `3.G.A` for the shape-property
problems (row "Shapes & attributes | K.G / 1.G / 2.G / 3.G.A"), and
`3.MD.D.8` for the perimeter comparison (row "Area & perimeter | 3.MD.C.7 /
3.MD.D.8") — each taken verbatim from `references/standards-map.md`.

## Build

All 21 gates green (exit 2 for the two declared manual items). The first build
passed every gate; two later compiles were cosmetic only — the bar graph's
value label for the first bar was being rotated into the y-axis by pgfplots'
auto-placement, fixed by giving the axis explicit numeric x limits, and the
line plot was widened so the stacks of X marks read cleanly. Page counts:
worksheet 5 (budget 6), answer key 3 (budget 6), study guide 2 against its hard
2-page cap.
