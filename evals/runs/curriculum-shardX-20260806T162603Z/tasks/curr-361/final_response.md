# Factoring Cubes and Higher Degrees — Algebra 2 concept set

Three PDFs are ready:

- **`ss_cubefactor_curr361.pdf` — Skills Summary (2 pages).** Three sections
  with a rule box, a worked example and a try-it: the two cube patterns (with
  the sign rule spelled out and the cubes 1, 8, 27, 64, 125 listed), factoring
  four terms by grouping, and recognising a quadratic in disguise. The watch-out
  box carries the two decisions that decide whether an answer is *complete*:
  take out a common factor first, and split a sixth power as squares before
  cubes.
- **`ws_cubefactor_curr361.pdf` — Student worksheet (5 pages), 10 problems.**
  A pattern table at the top gives the student a lookup model — what you see,
  the pattern, the factored form — and every problem then asks for the same
  thing in the same words ("factor completely"), so the work is method choice
  rather than instruction-following. Problem 7 connects the algebra to a graph:
  factor, list the intercepts, then sketch the curve on the grid provided.
  Problem 10 closes with a repeated factor and asks why the graph touches rather
  than crosses there. Difficulty runs 1 → 5.
- **`ak_cubefactor_curr361.pdf` — Answer key (3 pages).** Each solution names
  the pattern and its $a$ and $b$ before applying it, and says explicitly when a
  leftover factor genuinely cannot be broken down further (the trinomial from a
  cube pattern, the sum of squares $x^2 + 4$) — the point students most often
  mistake for an unfinished answer. The Quick Answers bank and the curriculum
  block (HSA-SSE.B.3 for the factoring items, HSA-APR.B.3 for the two zeros-and-
  graphs items) sit at the top.

## What is verified, and what is not

The set carries **14 declared responses across 10 problems. 12 are machine
checked** — every factorisation was confirmed by SymPy as an identity with the
original expression, and the two zero-sets were computed independently rather
than read off the factors. The study guide's three worked examples and three
try-its are verified the same way.

**2 responses are instructor-judged**, printed as `---` in the key:

- **Problem 7(c)** — sketching the quartic. A drawn curve is not machine
  checkable; the key lists the five features a correct sketch must have
  (four crossings at the listed intercepts, both ends rising) and tells you to
  grade the drawing against the intercepts the student wrote, so the sketch is
  scored separately from the factoring.
- **Problem 10(c)** — explaining why the graph touches the axis at the repeated
  zero. The key requires the multiplicity argument, or a sign test either side
  of the zero; naming the repeated factor with no statement about the graph
  earns nothing.

## Notes

- No misconception traps are declared. A factorisation has no single comparable
  value for the trap mechanism to measure, so the two classic errors are
  targeted structurally instead: problem 5 is not a difference of cubes until
  the common factor comes out, and problem 9 gives the wrong (incomplete) answer
  to anyone who reaches for cubes before squares. Both are called out in the key
  and in the study guide's watch-out box.
- The grade level appears on the answer key only.
