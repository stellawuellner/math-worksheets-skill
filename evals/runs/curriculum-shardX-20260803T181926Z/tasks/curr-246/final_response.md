# Scatter Plots — Direction, Form, and Strength (Grade 8 / Pre-Algebra)

Three PDFs are ready:

- **Worksheet** (`ws_scatter_curr246.pdf`, 8 pages) — 10 problems built around a
  panel of six scatter plots printed on the front (Plot A through Plot F), each
  chosen to show one thing clearly: strong positive, strong negative, no
  association, a curve, a weak positive, and a strong positive with one outlier.
- **Answer key** (`ak_scatter_curr246.pdf`, 4 pages) — worked solutions, a
  quick-answer bank at the top, a generated curriculum section, and per-problem
  grading notes.
- **Study guide** (`ss_scatter_curr246.pdf`, 2 pages) — one section per word:
  direction, form, strength. Each has a rule box, a worked example, and a try-it
  with the answer printed upside down inside the box.

## The idea the sheet is built on

Most students can say "positive" or "negative" from a glance and cannot say what
made them sure. So **every problem asks for a number first and a description
second**, and the description has to cite the number:

- **Direction** (problems 1, 2, 5): compare the y-value at the far left with the
  y-value at the far right. Problem 5 is the case where that method correctly
  reports *nothing* — the highest and lowest values on Plot C sit next to each
  other in the middle, which is what "no association" looks like.
- **Form** (3, 8): find the turning point. A straight line never reverses, so an
  x-value in the middle carrying the lowest y is proof of a curve. Problem 8 is an
  error-analysis: a student compares only the two end points of the curved plot
  and concludes "positive". The evidence is true and the conclusion is wrong.
- **Strength** (4, 6, 7, 9, 10): residuals. Problem 4 computes one residual on
  each of two plots; problem 7 gives the full residual list for both and asks for
  the range, which is a real number for "how wide is the band". Plots A and E have
  the *same trend slope of 5* and residual ranges of 2 and 15 — the sheet's way of
  making the point that strength is not slope.

Problems 6 and 9 handle outliers: finding the one on Plot F, then measuring how
far it drags the mean (34.13 with it, 37.57 without).

## What was checked by machine, and what wasn't

Thirteen checks cover problems 1 through 9 — every comparison, every extreme
value read off a plot, both residuals, both residual ranges, and both means —
recomputed by SymPy from the same data arrays that draw the plots, so a figure
and its answer cannot disagree. Problem 6 also declares the wrong answer it is
designed to catch (reading off the smallest x instead of the x where the smallest
y sits), and the checker confirmed that wrong value is rejected by the problem's
own answer.

**Problem 10 is flagged for manual review.** It asks for two complete written
descriptions and a judgement on a newspaper-style claim, which no computer
algebra system can grade. The answer key gives model descriptions of both plots,
the defensible verdict, and the three things a full-credit answer must contain —
including the note that the commonest wrong answer agrees with the claim because
Plot E's line is steep.

## Suggested order

Study guide first, then the worksheet with the guide beside it, then the key.
