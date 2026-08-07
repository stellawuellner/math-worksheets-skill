# Dividing Complex Numbers — Algebra 2 workshop set

Three PDFs are ready:

- **`ss_cxdivide_curr353.pdf` — Skills Summary (2 pages).** Three sections,
  each with a rule box, a worked example, and a try-it whose answer is printed
  upside down inside the box: dividing by a pure imaginary number, dividing by
  a complex binomial, and reading a quotient in an applied setting (voltage
  divided by impedance). A watch-out box names the single most common error —
  multiplying by the denominator instead of its conjugate.
- **`ws_cxdivide_curr353.pdf` — Student worksheet (6 pages), 10 problems.**
  Every problem is a division, and the conjugate is the tool in every one. Three
  problems are applied: two AC-circuit quantities with their units stated in the
  stem and printed on the answer line (amps, ohms), and one that undoes a
  complex-plane transformation and asks the student to plot the result on a
  labelled grid. Difficulty runs 1 → 5, ending with a sum of two conjugate
  quotients that comes out real.
- **`ak_cxdivide_curr353.pdf` — Answer key (3 pages).** Each solution names the
  conjugate, shows the multiplied-out numerator and denominator, and then
  divides — the three places students actually go wrong. The Quick Answers bank
  at the top gives the column at a glance, followed by the curriculum block
  (HSN-CN.A.3 with HSN-CN.B.4 on the complex-plane problem) and a "Common wrong
  answers" note.

## What is verified, and what is not

The set carries **12 declared responses across 10 problems. 10 are machine
checked** — each quotient was recomputed independently with SymPy, and the build
refuses to emit a PDF if any printed answer disagrees. The two declared units
(amps on problem 5, ohms on problem 8) are bound in both directions: the
worksheet's answer line and the key's boxed answer must carry the same unit the
JSON declares. The study guide's three worked examples and three try-it answers
are verified the same way.

**2 responses are instructor-judged**, and the answer key prints `---` for them
rather than a value:

- **Problem 7(b)** — plotting the recovered point on the complex plane and
  labelling the axes. The key tells you to grade the plot against whatever value
  the student wrote in part (a), so the plotting skill is scored separately from
  the arithmetic.
- **Problem 10(b)** — justifying in writing why the sum of the two quotients had
  to be real. The key states what full credit requires: naming the two quotients
  as conjugates, and saying that a number plus its conjugate cancels the
  imaginary parts.

No computer algebra system can grade a drawn point or a written argument, so the
sheet does not claim to.

## Notes

- Two misconception traps are declared and machine-checked to be distinguishably
  wrong: using $3i$ where the conjugate $-3i$ was needed (problem 3), and
  multiplying by the denominator itself instead of its conjugate (problem 4).
  Both are printed in the key's "Common wrong answers" block.
- The grade level appears on the answer key only; nothing the student holds is
  labelled with a level.
