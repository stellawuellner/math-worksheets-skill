# Finding Parameters That Make Piecewise Functions Continuous — AP Calculus AB/BC

Three PDFs are ready:

- **`ws_continuity_curr453.pdf`** — the student worksheet (5 pages, 8 problems)
- **`ss_continuity_curr453.pdf`** — the study guide / skills summary (2 pages)
- **`ak_continuity_curr453.pdf`** — the full step-by-step answer key (3 pages)

## What the worksheet covers

All eight problems are about the same question — *what value of the constant, if
any, makes this piecewise function continuous?* — approached three ways:

1. **Solve the junction equation** (problems 1, 3, 4, 7). Problem 1 is a single
   junction with one unknown; problem 3 is an applied oven-temperature model in
   degrees Celsius with $t$ in minutes; problems 4 and 7 have three pieces and
   two junctions, so two equations in $a$ and $b$. Problem 7 is deliberately
   asymmetric: one junction involves only $b$, so it must be solved first.
2. **Fill a removable hole with the limit value** (problems 2, 5, 6). These are
   $0/0$ forms that have to be resolved before the parameter can be read off —
   by factoring, by the conjugate of a radical, and by the exponential limit
   $\lim_{u\to0}(e^u-1)/u = 1$.
3. **Show that no constant works** (problem 8). The one-sided limits at
   $x = 3$ are $-\infty$ and $+\infty$, so the two-sided limit does not exist
   and a value assigned at the point cannot repair it.

Difficulty ramps 1 → 5 across the sheet, and the directions require the one-sided
limits to be written out explicitly, which is what the AP rubric awards.

## What was verified, and what is not

Seven of the eight problems were recomputed independently by SymPy and all seven
passed — the three limits, the two single-parameter equations, and the two
two-parameter systems.

**Problem 8 is deliberately labelled for manual review.** It asks for a
justification in words ("explain why no value of $k$ works, and name the type of
discontinuity"), which no computer-algebra check can grade. The answer key gives
a full model answer and a grading note listing the three things full credit
requires: both one-sided limits stated, the conclusion that the two-sided limit
does not exist, and the classification as an infinite (non-removable)
discontinuity. That is the correct outcome for an open-reasoning item, not a gap.

Three misconception traps were declared and machine-checked as distinguishably
wrong, so those problems really do separate the error from the correct method:
reporting $0$ for a $0/0$ form (problems 2 and 5) and reading the limit straight
off the exponent, ignoring the denominator (problem 6). Each is printed in the
key's common-wrong-answer block for grading.

The study guide's three worked examples and three try-it items were verified the
same way — eight limit and equation checks in total, all passed.

## Using them

Hand out the study guide first: it states the three-part continuity test, turns
it into an equation, and gives a worked example plus a try-it for each of the
three skills, with the try-it answers printed upside down inside their boxes.
The answer key opens with a quick-answer bank for fast grading and a curriculum
section listing the AP unit codes (LIM-1, LIM-2) and the difficulty range.
