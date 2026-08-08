# Adding, subtracting and multiplying polynomials — Algebra 1

Three PDFs are ready:

- **Study guide** (`ss_polyops_curr252.pdf`, 2 pages) — one section per operation. Each has a rule
  box, a worked example whose first line says *why* that method applies before any arithmetic, and
  a try-it with the answer printed upside down inside the box. The watch-out box flags the single
  most common error on this topic: writing $(2x+3)^2$ as $4x^2 + 9$.
- **Worksheet** (`ws_polyops_curr252.pdf`, 4 pages) — 12 problems on a clean ramp from difficulty 1
  to 5, with no two problems built on the same skeleton. It opens with a short "pattern to copy"
  panel (add, subtract, multiply, one line each), then interleaves the three operations so the
  student has to decide which rule applies rather than repeating one. Deliberate hard spots:
  problem 9 reverses the order ("subtract A from B"), problem 10 is a binomial times a trinomial
  (six products), problem 11 mixes a square with a difference of squares, and problem 12 is the
  synthesis — perimeter, area, and why one keeps its degree while the other does not.
- **Answer key** (`ak_polyops_curr252.pdf`, 4 pages) — every problem worked step by step with the
  reasoning named, plus a Quick Answers bank and a generated Curriculum block (HSA-APR.A.1,
  difficulty 1–5).

## What is verified, honestly

- **11 of the 12 problems are fully machine-checked.** Every sum, difference and product on the
  sheet was recomputed independently by SymPy against the answer key before anything compiled, so
  a wrong answer could not have reached the PDF.
- **Problem 12 is part machine-checked, part instructor-judged.** Its (a) perimeter and (b) area
  are verified; its (c) asks the student to explain why adding keeps the degree at 1 while
  multiplying raises it to 2. No program grades a sentence, so that part is flagged for you and
  the answer key prints the rubric: full credit contrasts the two operations, half credit names
  the degrees without the reason. The Quick Answers bank shows it as `—` rather than a value.
- No blanks on this sheet are marked as working space — every printed blank is an answer, and
  every one of them except 12(c) is machine-verified.

The grade level does not print on the worksheet or the study guide; it appears on the answer key,
next to the standards code.
