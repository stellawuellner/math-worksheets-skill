# Polynomial Arithmetic — Algebra 2 concept set

Three PDFs are ready:

- **`ss_polyarith_curr356.pdf` — Skills Summary (2 pages).** Three sections with
  a rule box, a worked example and a try-it: adding and subtracting like terms,
  the box (area) model for a product, and checking a product by degree and by
  substituting a number. The watch-out box names the two errors that account for
  most lost marks — a missing cell in the box, and a subtraction sign that
  reached only the first term.
- **`ws_polyarith_curr356.pdf` — Student worksheet (5 pages), 10 problems.**
  The model is stated once at the top with a worked $(x+2)(x^2+3x)$ box, then
  three problems supply a partly-filled box for the student to complete before
  collecting — so the visual model and the standard-form notation stay attached
  to each other. The rest are additions, subtractions and an area application
  (a garden bed measured in metres, answered in m$^2$). Difficulty runs 1 → 5.
- **`ak_polyarith_curr356.pdf` — Answer key (3 pages).** Each solution lists the
  partial products before collecting, and points out the structure where there
  is one (difference of cubes on problem 6, $A^2 - B^2$ on problem 8). The Quick
  Answers bank and the curriculum block (HSA-APR.A.1) sit at the top.

## What is verified, and what is not

The set carries **12 declared responses across 10 problems. 11 are machine
checked** — every expansion was re-expanded independently with SymPy and
compared as a symbolic identity, so a dropped term or a sign error cannot reach
the PDF. The declared unit on the garden problem (m$^2$) is bound in both
directions: the worksheet's answer line and the key's boxed answer must both
carry it. The study guide's three worked examples and three try-its are verified
the same way.

**1 response is instructor-judged** — problem 10(b), explaining how the degree
of a product relates to the degrees of its factors and why a subtraction can
lower the degree. That is a written argument, so the key prints `---` for it and
gives the rubric instead: full credit needs the sum-of-degrees rule *and* the
observation that the cubic and quadratic terms cancelled.

## Notes

- No misconception traps are declared on this sheet. The verification type used
  for a polynomial identity (`expand`) has no single comparable value, so the
  trap mechanism does not apply to it; the two classic errors are instead
  addressed directly in the study guide's watch-out box and in problem 10, which
  is built so that careless subtraction gives a visibly wrong degree.
- The grade level appears on the answer key only.
