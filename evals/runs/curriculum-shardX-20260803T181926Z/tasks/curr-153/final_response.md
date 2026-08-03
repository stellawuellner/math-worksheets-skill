# Tape Diagrams and Double Number Lines for Ratios — Grades 6–7

Three PDFs are ready:

- `ws_ratiodiagrams_curr153.pdf` — the student worksheet, 10 problems, 6 pages
- `ak_ratiodiagrams_curr153.pdf` — the full step-by-step answer key, 3 pages
- `ss_ratiodiagrams_curr153.pdf` — a 2-page skills summary / study guide

## What the worksheet asks

Every one of the ten problems is worked through a drawn diagram — there is no
"just cross-multiply" problem on the sheet. Each problem carries its own picture
inside its block, so no diagram can be mistaken for a neighbour's data.

- **Tape diagrams** (problems 1, 3, 6, 9) — punch mixed $2:3$ with $10$ cups of
  juice; a $48$ cm ribbon cut $3:5$ (the total covers *all eight* boxes, the
  error the key calls out); a $4:7$ walk-to-ride class where the $3$-box
  difference is $12$ students, which is set up and solved as $3x = 12$; and two
  recipes compared box by box.
- **Double number lines** (problems 2, 7, 10) — laps against minutes with two
  ticks to fill in, kilometres against hours in both directions, and a synthesis
  problem where one label is $x$ and the student writes and solves the
  proportion $x/8 = 15/24$.
- **Unit rate from the line** (problems 4, 8) — landing on the "1" tick by
  dividing both lines by the same number, then using the rate.
- **Comparing ratios** (problems 5, 9) — two brands of pens and two cookie
  recipes, where the answer needs a common basis (per pen, per part of flour)
  before any comparison is legal.

Answers that carry a unit have a unit-labelled answer line (cups, cm, minutes);
money answers say "in dollars" in the question, as the units convention here
requires.

Difficulty ramps 1, 1, 2, 2, 3, 3, 3, 4, 4, 5.

## What was verified

Twenty-four SymPy checks across the ten problems — every box value, every
unit rate, every filled-in tick label on the number lines, and both
comparisons. **Nothing is flagged for manual review**; the build finished with
all gates green, including the check that binds each printed answer in the key
to its own problem's verified value and unit.

The answer key shows the reasoning for each problem: which quantity the known
amount covers, what one box (or one unit) is worth, and the multiplication that
follows — plus a check ($18 + 30 = 48$ cm, $28 - 16 = 12$) and grading notes on
the two errors this topic produces most: adding instead of scaling, and dividing
a total by one side's parts.

## The study guide

Four sections, each with a rule box, a worked example whose first step explains
why that route is chosen, and a try-it item with the answer upside down inside
the box: tape diagrams (find one box first), double number lines (move both
lines together), reading the unit rate off the line, and comparing two ratios.
Small diagrams in the first two rule boxes show what each representation looks
like.

Standards: 6.RP.A.3 for the equivalent-ratio work, 6.RP.A.2 for the unit-rate
problems.
