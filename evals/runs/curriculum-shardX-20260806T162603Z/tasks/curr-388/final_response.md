# Matrix operations, set in a bike-share depot

Three PDFs for your Algebra 2 student, all on **performing basic matrix operations**:

- **`ws_matrixops_curr388.pdf`** — the student worksheet, 10 problems, 6 pages.
- **`ak_matrixops_curr388.pdf`** — the full step-by-step answer key, 4 pages.
- **`ss_matrixops_curr388.pdf`** — a 2-page study guide.

## The representation the sheet uses

Every matrix on the worksheet is a real table, and its rows, columns and units are stated
next to it: rentals in bikes (rows = depot, columns = bike type), prices in dollars per
rental, parts used per bike, staff minutes per rental. Nothing is decorative — there are no
irrelevant story details, and every number printed in a stem is a number the verification
actually uses.

That matters most in the multiplication problems. When the student computes $DE$ for
"bikes serviced per day" times "parts used per bike", the product's entry really is *parts
per mechanic per day* — so the shape rule (inner dimensions must agree) has a meaning
attached to it rather than being a rule to memorise.

## What the ten problems cover

| Problems | Operation |
|---|---|
| 1, 3 | adding and subtracting matrices, entry by entry |
| 2, 5 | scalar multiplication, including the combined form $3A - 2B$ |
| 4, 6, 8, 9 | matrix multiplication: $2\times2$ by $2\times1$, $2\times2$ by $2\times2$, a single named entry, and a $2\times3$ by $3\times1$ |
| 7, 10 | writing a system as a matrix equation and solving it (two unknowns, then three) |

Difficulty ramps from 1 to 5, the four operations are interleaved rather than blocked, and
each matrix answer has a printed empty bracket to fill so the layout tells the student
exactly what shape the answer should be.

## What was verified, and what was not

The key's generated "What is verified" note says it exactly: **27 of the 30 answers are
machine-checked with SymPy; 3 are instructor-judged.**

- **Machine-checked (27):** every single entry of every result matrix was recomputed
  independently — not the matrix "as a whole", but position by position, so a right answer
  with one wrong entry cannot slip through. Both systems (problems 7 and 10) were solved
  independently and confirmed to have exactly one solution.
- **Instructor-judged (3):** the written parts of problems 8, 9 and 10 — reading what a
  product entry *means* in context, explaining why the reversed product does not exist, and
  interpreting the three parts of a matrix equation. These are the interpretation skills the
  application format is for, and no computer can grade them. Each is marked `---` in the
  Quick Answers bank, and the key prints what a full-credit response must contain (for
  problem 9, "matrices do not commute" is explicitly not enough — the product does not exist
  at all).

## Study guide

Four sections, each with a rule box, a worked example that opens by saying why the method
applies, and a try-it with the answer upside down inside the box: adding/subtracting,
scalar multiplication, matrix multiplication (with the shape rule stated first), and writing
a system as a matrix equation. All 22 of its worked values are machine-verified.
