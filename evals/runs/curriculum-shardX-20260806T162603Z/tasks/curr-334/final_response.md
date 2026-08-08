# Which Quadrilateral Property Implies Which? — 6 error-analysis problems

Three PDFs are ready:

- **`ws_quadprops_curr334.pdf`** — the student worksheet (3 pages).
- **`ak_quadprops_curr334.pdf`** — the full step-by-step answer key with grading
  rubrics.
- **`ss_quadprops_curr334.pdf`** — a 2-page skills summary.

## What the worksheet covers

The whole sheet is about implications that run in **one direction only** — every
square is a rhombus, but not every rhombus is a square. Each problem pairs an
algebra step your student can check with a written diagnosis of a reversed
implication:

1. **Find and fix:** Kim assumes a parallelogram has right angles and gets
   $x = 15$. (Consecutive angles are supplementary; $x = 16$.)
2. One pair of opposite sides parallel *and* congruent — a parallelogram, but
   why not a rectangle?
3. A rhombus's perpendicular diagonals give a side of 15 — but a classmate
   jumps from "all sides equal" to "square".
4. **Find and fix:** Ravi misreads "bisect each other" as "each is half the
   other" and gets $y = 2.4$. (Correct: $y = 5$, diagonals 26.)
5. A kite whose two pairs measure 15 and 14 — so not a rhombus.
6. The challenge: a coordinate quadrilateral whose diagonals (9.85 and 5) settle
   the rectangle question.

## What is verified, and what is not

The sheet asks for **15 separate responses**.

- **9 are machine-checked.** Every value — each solved variable, each side and
  diagonal length — was recomputed with SymPy before the PDFs were built, and
  the answer key's boxed answers were bound back to those values.
- **6 are instructor-judged**, one per problem: the written explanation of which
  implication was reversed. That is the point of the sheet, and no computer can
  grade a sentence. Each is marked `---` in the Quick Answers bank, and the key
  gives you a model response plus a three-level rubric (full / half / no credit)
  for every one. The key's own "What is verified" note says 9 of 15.

There are no `[unchecked]` marks.

## The planted errors are machine-checked too

All three find-and-fix problems declare their wrong answer as a *trap*, so the
verifier confirmed the wrong method really does produce a distinguishably
different number. The key prints them under **Common wrong answers**: 15 (right
angles assumed), 21 (half-diagonals added instead of the Pythagorean theorem),
and 2.4 (the misread bisector). If your student's answer matches one, you know
exactly what to reteach.

## The study guide

An opening box gives the family tree — square $\Rightarrow$ rectangle
$\Rightarrow$ parallelogram, square $\Rightarrow$ rhombus $\Rightarrow$ kite —
with the rule that going *up* the tree always costs one extra condition you have
to name. Then three sections (angle tests, side tests, diagonal tests), each with
a worked example and a try-it whose answer is printed upside down in the box.
