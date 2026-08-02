Three PDFs are ready for an Algebra 2 student on sequences, series and the
binomial theorem, focused on using binomial coefficients and sequence structure
in expansions.

- **Worksheet** (12 problems, `ws_binomial_curr395.pdf`) — a two-problem warm-up
  on evaluating $\binom{n}{k}$, then the four subskills interleaved so the method
  has to be chosen each time: full expansions of $(x+2)^3$, $(2x-1)^4$ and
  $(a+3b)^3$; single-term extractions from $(x+2)^5$, $(3+y)^6$ and $(2x+y)^5$
  (each one designed so the binomial coefficient alone is the wrong answer); row
  sums and coefficient sums that expose the $2^n$ and $(1+c)^n$ structure; a
  solve-for-$n$ problem from $\binom{n}{2} = 45$; and a synthesis on $(3x-2)^4$
  that ends by explaining why the coefficients must sum to 1. A value-free
  Pascal's-triangle reference sits with the directions, not with any problem.
- **Answer key** (`ak_binomial_curr395.pdf`) — three labelled steps per problem
  (choose the tool, evaluate the two pieces, collect/check), a quick-answer bank,
  and a generated "Common wrong answers" block covering the four declared traps
  (permutation instead of combination, coefficient without the constant's power,
  wrong power on the constant, and 2 left unraised inside $2x$).
- **Study guide** (2 pages, `ss_binomial_curr395.pdf`) — four skills matching the
  worksheet's facets: binomial coefficients, full expansion, one specific term,
  and the structure of a row of coefficients. Each has a formula box, a two-step
  worked example, and an upside-down try-it, plus a watch-out on when
  $\binom{n}{k}$ *is* the coefficient and when it is only half of it.

**Verification.** All 12 worksheet answers are machine-checked with SymPy
(5 `eval` coefficient computations, 3 `expand` identities, 3 `series` sums, and
1 `solve`), and all 8 study-guide results are verified the same way. Nothing is
flagged manual. Four misconception traps were declared and proved distinguishably
wrong. The facet plan is bound to the printed subtitle and every worksheet facet
has a study-guide worked example. Full gate chain green on the first build.

*Note on the standards tag:* `references/standards-map.md` has no binomial-theorem
entry, so problems carry `HSA-APR.A.1` (polynomial arithmetic) and, for the
structure/sum problems, `HSA-SSE.B.3` — both verbatim from that file. No code was
invented.
