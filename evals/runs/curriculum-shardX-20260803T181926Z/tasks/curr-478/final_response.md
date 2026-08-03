Here are three PDFs on integrating rational functions with partial fractions.

**Worksheet (6 pages, 8 problems).** Every problem decomposes a rational
function with distinct linear factors and then integrates it; the work is
structured so the algebra is visible before the calculus:

- **Indefinite decompositions** (1, 2, 4) — two factors, then a linear
  numerator, then three distinct factors with three constants.
- **Definite integrals after the split** (3, 5, 7) — a marginal-cost integral in
  dollars per unit, a filter's flow rate in litres per minute, and the logistic
  separation $\int 10/[p(10-p)]\,dp$ that gives the time a population takes to
  grow from 2 to 4 thousand.
- **Improper integrals** (6, 8) — a leak rate integrated to infinity as an
  explicit limit, and a challenge on total emission that ends by asking why a
  rate decaying to zero does not by itself guarantee a finite total.

Every application states its units and its variable's meaning. Six of the eight
problems ask for an interpretation or a justification alongside the computation,
which is where the representations-and-applications framing does its work.

**Answer key (3 pages).** Each solution shows the decomposition being set up,
the root substitutions that produce each constant, the integration, and the
simplification to a single logarithm — then the boxed exact answer. Closing
notes cover the errors this topic actually produces: putting a coefficient
inside its logarithm, taking the limit of $\ln b - \ln(b+2)$ separately and
reaching an $\infty - \infty$, and forgetting to check the degree before
splitting. The quick-answer bank at the top gives every final answer at a
glance.

**Study guide (2 pages).** Three sections — the split itself, definite integrals
after the split, and improper integrals — each with a rule box, a worked example
whose first step names the strategy, and a try-it with the answer upside down
inside the box. The watch-out box carries the coefficient-outside-the-logarithm
rule and the convergence caution.

**Verification.** All 13 machine-checkable quantities across the 8 problems were
confirmed with SymPy: each decomposition was checked as an algebraic identity,
each antiderivative was differentiated back to its integrand, each definite and
improper integral was recomputed, and the two limits were evaluated
independently. All 6 study-guide boxes were verified the same way. Nothing is
flagged for manual review.

Standard tagged: FUN-6.D–FUN-6.E. Difficulty ramps 1 to 5 across the sheet.
