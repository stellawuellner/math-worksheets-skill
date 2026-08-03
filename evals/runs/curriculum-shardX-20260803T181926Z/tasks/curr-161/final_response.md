# Finding a Percent of a Quantity — three PDFs

- `ws_percent_curr161.pdf` — student worksheet (5 pages, 10 problems)
- `ak_percent_curr161.pdf` — full step-by-step answer key (2 pages)
- `ss_percent_curr161.pdf` — 2-page study guide / skills summary

## What the worksheet asks

All ten problems find a percent of a quantity, approached three different ways
so the student has to choose a route rather than repeat one:

1. Bar model: a bar for 80 books cut into ten parts — shade one and read 10%.
2. Bar model: a bar for 46 marbles cut in half — 50%.
3. Ratio table: 100% → 70, 10% → ?, 30% → ?, then the same thing in one
   multiplication.
4. Fraction shortcut: 25% of 64 as a quarter, checked against the decimal route.
5. Find the mistake: Dana moves the decimal one place for 5% of 120 and gets 12.
   She has actually found 10%; the correct value is 6.
6. A 15% tip on a 48-dollar meal, to the nearest cent.
7. 8% of 250 seats (answered with a unit).
8. A 20%-off jacket: write and solve an equation for the discount, then the sale
   price.
9. 12.5% of a 64-gram block, using the benchmark fraction 1/8.
10. Two percents in a row: 25% off 60 dollars, then 8% tax **on the sale price**.

Difficulty ramps 1 → 5. Every problem is tagged with a CCSS code
(6.RP.A.3.c / 7.RP.A.3), a Bloom level and a method facet; those tags generate
the Curriculum section on the answer key. The grade level prints there and
nowhere on the student's pages.

## What was verified

Every printed answer — twelve values across the ten problems, including both
parts of problems 8 and 10 — was recomputed by SymPy before anything compiled,
and the key's boxed answers are bound back to those verified values problem by
problem. **Nothing on this sheet is left to manual review.**

Four problems declare the misconception their numbers were chosen to catch, and
the verifier proved each wrong method lands on a visibly different number:

- 5% read as 10% → 12 instead of 6 (problem 5, the error-analysis problem)
- 10% used for a 15% tip → 4.80 instead of 7.20 (problem 6)
- 20 dollars off instead of 20% off → 15 instead of 28 (problem 8)
- tax charged on the original price → 64.80 instead of 48.60 (problem 10)

Those wrong answers are printed in the key's "common wrong answers" notes, so a
grader can tell which error produced a given answer.

## The study guide

Four sections, each with a rule box, a worked example whose first step says why
that route was chosen, and a try-it with the answer upside down inside the box:
benchmark percents on a bar model; multiply by the decimal; the fraction
shortcut (with the 50/25/75/20/10/12.5 percent table); and percents in a story,
including the rule that a second percent acts on the new amount.
