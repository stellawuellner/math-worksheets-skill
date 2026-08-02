# The Rational Root Theorem — Algebra 2 (curr-362)

Three PDFs are ready:

- **Worksheet** (`ws_rrt_curr362.pdf`, 6 pages) — 12 problems built as a fluency
  ladder. Problems 1–2 walk the whole routine on one polynomial (test a
  candidate, then divide it out and finish), and from there the skeletons keep
  changing rather than repeating: factor completely over the integers, a
  leading coefficient of 2 or 3 that puts halves and thirds on the candidate
  list, a cubic whose leftover quadratic is irrational, a quartic that needs the
  routine run twice, and one whose remaining zeros are non-real. It ends with a
  synthesis question about what the theorem does *not* prove.
- **Answer key** (`ak_rrt_curr362.pdf`, 3 pages) — a quick-answer bank, then for
  every problem: the candidate list, which candidate was tested and what it
  gave, the division result, and the boxed zeros or factorization. Several
  solutions add the idea behind the step — why $\frac12$ pairs with the factor
  $(2x-1)$, why the theorem could not produce $1 \pm \sqrt3$, and a
  product-of-zeros check on problem 2.
- **Study guide** (`ss_rrt_curr362.pdf`, 2 pages) — four sections (build and
  test the candidate list, find all rational zeros, factor completely, finish
  the non-rational leftovers), each with a rule box, a worked example that names
  the strategy first, and a try-it with the answer printed upside down. The
  watch-out box flags the two errors that cost the most marks: reading "no
  rational zero" as "no zero", and putting the divisors of the leading
  coefficient on top.

## Verification

11 of the 12 worksheet problems are machine-verified with SymPy: 2 `eval` checks
(candidate tests, both giving 0), 4 `zeros` checks (including one over the
complex domain so the full root set is required, and one with irrational roots
in exact form), 1 `solve`, and 3 `factor` checks (each factorization confirmed
equivalent to the original polynomial).

Problem 12 is flagged **manual review** and is correct to flag: it asks the
student to explain why exhausting the candidate list of $x^3-3x-1$ does not rule
out a real zero, and to give evidence of one. No CAS can grade that argument.
The answer key prints a model response with the two points that must appear
(the theorem is about rational zeros only; a sign change between $x=-1$ and
$x=0$ forces a real zero) plus what to accept and what not to.

All 8 study-guide items (4 worked examples + 4 try-its) are machine-verified.
The build ended green on the first run, exit 2 for the single manual item.
