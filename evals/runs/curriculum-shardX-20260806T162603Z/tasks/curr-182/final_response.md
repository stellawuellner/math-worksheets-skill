Here are the three PDFs for the Grade 7 one-step-inequality fluency set.

- **Worksheet** (`ws_onestep_ineq_curr182.pdf`) — 12 inequalities, each solved
  in one step and then graphed on its own number line, printed under the
  problem so the graph never gets orphaned from the question. The ramp is
  deliberate: two adding/subtracting warm-ups, then dividing by a positive,
  then the cases that catch people — a boundary that comes out negative from two
  positive givens ($n + 9 > 2$), a positive divisor with a negative answer
  ($7w < -21$, where the sign must *not* turn), the letter on the right-hand
  side ($15 \ge 3r$), and four items where dividing by a negative genuinely does
  turn the sign around. No two problems share a skeleton.
- **Answer key** (`ak_onestep_ineq_curr182.pdf`) — Quick Answers bank,
  generated Curriculum section (7.EE.B.4, difficulty 1–5), and for each problem
  the one step taken, why the sign did or did not turn, and a description of the
  correct graph (open or filled circle, which way it shades) with a test value
  where the reasoning is easy to get wrong.
- **Study guide** (`ss_onestep_ineq_curr182.pdf`) — three sections: undoing an
  addition, dividing by a positive, dividing by a negative. Each has the rule,
  the open-vs-filled circle rule, a two-step worked example that ends with the
  graph described, and a try-it. The negative-divisor section explains *why* the
  sign turns (2 < 5 but −2 > −5), and the watch-out separates "the divisor is
  negative" from "the answer is negative".

**What is verified — read this carefully, because the key's own note says
"0 of 12 problems fully machine-checked" and that is easy to misread.** Each
problem asks for **two** responses: the solution, and the graph of it. That is
24 responses in all.

- **12 are machine-checked** with SymPy: every solution set is recomputed with
  `solveset` over the reals from the inequality itself and compared with the
  declared interval, so a wrong boundary *or a wrong strictness* fails the
  build. All twelve passed.
- **12 are instructor-judged**: the drawings. No checker can read a hand-drawn
  number line, so each carries a rubric in the key naming the boundary, whether
  the circle is open or filled, and which way it shades — plus, on problem 12, a
  third instructor-judged response asking the student to justify the
  turned-around sign by testing a number from their own graph.

So "0 of 12 *problems* fully machine-checked" means no problem is
machine-checked *end to end* — every one has a drawing in it. The algebra on all
twelve is verified. All six study-guide checks are machine-verified too.
