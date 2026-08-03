# Fractions on a Number Line — Grade 2–3

Three PDFs are ready:

- **Study guide** (`ss_numberlines_curr082.pdf`, 2 pages) — read this first, with the child.
- **Worksheet** (`ws_numberlines_curr082.pdf`, 5 pages, 10 problems).
- **Answer key** (`ak_numberlines_curr082.pdf`, 3 pages) — full reasoning plus what to listen for.

## What the worksheet does

Every one of the ten problems is a number line with denominators drawn from
2, 3, 4, 6 and 8, so the whole sheet stays on the requested focus. What changes
is the job the line asks for:

- **Name the point that is already marked** (problems 1, 2, 3, 8): halves,
  fourths, thirds, and finally a line that runs to 2 in halves, where the
  answer 3/2 is past one whole.
- **Place a fraction you are given** (4, 5, 9, 10): mark 4/6 and rename it 2/3;
  mark 8/8 and discover it is the whole number 1; mark 5/3 on a 0-to-2 line and
  say how far past 1 it sits; and the closing error-analysis problem.
- **Compare two fractions on the line** (6, 7): 2/3 against 2/4 on two matched
  lines (same numerator, different cut sizes), then 5/8 against 3/4 on a single
  eighths line, which is a common-denominator argument met as a picture.

Difficulty ramps 1 → 4 with no repeated skeleton: the partition changes, the
end label changes (some lines run to 2), and the question asked changes from
"read it" to "place it" to "compare them" to "explain the mistake".

## What was verified

**9 of the 10 problems were machine-verified with SymPy** and every boxed answer
in the key was bound back to the recomputed value. Problem 10 is declared
`manual`: it asks for a written explanation of Ellie's misconception, which no
CAS can check. The key still prints a full model answer and a "full credit"
note so a parent can grade it.

Five misconception traps were declared and machine-checked as distinguishably
wrong:

- counting the five tick marks instead of the four equal parts (3/4 read as 3/5),
- counting the parts to the right of the point instead of from 0 (2/3 read as 1/3),
- believing a fraction can never reach a whole (8/8 answered 7/8),
- reading a 0-to-2 line as if it ended at 1 (3/2 answered 3/4),
- giving the whole distance from 0 instead of the distance past 1 (2/3 answered 5/3).

One honest limitation: the machine-printed "Common wrong answers" block takes a
**plain number** for the printed wrong value, and every wrong answer here is a
fraction (3/5, 1/3, 7/8, 3/4, 5/3). Printing those as decimals — "if they got
0.6" — would be worse than useless on a grade-3 fractions sheet, so the traps
were declared without a printed value (still fully machine-checked) and the
wrong answers are written out in the answer key's per-problem notes instead,
where they read as fractions.

## Standards and tagging

`3.NF.A` on all ten problems, taken verbatim from
`references/standards-map.md` ("Fractions: understand & equivalence"). Every
problem also carries a difficulty, a Bloom level (2 recall, 4 apply, 3 analyze,
1 justify), a skill tag and a facet tag; the three-facet plan is declared in the
verify JSON and its subtitle is bound to the worksheet title block.

## Study guide

Two pages, three sections matching the three skills. Each has a rule box, a
worked example whose first step says *why* that method applies, and a try-it
with the answer printed upside down inside the box. It closes with the two
warnings that matter most here: count the spaces, not the ticks, and read the
label at the right-hand end before deciding what one whole is.

## Gate chain

`build.sh` finished **BUILD PASSED** (exit 2, manual-review item) on the first
attempt — no gate failed. Template shells, both verification files, skill and
facet coverage, subtitle binding, layout and work space, three compiles inside
their page budgets (ws 5/6, ak 3/6, ss 2/2), per-problem answer-key binding,
study-guide structure, and prose consistency all green. The exit-2 status is the
`manual` tag on problem 10, which is the correct encoding for an open written
explanation, not a defect to remove.
