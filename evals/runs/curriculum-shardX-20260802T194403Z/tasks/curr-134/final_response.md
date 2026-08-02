# Multiplying & Dividing Fractions — Find the Flip Mistake (Grades 4–5)

Three PDFs built around one diagnosis: when is a reciprocal or a
cross-cancellation being misused?

- **Worksheet (4 pages, 8 problems).** Two rules are stated at the top (cancel
  top-with-bottom only; keep-change-flip flips only the divisor, and only
  after the division has been rewritten). Problem 1 establishes legal
  cancelling, problem 2 legal flipping, problem 5 is a missing-factor problem
  solved with a reciprocal, and the other five are diagnosis: **four
  find-and-fix items** (3, 4, 6, 8) plus a "who is right?" comparison (7).
  The planted errors are the real ones — flipping the dividend, cancelling two
  numerators, cross-cancelling a division before rewriting it, and a word
  problem whose wrong answer (1/6 batch) is visibly impossible. Every problem
  gets 5–7 cm of work space; problem 8 answers in **batches** and its unit is
  bound to the verify data.
- **Answer key (3 pages).** Each solution names the misconception in words
  before showing correct work, and several add a size check that catches the
  error without computing ("dividing by a fraction less than 1 must make the
  result bigger").
- **Study guide (2 pages).** Three sections — cancel-then-multiply,
  flip-only-the-divisor, find-and-fix-the-flip — each with a rule box, a
  worked example opening with a strategy sentence, and an upside-down try-it.
  The third section's example is itself an error to diagnose, so the student
  rehearses the worksheet's main task before starting it.

**Verification.** All 8 worksheet answers and all 6 study-guide results are
machine-checked with SymPy (exact rational arithmetic — no rounding). Nothing
is flagged manual. **Seven misconception traps are declared and
machine-checked**: verify.py recomputes each wrong method and confirms the
problem's own check rejects it, so every planted answer is provably
distinguishable from the correct one. The traps carry `desc` + `expr` only:
these answers are fractions, and the optional printed `value` field accepts
plain numbers only, so declaring a decimal there would have put decimals in a
grade-5 fraction key. The full gate chain passed green, including per-problem
answer binding, the unit binding on problem 8, layout, and the page budgets.
