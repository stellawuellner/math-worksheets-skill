# Binomial Coefficients and Sequence Structure in Expansions (Algebra 2)

Three PDFs are ready for an Algebra 2 student on sequences, series and the
binomial theorem, focused on using binomial coefficients and sequence structure
in expansions. The sheet is an interleaved review: after a two-problem warm-up
the four subskills rotate, so the method has to be chosen each time rather than
repeated.

- **Worksheet (7 pages, 12 problems).** Two warm-ups on evaluating
  $\binom{n}{r}$ (the second is a small find-and-fix: a classmate answers 72, and
  the student has to say what 72 counts). Then the rotation: full expansions of
  $(x+3)^3$, $(2x-1)^4$ and $(a+2b)^3$; single-term extractions from $(x+4)^5$,
  $(3+y)^6$ and $(2x+y)^5$, each designed so the binomial coefficient alone is
  the wrong answer; row-sum and coefficient-sum problems that expose the $2^n$
  and $(1+c)^n$ structure; a solve-for-$n$ problem from $\binom{n}{2} = 45$ that
  has two algebraic roots and one admissible answer; and a synthesis on
  $(3x-2)^4$ whose coefficient sum is 1. A **value-free** Pascal's-triangle
  reference sits with the directions, captioned so it cannot be mistaken for any
  problem's givens. Work space is 6–8.5 cm, declared as `workspace_cm` so the
  page budget charges for the expansions the sheet actually asks to be written
  out. The facet mix is 3/3/3/3 with a maximum same-facet run of 1.
- **Answer key (3 pages).** Three labelled steps per problem — choose the tool,
  evaluate both pieces, collect and check — plus the generated quick-answer bank
  and a **"Common wrong answers"** block covering all seven declared traps.
- **Study guide (2 pages).** Four skills matching the four facets: binomial
  coefficients, full expansion, one specific term, and the structure of a row.
  Each has a formula box, a two-step worked example opening with a strategy
  sentence, and an upside-down try-it.

## Verification

All 12 worksheet problems are machine-checked with SymPy: 7 `eval` coefficient
and structure computations, 3 `expand` identities, 1 `series` row sum, and 1
`solve`. All 8 study-guide boxes (4 worked examples + 4 try-its) are verified the
same way. **Nothing is flagged manual** and no tolerance was widened.

**Seven misconception traps are declared and machine-checked**: the permutation
count instead of the combination (72), the binomial coefficient reported alone
(10), doubling the row number instead of raising two to it (12), leaving the
constant unraised in two different terms (45 and 20), applying the plain $2^n$
row sum to a binomial whose second term is not 1 (32), and ignoring the minus
sign in $(3x-2)^4$ before raising (625). Verification proves each is a value the
problem's own check rejects, so every one of those items genuinely discriminates
its error.

The facet plan is bound to the printed subtitle, every worksheet facet has a
study-guide worked example, and worksheet prose numbers bind 29/31 to the JSON
givens. Standards are tagged `HSA-APR.C.5` — the binomial-theorem row of
`references/standards-map.md`, verbatim; no code was invented. Full gate chain
green — exit 0, no manual items.
