# Graphing Quadratics from Vertex or Standard Form — Algebra 1

Three PDFs are ready:

- **Study guide** (`ss_quadgraphs_curr282.pdf`, 2 pages).
- **Worksheet** (`ws_quadgraphs_curr282.pdf`, 7 pages, 12 problems).
- **Answer key** (`ak_quadgraphs_curr282.pdf`, 3 pages) — worked features plus the sketch description for each.

Seven pages is the honest cost of the topic: every one of the twelve problems
carries its own coordinate grid, because a graphing sheet with nowhere to graph
is not a graphing sheet. All twelve grids use the same window ($-6$ to $6$
across, $-10$ to $10$ up), so no problem needs a rescaled axis and every answer
lands on the paper.

## What the worksheet does

- **Graph from vertex form** (1, 2, 5, 8, 12): $(x-2)^2-1$, then
  $-(x+3)^2+4$ (sign flip on $h$ *and* a downward opening), then $2(x-1)^2-8$
  (stretch, plus intercepts straight out of vertex form), then
  $\tfrac12(x+2)^2-2$ (shrink), and finally building an equation from a vertex
  and one extra point.
- **Graph from standard form** (3, 6, 9, 11): $x^2-6x+5$ via $-b/2a$, then
  $-x^2+4x+5$ where $a<0$ and the vertex is a maximum, then $x^2+2x-3$ where
  the two routes to the vertex agree, then completing the square on
  $x^2-6x+4$.
- **Use the intercepts** (4, 7, 10): factoring, difference of squares, and a
  leading coefficient that must come out first.

Difficulty ramps 1 → 5 and no skeleton repeats: the form, the sign of $a$, the
size of $a$, and the feature asked for all change from problem to problem.

## What was verified

**19 machine checks across the 12 problems passed under SymPy** — vertex
heights by `eval` at the axis of symmetry, $x$-intercepts by `zeros`, and the
completed square in problem 11 by `equiv` (SymPy confirms
$x^2-6x+4$ and $(x-3)^2-5$ are the same function, so a slip in the constant
could not survive). Ten of the twelve problems carry two independent checks.
Every boxed answer in the key was bound back to its own problem.

**One item is `manual`:** the sketch-and-explain half of problem 12 — a
construction plus a written justification of how the extra point fixes $a$.
That is genuinely unverifiable, so it is declared `manual`; the key supplies a
model answer and a full-credit rubric.

Three misconception traps were declared and machine-checked as distinguishably
wrong, and they print in the key's "Common wrong answers" block:

- reading $h$ straight off $(x-2)^2$ as $-2$ (vertex height $15$ instead of $-1$),
- using $x = b/2a$ instead of $-b/2a$ (vertex height $32$ instead of $-4$),
- dropping the sign of $a$ in $-b/2a$ when $a=-1$ (vertex height $-7$ instead of $9$).

## Standards and tagging

Both codes are verbatim from `references/standards-map.md`:
`HSF-IF.A–HSF-IF.C` ("Function behaviour, notation, graphs") on the ten
graphing-feature problems, and `HSA-SSE.B.3` on the two where a change of form
is the point (problem 5, vertex form revealing the zeros; problem 11,
completing the square). Every problem also carries a difficulty, a Bloom level,
a skill tag and a facet tag; the three-facet plan is declared in the verify
JSON and its subtitle is bound to the worksheet title block.

## Study guide

Two pages, three sections. Section 1 includes a small worked graph so the
student can see what a finished sketch looks like; sections 2 and 3 are
algebraic. Each has a rule box, a worked example whose first step chooses the
method, and a try-it with the answer upside down inside the box. The watch-out
names the two sign errors that cost the most marks.

## Gate chain

Final run: **BUILD PASSED** (exit 2, manual-review item), all 21 gates green,
ws 7/8 pages, ak 3/8, ss 2/2.

**One gate failed on the first attempt: `compile-ss`,** with five
`Missing character: There is no . / 0 / 1 / p / t in font nullfont` faults.
Cause (isolated by bisection, not inferred): a **second `\addplot` in the same
pgfplots `axis`** — the documented "completed graph" pattern from
`references/latex-templates.md`, `\addplot[only marks, mark=*, ...] coordinates
{...}` layered over a function plot — makes the engine typeset a stray "0.1pt"
in `nullfont`, which `check_log.py` correctly treats as a hard failure. The
trigger is erratic with respect to `samples` (60 and 100 fail, 40 and 200 pass)
so it is not a simple option clash; adding an explicit colour or `solid` did
not help either. Replacing the marker plot with `\fill (axis cs:x,y) circle
(1.7pt);` inside the same axis draws the identical dots and compiles clean.
That is a real repo hazard worth recording: the marker-overlay pattern in the
templates reference can fail this gate, and the `\fill (axis cs:...)` form is a
safe substitute.
