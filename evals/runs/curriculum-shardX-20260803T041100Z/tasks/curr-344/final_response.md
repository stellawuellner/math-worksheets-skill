# Scale Factor Confusion: Linear, Square, Cubic — High School Geometry

Three PDFs are ready:

- **Worksheet** (`ws_scalefactor_curr344.pdf`, 4 pages) — 6 problems, all on one
  diagnosis: *which power of $k$ does this quantity take, and is the student running the
  rule the right way?* A value-free reference panel with the directions shows a square
  and a cube with their edges doubled, so the "four copies fit / eight copies fit" picture
  sits behind the exponents rather than the exponents being asserted.
- **Answer key** (`ak_scalefactor_curr344.pdf`, 3 pages) — generated quick-answer bank
  with a "common wrong answers" line per declared trap, then reasoning that names the rule
  before applying it and finishes with a forward check (scaling back up to confirm the
  factor), which is the habit that would have caught every planted error.
- **Study guide** (`ss_scalefactor_curr344.pdf`, 2 pages) — three sections (area by $k^2$,
  volume by $k^3$, recovering $k$ from a ratio), each with a rule box, a worked example
  whose first step names why that power applies, and a distinct try-it with the answer
  upside down inside the box.

## What was verified

5 of 6 problems are machine-checked (`verify_scalefactor_curr344.json`):

| # | Check | Answer |
|---|---|---|
| 1 | area 12 dilated by $k = 3$ | 108 cm² |
| 2 | volume 54 scaled by $k = 2$ | 432 cm³ |
| 3 | find-and-fix: area 18, ratio $5:2$ | 112.5 cm² |
| 4 | solve $9k^2 = 25$ for every root, then reject one | $k = \tfrac{5}{3}$ or $-\tfrac{5}{3}$ |
| 5 | find-and-fix: volumes 250 and 2000, linear factor | $k = 2$ |

**Problem 6 is flagged `manual`** — the student must sketch a box with doubled edges and
argue what happens to paint (surface area, $\times 4$) and to sand (volume, $\times 8$),
and why the exponent counts dimensions. That is an argument plus a drawing, so it is
labelled for manual review rather than claimed as verified; the build exits 2 and says so.
The key states exactly what full credit contains.

**Six misconception traps are declared and machine-checked** as distinguishable, printing
in the key's common-wrong-answers block:

- problem 1 — 36, the area scaled by $k$ instead of $k^2$;
- problem 2 — 108 (factor used once) and 216 (factor squared, the area rule on a volume);
- problem 3 — 45, the linear ratio applied to an area;
- problem 5 — 8 (the volume ratio reported as the scale factor) and 2.83 (a square root
  taken where a cube root belongs). Both wrong answers are printed in the stem, so the
  student diagnoses two different failures of the same rule.

Problems 3 and 5 are the two requested find-and-fix items. Problem 4 is deliberately the
algebra-facing one: the equation has two roots and the geometry rejects one, which is the
distinction the "just take the root" habit hides.

## A note on the standards code

`references/standards-map.md` has no `HSG-GMD` or `HSG-MG` row, which is where the
area/volume-ratio statements of this topic formally live. Rather than invent a code, every
problem is tagged with the map's on-grade similarity row, **`HSG-SRT.A.1–A.3,
HSG-SRT.B.4–B.5`** (dilations, scale factor, AA/SSS/SAS similarity), copied verbatim.
That row genuinely governs the dilation and scale-factor content driving these problems,
but a reader tracing area-and-volume-of-similar-solids to `HSG-GMD.A` / `HSG-MG.A` will
not find those rows in the map; adding them would be the cleaner fix.

## Gate chain

`BUILD PASSED` (exit 2 — one manual-review item). All 21 gates green: both verification
runs, skill and facet coverage, unit binding in both directions, three compiles inside
their page budgets (worksheet 4, key 3, guide 2), per-problem answer-key binding,
study-guide structure, and prose consistency at 18/18 on the worksheet and 22/22 on the
study guide.
