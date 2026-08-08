# Working with Line Plots — Grade 3 (10 problems)

Three PDFs are ready:

- **`ws_lineplots_curr097.pdf`** — the student worksheet (3 pages)
- **`ss_lineplots_curr097.pdf`** — a 2-page skills summary
- **`ak_lineplots_curr097.pdf`** — the full step-by-step answer key (3 pages)

## What the worksheet covers

Two data sets sit at the top of the sheet: **Line Plot A** (the length in centimetres of each of
twelve crayons, already plotted) and **Data Set B** (the number of books ten students read, given as
a plain list). Every problem says which one to use.

The ramp goes from reading to building to summarizing, and no two problems repeat a skeleton:

- **1–2** read one column, then count all the marks — the difference between "how many crayons are
  8 cm" and "how many crayons are there" is the first thing students confuse.
- **3–4** find the most common length and the spread from shortest to longest, both answered in
  centimetres on a unit-marked answer line.
- **5** is the build task: draw the line plot for Data Set B on the blank scale provided, then check
  it by counting marks against the list.
- **6–8** work from the plot the student just made: compare two columns, find the difference between
  greatest and least, and then the hardest one — how many books were read *altogether*, where the
  marks are no longer the answer and the values have to be added.
- **9** returns to Line Plot A for a two-column comparison.
- **10** is the synthesis: two more 7 cm crayons are added, the most common length changes, and the
  student explains what moved and how to see it without recounting.

Difficulty ramps 1 → 5.

## What is verified, and what is not

- **10 of the 12 checks are machine-verified** with SymPy, covering **8 of the 10 problems fully**.
  Every count, difference, total and most-common value was recomputed from the data arrays that also
  define the printed plot, so the picture and the answers cannot disagree.
- **Two responses are instructor-judged** and are marked `---` in the key's Quick Answers list:
  problem 5(a), the line plot the student draws (no machine can see where the marks went), and
  problem 10(b), the written explanation. For 5(a) the key states exactly what the finished plot must
  look like — even spacing, one mark per student, stacked in columns, ten marks in all — and names the
  usual error, marks bunched sideways instead of stacked.
- Three **common wrong answers** are declared and machine-checked as genuinely wrong, and printed in
  the key: 16 on problem 4 (added the longest and shortest instead of subtracting), 3 on problem 6
  (read one column and forgot to subtract the other), and 10 on problem 8 (counted the marks instead
  of adding the values they sit above). That last one is the most instructive error on the sheet.

## The study guide

Three sections — reading a plot, building one from a list, and summarizing/comparing — each with a
rule box, a worked example whose first step says why that method applies, and a try-it with the
answer upside down inside the box. The watch-out box flags the error that runs through the whole
topic: counting tick marks on the scale instead of the $\times$ marks above it.

The grade level and standards code (3.MD) appear on the answer key only.
