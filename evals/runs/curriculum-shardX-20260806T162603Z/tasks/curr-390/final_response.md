# Interleaved review: modeling with systems and matrices

Three PDFs for your Algebra 2 student, all on **using matrices or systems in multivariable
modeling**:

- **`ws_multimodel_curr390.pdf`** — the student worksheet, 12 problems, 6 pages.
- **`ak_multimodel_curr390.pdf`** — the full step-by-step answer key, 5 pages.
- **`ss_multimodel_curr390.pdf`** — a 2-page study guide.

## Why the order matters

This is an interleaved review, so the sheet deliberately does *not* group problems by method.
Problems 1 and 2 are the warm-up — two two-variable systems, one that wants substitution and
one that wants elimination. From problem 3 on, the four subskills alternate:

| Subskill | Problems |
|---|---|
| two-variable systems | 1, 2, 8 |
| writing a system as a matrix equation | 3, 6, 11 |
| three-variable systems | 5, 9 |
| a line meeting a curve (nonlinear) | 4, 7, 10, 12 |

No method appears twice in a row after the warm-up, so the student has to read the situation
and *decide* what to do — which is the whole point of a review sheet and the thing a blocked
sheet cannot teach. Every problem is a real model: ticket prices, crate masses, a coffee
blend, a fountain jet crossing a wire, a workshop's cutting and finishing hours, a gravel
path crossing a pond, two rental plans, a cafe's drink mix, a garden, a feed blend.

Problem 12 is the synthesis challenge: three-sided fencing plus a fixed area, which produces
two designs that are *both* legitimate — the trap being to discard one.

## What was verified, and what was not

The key's generated note says it exactly: **12 of the 16 answers are machine-checked with
SymPy; 4 are instructor-judged.**

- **Machine-checked (12):** every system was solved independently by the computer algebra
  system, and — importantly for the nonlinear problems — the check confirms the answer set is
  *complete*, not merely that the printed solutions work. A key that found only one of two
  intersection points would fail the gate.
- **Instructor-judged (4):** the written parts of problems 6, 8, 10 and 12 — what each row of
  a coefficient matrix records, which rental plan wins at ten hours and why, why two
  algebraic pairs describe one garden, and whether both fencing designs are usable. These are
  the modeling-interpretation asks; they are marked `---` in the Quick Answers bank rather
  than given a fake value, and the key states what a full-credit response must contain.

## Study guide

Four sections, each with a rule box that says *how to choose* a method rather than just
stating one, a worked example whose opening step explains that choice, and a try-it with the
answer upside down inside the box: two-unknown systems, three-unknown systems, the matrix-
equation translation, and a line meeting a curve. All 8 of its worked answers are
machine-verified.
