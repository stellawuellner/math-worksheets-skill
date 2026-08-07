# Telling Exponential Change from Linear Change — Algebra 1

Three PDFs are ready:

- **Worksheet** (`ws_expvslin_curr276.pdf`) — 10 problems built round one idea: over equal input
  steps, linear change has constant **differences** and exponential change has constant
  **ratios**. Three problems run that test on tables (one growing linearly, one growing
  exponentially, one decaying by halves); three evaluate a linear and an exponential rule
  side by side, including percentage growth and decay written as multipliers 1.15 and 0.88;
  and four compare the two models over the long run — a town, two savings plans, two ways of
  valuing a car, and a closing problem where the student locates the input at which the
  exponential overtakes the line. Difficulty ramps 1 → 5.
- **Answer key** (`ak_expvslin_curr276.pdf`) — each solution states which test is being run and
  why, shows the power computed before the multiplication, and adds the extra differences and
  ratios so a parent can see the pattern rather than just the answer. Rubrics for the three
  written parts. Quick Answers and a Curriculum block (HSF-LE.A.1, HSF-LE.A.3) at the top.
- **Study guide** (`ss_expvslin_curr276.pdf`) — 2 pages: the differences-and-ratios test,
  evaluating each kind of rule (with the percentage-to-multiplier conversion), and why a growing
  exponential eventually passes any line. Rule box, worked example with a stated strategy step,
  and try-it per section.

## What is verified, honestly

- **24 machine checks passed.** Every difference, every ratio, every evaluation of both models,
  the exponential equation in problem 8, and all six rounded two-decimal answers (349.80,
  1006.10, 12665.57, 172.80, 207.36 and the rest) were recomputed by SymPy at full precision and
  matched what the key prints.
- **3 responses are instructor-judged**: 1(c) "which model, and why", 7(c) "which plan, and does
  the advantage last", and 10(e) "where does the exponential overtake, justified". These are the
  conceptual heart of the sheet and cannot be graded by a computer algebra system; each carries a
  printed rubric. The key's note names problems 1, 7 and 10 as the `---` items.
- **1 misconception trap** was machine-tested: continuing the halving table by subtracting 10
  each time, which lands on 40 instead of 5.
- All six study-guide examples and try-its were verified.

Nothing is marked `[unchecked]`.
