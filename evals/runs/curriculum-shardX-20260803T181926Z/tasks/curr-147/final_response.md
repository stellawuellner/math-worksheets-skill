# Fractional line plots — Grades 4–5 practice set

Three PDFs are ready:

- **Study guide** — `ss_fraclineplots_curr147.pdf` (2 pages)
- **Worksheet** — `ws_fraclineplots_curr147.pdf` (5 pages, 12 problems)
- **Answer key** — `ak_fraclineplots_curr147.pdf` (4 pages)

## What's on the worksheet

Twelve problems on reading and interpreting line plots whose scale is marked in
fractions — the grade-5 measurement standard. Everything is built around one
distinction that decides most of these questions: an X is a *thing*, and the
fraction underneath it is a *size*. "How many" questions are answered by counting
X's; "how much" questions are answered by adding the fractions.

- **Problems 1–6** use a plot of water poured into beakers, marked in eighths of
  a cup: count a stack, find the commonest amount, compare two stacks, count the
  beakers, add all the fractions to get the total (3 cups), then share that total
  equally among the eight beakers (3/8 cup each).
- **Problems 7–11** switch to a plot of leaf lengths marked in quarter-inches, so
  the child has to re-read the scale before reading anything else: read a stack,
  find how much longer the longest leaf is than the shortest, count the leaves
  above a threshold, total the lengths end to end (7 1/2 in), and share that
  total among the ten leaves (3/4 in each).
- **Problem 12** closes with a two-part question: part (a) reads a stack, part (b)
  asks the child to explain in writing which part of the plot answers "how long is
  one leaf?" and which answers "how long are they all together?", and why counting
  X's can never answer the second.

Difficulty ramps 1 → 5 and the three skills (reading a fraction plot, comparing
values on it, totalling and sharing) are interleaved after the warm-up, so a
child cannot get through the sheet on autopilot.

## What was verified

All twelve problems were machine-checked with SymPy through the skill's
verification gate — every stack height, both totals (3 cups and 15/2 inches),
both equal-share answers (3/8 cup and 3/4 inch), the range, and the
above-threshold count. The fractions were checked as exact rationals, not
decimals, and the answer key's boxed answers are bound to those verified values,
so no number can drift between the key and the data.

Five **misconception traps** were declared and proved distinguishable: subtracting
the two fractions instead of the two stack heights; counting X's instead of adding
the amounts (8 rather than 3 cups, 10 rather than 7 1/2 inches); and dividing by
the number of marks on the number line instead of by the number of items (both on
the sharing problems). Each prints in the key as a "if they got N…" line, so a
wrong answer identifies the mistake.

One thing worth knowing as a parent: on the leaf plot the equal-share answer
(3/4 in) happens to equal the commonest length, so a child can reach the right
answer by the wrong route. The key flags this explicitly and suggests asking which
method they used.

## What is flagged for manual review

**Problem 12, part (b)** is an open written explanation, labelled `manual` in the
verification data and reported as a manual-review item by the build — no machine
checked it. The key supplies a model answer, a three-level marking guide, and a
prompt to use if the child is stuck.

Everything else on the sheet is machine-verified.
