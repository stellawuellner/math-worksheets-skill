# Integrating Rational Functions with Partial Fractions — three PDFs

**Course:** AP Calculus AB/BC · **Topic:** substitution, parts, partial
fractions and improper integrals, focused on integrating rational functions
with partial fractions · **8 problems**

## What you get

- **`ws_partfrac_curr478.pdf` — the student worksheet.**
  Eight problems, all partial fractions, and the applied ones carry real
  models with stated units: a reaction producing grams per minute, a filter
  removing kilograms per year, and the logistic separation
  $\int \frac{dP}{P(10-P)}$ that is the reason partial fractions appear in a
  differential-equations unit at all. The decomposition types build in order —
  distinct linear factors, a repeated factor, an irreducible quadratic (whose
  numerator has to be linear) — and problem 8 ends with an improper integral
  evaluated as a limit.
- **`ak_partfrac_curr478.pdf` — the full answer key.**
  Every problem restated and worked, with the unknowns solved for explicitly
  (substituting the root that kills each term) before any integration. It opens
  with a generated Quick Answers bank, a "What is verified" note, and a
  Curriculum block.
- **`ss_partfrac_curr478.pdf` — the study guide (2 pages).**
  Three sections: distinct linear factors, repeated and quadratic factors (with
  the count-your-unknowns check), and totals from a rational rate. Each has a
  rule box, a worked example whose first step names the decomposition to use,
  and a try-it with its answer printed upside down.

## Verification, stated honestly

The eight problems ask for **12 responses**.

- **11 of 12 are machine-checked** with SymPy. The decomposition in problem 1
  is checked as an algebraic identity; every antiderivative is checked by
  differentiating it back to the original rational function, so a wrong
  constant cannot pass; every definite integral and the improper integral's
  limit are recomputed exactly, and the decimal answers are checked separately
  at the precision they are asked for.
- **1 of 12 is instructor-judged**: problem 8(c), what the limit says about the
  filter's lifetime total. It prints as `---` in the Quick Answers bank, and
  the key states that full credit needs the finite-total (convergence)
  conclusion, not just the value of the limit.

The study guide's six results are all machine-checked.

## Units

Problems 3 and 7 declare their units in the verification data (grams,
kilograms). The worksheet's answer lines and the key's boxed answers are both
bound to those declarations, so the sheet cannot ask for grams and be answered
in something else.

## Suggested order

Study guide first, then the worksheet, then the answer key.
