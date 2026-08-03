# Absolute-Value and Piecewise Functions — Evaluating (Algebra 1)

Three PDFs are ready:

- **Worksheet** (`ws_piecewise_curr296.pdf`, 6 pages) — 10 problems with a
  "Function Reference" panel at the top holding every rule the sheet uses plus a
  labelled graph of $y = |x-3|+2$, so no problem depends on remembering a
  definition from two pages back.
- **Answer key** (`ak_piecewise_curr296.pdf`, 4 pages) — a worked solution per
  problem, a quick-answer bank at the top for fast grading, a generated
  curriculum section, and a "common wrong answers" note where the sheet was
  designed to catch a specific error.
- **Study guide** (`ss_piecewise_curr296.pdf`, 2 pages) — three sections, each a
  rule box, one short worked example, and a try-it with the answer printed
  upside down inside the box.

## What the sheet actually practises

The focus is *evaluating* — producing an output from a rule and an input. The
ten problems split three ways:

1. **Absolute-value evaluation** (problems 1, 2, 3, 7) — finish the inside of the
   bars first. Problem 2 is a table of values that the student then checks
   against the printed V-graph, which is where the "distance from the vertex"
   idea becomes visible rather than stated.
2. **Choosing the branch of a piecewise rule** (4, 6, 9, 10) — every one of these
   includes an input that sits exactly on a boundary, because that is the input
   students lose marks on. Problem 9 asks for the explanation in words.
3. **A piecewise model in context** (5, 8) — a parking-garage price ladder, used
   forwards (find the cost) and backwards (find the hour where the rate goes
   flat).

Difficulty ramps from 1 to 5: problems 1–3 are single substitutions, 4–8 are
multi-step with a decision in them, and problem 10 is a challenge that asks where
the two branch formulas would agree and whether that makes the function
continuous.

## What was checked by machine, and what wasn't

Every numeric answer was recomputed independently with SymPy before the PDFs were
allowed to compile — 15 checks covering all ten problems, including both
solutions of the challenge system. Two problems additionally declare the specific
wrong answer they were designed to catch (using the top branch at the boundary,
$3(2)+1 = 7$; dropping the absolute-value bars, $2(-9+4)-5 = -15$), and the
checker confirmed those wrong values really are rejected by the problem's own
answer — so the problems can distinguish the error they target. Those wrong
values are printed in the answer key so a grader knows what a particular mistake
means.

**Problem 9 is flagged for manual review** and cannot be otherwise: it asks the
student to explain, in words, why the two branch formulas disagree at $x = 2$ and
what the graph does there. No computer algebra system can grade an explanation.
The answer key gives a full model answer with the three points a complete
response makes, plus what should and should not earn credit.

One note on the verification file: problem 7 ($|x-3|+2 = 6$) is verified in the
equivalent squared form $(x-3)^2 = (6-2)^2$, which has the same two solutions,
$x = -1$ and $x = 7$. The solver cannot take an absolute value directly. The
worksheet and the answer key both work the problem the way a student should — by
splitting into two cases.

## Suggested order

Give the student the study guide first, let them work the worksheet with it
beside them, and keep the answer key.
