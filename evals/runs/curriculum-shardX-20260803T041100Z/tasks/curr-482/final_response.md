# Separable Differential Equations with Initial Conditions — AP Calculus AB/BC

Three PDFs are ready:

- **Study guide** (`ss_sepdiffeq_curr482.pdf`, 2 pages).
- **Worksheet** (`ws_sepdiffeq_curr482.pdf`, 6 pages, 10 problems).
- **Answer key** (`ak_sepdiffeq_curr482.pdf`, 4 pages) — separation, integration, the constant, and the branch or domain question each problem raises.

## What the worksheet does

- **Separate and integrate** (1, 3, 5, 8): starting where separation is trivial
  ($dy/dx = 6x^2$), then $dy/dx = xy$ (log-and-exponentiate), then
  $dy/dx = y^2$ (reciprocal antiderivative, with a finite interval of
  validity), then $dy/dx = 3x^2/(2y)$ (implicit solution, one branch selected
  by the condition).
- **Apply the initial condition** (2, 4, 7): finding $C$ explicitly, applying
  the condition *before* isolating $y$ in $dy/dx = (2x+1)/y$, and
  $dy/dx = y\cos x$ where the constant enters multiplicatively after
  exponentiating.
- **Use the particular solution** (6, 9, 10): radioactive decay from a
  half-life, a population reaching a target, and a logistic slope field with
  equilibrium solutions and long-run behaviour.

Difficulty ramps 1 → 5. Every problem is a different separation shape, and
three of them turn on something beyond the mechanics: the interval of validity
(5), the sign of the square-root branch (8), and the fact that only the ratio
of populations enters the logarithm (9).

## What was verified

**17 machine checks across the 10 problems passed under SymPy.** Each of
problems 1–9 carries two independent checks: an `integrate` or `solve` check on
the calculus step (SymPy differentiates the claimed antiderivative back to the
integrand, so a wrong separation cannot survive), and an `eval`/`approx` check
on the particular solution at a stated point. Problem 10 has a `solve` check
for the equilibrium solutions. Every boxed answer in the key was bound back to
its own problem, and the two answers carrying units (`mg`, `years`) were bound
in both directions — sheet `\answerline` to JSON `answer_unit`, and JSON to the
key's boxed `\text{mg}` / `\text{years}`.

**One item is `manual`:** the slope-field sketch and the long-run-behaviour
sentence in problem 10(b). A hand-drawn field and a written argument are not
CAS-checkable, so they are declared `manual`; the key gives the slope in every
lattice row, the asymptotic argument, and a full-credit rubric that names the
error to look for (segments that cross $y = 3$).

Five misconception traps were declared and machine-checked as distinguishably
wrong; they print in the key's "Common wrong answers" block:

- never applying the initial condition, leaving the coefficient at 1 ($7.39$ instead of $14.78$),
- not doubling through before taking the square root ($3.24$ instead of $4.58$),
- rounding 25 days to two whole half-lives ($20$ mg instead of $14.14$ mg),
- integrating $\cos$ to $-\sin$ ($1.72$ instead of $9.28$),
- taking $\ln 1500$ rather than $\ln 3$ ($91.42$ years instead of $13.73$).

## Standards and tagging

`FUN-7` on every problem, taken verbatim from `references/standards-map.md`
("Differential equations", AP Calculus CED unit codes). Every problem carries a
difficulty, a Bloom level (2 recall, 10 apply, 5 analyze, 1 justify), a skill
tag and a facet tag; the three-facet plan is declared in the verify JSON and its
subtitle is bound to the worksheet title block.

## Study guide

Two pages, three sections. The rule box states the three moves and the one
antiderivative students most often mangle, $\int dy/y = \ln|y|$. Each section
has a rule box, a worked example whose first step chooses the method, and a
try-it with the answer upside down inside the box. The watch-out covers the two
things the worksheet's hardest problems actually test: the initial condition
picks the branch, and the interval of validity is the one containing the
initial point.

## Gate chain

`build.sh` finished **BUILD PASSED** (exit 2, manual-review item) on the first
attempt — no gate failed. All 21 gates green: ws 6/6 pages, ak 4/6, ss 2/2.

One thing worth recording, found while drafting rather than by a gate: the
`integrate` checker rejects `ln(y)` as the antiderivative of `1/y` with the
message "antiderivative undefined/non-real at y=-1.3 ... use Abs() form", and
accepts `ln(Abs(y))`. That is the checker being right — it is exactly the
absolute value students drop — and the study guide's try-it now teaches it.
Any generator writing a separable-equation sheet will meet this; the fix is
`ln(Abs(y))` in the JSON, not a workaround. I hit and confirmed this directly.
