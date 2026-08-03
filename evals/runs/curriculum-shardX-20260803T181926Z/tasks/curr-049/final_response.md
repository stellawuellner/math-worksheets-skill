# Halves and Fourths --- Are the Parts Really Equal? (Kindergarten--Grade 1)

Three PDFs are ready: the student worksheet, a full step-by-step answer key, and
a two-page study guide.

## What is on the worksheet (6 problems)

Every problem is about the same misconception: a shape cut into two or four
pieces gets called "halves" or "fourths" even when the pieces are different
sizes. Each problem shows a rectangle drawn on a grid of little squares, so a
five- or six-year-old can decide the question by **counting**, not by guessing
from the shape.

1. **Warm-up** --- a rectangle cut down the middle. Count both parts and write
   $=$, $<$, or $>$ between the counts. (Answer: $6 = 6$, so they are halves.)
2. **Find and fix** --- Kim calls a 3-square part "one half" of a shape whose
   other part has 9 squares. The child writes the true comparison, $3 < 9$, and
   says why two pieces are not automatically two halves.
3. **Find and fix** --- Ben has parts of 4 and 8 squares and wants to move 4
   squares across. Moving 4 only swaps which part is bigger; the correct move is
   **2** squares.
4. Kai's square is cut into four pieces of 2, 6, 6, and 2 squares and called
   "fourths". The child writes the counts in order (2, 2, 6, 6) and sees that
   they do not all match.
5. **Find and fix** --- Ivy folds a 20-square rectangle once, counts one part,
   and writes 10 for a fourth. One fold makes halves, not fourths; each fourth
   is **5** squares.
6. **Challenge (open)** --- draw one line that makes halves and explain how the
   squares show it. This one is genuinely open, so it is labelled for **manual
   review**; the key gives a model answer and tells you exactly what to look
   for (and what the misconception sounds like when it is still there).

Problems 2, 3 and 5 are the find-and-fix items --- three, not the two the
request asked for.

## What was machine-verified

Five of the six problems were checked independently by the SymPy verifier
before anything was printed: the two comparisons, the "how many squares move"
computation, the ordering of the four piece sizes, and the fourths division.
Problem 6 is the only one flagged manual, because a drawing and an explanation
cannot be checked by a computer --- so the build reports it rather than
pretending otherwise.

Two of the wrong answers are **declared misconception traps**, and the verifier
proved each one is distinguishably wrong before the sheet was allowed to print:

- moving the whole difference (4) instead of half of it (2);
- folding once and calling the half (10) a fourth (5).

Both appear in the answer key's "Common wrong answers" block, so whoever grades
the sheet can tell *which* mistake a child made, not just that the answer was
wrong.

## The study guide

Two pages, three sections, each with a rule box, one worked example, and a
separate try-it whose answer is printed upside down inside the box:

1. checking whether two parts are really halves (share the whole between two
   parts to find the fair share);
2. fixing a cut that is not halves (only *half* the gap moves);
3. fourths --- all four parts must match, and one fold makes halves, not fourths.

A watch-out box closes with the idea the whole sheet turns on: the name says how
many **equal** parts, not how many cuts.

## Notes

- The grade level is printed on the answer key only, in the generated Curriculum
  section (standard 1.G, difficulties 1--5); nothing the child holds carries a
  grade label.
- The worksheet runs 4 pages because each problem keeps a full grid picture plus
  real room to work --- worth the paper at this age.
