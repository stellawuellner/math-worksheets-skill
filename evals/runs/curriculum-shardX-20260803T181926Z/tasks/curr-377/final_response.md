# Properties of Logarithms — Algebra 2 practice set

Three PDFs are ready:

- **`ss_logprops_curr377.pdf` — Skills Summary (2 pages).** Three sections, each
  with a rule box, a worked example, and a "try it" whose answer is printed upside
  down inside the box: (1) **expanding** a logarithm into separate terms,
  (2) **condensing** several terms into a single logarithm — including the rule that
  coefficients must be dealt with first — and (3) **evaluating and solving** with the
  properties, with the reminder to check that every original argument stays positive.
  The first formula box states all three properties (product, quotient, power) in one
  place; a watch-out box names the two classic errors, `log M + log N = log(M+N)` and
  `2 log 3 = log 6`.
- **`ws_logprops_curr377.pdf` — Student worksheet (4 pages), 12 problems.** Every
  problem on the sheet turns on the product, quotient, or power property. The four
  strands — evaluate, expand, condense, solve — are rotated rather than blocked, so
  the student has to decide which direction to read the properties in. It opens with
  `log₂8 + log₂4` and finishes with three multi-step items: approximating `log 48`
  from `log 2` and `log 3` alone, a two-part condense-then-evaluate, and
  `3 log₂ x = log₂ 27`. Problems 8 and 11 are two-part (expand/condense, then
  evaluate at given values). Difficulty ramps 1 → 4; each problem has 4–6 cm of work
  space and its own answer line.
- **`ak_logprops_curr377.pdf` — Answer key (3 pages).** Each solution names the
  property used at each step rather than just producing the number, and the two
  solve-type problems explicitly check the domain condition so extraneous solutions
  are part of the taught method. It opens with a quick-answer bank and a generated
  Curriculum section (HSF-BF.B.5 for the property work, HSF-LE.A.4 for the equations)
  with the difficulty range, and prints one "common wrong answer" note: `0.575`, the
  result of multiplying `4 log 2` by `log 3` instead of adding.

**Verification.** All 13 machine checks were recomputed independently with SymPy and
passed, and the six study-guide examples and try-its were verified the same way.
**Nothing is flagged for manual review.**

One point worth being precise about, since it affects what "verified" means here.
Nine of the twelve problems are verified symbolically or exactly: the expansions and
condensations that involve only numeric arguments (problems 2, 3, 5, 7) are checked
as full identities, and the three equations are solved from the change-of-base form of
the original equation, not from an already-simplified version. Problems 8 and 11 ask
for a symbolic result in part (a) and its value at stated inputs in part (b); the
part-(b) value is what the checker recomputes. A general identity in two positive
variables (for example `ln(x⁴/y) = 4 ln x − ln y`) cannot be machine-proved without
positivity assumptions the tool does not carry, so those two are bound at their stated
values instead of asserted symbolically. Both answer keys show the full symbolic
derivation.
