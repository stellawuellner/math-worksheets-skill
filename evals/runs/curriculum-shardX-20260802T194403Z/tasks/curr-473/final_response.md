# Differentiating Accumulation Functions with the FTC — AP Calculus AB/BC

Three PDFs are ready:

- **Worksheet** (`ws_ftcaccum_curr473.pdf`, 4 pages) — 8 problems with full work space.
- **Answer key** (`ak_ftcaccum_curr473.pdf`, 3 pages) — quick-answer bank, then a worked
  solution for each problem that names *which* form of the theorem is being used before it
  computes, plus the common slip to watch for.
- **Study guide** (`ss_ftcaccum_curr473.pdf`, 2 pages) — four rules, four worked examples,
  four try-it items.

## What the worksheet practices

All 8 problems are about accumulation functions $g(x) = \int_a^{u(x)} f(t)\,dt$; six of them
are direct FTC differentiation.

1. **Plain FTC derivative** (problems 1, 5, 7) — constant lower limit; a variable *lower*
   limit (sign flip); and one problem that evaluates the integral explicitly and then
   differentiates it, so the student sees the theorem close its own loop.
2. **Chain-rule form** (3, 8) — upper limit $x^2$; problem 8 is the synthesis challenge and
   asks for a fully simplified $g'(x)$ and then a value.
3. **Accumulated change with units** (2, 6) — inflow rates in L/min; problem 6 asks for both
   $V(10)$ and $V'(10)$ so the student has to choose between integrating and differentiating
   the same accumulation function.
4. **Reading $g$ from $f$** (4) — a table of values of $f$, and a justification of where $g$
   increases, decreases, and attains its maximum.

Difficulty ramps 1 → 5 and no subskill repeats twice in a row.

## Verification

11 checks across the 8 problems. **Ten are machine-verified with SymPy**: `eval` checks for
each FTC derivative value (including the exact $4\sqrt{65}$ and $-\ln 5$), `definite_integral`
checks for the two accumulated-volume answers, an `integrate` check and a matching `diff`
check for problem 7 (the integrate-then-differentiate pair), and an `equiv` check that
$\frac{3}{x^2}\cdot 2x$ really does simplify to $\frac{6}{x}$ in problem 8.

**One item is flagged for manual review, correctly**: problem 4 asks for a justified argument
about where $g$ increases, decreases, and peaks. That is open reasoning, so it is declared
`{"type": "manual"}` and the build ends with
`BUILD PASSED — 1 verification run(s) flagged manual-review items (exit 2)`. The answer key
gives the full three-part model argument, what to accept, and what not to accept (a zero of
$f$ without a sign change is not an extremum).

The study guide's four worked examples and four try-it answers are verified by their own
verification file, and both the key and the guide were bound back to those files problem by
problem.
