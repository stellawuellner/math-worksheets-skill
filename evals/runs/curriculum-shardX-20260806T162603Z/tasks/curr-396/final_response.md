# Identifying conics and reading their key features

Three PDFs for your Algebra 2 student, all on **identifying conics from equations and key
features**:

- **`ws_conicid_curr396.pdf`** — the student worksheet, 10 problems, 6 pages.
- **`ak_conicid_curr396.pdf`** — the full step-by-step answer key, 4 pages.
- **`ss_conicid_curr396.pdf`** — a 2-page study guide.

## The model the sheet is built on

The first page carries a **shape strip** — a circle, an ellipse, a parabola and a hyperbola
drawn side by side with no numbers on them — and directly beneath it a **table of the four
standard forms**. That pairing is the point of the sheet: the picture says what the curve
looks like, the table says what its equation looks like, and every problem afterwards moves
between the two.

The connective idea is the **sign test**: put both squared terms on one side, multiply their
coefficients, and the sign of the product tells you which of the four pictures you are
looking at. Problems 2 and 5 make the student compute that product and then justify the name
from it, rather than recognising the shape by memory.

## What the ten problems cover

| Problems | Feature |
|---|---|
| 2, 5 | classify a conic from its equation, with the reason |
| 1, 3, 9, 10 | circles: radius from standard form, centre and radius from a diameter, completing the square, and a line cutting the circle |
| 4, 7 | parabolas: vertex from the axis of symmetry, then substitution |
| 6, 8 | ellipse and hyperbola: semi-major axis, focal distance, vertex distance, asymptote slope |

Difficulty runs 1 to 5, and the four feature types alternate rather than sitting in blocks.
Problem 10 is the challenge: the line $y = x+1$ against $x^2+y^2=25$, followed by the
question of what the *number* of solutions says about secants, tangents and misses.

## What was verified, and what was not

The key's generated note says it exactly: **17 of the 20 answers are machine-checked with
SymPy; 3 are instructor-judged.**

- **Machine-checked (17):** every radius, centre coordinate, vertex coordinate, focal
  distance, asymptote slope and intersection point was recomputed independently. The
  completing-the-square circle in problem 9 was checked from the original coefficients, not
  from my rearrangement, and the intersection in problem 10 was confirmed to be the *complete*
  solution set.
- **Instructor-judged (3):** the justifications in **2(b)**, **5(b)** and **10(b)** — naming
  the conic and saying why, and explaining what the count of real solutions means. These are
  reasoning answers, so they are marked `---` in the Quick Answers bank rather than given a
  value, and the key states what full credit needs. In 2(b) and 5(b) the key is explicit that
  the *name alone* is only partial credit; the reason from the equation is the assessed part.

## Study guide

Four sections, each with a rule box, a worked example whose first step explains the choice of
method, and a try-it with the answer upside down inside the box: naming a conic by the sign
test, centre and radius of a circle (including from the expanded form), the vertex of a
parabola, and ellipse/hyperbola features. All 16 of its worked values are machine-verified.
