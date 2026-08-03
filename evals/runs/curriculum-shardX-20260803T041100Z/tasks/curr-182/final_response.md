# Solving and Graphing One-Step Inequalities — Grade 6–7

Three PDFs are ready:

- **Study guide** (`ss_inequalities_curr182.pdf`, 2 pages).
- **Worksheet** (`ws_inequalities_curr182.pdf`, 5 pages, 12 problems).
- **Answer key** (`ak_inequalities_curr182.pdf`, 3 pages) — every solution worked out, with a check and the common wrong answer.

## What the worksheet does

Every problem is a one-step inequality that must be **solved and graphed** — a
number line is printed with each one, so graphing is not an optional extra. The
twelve split three ways:

- **Undo an addition or subtraction** (1, 2, 3, 7, 10): `x + 4 < 9`,
  `n - 6 ≥ 2`, then boundaries that come out negative, then the word problem
  ("the chess club has 18 members and needs at least 25").
- **Undo a multiplication or division** (4, 5, 8, 11): `4x > 20`, `m/3 ≤ 2`,
  then `6w ≤ -18` — chosen deliberately because the *answer* is negative while
  the divisor is not, which is where students flip when they shouldn't — then
  the ticket-budget word problem.
- **Flip for a negative** (6, 9, 12): `-2x > 8`, `-x/3 < 2`, and the closing
  error-analysis problem where Jordan divides `-5x ≥ 20` by `-5` and keeps the
  sign.

Difficulty ramps 1 → 5, no skeleton repeats (the operation, the sign, the sign
of the boundary, and the form of the question all vary), and the two word
problems arrive after the fluency is built rather than instead of it.

## What was verified

**13 machine checks across the 12 problems passed under SymPy.** Twelve are
`inequality` checks: SymPy solves each one independently and compares the full
solution *set*, including whether the endpoint is open or closed, so a wrong
flip or a wrong circle type could not pass. Problem 10 carries a second `solve`
check for the boundary value asked in part (b). Every boxed answer in the key
was bound back to its own problem.

**One item is flagged `manual`:** the written half of problem 12 — explaining
*why* dividing by a negative reverses the sign. That is a genuine explanation,
so it is declared `manual` rather than dressed up as verified. The key prints a
model sentence and a full-credit rubric.

One honest note on traps: the misconception here (forgetting the flip) is the
sheet's central design idea, but declared `"traps"` are only allowed on types
with a single comparable scalar answer, and `inequality` is not one of them —
its answer is an interval. So the misconception is carried by problem design
instead: problem 8 is built so the un-flipped and flipped answers differ, and
problem 12 makes the error the object of study. The wrong answers are written
out in the key's per-problem notes (`x > -4`, `w ≥ -3`, `n ≥ -4`, `m ≤ 2/3`) so
a grader still gets the diagnosis.

## Standards and tagging

`7.EE.B.4` on all twelve, taken verbatim from `references/standards-map.md`
("One/two-step equations | 6.EE.B.7 / 7.EE.B.4"). Every problem carries a
difficulty, a Bloom level (7 apply, 6 analyze, 1 justify), a skill tag and a
facet tag; the three-facet plan is declared in the verify JSON and its subtitle
is bound to the worksheet title block.

## Study guide

Two pages, three sections matching the three skills. Each has a rule box, a
worked example with a **graphed** solution drawn on a number line (the point of
the sheet is the graph, so the guide shows one), and a try-it whose answer —
including which circle to draw — is printed upside down inside the box. The
closing watch-out states the rule precisely: the flip keys on what you divide
*by*, not on any minus sign that happens to appear.

## Gate chain

`build.sh` finished **BUILD PASSED** (exit 2, manual-review item) on the first
attempt — no gate failed. All 21 gates green: template shells, both
verification files, skill and facet coverage, subtitle binding, layout and work
space, three compiles inside their page budgets (ws 5/6, ak 3/6, ss 2/2),
per-problem answer-key binding, study-guide structure, and prose consistency.
