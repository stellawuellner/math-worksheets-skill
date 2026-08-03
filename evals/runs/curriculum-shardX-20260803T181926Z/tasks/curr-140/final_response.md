# Estimating and Solving with Decimals — Grades 4–5

Three PDFs are ready:

- **`ws_decimals_curr140.pdf`** — the student worksheet, 12 problems, 5 pages.
- **`ak_decimals_curr140.pdf`** — the step-by-step answer key, 3 pages.
- **`ss_decimals_curr140.pdf`** — a 2-page study guide.

## What the worksheet covers

Every problem is a decimal application, and the sheet keeps switching between
*estimating* and *solving exactly* so your child has to read the question and decide
which is being asked. Four kinds are interleaved after a short warm-up:

1. **Estimate by rounding** (problems 1, 2, 7) — round first, then compute. The key
   is explicit that rounding the exact answer afterwards is checking, not estimating.
2. **Exact addition and subtraction** (3, 6, 10) — lining up decimal points, and
   two-step money problems.
3. **Exact multiplication and division** (4, 8, 11) — counting decimal places in a
   product, sharing a length into equal pieces, and dividing by a decimal.
4. **Comparing and checking** (5, 9, 12) — ordering four close decimals, catching a
   misplaced decimal point, and comparing an estimate against the exact total.

Problem 9 is an error-analysis problem: Sam writes $4.6 \times 3 = 1.38$, and the
student has to find the exact product, compare it with Sam's, and say which place
value he slipped into. Problem 12 pulls the whole sheet together — estimate, exact
total, compare the two, and find the change from \$40.

## What was verified

All 19 checks (12 problems, several with more than one part) were recomputed by SymPy
before the PDFs were built, and all 19 passed. Nothing on this sheet is left for a
human to check.

Two things worth knowing about how the checking works here:

- The **estimates are checked as estimates.** The verifier rounds each number in the
  expression to the stated place and *then* computes, so an answer that came from
  rounding at the end would not match.
- The **comparisons are checked as comparisons.** Problem 9's "which is bigger" and
  problem 12's estimate-versus-exact are verified as relations, not just asserted in
  the key.

Three **misconception traps** are declared and machine-checked, and the answer key
prints them under **Common wrong answers**:

- Problem 3: subtracting only the first purchase gives \$31.25 instead of \$24.85.
- Problem 4: putting the decimal point one place too far left gives 1.44 kg instead
  of 14.4 kg.
- Problem 8: multiplying instead of dividing gives 28.8 m instead of 1.8 m.

Units are bound in both directions: km, kg, L and m appear on the worksheet's answer
lines and inside the key's boxed answers, and both were checked against the
verification data.

## The study guide

Four short sections — estimating by rounding, adding and subtracting, multiplying and
dividing, and comparing. Each has the rule in plain words, a worked example whose
first line says why that method is the one to use, and a try-it problem with the
answer printed upside down. The comparing section flags the mistake that trips most
children at this age: a decimal with more digits is not automatically bigger.
