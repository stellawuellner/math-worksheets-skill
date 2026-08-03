# Rounding Multi-Digit Numbers to Named Places — Grades 4–5

Three PDFs are ready:

- `ws_rounding_curr103.pdf` — the student worksheet, 10 problems, 4 pages
- `ak_rounding_curr103.pdf` — the full step-by-step answer key, 3 pages
- `ss_rounding_curr103.pdf` — a 2-page skills summary / study guide

## What the worksheet asks

Every problem is worked on a number line, because that is what makes rounding a
*decision between two benchmarks* rather than a digit trick to memorise. Each
problem carries its own line, labelled with the benchmark below, the halfway
number, and the benchmark above, and the child marks the number on it.

- **Rounding on the line** (problems 1, 2) — $3847$ to the nearest thousand,
  $2614$ to the nearest hundred.
- **Rounding to a named place** (problems 3, 4, 7, 10) — $48362$ to the nearest
  thousand; $7952$ to the nearest hundred, where rounding up carries into the
  thousands digit; $5499$ rounded to two *different* places, which give answers
  in opposite directions (the "don't round a rounded number" case); and the
  challenge, finding the least and greatest whole numbers that round to $4600$.
- **Estimating by rounding** (problems 6, 8) — round each addend to the nearest
  hundred and add; round each number to the nearest thousand, subtract, then
  compute the exact difference and say whether the estimate came out smaller or
  larger, and why.
- **Rounding in context** (problems 5, 9) — a stadium crowd of $26481$ reported
  to the nearest thousand, and two hiking trails ($12438$ m and $12509$ m) where
  rounding to the nearest thousand puts two nearly-equal lengths $1000$ apart.

Difficulty ramps 1, 1, 2, 2, 3, 3, 3, 4, 4, 5. Numbers are printed without
comma separators so the digits line up with the place-value talk.

## What was verified

Thirty-six SymPy checks across the ten problems. As well as each rounded answer,
the checks cover the *benchmarks and halfway numbers printed on every number
line* — so no line on the sheet can carry a label the mathematics does not
support. The exact difference in problem 8 and both comparisons are verified
too. **Nothing is flagged for manual review**; the build finished with all gates
green.

One misconception trap is declared and machine-proved distinguishable: reporting
the stadium crowd as $30000$, i.e. rounding to the nearest ten thousand instead
of the named place. It prints in the answer key as a "common wrong answer".

The answer key walks each problem the same way the worksheet does — the two
benchmarks, the halfway number, which side the number falls on — and boxes every
verified value, including the intermediate benchmarks, so a parent can check the
child's number line and not just the final answer.

## The study guide

Four sections, each with a rule box, a worked example whose first step names the
strategy, and a try-it item with the answer upside down inside the box:
rounding on a number line, the digit rule for any named place (with a carry case
in the try-it: $9963 \to 10000$), estimating a sum or difference, and rounding
numbers from real situations.

Standards: 4.NBT.A.3 for the rounding problems, 4.NBT.B.4 for the estimated sum
and difference.
