# Multiplying by a One-Digit Number — Grades 4–5

Three PDFs are ready: the student worksheet, a full step-by-step answer key,
and a two-page study guide.

## What's in the worksheet (12 problems)

Every problem multiplies a three- or four-digit number by a single digit, the
skill in CCSS **4.NBT.B.5**. The set ramps from difficulty 1 to 5 and rotates
through three related skills so your child has to choose the method rather
than repeat one:

- **Multiply by one digit (8 problems)** — the standard algorithm, starting
  with a single regroup (214 × 3) and building to regrouping in every column
  (4975 × 9), plus a number with a zero in the tens place (3608 × 5), which is
  the column students most often skip.
- **Estimate and check (2 problems)** — round a factor to the nearest thousand
  or hundred, estimate the product, then compute the exact one and compare.
  This is how a child learns to notice their own wrong answers.
- **Multiply in a story (2 problems)** — equal groups (rolls per van), and one
  two-step finish where the total has to be multiplied and then reduced by
  what was used.

Problem 10 is an error-analysis problem: Dana's answer of 9000 for 1806 × 5 is
exactly what you get if you write the zero in the tens place and forget the
regrouped 3. Finding that is more useful than another clean computation.

## What was verified

All 14 machine-checkable answers were recomputed independently with SymPy and
match the answer key exactly, including both the estimate and the exact
product on each of the two estimation problems. Three misconception traps were
also machine-checked to be distinguishably wrong (skipping the zero column,
dropping a carry, and forgetting the second step of the two-step story), and
they are printed in the answer key as "common wrong answers" so you know what
a particular wrong number means.

**One item is flagged for manual review**, honestly rather than pretended:
problem 10 also asks the student to *describe* the mistake in words. No
computer can grade that sentence, so the answer key tells you what to accept —
any answer saying the regrouped 3 was never added into the tens column.

## The study guide

Two pages, three sections, each with a rule box, a worked example that starts
by naming *why* that method applies, and a separate try-it problem with the
answer printed upside down so the student attempts it before checking. It also
carries a watch-out box for the two errors that cost the most marks: adding
the carry before multiplying, and skipping a zero digit.

Every printed answer in the guide is verified too — including the estimate and
exact product in the try-it.
