# One-Variable Inequalities: When Does the Symbol Flip? — Grades 6–7

Three PDFs are ready: the student worksheet, a full step-by-step answer key, and
a two-page study guide.

**Worksheet (`ws_flip_sign_curr184.pdf`, 4 pages, 8 problems).** Every problem
sits on the one misconception the sheet targets — forgetting to reverse the
inequality symbol after multiplying or dividing by a negative.

- Problem 1 makes the rule visible instead of asserting it: start from the true
  statement $6 > -2$, multiply both sides by $-4$, and watch $>$ turn into $<$.
- Problems 2, 4 and 6 are ordinary solves chosen so the flip is unavoidable
  (a negative coefficient, a negative fraction, and a two-step where the flip
  comes second).
- Problems 3 and 7 are the two requested **find-and-fix** items. Each shows a
  named student's complete, plausible work, and each asks the student to
  *disprove* the wrong answer with a test value before correcting it — the habit
  that makes this error self-detectable.
- Problem 5 is a boundary check that isolates the sign arithmetic itself.
- Problem 8 asks for the explanation: why multiplying by a negative reverses
  order while adding a negative does not.

**Answer key (`ak_flip_sign_curr184.pdf`).** Full reasoning, not answers only.
Every solve marks the exact step where the symbol turns (written as
$\overset{\text{flip}}{<}$ over the relation) and finishes with a substitution
check. The find-and-fix entries answer all three parts — the failing test value,
the error named in one sentence, and the corrected solution. Problem 8 carries a
model explanation plus explicit accept/reject guidance for the grader.

**Study guide (`ss_flip_sign_curr184.pdf`, 2 pages).** Three sections: the rule
itself (with a number-line picture showing that multiplying by $-1$ *reflects*
the line through 0, so the two numbers trade order), isolate-then-flip, and
diagnosing a missing flip with the two-second substitution test. Each section
has a rule box, a worked example that opens by naming the strategy, and a try-it
with the answer printed upside down inside the box.

## Verification

- **7 of 8** worksheet problems are machine-verified with SymPy: five as
  `inequality` checks (the computed solution *set* is compared against the
  expected interval, so a reversed symbol cannot pass) and two as `eval`
  arithmetic.
- **Problem 8 is flagged `manual`** — it asks for a justification, which no CAS
  can check. The build reports it as a manual-review item (exit 2), and the
  answer key gives the model argument a human should grade against.
- **Two planted wrong results are declared as machine-checked traps.** The
  verifier recomputes the wrong method and confirms both that it really produces
  the printed wrong number and that the problem's own check rejects it:
  problem 1's $-8$ (keeping the sign of the first factor) and problem 5's $-22$
  (reading $-5(-4)$ as $-20$). Both are printed in the key's "common wrong
  answers" block so a grader can diagnose from the number alone.
- The wrong answers in the two find-and-fix stems ($x \le -3$ and $x \ge -3$)
  are *inequalities*, not scalars, so the trap schema cannot carry them; instead
  each is machine-refuted by its problem's own `inequality` check, which proves
  the correct solution set is the opposite one.
- All 6 study-guide boxes (3 worked examples + 3 try-its) are verified the same
  way. Standard `7.EE.B.4` throughout; difficulty ramps 1 → 5 with no drops.
