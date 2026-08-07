# Interpreting the solution of a system on a graph — Algebra 1

Three PDFs are ready:

- **Study guide** (`ss_sysgraph_curr261.pdf`, 2 pages) — three sections: what a solution *is*
  (the one point on both lines, and why a point on only one line does not count), how to tell one
  solution from none or infinitely many by comparing slopes and intercepts, and how to graph a
  system to solve it. Each has a rule box, a worked example that opens with the strategy sentence,
  and a try-it with the answer printed upside down inside the box.
- **Worksheet** (`ws_sysgraph_curr261.pdf`, 5 pages) — 10 problems, difficulty 1 → 5. Every problem
  carries its own coordinate grid: seven have the lines already drawn and labelled $A$ and $B$ for
  the student to read, three are empty grids to graph on. The set covers all three cases —
  crossing once, parallel (problem 3), and one line drawn twice (problem 6, where solving
  $4x + 2y = 8$ for $y$ reveals it is the first equation again). Two problems are modelling
  contexts (gym memberships, van rentals) where the crossing point is a break-even point.
- **Answer key** (`ak_sysgraph_curr261.pdf`, 3 pages) — each problem worked both graphically and
  algebraically so the two readings confirm each other, plus a Quick Answers bank and a Curriculum
  block (HSA-REI.C.6, difficulty 1–5).

## What is verified, honestly

- **10 checks are machine-verified.** Every ordered-pair solution was recomputed by SymPy against
  *both* equations of its system — including problem 3, where SymPy independently confirms the
  system is inconsistent and has no solution at all, and problem 6(a)'s rearrangement.
- **5 of the 10 problems (3, 6, 8, 9, 10) carry an instructor-judged part** alongside their
  verified one: "explain why the lines never meet", "why is a point on one line not a solution",
  "which plan is cheaper after the crossing". Those are prose, and no program grades prose. The
  answer key prints a rubric for each — what a full-credit response must say, and what earns half
  credit — and the Quick Answers bank marks them `—` rather than claiming they were checked.
- The other 5 problems (1, 2, 4, 5, 7) are fully machine-checked.
- No blanks are marked as working space. Problem 10(a) asks the student to draw the two lines; a
  drawing is its own answer, so it carries no separate answer blank.

The grade level prints on the answer key only.
