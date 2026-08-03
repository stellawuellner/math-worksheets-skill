# Transformations with Multiple Parameters — Precalculus

Three PDFs are ready:

- **Worksheet** — `ws_transforms_curr401.pdf` (5 pages, **10 problems**)
- **Answer key** — `ak_transforms_curr401.pdf` (4 pages, parameter-by-parameter reasoning)
- **Study guide** — `ss_transforms_curr401.pdf` (2 pages, 3 skill sections)

## What the worksheet does

The sheet is organised around one visual model printed at the top — a **parameter map** of

$$g(x) = a \cdot f\bigl(b(x - h)\bigr) + k$$

with each slot annotated underneath (stretch/reflect, horizontal compress, shift right,
shift up) and the governing distinction stated in words: *outside* parameters act on the
output and do what they say; *inside* parameters act on the input and do the opposite, and
$h$ cannot be read at all until the inside is factored into $b(x-h)$. A value-free graph of
the parent $f(x)=\sqrt{x}$ is printed below the map and reprinted where it is needed again.

Three models connect to notation across the ten problems:

- **Tabular** — problem 1 is a chain table ($x \to x-2 \to f(x-2) \to 3f(x-2) \to
  3f(x-2)-4$) so the parameter order is something the student walks through rather than
  recalls.
- **Graphical** — problems 8 and 10 work from the printed parent graph; problem 10 supplies
  a blank grid for the sketch.
- **Symbolic** — problems 3, 6, 7, 9 undo or refactor the parameter chain.

Skills interleave with a maximum same-skill run of 2: **table-transform** (1, 2, 8),
**parameters-from-equation** (3, 4, 7, 9, 10), **composition-order** (5, 6). Difficulty
ramps 1, 2, 2, 3, 3, 3, 4, 4, 4, 5.

The conceptual core appears three times in different clothing: problem 7 asks why the phase
shift of $4\sin(3x - \pi/2)$ is $\pi/6$ and not $\pi/2$; problems 5–6 show that composing a
shift then a stretch scales the shift ($3x + 15$) while the other order does not
($3x + 5$); and problem 10 asks why $x/3 + 1$ shifts **3 units left** despite reading "+1".

## Verification and traps

- **9 of 10 problems machine-verified**: chain evaluations as `eval` (including a
  trigonometric one at $x = \pi/2$), the refactoring identities as `equiv` (SymPy confirms
  $4\sin(3x - \pi/2) \equiv 4\sin(3(x - \pi/6))$), and the undo-the-parameters equations as
  `solve`. Every boxed answer binds back to its own problem's verified value.
- **Four misconception traps are declared and machine-checked** — this is the change from
  the previous artifact, which shipped with none: **143** (moved the input the way the
  printed sign reads, using $x+2$ for $x-2$), **14** (reflected the input before squaring
  instead of the output after it), **4.12** (dropped the horizontal factor when
  substituting into $3\sin(2(x - \pi/4)) + 2$), **3** (left $b$ out of the input, taking
  $\sqrt{5-1}$ instead of $\sqrt{4(5-1)}$). Each was proved to be a value the problem's own
  check rejects, and all four print in the key's "Common wrong answers" block. The `solve`,
  `equiv` and `manual` problems take no traps — the trap field is only allowed on
  single-comparable-answer types.
- **1 problem flagged manual** — problem 10 is a graph sketch plus a written ordering
  argument, which no CAS can check, so it is declared `{"type": "manual"}`. The key still
  gives a complete model response: the factored inside, the four parameters with input moves
  before output moves, the image of the parent's starting point at $(-3, 2)$, two further
  plotted points, the domain, and an explicit full-credit standard. Build result:
  **BUILD PASSED — 1 verification run flagged manual-review items (exit 2)**.

Standards come verbatim from `references/standards-map.md`: `HSF-BF.A.1c` on the
composition and transformation problems, `HSF-TF.B.5` on the two trigonometric ones.

## Study guide

Opens with the parameter map as a four-row table (each parameter, inside or outside, its
effect, and whether it does what it says), then three sections: walking one input through
the whole chain, factoring before reading a phase shift, and composition order. All six
worked examples and try-its are machine-verified. The watch-out box names the dominant
multi-parameter error — reading a shift off an unfactored inside — and gives the
outside-in order for undoing parameters when solving.

## Gate chain

Green on the first attempt. The answer key `\input`s the generated quick-answer bank
directly under `\aktitleblock` with **no `\raggedright` and no `\emergencystretch`** — the
previous artifact wrapped that `\input` in `{\raggedright ... \par}`; the workaround is
gone. All four `\commonerror` lines set, including the longest description on the sheet, and
the key compiles clean at 4 pages with no overfull box.
