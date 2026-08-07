# Distributive structure in context — Algebra 1

Three PDFs are ready:

- **Study guide** (`ss_distrib_curr253.pdf`, 2 pages) — three sections: distributing a factor,
  taking a common factor out, and choosing between the two forms depending on what the question
  asks. Each has a rule box, a worked example set in a real measurement context whose first step
  says *why* that direction was chosen, and a try-it with the answer upside down inside the box.
  The watch-out box covers the minus-in-front-of-a-bracket slip.
- **Worksheet** (`ws_distrib_curr253.pdf`, 5 pages) — 10 applied problems, difficulty 1 → 5. Every
  quantity carries its unit and the answer blanks name the unit expected (metres, square metres,
  square centimetres, or dollars). Contexts are kept lean on purpose — a dog run, a hallway, a
  patio, a stall's profit, a metal sheet — with no decorative numbers that the mathematics does
  not use. The last problem is the synthesis: write one area in both forms, then decide which form
  answers the workshop's question.
- **Answer key** (`ak_distrib_curr253.pdf`, 4 pages) — full reasoning per problem, a Quick Answers
  bank, and a generated Curriculum block (HSA-APR.A.1 and HSA-SSE.B.3, difficulty 1–5).

## What is verified, honestly

- **7 of the 10 problems are fully machine-checked** by SymPy — every expansion, factorisation and
  rewrite was recomputed independently of the key before anything compiled. The units are checked
  too, in both directions: a declared unit that the sheet does not print, or a unit printed on the
  key that the data never declared, fails the build.
- **3 problems (4, 8, 10) are part machine-checked, part instructor-judged.** In each, the
  computed part is verified and the "say which form shows it, and why" part is prose that no
  program can grade. Those parts are flagged for you and the key prints the rubric — what a
  full-credit answer must name, and what earns half credit. The Quick Answers bank shows them as
  `—` rather than as verified values.
- No blanks are marked as working space on this sheet; every printed blank is an answer.

The grade level prints on the answer key only, beside the standards codes.
