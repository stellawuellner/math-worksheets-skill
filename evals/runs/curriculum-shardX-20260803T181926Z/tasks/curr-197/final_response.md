# Centre and spread — Grades 6–7 practice set

Three PDFs are ready:

- **Study guide** — `ss_centerspread_curr197.pdf` (2 pages)
- **Worksheet** — `ws_centerspread_curr197.pdf` (7 pages, 12 problems)
- **Answer key** — `ak_centerspread_curr197.pdf` (4 pages)

## What's on the worksheet

Twelve problems on computing *and interpreting* measures of centre and spread.
The sheet is deliberately built in two halves, and the second half is where the
interpretation lives.

- **Problems 1–7** use a dot plot of goals scored in eleven games — a well-behaved
  data set. The student finds the mode, the median, the mean, the range, the two
  quartiles, and the interquartile range, then works out the probability that a
  randomly chosen game finished with three or more goals. On this data set the
  mean and the median are both 2, which is the point: the measures agree when
  nothing unusual is going on.
- **Problems 8–12** switch to nine students' summer reading totals, one of whom
  read 24 books against everyone else's 3 to 10. Now the measures disagree — mean
  8 against median 6, range 21 against IQR 4.5 — and problems 11 and 12 ask the
  student to compute the alternative (the mean without the outlier, and the IQR)
  and then argue in writing which measure describes the group better and why.

Difficulty ramps 1 → 5, and the four skills (median/mode, mean, range/IQR,
probability from data) are interleaved after the warm-up so the student has to
choose the method rather than repeat one.

## What was verified

All twelve problems were machine-checked with SymPy through the skill's
verification gate: every mode, median and mean; the ranges; both quartile pairs;
both interquartile ranges; the mean of the eight non-outlier values; and the
probability as an exact fraction (4/11). Quartiles use the school
median-of-halves convention, and the answer key says so explicitly since some
textbooks include the median in both halves. The key's boxed answers are bound to
the verified values, so nothing can drift between the key and the data.

Five **misconception traps** were declared and proved distinguishable: averaging
the six labels on the dot-plot axis instead of the eleven games (2.5 instead of
2); giving the range where the IQR was asked (5 instead of 2, and 21 instead of
4.5); counting axis labels instead of games in the probability problem (3/11
instead of 4/11); and reporting the median where the mean was asked (6 instead of
8). Each appears in the key as an "if they got N…" line, so a wrong answer names
the mistake.

## What is flagged for manual review

Two items are open written explanations, labelled `manual` in the verification
data and reported as manual-review items by the build:

- **Problem 11(c)** — which measure of centre describes the readers better, and
  what Devi's 24 books do to each.
- **Problem 12(c)** — why the interquartile range is a fairer measure of this
  group's spread than the range.

Both have a model answer in the key plus a three-level marking guide, and both
accept more than one defensible position provided the reasoning is there. The
computed parts of those problems — the mean of the eight, and the IQR — are
machine-verified.
