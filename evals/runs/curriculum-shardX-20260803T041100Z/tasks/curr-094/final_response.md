Three PDFs are ready for a Grade 2–3 learner on area and perimeter, focused on
correcting the confusion between the two.

- **Worksheet** (8 problems, `ws_areaperim_curr094.pdf`, 4 pages) — problems 1
  and 2 deliberately use the *same* 8 cm by 3 cm card so the student sees one
  rectangle produce two different correct answers (22 cm of ribbon, 24 squares).
  Problems 3 and 4 are the find-and-fix items: Milo multiplies 6 × 4 = 24 and
  calls it a perimeter, Sara adds 9 + 2 + 9 + 2 = 22 and calls it an area — each
  asks the student to *name* which measurement was actually computed before
  redoing it. Problem 5 is the square-side trap (4 × 7 fence vs 7 × 7 soil),
  problem 6 asks the student to circle "perimeter" or "area" before computing,
  and problem 7 gives two gardens with equal perimeters and different areas, so
  the student must discover that equal fences do not mean equal space. Problem 8
  is an open task on a printed grid. Work space runs 4.5–5 cm plus the grid, and
  every problem carries an `\answerline` with its unit — cm for perimeter,
  cm²/m² for area — because the unit is the fastest self-check for this
  misconception.
- **Answer key** (`ak_areaperim_curr094.pdf`) — three or four numbered steps per
  problem, always starting by naming the deciding word in the question ("around"
  vs "cover") before any arithmetic, then the computation, then the boxed answer
  with its unit. Every find-and-fix solution states in plain words what the
  student's number really was. It carries the generated quick-answer bank and the
  generated "Common wrong answers" block (24, 22, 24, 22, 49, 60, 0), and gives a
  full model answer plus a full-credit checklist for the open item.
- **Study guide** (2 pages, `ss_areaperim_curr094.pdf`) — three skills matching
  the worksheet tags: perimeter as adding around, area as multiplying to cover,
  and deciding which one a question wants (deciding words, then a unit check).
  Each section has a rule box, a two-step worked example, and an upside-down
  try-it, plus a watch-out box on the fact that one rectangle has two different
  correct answers.

**Verification.** 7 of the 8 worksheet problems are machine-checked with SymPy
(`eval` on the perimeter, area and difference computations), and all 6
study-guide results are machine-checked. Problem 8 asks the student to draw two
rectangles and write their own sentence — genuinely open, with many correct
answers — so it is declared `{"type": "manual"}` and the build correctly exits 2
with one manual-review item. It is not described anywhere as machine-verified.
Seven planted wrong answers (24, 22, 24, 22, 49, 60 and 0) are declared
misconception traps, so the verifier proved each one is distinguishably wrong and
really is what the swapped method computes; they print in the key's "Common wrong
answers" block so a parent can diagnose from the wrong number alone.

**Standards.** Every problem is tagged `3.MD.C.7 / 3.MD.D.8`, taken verbatim from
`references/standards-map.md` ("Area & perimeter"), which is also the code the
task itself names.

**Gate-log note.** The study guide's prose report flags 14, 4, 24 and 10 — these
are the intermediate sums written inside the worked examples (7 + 7 = 14 and
2 + 2 = 4; 12 + 12 = 24 and 5 + 5 = 10), i.e. derived values rather than givens,
which that checker documents as the expected false-flag case. The worksheet
matches 16 of 16 prose numbers.
