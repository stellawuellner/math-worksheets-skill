# Polynomial Long Division — Algebra 2 fluency set

Three PDFs are ready:

- **`ss_polydiv_curr357.pdf` — Skills Summary (2 pages).** Four sections with a
  rule box, a worked example and a try-it whose answer prints upside down inside
  the box: division that comes out even, quotient-plus-remainder (including the
  stop rule), zero placeholders for missing powers, and the remainder theorem as
  a shortcut. The four-step loop is stated once and reused in every example.
- **`ws_polydiv_curr357.pdf` — Student worksheet (6 pages), 12 problems.**
  The ramp is deliberate and no skeleton repeats: two short quadratic divisions,
  then cubics, then a dividend with missing powers, then a quadratic divisor
  (where the stop rule bites), then a quartic with a gap, then two problems that
  connect the division to the remainder and factor theorems, closing with an
  unknown coefficient $k$ to be found from a zero-remainder condition. Every
  problem gets 6–7.5 cm of writing room, which is what a long-division frame
  actually needs.
- **`ak_polydiv_curr357.pdf` — Answer key (3 pages).** Each solution shows the
  divide–multiply–subtract steps and what is left after each one, not just the
  quotient, and says explicitly where the division stops and why. The Quick
  Answers bank and the curriculum block (HSA-APR.D.6 for the divisions,
  HSA-APR.B.3 for the remainder/factor-theorem items) sit at the top.

## What is verified, and what is not

The set carries **15 declared responses across 12 problems. 14 are machine
checked.** Each division is verified as an algebraic identity: SymPy confirms
that the printed
quotient-plus-remainder-over-divisor is the *same function* as the original
fraction, so a wrong remainder or a lost term cannot pass. Problem 11's complete
factorisation and problem 12's value of $k$ are checked independently as well.
The study guide's four worked examples and four try-its are verified the same
way.

**1 response is instructor-judged** — problem 12(b), explaining how the
remainder theorem finds $k$ without doing the division. The key prints `---` for
it and gives the rubric: full credit needs the theorem stated *and* the
observation that "no remainder" becomes a single linear equation in $k$;
describing the long division the theorem replaces earns nothing.

## Notes

- No misconception traps are declared here. The verification type that expresses
  a division as an identity (`equiv`) has no single comparable value for a trap
  to be measured against, so instead the two classic errors are targeted by
  design: problems 4, 6 and 10 all have missing powers in the dividend (the
  column-alignment error), and problem 9 has a quadratic divisor, where stopping
  too late is the usual slip. The study guide addresses both directly.
- The grade level appears on the answer key only.
