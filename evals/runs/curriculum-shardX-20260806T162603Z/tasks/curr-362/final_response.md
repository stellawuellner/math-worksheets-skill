# The Rational Root Theorem — Algebra 2 fluency set

Three PDFs are ready:

- **`ss_ratroot_curr362.pdf` — Skills Summary (2 pages).** Four sections with a
  rule box, a worked example and a try-it whose answer prints upside down inside
  the box, following the method in the order a student actually uses it: build
  the candidate list, test a candidate (including one that *fails* — the guide
  deliberately works an example that comes out non-zero), divide the zero out
  and finish with the quadratic, and report every zero with a count check.
- **`ws_ratroot_curr362.pdf` — Student worksheet (5 pages), 12 problems.**
  The ramp is deliberate and no skeleton repeats: two short evaluations, then
  monic cubics, then a leading coefficient of 3 (where the fractional candidates
  matter and problem 6 has a zero of $\tfrac{2}{3}$), then a quartic, then a
  cubic with two irrational zeros, closing with one whose remaining zeros are
  non-real. Problems 1 and 5 ask for the candidate list itself; problems 3 and 6
  reuse the polynomial from the problem before, so the theorem is practised as a
  sequence rather than as isolated drills.
- **`ak_ratroot_curr362.pdf` — Answer key (3 pages).** Each solution names the
  candidate list, shows the test that succeeded, and shows the synthetic-division
  quotient before factoring it — the three steps a grader needs to see. The Quick
  Answers bank and the curriculum block (HSA-APR.B.3) sit at the top.

## What is verified, and what is not

The set carries **18 declared responses across 12 problems. 14 are machine
checked** — every evaluation, factorisation and zero-set was recomputed
independently with SymPy. The zero sets are checked for *completeness*, not just
correctness, so a key that stopped after the rational zero of problem 11 would
fail the gate rather than pass it. The study guide's four worked examples and
four try-its are verified the same way.

**4 responses are instructor-judged**, printed as `---` in the key:

- **Problems 1(a) and 5(a)** — the candidate lists. A list of eight or twelve
  values is not something the verifier can compare against a single answer, so
  the key prints the exact list and says what to deduct for: on problem 1, a
  list missing the negatives; on problem 5, a list missing the thirds, which is
  the error that problem is built to expose.
- **Problem 8** — saying which of two tested numbers is a zero and why. The key
  requires the reason ("the value came out zero"), not just the name.
- **Problem 12(c)** — explaining why the theorem could never have produced the
  two non-real zeros. The key requires the point that the theorem proposes only
  rational candidates.

## Notes

- No misconception traps are declared. The verification types used here
  (`zeros`, `factor`) express a whole solution set rather than one comparable
  value, so the trap mechanism does not apply; instead the two classic errors
  are built into the problem set directly — problem 5/6 punishes a candidate
  list without fractions, and problem 11 punishes stopping once the rational
  zero is found.
- The grade level appears on the answer key only.
