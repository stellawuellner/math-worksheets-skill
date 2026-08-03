# Unit Circle and Trigonometric Graphs — Precalculus

Three PDFs are ready: the student worksheet, a full step-by-step answer key,
and a two-page study guide.

## What is on the worksheet (12 problems, 6 pages)

The focus is modelling periodic behaviour and recovering the parameters of
$y = A\sin(B(t - C)) + D$ from what you are given. The four moves are
interleaved after the opening block, so the student has to decide which one
applies:

- **Recovering parameters from a graph** (Problems 2, 3, 4, 9) — amplitude,
  midline and period read off Curve G, printed on page 1, and then the same
  three recovered from a verbal description of a graph.
- **Building a model from a situation** (Problems 5, 8, 12) — a Ferris wheel
  from its diameter, clearance and turn time; a harbour tide from its high and
  low water; and a closing synthesis on two different-looking models of the
  same wheel.
- **Evaluating a model** (Problems 1, 6, 10) — exact values at unit-circle
  angles.
- **Solving a periodic equation on one cycle** (Problems 7, 11) — every
  solution in the interval, not just the first one.

The two errors this sheet is built to catch are both structural rather than
arithmetic: treating a peak-to-trough gap as a whole period (it is half), and
reporting a single solution to a periodic equation where a horizontal line cuts
each cycle twice. Difficulty ramps from 1 to 5.

## What was machine-verified

Nineteen of the twenty checks were recomputed independently with SymPy and all
passed: every parameter recovery, every model evaluation (kept exact, including
$10\sqrt{3} + 23$ in the synthesis), and both periodic equations. The two
`solve_interval` checks confirm *completeness* on the interval, not just that
the listed roots work — so an answer key that found one of two solutions would
have failed the gate rather than shipped. The answer key's quick-answer bank is
regenerated from that verified data each build.

Three misconception traps are declared and machine-checked to be
*distinguishably* wrong, and each prints in the key as a common wrong answer:

- taking the full peak-to-trough rise as the amplitude (10 instead of 5);
- evaluating the cosine in degree mode on the Ferris wheel, which returns a
  plausible 3.05 instead of 33;
- reading a maximum-to-next-minimum gap as a whole period (6 instead of 12).

## What is flagged for manual review

**Problem 12(b)** is genuinely open reasoning and is labelled as such: why a
cosine model and a quarter-period-shifted sine model describe the same wheel,
and which parameters a graph pins down uniquely. The answer key supplies the
identity $\sin(\theta - \tfrac{\pi}{2}) = -\cos\theta$, the point that
amplitude, midline and period are determined while the phase shift, the choice
of sine against cosine, and the sign of $A$ trade off against one another, and
a note on the answer to push back on.

## The study guide (2 pages)

Four sections — reading the period off a graph, building a model, evaluating a
model, solving a periodic equation — each with a rule box, a worked example
whose first step names why that method applies, and a try-it with the answer
printed upside down inside the box. The opening panel carries the parameter
formulas with a worked amplitude and midline, plus the radian-mode warning. All
eight study-guide answers were verified by the same gate as the worksheet.
