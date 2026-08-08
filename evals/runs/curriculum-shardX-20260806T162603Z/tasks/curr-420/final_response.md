# Modeling periodic behavior from graphs (Precalculus)

Three PDFs are ready.

**Study guide (`ss_sinusoids_curr420.pdf`, 2 pages)** — four sections, each a rule
box, a worked example whose first step names the decision being made, and a
try-it with the answer printed upside down inside the box: amplitude and midline
from the two extremes, period and the value of $B$, assembling the whole model
from three readings, and solving an equation built on the model.

**Worksheet (`ws_sinusoids_curr420.pdf`, 7 pages)** — 12 problems, **every one of
them carrying its own graph**, which is what "recovering parameters from graphs"
requires. Problems 1 and 2 are a blocked warm-up on amplitude and midline; after
that the four subskills interleave (no subskill runs more than twice in a row),
so the student has to decide *which* reading the question wants rather than
repeat one procedure. Contexts are real ones with stated units: harbour depth,
a vibration sensor, a greenhouse thermostat, and two ferris wheels. Problem 9
gives a blank labelled grid to sketch two revolutions on; problem 12 is the
synthesis challenge — read all three parameters off a shifted cosine graph, write
the model, then solve it for a given height.

**Answer key (`ak_sinusoids_curr420.pdf`, 4 pages)** — worked solutions that show
the reasoning (including *why* each solution list is complete over its interval,
not just what the roots are), a Quick Answers bank, and a generated Curriculum
section for HSF-TF.B.5.

## What is verified, honestly

The sheet asks for **24 responses across the 12 problems**.

- **22 are machine-checked** by SymPy: every amplitude, every midline value,
  every $B$, and both solution sets. The two `solve` items and problem 12's
  shifted-cosine equation are checked for *completeness* on their stated
  interval, so "the student found only one of the two times" is a real failure
  mode the check would catch.
- **2 are instructor-judged**, printed as `---` in the Quick Answers bank:
  problem 9(c), the sketch on the grid, and problem 11(c), the written
  explanation of why amplitude is not the maximum. A drawn curve and a sentence
  of reasoning cannot be graded by a computer algebra system. The answer key
  prints a checklist for the sketch (midline at 22, peaks at 42, troughs at 2,
  first peak at $t=2$, smooth not segmented, three labels) and a rubric for the
  explanation, which requires the *midline as reference level* and not merely
  the arithmetic.

That matches the key's own "What is verified" note: 22 of 24, across 12 problems,
with 9 and 11 flagged. Nothing is marked `[unchecked]`.

One note on paper: the sheet runs 7 pages because 12 graphs plus real writing
room genuinely need that much. The graphs were sized down to fit two problems on
most pages; the work space was not reduced below the point where a student can
show the algebra.
