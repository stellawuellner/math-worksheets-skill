# Adding, Subtracting, and Multiplying Complex Numbers (Algebra 2)

Three PDFs are ready.

- **Worksheet** (`ws_complex_arith_curr352.pdf`, 5 pages) — 12 problems in a
  procedural-fluency format. The directions box states the one fact the whole
  sheet turns on ($i^2=-1$) and the period-4 cycle of powers of $i$. Problems
  1–4 are the warm-up (one sum, one difference, monomial times binomial,
  binomial times binomial); after that the four methods are interleaved. No
  skeleton repeats: problem 5 is a single power of $i$, problem 6 chains three
  numbers and asks what happened to the imaginary parts, problem 7 is a
  conjugate pair and asks *why* the answer is real, problem 8 is a square,
  problem 9 sums two powers with different remainders, problem 10 solves a
  quadratic with negative discriminant, problem 11 is a three-factor product,
  and the closing challenge multiplies $\bigl(x-(5+i)\bigr)\bigl(x-(5-i)\bigr)$
  and asks why the coefficients came out real.
- **Answer key** (`ak_complex_arith_curr352.pdf`, 3 pages) — a quick-answer
  bank, then a worked solution per problem showing all four products before
  the $i^2$ substitution, the substitution on its own line, and the boxed
  answer in standard form $a+bi$. Three problems carry a grading note naming
  the exact wrong number a specific misconception produces (21 on problem 7
  means $i^2$ was read as $+1$; 25 on problem 8 means each term was squared
  separately).
- **Study guide** (`ss_complex_arith_curr352.pdf`, 2 pages) — four sections
  (add/subtract, multiply, powers of $i$, complex solutions), each with a rule
  box, a worked example whose first line says *why* that method applies, and a
  try-it with the answer printed upside down inside the box.

## Verification

All 12 worksheet problems are machine-verified with SymPy — 13 checks in total,
since problem 12 asks for both a product and its zeros and therefore carries
two entries under one problem id. Nine `eval` checks recompute the complex
arithmetic symbolically (the operands are passed as named givens, so the
checker sees the same numbers the stem prints), one `solve` and one `zeros`
check run in the complex domain (`"domain": "complex"`, which requires the full
conjugate-pair root set rather than silently dropping non-real roots), and one
`expand` check confirms the synthesis product. Nothing is flagged manual.

One misconception trap is declared and machine-checked: on problem 7 the value
21 is what $(5+2i)(5-2i)$ becomes if $i^2$ is treated as $+1$, and the verifier
confirms the problem's own check rejects it. It prints in the key's "common
wrong answers" block.

All 8 study-guide items (4 worked examples + 4 try-its) are verified the same
way, and each of the four worksheet facets has a matching worked example.

**Standards used:** `HSN-CN.A.1–A.3` for the arithmetic problems and
`HSN-CN.C.7–C.9` for the two complex-solution problems, both taken verbatim
from `references/standards-map.md`.

## Build

One gate failed on the first attempt: `facet-coverage` rejected the declared
subtitle because the worksheet printed "powers of $i$" (math italic) where the
JSON said "powers of i" — the binding is a verbatim string match, so the
`$…$` broke it. Rewording both sides to "powers of the imaginary unit" fixed
it. The second build is green on all 21 gates, including the per-problem
answer-key binding and the page budget (worksheet 5 pages, key 3, guide 2
against its hard 2-page cap).
