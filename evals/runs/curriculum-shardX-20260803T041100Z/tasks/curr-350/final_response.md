# Compass-and-Straightedge Constructions — High School Geometry

Three documents, all compiled and gated: a 10-problem student worksheet, a full
step-by-step answer key, and a 2-page study guide.

## What is on the worksheet

Ten problems on **planning classical compass-straightedge constructions and
justifications**. All ten are about constructions; the sheet separates the three things a
student actually has to be able to do with one:

- **plan-the-construction** (3 problems) — write the construction as a numbered list where
  every arc states its centre, whether the opening changed, and what the new point is
  called: perpendicular bisector, angle bisector, and a parallel through a point by
  copying an angle;
- **justify-the-construction** (3 problems) — the SSS/CPCTC argument for the perpendicular
  bisector, the definition-of-a-circle argument for the equilateral triangle, and the
  synthesis challenge (the quarter point, plus why repeated bisection can never trisect);
- **check-on-coordinates** (4 problems) — a construction's output is handed back and the
  student names the property it promised, then tests it with the distance formula:
  equidistance on a perpendicular bisector, side-equals-radius on an inscribed hexagon,
  congruence of a copied segment, and the three equal distances at a circumcentre.

A value-free reference panel (segment, angle, line-and-point, circle — letters only, no
measurements) sits with the directions before problem 1. Two-problem warm-up, then
interleaved; the longest same-facet run after the warm-up is 3. Difficulty ramps
1, 2, 2, 3, 3, 3, 3, 4, 4, 5 with no drops. Construction and proof problems carry
`\noansline`: their worked product is the answer, so a single answer blank would be
misleading.

## What was verified, and what is flagged manual

- **4 of 10 problems (8 checks) machine-verified** by SymPy, all `distance`: 7.07 twice on
  the perpendicular-bisector check, 10 on the hexagon side, 10 twice on the segment copy,
  and 5 three times on the circumcentre. Problems 3, 7 and 9 each carry several verify
  entries under one id, one per distance the property requires, with identical difficulty.
- **6 flagged manual** (problems 1, 2, 4, 6, 8, 10): three construction plans, two
  justifications, and the synthesis. These are the honest encoding — a construction plan
  and a congruence proof have no single value a CAS can recompute, and the suite's own
  verification targets for this task are `distance` and `manual`. The build exits 2 with
  all six listed. The answer key gives each one a full-credit plan or proof plus an
  explicit grading note (what must be present, and what a common non-answer looks like),
  so a human marker has something concrete to mark against.
- **2 misconception traps declared and machine-checked as distinguishable**: adding the
  coordinate differences instead of using the distance formula (problem 3 → 8), and
  measuring from the midpoint of a side instead of from the constructed circumcentre
  (problem 9 → 7.21). Both print in the key's "Common wrong answers" block.

The study guide has one section per facet (rule box → worked example → try-it), 6 boxes: 2
machine-verified (`distance`) and 4 manual — the plan and justification examples, each
paired with a manual try-it, which is the one case the study-guide gate permits a manual
try-it.

## Standards

Every problem is tagged `HSG-CO.A–HSG-CO.D`, the "Congruence: transformations, triangle
congruence, proofs" row of `references/standards-map.md`, copied verbatim including the
en-dash. No gap here.

## Gate result

`BUILD PASSED`, exit 2 with the six manual-review items. Worksheet 7 pages (budget 7),
answer key 5 (budget 7), study guide 2 (cap 2). Prose consistency 100% on both the
worksheet and the study guide.

**Two things failed before the passing run, both caught by `verify.py` rather than a
compile gate.** (1) The two perpendicular-bisector distances are $5\sqrt{2}$, and
`expected: 7.07` with no tolerance was rejected as a mismatch — fixed by declaring
`"tol": 0.01`, which is inside the cap. (2) The facet-interleave check counts *entries*,
not problems, so the circumcentre problem's three `distance` entries plus the next
problem read as a run of four `check-on-coordinates` in the post-warm-up window. Fixed by
reordering the sheet so the hexagon check comes earlier and a justification problem sits
between the multi-entry checks, not by deleting a check.
