# Volumes by Known Cross Sections and Shells — AP Calculus AB/BC

Three PDFs are ready:

- **Study guide** (`ss_volumes_curr488.pdf`, 2 pages) — both set-ups, three worked examples, three try-its.
- **Worksheet** (`ws_volumes_curr488.pdf`, 4 pages, 8 problems).
- **Answer key** (`ak_volumes_curr488.pdf`, 3 pages) — full set-up-to-answer reasoning, a quick-answer bank, and the common wrong answers.

## What the worksheet does

Eight problems, every one of them a volume by cross sections or by shells:

- **Known cross sections** (1, 2, 4, 6): squares over a triangular base;
  semicircles whose *diameter* lies in the base (the classic diameter-vs-radius
  decision); squares over a semicircular base, where squaring the side kills the
  radical; and equilateral triangles over the region under $y = 4 - x^2$, asked
  both exactly and to two decimals.
- **Cylindrical shells** (3, 5, 7): $y = x^2$ about the $y$-axis; $y = \sqrt{x}$
  about the $y$-axis, where shells specifically avoid inverting the function;
  and the region *between* $y = 2x$ and $y = x^2$, where the student must first
  find the intersections and then use the gap between the curves as the shell
  height.
- **Choosing the method** (8): the region bounded by $y = x^2$, the $y$-axis and
  $y = 4$, revolved about the $y$-axis — justify shells in $x$, set up, evaluate.

Difficulty ramps 1 → 4 and the two methods alternate, so the sheet tests
*recognition* of which set-up a region calls for, not just the mechanics of one.

The sheet opens with a single **value-free reference figure** — a vertical strip
of a region labelled "radius $x$" and "height", the shell picture — placed with
the directions and captioned so it cannot be mistaken for any problem's givens.
No problem carries its own valued figure.

## What was verified

**Ten machine checks passed.** Every volume is recomputed by SymPy's
`definite_integral` verifier from the integrand and limits the answer key
prints, so the printed exact answers ($\frac{64}{3}$, $\frac{81\pi}{16}$,
$\frac{81\pi}{2}$, $\frac{256}{3}$, $\frac{128\pi}{5}$,
$\frac{128\sqrt{3}}{15}$, $\frac{8\pi}{3}$, $8\pi$) are bound to recomputed
values rather than retyped. Problem 6's decimal form is separately verified with
`approx` (14.78), and problem 7's limits of integration are verified with
`solve` ($x = 0$ and $x = 2$).

**One item is flagged for manual review**: the written justification in problem 8
for choosing shells over washers. That is open reasoning and is declared
`manual`, so the build ends at exit 2 with it named. The key states what to
accept — including the note that a student who correctly sets up the washer
integral in $y$ and reaches $8\pi$ has also answered the question.

**Seven misconception traps** are declared and machine-checked as
distinguishably wrong; each prints in the key's "Common wrong answers" block:

- 8 — integrated to find the base's area, not the solid's volume (1)
- 63.6 — took the base height as the semicircle's radius, not its diameter (2)
- 20.25 — dropped the $2\pi$ shell factor (3)
- 25.13 — integrated the side length instead of its square (4)
- 25.13 — used discs about the $x$-axis instead of shells about the $y$-axis (5)
- 34.13 — used the square-slice area where the equilateral-triangle area belongs (6)
- 33.5 — used only the upper curve as the shell height (7)

Every problem also declares `"answer_unit": "cubic units"`, and the gate binds it
in both directions: the sheet's answer blank prints it and each boxed answer in
the key must carry it.

## Standards and tagging

`FUN-6` — the AP CED unit code from the "Riemann sums & FTC" row of
`references/standards-map.md`, used verbatim, on every problem; it is the code
the task itself names. Each problem carries a difficulty (ramp 1,2,2,3,3,3,4,4),
a Bloom level (3 apply, 7 analyze, 1 justify) and one of three skill tags; the
three-facet plan is declared in the verify JSON and its subtitle is bound
verbatim into the worksheet title block.

## Study guide

Two pages, three sections: cross sections, shells, and choosing between them.
Each has a rule box, a worked example whose first step justifies the method
before any integration, and a try-it that re-parameterizes it, with the answer
printed upside down inside the box. The third section is the one students
usually lack — a three-question checklist (axis, description, strip direction)
for deciding between shells and washers. The watch-out box carries the
diameter-vs-radius factor of four and the dropped $2\pi$.

## Gate chain

`build.sh` finished **BUILD PASSED** (exit 2 — green with one manual-review
item): template shells, both verification files, skill and facet coverage,
subtitle binding, figure scope and work space, unit binding on the sheet and in
the key, three compiles inside their page budgets (4 / 3 / 2 pages), per-problem
answer-key binding, study-guide structure, and prose consistency at 100% on the
worksheet. No gate failed on the first attempt.
