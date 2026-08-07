# Find and Fix the Mistake — Grade 3 error analysis (8 problems)

Three PDFs are ready:

- **`ws_finderror_curr099.pdf`** — the student worksheet (3 pages)
- **`ss_finderror_curr099.pdf`** — a 2-page skills summary
- **`ak_finderror_curr099.pdf`** — the full step-by-step answer key (3 pages)

## What the worksheet covers

Every one of the eight problems is a find-and-fix item, and each has the same two parts: **(a) fix the
answer**, **(b) say what went wrong in a sentence**. Two shared references sit at the top: **Line Plot
P** (books borrowed by twelve students) and **Shape Set Q** (a square, a rhombus, a trapezoid and a
rectangle labelled W–Z).

The errors are the real ones children make at this level:

- **Scale errors (1, 7)** — a scale labelled 1, 2, 3, 5, 6, and a scale whose gaps are unequal widths.
- **Reading errors (2, 4, 5)** — counting the labels on the scale instead of the marks above them;
  adding the scale numbers to find how many students there are; adding greatest and least instead of
  subtracting to get a difference.
- **Shape-attribute errors (3, 6)** — calling a rhombus a square because it has four equal sides, and
  putting a trapezoid in the "two pairs of parallel sides" group.
- **8** is the synthesis: a copy of the plot is one mark short, and the child has to say how to find
  *which* value went missing without redrawing the whole thing.

Difficulty ramps 2 → 5. Everything on the sheet is diagnostic work, which is why the cognitive mix is
entirely analyse-and-justify.

## What is verified, and what is not

This is the honest headline: **every problem on this sheet has one machine-checked half and one
instructor-judged half.**

- **All 8 corrections — the (a) parts — are machine-verified** with SymPy against the plot and shape
  data, so the numbers the child is asked to fix cannot be wrong in the key.
- **All 8 diagnoses — the (b) parts — are instructor-judged.** Naming an error is prose; no machine
  grades it. The Quick Answers bank prints `---` beside every problem and the key's "What is
  verified" note says plainly that 0 of 8 problems are *fully* machine-checked, because each carries a
  written half. The worked solution for every (b) gives a model answer and states what falls short —
  for example, on problem 5 writing "4" without saying that a difference means subtracting is not full
  credit.
- **Seven planted wrong results are declared as misconception traps and machine-checked as genuinely
  wrong**, then printed in the key's "Common wrong answers" block: 5 (kept the uneven scale label),
  5 (counted scale ticks instead of marks), 4 (assumed equal sides means square corners), 15 (added
  the scale numbers), 6 (added instead of subtracting), 2 (assumed every quadrilateral has two pairs
  of parallel sides), and 5 (counted ticks instead of gaps). Each was verified to be distinguishable
  from the correct answer, so no planted error accidentally coincides with the right one.

## The study guide

Three sections: checking a scale, counting the right thing, and checking a shape against the
attribute the group actually asks for. Each has a rule box, a worked example that opens with the
strategy, and a try-it with its answer upside down inside the box. The watch-out box makes the point
the whole sheet rests on: getting the right answer is only half of a find-and-fix problem — naming
the mistake is what stops you repeating it.

The grade level and standards codes (3.MD, 3.G.A) appear on the answer key only.
