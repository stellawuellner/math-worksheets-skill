# Writing Equations from Word Situations — Grades 6–7

Three PDFs are ready:

- **Worksheet** (`ws_wordequations_curr178.pdf`, 4 pages) — 10 word situations,
  each asking the student to *write* the equation before solving it.
- **Answer key** (`ak_wordequations_curr178.pdf`, 3 pages) — a three-step solution
  per problem (name the unknown → write the equation → solve), a quick-answer
  bank, and a generated Curriculum section listing 6.EE.B.7, 7.EE.B.4 and 6.EE.A
  with the difficulty range.
- **Study guide** (`ss_wordequations_curr178.pdf`, 2 pages) — three sections, each
  with a rule box, a worked example, and a separate try-it.

## What is on the worksheet

The sheet is built around the one decision that makes modelling hard: which
number is a **rate** (multiplied by the letter) and which is a **one-time
amount** (added or subtracted once).

1. **One-step models** (1, 2, 6): equal packs of pencils, a club fund before a
   purchase, and a recipe with a fractional rate of 3/4 cup per batch.
2. **Two-step models** (4, 5, 8, 9, 10): a gym joining fee plus a monthly charge,
   a perimeter with a known width, a coupon taken off before a bill is split
   three ways, and a challenge with a fractional coefficient (two thirds of the
   club, less 4, is 18).
3. **Write an expression and evaluate it** (3, 7): a taxi fare rule evaluated at
   7 miles, and a draining pool evaluated at 18 minutes.

Problem 9 is error analysis: a student wrote `5h + 3 = 23` for a rink that
charges 5 dollars plus 3 dollars an hour. The student has to say why the roles
are swapped before writing the correct equation.

Every problem states its unit, and each answer blank is labelled with it
(pencils, dollars, months, cm, batches, gallons, hours, students). Difficulty
ramps 1 → 4, and the three model types alternate after the warm-up.

## What was verified

All 10 problems were machine-checked with SymPy — eight as `solve` checks on the
equation the story produces, two as `eval` checks on the expression evaluated at
the given value — and the answer key's boxed answers were bound problem by
problem to those verified values, units included. The six study-guide items were
verified the same way.

Two misconception traps are declared and were machine-tested to be
distinguishable from the right answer: folding the flat fee into the per-mile
rate on the taxi problem, and subtracting a drain rate once instead of once per
minute. Both print in the answer key as "common wrong answers".

**Nothing is flagged for manual review.** The build finished all green. Two
intermediate quantities inside study-guide examples (the 20 in `4h = 20` and the
90 in `15 × 6`) appear as expected flags in the consistency report — they are
steps of the shown work, not givens.
