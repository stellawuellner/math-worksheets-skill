# Transformations with Multiple Parameters — Precalculus

Three PDFs are ready:

- **Worksheet** — `ws_transforms_curr401.pdf` (5 pages, 10 problems)
- **Answer key** — `ak_transforms_curr401.pdf` (4 pages, parameter-by-parameter reasoning)
- **Study guide** — `ss_transforms_curr401.pdf` (2 pages, 3 skill sections)

## What the worksheet does

The sheet is organised around one visual model printed at the top — a **parameter map** of

    g(x) = a · f( b(x − h) ) + k

with each slot annotated underneath (stretch/reflect, horizontal compress, shift right,
shift up) and the governing distinction stated in words: *outside* parameters act on the
output and do what they say; *inside* parameters act on the input and do the opposite, and
`h` cannot be read at all until the inside is factored into `b(x − h)`. Every problem is
meant to be read against that map. A graph of the parent function `f(x) = √x` is printed
below it and reprinted on the page where it is needed again.

Three models connect to notation across the ten problems:

- **Tabular** — problem 1 gives a chain table (`x` → `x − 3` → `f(x−3)` → `2f(x−3)` →
  `2f(x−3) − 5`) so the order of the parameters is something the student physically walks
  through rather than recalls.
- **Graphical** — problems 8 and 10 work from the printed parent graph; problem 10 supplies
  a blank grid for the sketch.
- **Symbolic/algebraic** — problems 3, 6, 7, 9 undo or refactor the parameter chain.

The three skills interleave (max run of 2): **table-transform** (1, 2, 8),
**parameters-from-equation** (3, 4, 7, 9, 10), **composition-order** (5, 6). Difficulty
ramps 1, 2, 2, 3, 3, 3, 4, 4, 4, 5.

The conceptual core shows up three times in different clothing: problem 7 asks why the
phase shift of `3sin(2x − π/3)` is π/6 and not π/3; problems 5–6 show that composing a
shift then a stretch scales the shift (2x + 8) while the other order does not (2x + 4); and
problem 10 asks why `x/2 + 1` shifts **2 units left** despite reading "+1".

## Verification

- **9 of 10 problems machine-verified**: chain evaluations as `eval` (including a
  trigonometric one at `x = 5π/12`), the refactoring identities as `equiv` (SymPy confirms
  `3sin(2x − π/3) ≡ 3sin(2(x − π/6))`), and the undo-the-parameters equations as `solve`.
  Every boxed answer in the key is bound back to its own problem's verified value.
- **1 problem flagged manual** — problem 10 is a graph sketch plus a written ordering
  argument, which no CAS can check, so it is declared `{"type": "manual"}`. The key still
  gives a complete model response: the factored inside, the four parameters with input moves
  before output moves, the image of the parent's starting point at (−2, 3), two further
  plotted points, the domain, and an explicit full-credit standard.
- Build result: `BUILD PASSED — 1 verification run flagged manual-review items (exit 2)`.

## Study guide

Opens with the same parameter map as a four-row table (each parameter, inside or outside,
its effect, and whether it does what it says), then three sections: walking one input
through the whole chain, factoring before reading a phase shift, and composition order. All
six worked examples and try-its are machine-verified. The watch-out box names the dominant
multi-parameter error — reading a shift off an unfactored inside — and gives the outside-in
order for undoing parameters when solving.
