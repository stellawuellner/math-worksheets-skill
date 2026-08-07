# Find and Fix: Input, Output, and Function Notation — Grade 8 / Pre-Algebra

Three PDFs are ready:

- **Worksheet** (`ws_notation_curr234.pdf`, 3 pages) — 8 error-analysis problems, all
  aimed at the same confusion: which number in `f(a) = b` is the input and which is
  the output. Three of them are full find-and-fix items (problems 2, 5 and 8), where
  a named student's wrong work is printed and the student has to correct it *and*
  say what went wrong. Problem 7 puts the same number `5` in both roles in one
  problem — `p(5)` in part (a), `p(x) = 5` in part (b) — which is where this
  misconception usually surfaces.
- **Answer key** (`ak_notation_curr234.pdf`, 3 pages) — Quick Answers, a "What is
  verified" note, a **Common wrong answers** block listing each planted error next to
  the number it produces, and a worked solution per problem.
- **Study guide** (`ss_notation_curr234.pdf`, 2 pages) — three sections: telling input
  from output, working backwards from an output, and spotting a swapped
  substitution, each with a rule box, a worked example and a try-it.

## Machine-checked misconception traps

The wrong results printed in the stems are not typed in by hand — each is declared in
the verification data and recomputed:

- Devin's `4(-9) - 2 = -38` (problem 2) — the swapped substitution.
- Reading `f(15) = 37` when asked to solve `f(x) = 15` (problem 3).
- Answering `19` when asked which input gives the output `19` (problem 5).
- Answering `p(5) = 1` when asked to solve `p(x) = 5` (problem 7).

Each was checked to be *distinguishably* wrong — a trap that the problem's own check
would have accepted is rejected by the build, so none of these can quietly coincide
with the right answer.

## What is verified

**4 of the 8 problems are fully machine-checked** (problems 1, 3, 4 and 7); the other
four — 2, 5, 6 and 8 — are **partly instructor-judged**. In each of those, the numeric
half is machine-checked and the written half is not:

| Problem | Machine-checked | Instructor-judged |
|---|---|---|
| 2 | the corrected value `h(-2) = -17` | the description of Devin's error |
| 5 | the corrected input `x = 3` | the description of Rosa's error |
| 6 | `f(2) = 10`, `g(2) = 11`, and `10 < 11` | the judgement of the student's claim |
| 8 | `d(6) = 20` from the rule | the rewritten sentence |

That is the same split the key's "What is verified" note prints, and each written half
carries a grading rubric in the key saying what a correct response must contain.

## Notes for you

- The grade level appears on the answer key only.
- Standard covered: 8.F.A across all eight problems.
- The point of the sheet is that a correction alone is not a full answer. If your
  student writes only the fixed number on problems 2, 5 and 8, they have done the
  arithmetic without diagnosing anything — the rubrics in the key say as much.
