# Slope and Rate of Change — Grade 8 / Pre-Algebra

Three PDFs are ready: the student worksheet, a full step-by-step answer key,
and a two-page study guide.

## What is on the worksheet (12 problems, 6 pages)

The focus is comparing rates of change when they arrive in different forms. The
four ways of getting a rate rotate through the sheet rather than sitting in
blocks, so the first decision on each problem is *where the rate is hiding*:

- **Slope from two points** (Problems 1, 2, 4, 7, 11) — the formula on clean
  points, three lines read off Figure 1 on page 1, and a final pair with
  negative coordinates where subtracting in opposite orders flips the sign.
- **Rate from a table** (Problems 5, 9) — a tub filling at a steady rate, and a
  table that is deliberately *not* linear, where computing the rate over two
  different intervals is how the student proves it.
- **Rate from an equation** (Problems 3, 8) — a taxi fare and a leaking barrel,
  both in $y = mx + b$ form, where the constant term is not part of the rate.
- **Comparing two rates** (Problems 6, 10, 12) — a plan given as an equation
  against a plan given as a table, a runner's table against a runner's
  equation, and a closing synthesis.

Problem 12 pulls the four rates the student already found — two from the graph,
one from a table, one from an equation — and asks for them in order from least
to greatest. That ordering is where the negative rates matter: $-5$ is the
fastest fall and still the smallest number, and the key names the student who
orders by steepness instead.

Difficulty ramps from 1 to 5. Eight of the twelve problems are split into parts
(a) and (b) so the intermediate step is written down.

## What was machine-verified

Eighteen of the nineteen checks were recomputed independently with SymPy and
all passed: every slope (including from the graph's lattice points), both table
differences, both equation evaluations, and all three comparisons — including
the four-way ordering in Problem 12, which was checked as a sorted list, not
just as four separate numbers. The answer key's quick-answer bank is
regenerated from that same verified data each build.

Two misconception traps are declared and machine-checked to be
*distinguishably* wrong, and both print in the key as common wrong answers:

- charging the taxi's flat pick-up fee once per mile, giving \$33 instead of
  \$19;
- computing the slope through $(-3, 5)$ and $(2, -5)$ with the subtractions in
  opposite orders, giving $+2$ instead of $-2$.

## What is flagged for manual review

The second half of **Problem 12** — one sentence on which representation the
student found easiest to read a rate from, and why — is genuinely open and is
labelled as such rather than claimed verified. The answer key accepts any of
the three representations and gives the reason that would earn credit for each,
plus a note that a reason tied to *how* the rate is obtained is required.

## The study guide (2 pages)

Four sections, one per skill, each with a rule box, a short worked example whose
first step says why that method applies, and a try-it with the answer printed
upside down inside the box. The opening panel is the connective tissue: one
idea, four places to find it. All eight study-guide answers were verified by
the same gate as the worksheet.
