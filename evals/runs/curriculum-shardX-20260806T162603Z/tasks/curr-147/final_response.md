# Reading a Line Plot with Fractions — Grades 4–5

Three PDFs: the student worksheet, a full step-by-step answer key, and a two-page study
guide.

**Worksheet (12 problems).** All twelve read from a single **Beaker Plot** at the top of
the sheet: sixteen beakers of water recorded to the nearest eighth of a litre, one
cross per beaker, from 1/8 up to 3/4. Keeping one data set across the whole sheet is
deliberate — this is a fluency sheet, so the *data* stays put and the *question* changes,
which is what builds the reading habit.

The ramp runs from counting to reasoning, and no two problems share a skeleton:

- **1–3** read the plot directly (how many at 3/8, how many altogether, which amount is
  most common);
- **4–6** combine fractional amounts (two beakers of 5/8 poured together; the range;
  the total held by everything below half a litre);
- **7, 10** redistribute (four beakers of 3/8 shared between three; how much more the
  half-litre group holds than the quarter-litre group);
- **8, 12** find the centre (the median of 16 values, then the median again after a
  seventeenth beaker at 7/8 is added);
- **9** is the big one — the total water in the cupboard, 6¾ litres, which takes all six
  stacks;
- **11** turns on the word *more than*, which excludes the stack sitting exactly on 1/2.

Problem 12 closes with the interesting question: adding the largest amount on the plot
barely moves the median, and part (b) asks why.

**Answer key.** Every solution works in eighths so the addition is visible, shows the
reduction, and converts to a mixed number where the amount exceeds a litre. The median
solutions count crosses from the left and name which cross sits in the middle place.
Litres are printed inside the boxed answers and were bound back to the verify data.

**Study guide (2 pages).** Four sections: reading counts off a plot (crosses vs
fractions — the trap of answering "how much" to a "how many" question), adding up one
whole stack, finding the middle of the data, and the two-step pour-then-share. Each has
a rule box, a worked example whose first step names the strategy, and a try-it with the
answer upside down inside the box.

## What is verified, honestly

The sheet asks for 13 separate responses across the 12 problems.

- **12 are machine-checked** with SymPy: every count, every fraction sum, both medians,
  the range, the shared amount, and the 6¾ litre total. The plot's data lives in the
  verification file — the same numbers the plot is drawn from — so the picture and the
  answers cannot disagree, and the printed key was bound back to the verified values by
  the build.
- **1 is instructor-judged** and prints as `---` in the Quick Answers bank: problem
  12(b), the explanation of why adding a 7/8-litre beaker leaves the median where it
  was. The key states what a full-credit answer needs: reasoning about *position* in the
  ordered list, not about the size of the new value. "Because it's only one beaker" is
  not enough.

Eleven of the twelve problems are fully machine-checked end to end.
