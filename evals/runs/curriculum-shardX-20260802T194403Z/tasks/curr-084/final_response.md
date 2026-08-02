# Fraction Models: Are the Parts Equal? — Grade 2–3

Three PDFs are ready:

- **Study guide** (`ss_fractions_curr084.pdf`, 2 pages) — read this first.
- **Worksheet** (`ws_fractions_curr084.pdf`, 4 pages, 8 problems).
- **Answer key** (`ak_fractions_curr084.pdf`, 2 pages) — full reasoning, not just answers.

## What the worksheet does

Every problem is about the one idea a lot of children skip: a fraction only
names the parts of a whole when **all the parts are the same size**. Problem 1
shows a model that is already correct, so your child has a clean case to compare
against. Problems 2, 4, 6 and 7 are find-and-fix items — Ben, Nina, Tara and Cal
each counted *pieces* instead of *equal parts*, and your child has to say what
went wrong and then give the right answer. Problem 5 compares 1/4 with 1/6 using
two identical paper strips. Problems 3 and 8 ask for a drawing and a sentence:
redraw the model so the parts really are equal.

Difficulty climbs from 1 to 5 across the sheet, and every problem is tagged to
Common Core standard 3.NF.A.

## What was verified, and what was not

- **6 of the 8 problems were machine-verified** with SymPy: every fraction and
  every count in the answer key was recomputed independently and matched.
- **4 misconception traps were declared and machine-checked.** For each
  find-and-fix problem, the wrong answer a child would get by counting pieces
  (for example 1/3 instead of 1/6) was computed and proved to be *distinguishably*
  wrong — so the problem really does catch the error it is aimed at. Those wrong
  answers are printed in the answer key as "Common wrong answer" notes, which
  tells you what the mistake was rather than just that there was one.
- **2 problems (3 and 8) are flagged for manual review**, and honestly so: they
  ask for a drawing and an explanation in the child's own words, which no
  computer algebra system can check. The answer key gives a model sentence, a
  description of the correct drawing, and what *not* to accept.

## Study guide

Four short sections, one per skill the worksheet tests: check the parts first,
name the fraction from the equal parts, fix a model with unequal parts, and why
more equal parts means smaller pieces. Each has a rule box, a worked example with
the reasoning written out, and a try-it whose answer is printed upside down in the
box so your child can attempt it before checking.

## Gate chain

`build.sh` ran all 21 gates green: template shells, both verification files,
skill coverage, layout and work space, answer-line binding, three compiles inside
their page budgets, per-problem answer-key binding, study-guide structure, and
prose/figure consistency. The final verdict is **BUILD PASSED** with the two
manual-review items reported (exit 2), which is the correct outcome for
draw-and-explain problems.
