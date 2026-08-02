# Terms, Factors, Coefficients, and Degree — Algebra 1

Three PDFs for guided concept practice on reading the *structure* of a
polynomial expression rather than just computing with it.

- **Worksheet (5 pages, 10 problems).** Every problem pairs a computation with
  a structural reading, and the models are connected to notation explicitly:
  three **area/box models** the student fills in (problems 1, 2, 7 — cells are
  terms, side lengths are factors, and four cells collapse to three terms
  because two cells are like terms), a **term table** where coefficient and
  degree are read off term by term before writing standard form (3), factoring
  as "sum of terms → product of factors" (4, 8), degree behaviour under
  addition (6 — the degree drops when the leading terms cancel) and under
  multiplication (9 — degrees add), and two problems that separate the *form*
  of an expression from the expression itself (5, 10).
- **Answer key (2 pages).** Each solution shows the work and then names what
  the answer says about terms, factors, coefficients, and degree — including
  the two traps this topic reliably produces: reading the leading coefficient
  off the first term as typed rather than from standard form, and treating the
  invisible coefficient 1 or the degree-0 constant as "no coefficient".
- **Study guide (2 pages).** Four sections matching the worksheet's four
  skills, each with a rule box, a worked example whose first step states the
  strategy, and an upside-down try-it.

**Verification.** 10 of the 10 worksheet problems are machine-checked with
SymPy (`expand`, `factor`, `equiv`), and all 8 study-guide boxes are checked.
Problem 10 carries one **additional `manual` entry**: its algebra is verified,
but the "explain how one expression can be both a product of two factors and a
sum of three terms" part is open reasoning and is flagged for human review
rather than claimed as verified — that is why the run reports exit 2. The gate
chain is otherwise green, including per-problem binding of every boxed answer,
facet and skill coverage, layout, and page budgets.
