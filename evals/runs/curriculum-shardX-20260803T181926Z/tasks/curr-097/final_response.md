# Line plots — Grade 2–3 practice set

Three PDFs are ready:

- **Study guide** — `ss_lineplots_curr097.pdf` (2 pages)
- **Worksheet** — `ws_lineplots_curr097.pdf` (4 pages, 10 problems)
- **Answer key** — `ak_lineplots_curr097.pdf` (3 pages)

## What's on the worksheet

Ten problems on whole-number line plots, all built around one idea a child of this
age reliably trips on: a line plot carries two different kinds of number. The
labels along the bottom are the thing being counted (books, centimetres); the X's
stacked above them are how many. Every problem forces that distinction.

- **Problems 1–5** work from a finished line plot of books read by Room 4: count
  one stack, find the tallest and the shortest stack, total the whole plot, and
  compare two stacks ("how many more?").
- **Problems 6–9** move to measurement data. Problem 6 hands over a list of shell
  lengths with the plot half-drawn and asks the child to finish it; 7–9 then
  total it, compare two stacks, and find how much longer the longest shell was
  than the shortest — the one answer on the sheet that is a length, so it is
  answered in centimetres.
- **Problem 10** is a two-part closer: part (a) reads the empty column above 9,
  part (b) asks the child to explain to a classmate what that empty space means
  and why the 9 must stay on the number line.

Difficulty ramps 1 → 5 across the set, and the three skills (reading a plot,
building one, comparing/totalling) are interleaved after the warm-up rather than
blocked, so the child has to decide which move a question wants.

## What was verified

All ten problems were machine-checked with SymPy through the skill's verification
gate: every stack count, the two totals (16 children, 12 shells), both "how many
more" comparisons, the longest-minus-shortest range, and the zero above 9. The
answer key's printed boxed answers are bound to those verified values, so a
number cannot drift between the key and the data.

Four **misconception traps** were declared and proved distinguishable — adding
two stacks instead of subtracting them (9 instead of 3), counting the marks on
the number line instead of the X's (6 instead of 12), subtracting the two labels
instead of the two stacks (1 instead of 2), and counting marks instead of steps
for the range (6 instead of 5). Each prints in the key as a "if they got N…"
line, so a wrong answer tells you which mistake was made.

## What is flagged for manual review

**Problem 10, part (b)** is an open written explanation and is labelled `manual`
in the verification data — no machine checked it, and the build reports it as a
manual-review item. The key gives a model answer plus a marking guide (what earns
full credit, what earns partial, what is not sufficient) and a suggestion for
what to do if the child sides with Sam.

Everything else on the sheet is machine-verified.
