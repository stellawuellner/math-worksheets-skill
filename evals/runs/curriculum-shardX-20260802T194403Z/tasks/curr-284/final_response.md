# Sign Errors in Parabola Transformations — Algebra 1 error analysis

Three PDFs are ready:

- **Worksheet** — `ws_parabola_curr284.pdf` (4 pages, 8 problems)
- **Answer key** — `ak_parabola_curr284.pdf` (3 pages, with a quick-answer bank and a
  machine-checked "common wrong answers" list)
- **Study guide** — `ss_parabola_curr284.pdf` (2 pages, 3 skill sections)

## What the worksheet does

Everything on the sheet turns on one idea, stated in a box at the top: in
`y = a(x − h)² + k` the vertex sits at the `x` that makes the squared factor **zero**, so
the horizontal shift runs opposite the printed sign, and a negative `a` reflects the
parabola without moving it.

The eight problems interleave three skills:

- **vertex-from-form** (1, 3) — locate the vertex and the x-intercepts from vertex form
- **transform-to-equation** (2, 5, 7) — write the equation from a description (left/right,
  reflection, stretch) and then test your own equation by substituting
- **find-and-fix** (4, 6, 8) — diagnose a planted sign error

Problems 2, 5 and 7 are built so the sign choice is *load-bearing*: the student writes the
equation and then evaluates it at a point where a flipped sign gives a visibly different
number, so a wrong direction cannot hide.

Three find-and-fix items, exceeding the two requested:

- **Problem 4** — Jamal reports a maximum of −61 for `y = −(x − 4)² + 3` because he used
  `x = −4`.
- **Problem 6** — Mia calls `(x + 5)` a shift right and reports a minimum of 96.
- **Problem 8** — an open study-card audit: three sign rules, exactly one correct; the
  student must label each, explain why, and rewrite the wrong ones.

Difficulty ramps 1, 2, 2, 3, 3, 3, 4, 5.

## Verification

- **7 of 8 problems machine-verified** — vertex values as `eval` at the true vertex,
  x-intercepts as `zeros`.
- **5 declared misconception traps**, all machine-checked to be values the problem's own
  check rejects: 41 (read `x − 3` as vertex `−3`), 142 (wrote `(x − 6)²` for a left shift),
  −61 (substituted `x = −4`), 16 (dropped the reflection), 96 (read `x + 5` as right 5).
  These print in the key's "common wrong answers" block, so the grader sees *which*
  misreading produced each wrong number rather than just marking it wrong.
- **1 problem flagged manual** — problem 8 is written reasoning about three rules, so it is
  declared `{"type": "manual"}`. The key supplies a model answer for each rule plus an
  explicit full-credit standard (naming R1 and R3 as wrong is not enough; the explanation
  must appeal to what makes the parentheses zero, and to `a` scaling outputs rather than
  inputs). Build result: `BUILD PASSED — 1 verification run flagged manual-review items`.

## Study guide

Three sections matching the three worksheet skills. Section 3 gives a three-check audit
routine for someone else's work — the thing this worksheet actually asks for — and its
worked example and try-it are themselves find-and-fix items with verified traps (139 and
58). The watch-out box names why these errors survive: a wrong `h` still produces a real
point on the parabola, just not the vertex.
