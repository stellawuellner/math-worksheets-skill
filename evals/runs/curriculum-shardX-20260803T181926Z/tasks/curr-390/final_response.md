# Modeling with Systems and Matrices — Algebra 2

Three PDFs are ready:

- **`ws_matrixsys_curr390.pdf`** — the student worksheet, 12 problems, 6 pages.
- **`ak_matrixsys_curr390.pdf`** — the full step-by-step answer key, 5 pages.
- **`ss_matrixsys_curr390.pdf`** — a 2-page skills summary to keep beside the worksheet.

## What the worksheet covers

Every problem is a multivariable model: a situation with two or three unknown
quantities that has to be turned into a system and then solved. Three methods are
interleaved so your student has to *choose* one rather than repeat one:

1. **Systems from a story** (5 problems) — tickets, a mixture, a kayak against a
   current, a split investment, and a three-variable concert problem to finish.
2. **Matrix equations** (4 problems) — write the model as $AX = B$, compute
   $\det A$, and solve by the inverse or Cramer's rule.
3. **Nonlinear systems** (3 problems) — a line meeting a parabola, a flight path
   crossing a circle, and perimeter-with-area, all solved by substitution.

The first four problems block by method (that is the warm-up); after that the
methods rotate, so from problem 5 onwards choosing the tool is part of the work.
Difficulty runs 2 → 5, ending with the three-variable ticket problem.

Problem 10 is deliberately the one with a **zero determinant**: the two order
sheets are inconsistent, so the system has no solution. Students who have only
ever seen systems that work out learn a lot from it.

## What was verified

All 12 problems were machine-checked with SymPy before the PDFs were built —
17 checks in total, since the matrix problems are checked twice (the determinant
and the solution separately):

- Every system's solution was substituted back into every equation, **and** the
  solution count was compared with the computer algebra system's full solution
  set, so a key that lists one of two intersection points cannot pass.
- Problem 10 was verified as genuinely *inconsistent* — "no solution" is a
  checked result here, not an assertion.
- Two misconception traps are declared and machine-checked: on problems 4 and 7,
  computing $bc - ad$ instead of $ad - bc$ gives $+11$ and $+10$ instead of
  $-11$ and $-10$. The answer key prints these under **Common wrong answers**, so
  a wrong sign on the determinant is diagnosable at a glance.
- The study guide's three worked examples and three try-it problems were verified
  the same way.

**Flagged for manual review (1 item):** problem 10(c) asks the student to
*explain* what the zero determinant says about the two order sheets. That is an
open response — no verifier can grade it — so it is labelled as such and the
answer key carries a full model answer to compare against.

## Notes

- The grade level prints on the answer key only (in the generated Curriculum
  section, with the standards codes and the difficulty range), never on the
  worksheet or the study guide.
- Standards tagged: HSA-REI.C.6 (systems from context), HSN-VM.C.6–C.12 (the
  matrix problems) and HSA-REI.C.7 (the line-meets-curve problems), all from the
  skill's standards map.
- Answers requiring units — the acid mixture (L) and the garden dimensions (m) —
  carry the unit on the worksheet's answer line and inside the boxed answer in the
  key, and both were checked against the verification data.
