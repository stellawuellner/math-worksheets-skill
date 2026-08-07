# Reading and Plotting Points on a Grid — Grades 4–5

Three PDFs: the student worksheet, a full step-by-step answer key, and a two-page study
guide.

**Worksheet (10 problems).** The sheet is built around models a child can point at
rather than rules to memorise. It opens with a **Park Map** — a first-quadrant grid with
five labelled landmarks — and problems 1 to 4 all read from it: name a landmark's
ordered pair, say which one is farthest right, walk four right and five up from one
landmark and name where you land, and measure the gap between two landmarks on the same
horizontal line. Problems 5, 7 and 8 each carry their own blank grid to draw on (plot
three points; plot and join a rectangle; plot the first three points of a growing rule).
Problems 6, 9 and 10 turn a burning candle and two "y from x" rules into ordered pairs
and read statistics off them.

Every model is tied back to notation, which is the concept the sheet is really teaching:
the ordered pair is *across first, then up*, and the answer key names the reversed-order
error — plotting (4, 1) for (1, 4) — as the thing to look for when checking the drawings.

Four skills rotate after the warm-up: naming a point, moving on the grid, plotting a
point, and turning a pattern into points. No two neighbouring problems use the same one
for more than three in a row.

**Answer key.** Every solution counts the squares out loud rather than quoting a
formula, and the drawing problems get an explicit checking list (what each mark's
position should be, what the common error looks like). Units — units and centimetres —
are printed inside the boxed answers.

**Study guide (2 pages).** Four sections, one per skill, each with a rule box, a worked
example whose first step names the strategy, and a try-it with the answer upside down
inside the box.

## What is verified, honestly

The sheet asks for 19 separate responses across the 10 problems.

- **15 are machine-checked** with SymPy: every coordinate read from the Park Map (the
  map's landmark positions live in the verification data, so the map and the answers
  come from one source), both coordinates of the landing point, the gap between L and M,
  the candle's height at hour 5, the mean and range of the candle heights, both rule
  values at x = 4, and the x where the two rules agree.
- **4 are instructor-judged** and print as `---` in the Quick Answers bank: the plotted
  points in problem 5, the sketched rectangle in problem 7(b), the three plotted points
  in problem 8(b), and the written explanation in problem 10(d). Three of those four are
  *drawings* — nothing in a computer algebra system can look at a page and say whether a
  dot landed on the right intersection — and the fourth is written reasoning.

Six of the ten problems are fully machine-checked end to end. For the four that are not,
the answer key states exactly what to look at: the coordinates each mark should sit on,
and (for 10(d)) that a stated method is required, not just the number 6.
