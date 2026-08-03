# Distributions — Center, Spread, and Shape (Precalculus / Statistics)

Three PDFs are ready:

- **Worksheet** (`ws_distributions_curr446.pdf`, 6 pages) — 10 problems working
  from three displays printed on the front: a dot plot of Class A quiz scores
  (skewed right, one score at 96), a dot plot of Class B (symmetric), and a
  histogram of commute times for 40 workers (skewed right).
- **Answer key** (`ak_distributions_curr446.pdf`, 5 pages) — full worked
  solutions, a quick-answer bank, a generated curriculum section, and grading
  notes that say what to accept and what not to.
- **Study guide** (`ss_distributions_curr446.pdf`, 2 pages) — three sections:
  mean or median, range or IQR, and reading shape off the two centres. Each has a
  rule box, a worked example, and a try-it with the answer upside down inside the
  box.

## What the sheet is really about

Not computing statistics — *choosing* them. The two quiz distributions were built
so that they have nearly the same interquartile range (12.5 and 12) and wildly
different ranges (44 and 22). A student who reports whichever number came first
gets a defensible answer for one class and a badly misleading one for the other,
and problem 7 makes them confront that head-on: one pair of statistics says the
classes are very different, the other says they are nearly the same, and the
student has to say which is telling the truth about the bulk of the data.

The progression: median and range for Class A (1, 2), then the mean (3) and the
quartiles (4), then the comparison mean-versus-median that names the shape (5).
Class B repeats the same computations on symmetric data (6, 7) so the contrast is
visible rather than asserted. The histogram problems (8, 9) move the same
reasoning to a grouped display and add a tail probability, 7/40. Problem 10 asks
for the reporting decision on all three distributions with a justification.

## What was checked by machine, and what wasn't

Fourteen checks cover problems 1 through 9 — every mean, median, quartile, IQR,
range, the modal interval and total read off the histogram, and the tail
probability — recomputed independently by SymPy from the same data arrays that
draw the displays. Problem 3 also declares the wrong answer it targets (averaging
only the smallest and largest value, which gives 74 instead of 66.67), and the
checker confirmed that wrong value is rejected by the problem's own answer.

**Problem 10 is flagged for manual review.** It asks for three reporting
decisions with written justifications, which no computer algebra system can
grade. The answer key gives the model answer for each distribution and states the
three things a full-credit justification contains — the shape named, the choice,
and what would go wrong with the other choice — plus a note that "always use the
median because it is safer" should not be accepted, since that blanket rule is
the absence of the judgement being tested.

One convention worth knowing: quartiles use the school median-of-halves method,
stated in the directions, so answers will match a textbook using that convention
(some calculators use a different one and will give slightly different quartiles).

## Suggested order

Study guide first, then the worksheet with the guide beside it, then the key.
