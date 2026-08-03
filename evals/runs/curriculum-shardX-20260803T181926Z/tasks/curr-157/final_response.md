# Unit Rates with Fractions — Grades 6–7

Three PDFs are ready: the student worksheet, a full step-by-step answer key,
and a two-page study guide.

## What's in the worksheet (12 problems)

Every problem asks for a unit rate, and in every one at least one of the two
quantities is a fraction or a mixed number — the skill in CCSS **6.RP.A.2 and
6.RP.A.3**. The set ramps from difficulty 1 to 5 and moves between three
related skills so the student has to decide what to do rather than repeat one
recipe:

- **Find a unit rate from two fractions (6 problems)** — half a mile in a
  quarter hour to start, then answers that are themselves fractions
  (5/8 mile in 5/6 hour), a mixed number that must become improper before the
  reciprocal step, and a whole number divided by a fraction (price per pound).
- **Compare two rates (2 problems)** — two walkers, and a better-buy problem.
  Each asks for both unit rates and then the > or < between them, because the
  point is that the raw numbers cannot be compared until they are unit rates.
- **Find a unit rate in a story (4 problems)** — a hose, a wall being painted,
  a cyclist with a mixed number, and a closing two-step problem where the unit
  rate has to be found first and then scaled to four minutes.

## What was verified

All 16 machine-checkable answers — twelve problems, with three answers each on
the two comparison problems — were recomputed independently with SymPy and
match the answer key exactly, fractions included (12/5, 8/15, 7/4 and the
rest are checked as exact rationals, not decimals). The two comparisons were
checked as relations, so a key printing the wrong direction could not pass.

Four misconception traps were machine-checked to be distinguishably wrong.
Three of them are the same error in different clothes — dividing the wrong way
round, hours over miles instead of miles over hours — which is far and away
the most common mistake on this topic. The fourth is treating the given amount
as if it were already the per-minute rate. All four print in the answer key as
"common wrong answers", so a wrong number tells you which misunderstanding
produced it.

Nothing needed to be flagged for manual review: every question asks for a
number or a comparison sign, and all of them were checked.

## The study guide

Two pages, three sections. Each has a rule box, a worked example whose first
step names *why* the method fits before any arithmetic, and a separate try-it
with the answer upside down. The watch-out box targets the divide-the-wrong-
way error directly, with a practical fix: say the answer out loud with its
units before you flip anything, because "miles per hour" tells you which
quantity belongs underneath.

Every answer printed in the guide is verified, including both unit rates and
the comparison sign in the comparison try-it.
