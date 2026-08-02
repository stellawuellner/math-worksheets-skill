# Radical Equations and Extraneous Roots — Algebra 2

A representations-and-applications workshop: every problem either solves a
radical equation or tests a candidate root, and the checking step is treated
as part of solving rather than an optional afterthought.

- **Worksheet (5 pages, 10 problems).** The header states why checking is
  mandatory (squaring is not reversible: `a = b` implies `a² = b²`, but the
  converse only gives `a = ±b`). Problems 1 and 9 are isolate-and-square (the
  last with two radicals, requiring two squarings); 3, 7 and 10 are explicit
  extraneous-root work — substitute each candidate and report the value of the
  original difference; 7 is the equation `√(x−2) = −3` with **no real
  solution**, where squaring manufactures a root out of nothing; 10 supplies a
  **table representation** of both sides at both candidates and asks the
  student to explain the extra intersection the squared equation creates.
  Problems 5 and 6 are applied models with stated givens and units — free fall
  `t = √(h/16)` (h in **ft**, t in s) and skid length `s = √(24x)` (s in mph,
  x in **ft**) — each solved as a radical equation, not by plugging in. Both
  units are declared in the verify data and bound to the sheet's answer lines.
  Problems 2 and 8 connect radical and rational-exponent form.
- **Answer key (2 pages).** Each solution shows the algebra, the substitution
  check, and *why* a rejected candidate is extraneous (the non-radical side is
  negative there). Problem 10's explanation is worked graphically as well:
  `y = √(x+5)` never dips below the axis, so it can meet `y = x−1` only where
  the line is non-negative; squaring replaces the line with a parabola that is
  non-negative on both sides.
- **Study guide (2 pages).** Four sections — isolate-and-square,
  check-extraneous, rational-exponent-form, radical-model-application — each
  with a method box, a worked example opening with a strategy sentence, and an
  upside-down try-it. It includes the fast filter that decides most extraneous
  roots without arithmetic: a candidate making the non-radical side negative
  cannot be a solution.

**Verification.** All 10 worksheet problems are machine-checked by SymPy
across 17 checks: the true solution set of each radical equation, the roots of
the corresponding squared equation, and the substitution value that proves a
candidate extraneous (e.g. `√(x+6) − x = 4` at `x = −2`, so it fails). The
empty solution set of problem 7 is verified as empty. All 8 study-guide boxes
are checked. Nothing is flagged manual, and the whole gate chain is green.

**One authoring note.** `references/standards-map.md` has no code for radical
equations or rational exponents, so rather than inventing one (the natural
code would be HSA-REI.A.2), the problems carry the nearest codes the map
actually lists, verbatim: `HSA-REI.B.4` for the equation-solving problems —
squaring produces the quadratic that is solved — and `HSA-SSE.B.3` for the
rational-exponent rewriting.
