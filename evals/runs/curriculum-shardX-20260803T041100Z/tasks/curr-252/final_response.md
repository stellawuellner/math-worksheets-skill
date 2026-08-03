# Adding, Subtracting, and Multiplying Polynomials (Algebra 1)

Three PDFs are ready.

- **Worksheet** (`ws_polynomial_ops_curr252.pdf`, 5 pages) — 12 problems in a
  procedural-fluency format. The directions box states the three rules the
  whole sheet runs on (like terms, distributing the minus sign, adding
  exponents when multiplying). Problems 1–4 are the warm-up, one of each
  operation; after that the four methods are interleaved so the student must
  decide what each expression calls for. No skeleton repeats: problem 5 has
  missing degrees, problem 6 cancels two of its four terms and asks the student
  to say which and why, problems 8 and 9 move to two variables (where
  "like terms" gets its real test), problem 10 is an error-analysis item on
  $(x-3)^2 \neq x^2-9$, problem 11 asks for a product and then a substitution,
  and the closing challenge multiplies a binomial by a trinomial and subtracts
  a second product.
- **Answer key** (`ak_polynomial_ops_curr252.pdf`, 3 pages) — a quick-answer
  bank for fast grading, then a full worked solution per problem: the
  rewritten-as-addition line for every subtraction, all four products written
  out before combining, and the boxed answer in standard form. Four problems
  carry a grading note naming the exact wrong expression a specific
  misconception produces.
- **Study guide** (`ss_polynomial_ops_curr252.pdf`, 2 pages) — four sections,
  each with a rule box, a worked example whose first line says *why* that
  method applies, and a try-it with the answer printed upside down inside the
  box. The framing sentence is the one a student can carry into the worksheet:
  adding and subtracting is about matching terms, multiplying is about pairing
  them, and the exponent rules are opposite in the two cases.

## Verification

All 12 worksheet answers are machine-verified with SymPy: 10 through the
`expand` checker (SymPy expands the stated expression and confirms it is
identical to the key's printed answer), 1 through `equiv` (the error-analysis
problem, where the point is that $(x-3)^2$ and $x^2-6x+9$ are the same function
while $x^2-9$ is not), and 1 through `eval` (product evaluated at $x=2$).
Nothing is flagged manual.

One misconception trap is declared and machine-checked: on problem 11 the
classmate's reported value of $-2$ is computed from the wrong method
($3x\cdot x - 2\cdot 7$, i.e. FOIL with the outer and inner products skipped),
and the verifier confirms the problem's own check rejects it. It prints in the
key's "common wrong answers" block.

All 8 study-guide items (4 worked examples + 4 try-its) are verified the same
way, and each of the four worksheet facets has a matching worked example.

**Standard used:** `HSA-APR.A.1`, taken verbatim from
`references/standards-map.md` (row "Polynomial arithmetic/factoring").

## Build

Green on the first build — all 21 gates pass, including the per-problem
answer-key binding and the page budget (worksheet 5 pages, key 3, guide 2
against its hard 2-page cap).
