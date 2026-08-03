# Adding, subtracting, and multiplying higher-degree polynomials (Algebra 2)

Three PDFs, all gated:

- **Worksheet** `ws_poly_arithmetic_curr356.pdf` — 10 guided concept-practice
  problems, 6 pages. Every problem carries the model that matches its
  operation: a **like-terms column table** (one column per power) for the sums
  and differences, and an **area box** (rows = terms of one factor, columns =
  terms of the other) for the products, plus 3.5–4.5 cm of work space and an
  answer line.
- **Answer key** `ak_poly_arithmetic_curr356.pdf` — quick-answer bank plus a
  full solution per problem with the model *filled in*, so a student can
  compare cell by cell rather than only comparing the final polynomial.
- **Study guide** `ss_poly_arithmetic_curr356.pdf` — 2 pages, four skill
  sections (add by like terms · subtract by distributing the minus · multiply
  with an area box · check a product two ways), each with a rule box, a
  strategy-first worked example, and a distinct try-it.

## Facet plan

`add-polynomials` (2), `subtract-polynomials` (2),
`multiply-binomial-by-polynomial` (3), `multiply-and-verify` (3). The subtitle
is composed from that list and bound verbatim to the title block. Max
same-facet run: 2, so after the two warm-up sums the student must decide which
model applies.

## Verification

- Worksheet JSON: **10 of 10 machine-verified**, 0 manual — six `expand`
  (sums, differences, and products, all checked against SymPy's own
  expansion), one `eval` (substitution check at $x = 2$), one `factor`
  (factoring the product back), one `equiv` (the corrected square), covering
  all four requested targets `expand`/`factor`/`eval`/`equiv`.
- Study-guide JSON: **8 of 8 machine-verified** (4 examples + 4 try-its).
- **1 trap declared, confirmed distinguishable**: distributing only the $x$
  through the trinomial and never the $+3$, which evaluates to 10 instead of 25
  at $x = 2$. It prints in the key's "common wrong answers" block, and problem 6
  is deliberately the substitution check that would catch it.
- Two problems are error-analysis by design: problem 6 (does the claimed
  expansion survive a substitution?) and problem 10 ($(x^3-2)^2 = x^6 - 4$,
  where squaring was distributed across a subtraction and both cross terms were
  dropped).
- Difficulty ramp `[1, 1, 2, 2, 2, 3, 3, 3, 4, 4]`; standard
  `HSA-APR.A.1, HSA-SSE.B.3` taken verbatim from
  `references/standards-map.md`.

`BUILD PASSED` — all 21 gates green, first attempt. Worksheet prose match rate
41/42; the residual study-guide flags are intermediate values printed inside
the worked examples (the $-12x$ cell, the $27 + 9 - 30 + 8$ substitution), the
expected false-flag class.
