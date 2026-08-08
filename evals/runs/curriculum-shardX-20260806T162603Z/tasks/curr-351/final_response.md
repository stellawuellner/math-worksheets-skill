# Powers of $i$ and the Complex Plane — Algebra 2 concept set

Three PDFs are ready:

- **`ss_ipowers_curr351.pdf` — Skills Summary (2 pages).** Three sections, each
  with a rule box, a worked example and a try-it whose answer is printed upside
  down inside the box: the four-step cycle of powers of $i$, points and
  distances on the plane (with a small plotted diagram), and multiplying by $i$
  as a quarter turn. A watch-out box names the sign slip that costs the most
  marks — reading a remainder of 2 as $+1$.
- **`ws_ipowers_curr351.pdf` — Student worksheet (5 pages), 10 problems.**
  The sheet is built on two models and keeps returning to them: a cycle table
  the student completes in problem 1, and four blank complex planes to plot on.
  Every problem exercises either a power of $i$ or the plane (usually both) —
  simplifying $i^{27}$, plotting $z$, $-z$ and $2z$, finding a distance from the
  origin, and reading $i$, $i^2$ and $i^3$ as one, two and three quarter turns.
  Difficulty runs 1 → 5.
- **`ak_ipowers_curr351.pdf` — Answer key (3 pages).** Each solution shows the
  reduction step (for example $i^{27} = (i^4)^6 \cdot i^3$) rather than a bare
  value, and each plotting problem lists the coordinates that must appear on the
  grid. The Quick Answers bank, curriculum block (HSN-CN.A.1 and HSN-CN.B.4)
  and a "Common wrong answers" note sit at the top.

## What is verified, and what is not

The set carries **19 declared responses across 10 problems. 14 are machine
checked** — every power, product and distance was recomputed independently with
SymPy, and the build refuses to emit a PDF if a printed answer disagrees. The
study guide's three worked examples and three try-it answers were verified the
same way.

**5 responses are instructor-judged**, and the answer key prints `---` for them
rather than a value. They fall into two kinds:

- **Plotted work (problems 3, 5, 7, 10).** A drawn point is not something a
  computer algebra system can check. For each one the key lists the exact
  coordinates that should appear, and tells you to grade the plot against the
  value the student wrote in the algebra part, so plotting is scored separately
  from arithmetic.
- **Written reasoning (problems 5, 8, 10).** "Describe what multiplying by $i$
  did", "explain why two quarter turns negate both parts", "justify why three
  turns is $i^3$". The key states what full credit requires in each case — in
  every one, the answer must connect the algebra to a turn about the origin, not
  just recite $i^2 = -1$.

## Notes

- One misconception trap is declared and machine-checked to be distinguishably
  wrong: reducing an exponent modulo 4 correctly but then reading a remainder of
  2 as $+1$. It is printed in the key's "Common wrong answers" block.
- The grade level appears on the answer key only.
