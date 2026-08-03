# Adding Three-Digit Numbers with Regrouping — Grades 2–3

Three PDFs are ready: the student worksheet, a full step-by-step answer key,
and a two-page study guide.

## What's in the worksheet (10 problems)

Every problem adds three-digit numbers, and every one of them needs regrouping
somewhere — the skill in CCSS **2.NBT.B.5 / 3.NBT.A.2**. The set starts easy
and gets harder, and it rotates between three related skills so your child has
to think about which one the problem is asking for:

- **Add with regrouping (6 problems)** — first a single carry out of the ones
  (348 + 125), then a carry out of the tens only (265 + 173), then two carries
  in a row, then a zero in the tens column that still receives a carry
  (596 + 208), and finally a sum that crosses one thousand (675 + 349).
- **Estimate a sum (2 problems)** — round both numbers to the nearest hundred,
  add the easy numbers, then add exactly and compare. On the second one the
  estimate lands within one of the true answer, which is a good moment to talk
  about why.
- **Add in a story (1 problem)** plus a closing error-analysis problem where
  Ben's answer of 623 for 457 + 276 is exactly what you get if you write only
  the last digit of each column and never carry.

## What was verified

All 12 machine-checkable answers — the ten worksheet answers plus the extra
estimate on each of the two estimation problems — were recomputed
independently with SymPy and match the answer key exactly. The two rounding
estimates were recomputed by rounding each addend and adding, not by trusting
the printed answer.

Four misconception traps were also machine-checked to be distinguishably wrong
(dropping the second carry, dropping the first carry into a zero column, and
carrying nothing at all). They are printed in the answer key as "common wrong
answers", so if a particular wrong number turns up you will know which slip
produced it rather than just marking it wrong.

Nothing on this sheet needed to be flagged for manual review: every question
asks for a number, and every number was checked.

## The study guide

Two pages, three sections. Each has a rule box, a worked example whose first
step says *why* that method fits before any arithmetic happens, and a separate
try-it problem with the answer printed upside down so the student attempts it
first. The watch-out box names the two costliest errors: writing a two-digit
total under one column, and carrying a ten but forgetting to add it in.

Every answer printed in the guide is verified too, including both answers in
the estimation try-it.
