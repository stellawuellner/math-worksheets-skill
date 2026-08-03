# Building Bigger Shapes — Kindergarten / Grade 1

Three documents, all compiled and gated: a 10-problem student worksheet, a full
step-by-step answer key, and a 2-page study guide.

## What is on the worksheet

Ten problems on **composing larger shapes from smaller two-dimensional shapes**, all ten
inside that focus. Three subskills are interleaved after a two-problem warm-up, so the
child has to decide what a problem is asking before answering:

- **count-the-pieces** (4 problems) — how many small shapes cover the bigger one, with
  equal groups and, later, two layers of pieces (triangles inside trapezoids inside
  hexagons);
- **name-the-new-shape** (3 problems) — draw the build two identical pieces make and
  name it from its outline;
- **compare-two-builds** (3 problems) — the same hexagon or rectangle covered two ways,
  compared by the number of pieces.

Problem 10 is the synthesis challenge: one hexagon covered three different ways, ordered
from fewest pieces to most, which is where the "smaller pieces means more of them" idea
lands. Difficulty ramps 1, 1, 2, 2, 2, 3, 3, 3, 4, 5 with no drops; max same-subskill run
after the warm-up is 1.

A value-free pattern-block key sits with the directions (before problem 1) so the piece
names are shared without any figure carrying numbers into a neighbouring problem. Work
space is 5–8 cm per problem; problems 8, 9 and 10 declare extra room
(`workspace_cm` 7, 8, 7) because they need a drawn build rather than a single number.

## What was verified, and what is flagged manual

- **7 of 10 machine-verified** by SymPy: 4 `eval` piece-counts (8, 6, 12, 12) and 3
  `compare` checks (`6 > 3`, `8 < 16`, and the ordering `[2, 3, 6]`).
- **3 flagged manual** (problems 3, 6, 9): drawing a build and naming the shape, building
  two different shapes from the same two triangles, and explaining why four triangles make
  a triangle. These are drawings and an explanation — there is no answer a CAS can
  recompute, so they are declared `{"type": "manual"}` and the build exits 2 with them
  listed, which is the honest encoding rather than a fabricated check.
- **2 misconception traps declared and machine-checked as distinguishable**: adding the
  two numbers instead of making equal groups (problem 5 → 7), and counting only one of the
  two hexagons (problem 8 → 6). Both print in the answer key's "Common wrong answers"
  block.

The study guide has one section per worksheet subskill (rule box → worked example →
try-it), 6 boxes verified positionally: 4 machine-verified, 2 manual (the shape-naming
example and its try-it, manual for the same reason as the worksheet's naming problems).

## Standards

Tagged `K.G / 1.G / 2.G / 3.G.A`, the "Shapes & attributes" row of
`references/standards-map.md`, copied verbatim. The sheet itself targets the K.G / 1.G
part of that row — the map does not split the row by grade, so the whole code string is
used rather than an invented narrower one.

## Gate result

`BUILD PASSED` on the first run, exit 2 with the manual-review items above. Worksheet 5
pages (budget 6), answer key 3 (budget 6), study guide 2 (cap 2).
