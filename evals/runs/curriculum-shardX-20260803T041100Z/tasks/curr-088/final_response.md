# One-Step Mass and Liquid Volume Problems — Grades 2–3

Three PDFs are ready:

- **Study guide** (`ss_mass_volume_curr088.pdf`, 2 pages) — read this first with your child.
- **Worksheet** (`ws_mass_volume_curr088.pdf`, 4 pages, 10 problems).
- **Answer key** (`ak_mass_volume_curr088.pdf`, 2 pages) — the reasoning for every problem, plus a quick-answer bank and the common wrong answers.

## What the worksheet does

All ten problems are one-step measurement problems: two given amounts, one
operation, one answer with a unit. Nothing on the sheet needs unit conversion
(that is grade 4 work) — grams stay grams and millilitres stay millilitres, so
the only decision is *which single operation*.

- **Mass in grams** (1, 4, 7): total of two bags, four apples of equal mass,
  one book taken out of a box — add, multiply, subtract in that order.
- **Liquid volume in millilitres** (2, 5, 8, 10): poured out, combined,
  shared into 4 bowls, and finally shared into 5 cups where the numbers are
  not friendly tens.
- **Read the record, then take one step** (3, 6, 9): a measurement table the
  student must read before computing. Problem 6 lists three fruits and asks
  about two of them, so choosing the right rows is part of the work; problem 9
  is an error-analysis item — a recorded answer of 1050 mL that is larger than
  the 750 mL the bottle started with.

The four operations are spread across the sheet rather than blocked, so after
the first two problems the student has to choose the operation rather than
repeat one. Difficulty ramps 1 → 4.

## What was verified

Ten of the eleven verification entries are machine-checked with SymPy: every
arithmetic answer, plus the two table problems, which are computed from the
same data the table prints. **One entry is flagged for manual review** — the
written sentence in problem 9 explaining Noah's mistake. That is an open
response and is marked `manual` rather than claimed as verified; the build
therefore ends at exit 2 with the manual item named, which is the correct
outcome, not a failure.

Eight misconception traps were declared and machine-checked as distinguishably
wrong; they print in the answer key's "Common wrong answers" block, so a wrong
number usually names the error:

- 50 g — subtracted the two masses instead of adding (problem 1)
- 1150 mL — added instead of taking away (problem 2)
- 154 g — added 4 to 150 instead of multiplying (problem 4)
- 500 g — compared the melon with the mango instead of the pineapple (6)
- 1125 g, 2400 mL, 1050 mL, 4750 mL — the same add/subtract and
  multiply/divide swaps on problems 7, 8, 9 and 10.

Every problem also declares its answer unit in the verification data, and the
gate binds that unit in both directions: the sheet's answer blank prints it and
the key's boxed answer must carry the same one.

## Standards and tagging

The code is `2.MD / 3.MD` — "Measurement & data (length, mass, time)" — taken
verbatim from `references/standards-map.md`, on all ten problems. Every problem
also carries difficulty (ramp 1,1,2,2,2,3,3,3,4,4), a Bloom level (2 recall,
5 apply, 3 analyze, 1 justify), and one of three skill tags; the three-facet
plan is declared in the verify JSON and its subtitle is bound verbatim to the
worksheet title block.

## Study guide

Two pages, three sections matching the three skills: mass, liquid volume, and
reading a record table before computing. Each has a rule box, a worked example
whose first step says *why* that operation is chosen, and a try-it with the
answer printed upside down inside the box. The closing watch-out box gives the
size check that catches most errors on this topic: on a "poured out" problem
the answer must be smaller than what you started with, and an answer with no
unit is not an answer.

## Gate chain

`build.sh` finished **BUILD PASSED** (exit 2 — green with one manual-review
item): template shells, both verification files, skill and facet coverage,
subtitle binding, layout and work space, unit binding on the sheet and in the
key, three compiles inside their page budgets (4 / 2 / 2 pages), per-problem
answer-key binding, study-guide structure, and prose consistency. No gate
failed on the first attempt.
