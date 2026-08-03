# Function Notation, Domain, and Range — Algebra 1

Three PDFs are ready: the student worksheet, a full step-by-step answer key,
and a two-page study guide.

## What is on the worksheet (12 problems, 5 pages)

Every problem is about connecting the four faces of one function — a rule, a
table, a graph, and the story a function lives inside. The set is interleaved
rather than blocked: after a two-problem warm-up the method changes almost
every problem, so your student has to decide *which* move to make instead of
repeating the last one.

- **Evaluating a rule** (Problems 1, 4, 9) — including a negative input, where
  the classic slip is writing $-2^2$ when the problem means $(-2)^2$.
- **Finding the input for a given output** (Problems 5, 8) — the same rule run
  backwards, which is what "solve" means here.
- **Reading a table or a graph** (Problems 2, 3, 6, 10) — two readings off a
  drone-flight graph printed at the top of the sheet, then building a linear
  rule from a kayak-rental table and using it to reach an hour the table never
  lists. Problem 10 is a find-and-fix-the-mistake problem built on the same
  table.
- **Domain and range in context** (Problems 7, 11, 12) — where a tank's domain
  stops because the tank empties, why a ticket function's domain is only nine
  whole numbers, and a closing synthesis paragraph.

Difficulty ramps from 1 to 5: two warm-ups, a middle of standard multi-step
work, and the final problem a written synthesis.

## What was machine-verified

Twelve of the fourteen checks in the verification file were recomputed
independently with SymPy and all passed — every evaluation, every solve, both
graph readings and both table readings. The build also regenerates the answer
key's quick-answer bank from that same verified data, so the printed answers
cannot drift from the checked ones.

Three misconception traps are declared and machine-checked to be
*distinguishably* wrong, and each is printed in the answer key as a "common
wrong answer" so you can tell a method error from an arithmetic slip:

- subtracting the two inputs (6 − 2 = 4) instead of the two heights on the
  graph;
- reading $(-2)^2$ as $-4$, giving 8 instead of 16;
- treating the first table cost, \$22, as the hourly rate, giving \$110.

## What is flagged for manual review

Two parts are genuinely open reasoning and are labelled as such rather than
claimed as verified:

- **Problem 11(b)** — explaining why the ticket function's domain is only the
  whole numbers 0 through 8.
- **Problem 12** — the closing paragraph comparing domain and range across the
  graph and the rule, and justifying which representation showed each better.

The answer key gives a model answer and a grading note for both, including the
wrong answer to listen for ("the domain is all real numbers, because you can
multiply anything by 9").

## The study guide (2 pages)

Four sections, one per skill on the worksheet, each with a rule box, a short
worked example whose first step says *why* that method applies, and a try-it
with the answer printed upside down inside the box so your student can check
without reading a solution. Section 3 covers reading a graph and turning a
table into a rule; section 4 covers the domain a story imposes. All eight
study-guide answers were verified by the same gate as the worksheet.
