# Adding and Subtracting Mixed Numbers — Grades 4–5

Three PDFs are ready:

- **Worksheet** (`ws_mixednumbers_curr128.pdf`, 4 pages) — 10 word problems on
  adding and subtracting mixed numbers, every one set in a real context with a
  named unit.
- **Answer key** (`ak_mixednumbers_curr128.pdf`, 3 pages) — a three-step solution
  for each problem, a quick-answer bank for fast grading, and a generated
  Curriculum section listing the standards (4.NF.B.3 and 5.NF.A.1) and the
  difficulty range.
- **Study guide** (`ss_mixednumbers_curr128.pdf`, 2 pages) — three skill sections,
  each with a rule box, a worked example, and a separate try-it item.

## What is on the worksheet

Ten contexts — a walk, two juices, piano practice, birdseed, a pitcher, soup
stock, a bike path, a rain barrel, a piece of trim, and a bread recipe — chosen
so the numbers, not the story, do the work. The three methods are:

1. **Adding with like denominators** (1–3), including one sum whose fraction part
   passes a whole and has to be traded.
2. **Subtracting with regrouping** (4, 5, 8, 9), including two problems that ask
   the student to write an equation with a letter for the unknown before solving,
   and one error-analysis item where a student reversed the fraction column.
3. **Different denominators** (6, 7, 10), where both fractions must be rewritten
   first; the last problem needs a common denominator *and* regrouping.

Every answer line is labelled with its unit (miles, cups, hours, pounds,
gallons, inches), so the unit is part of the answer rather than an afterthought.
Difficulty ramps from 1 to 4, and after the warm-up the three methods alternate
so the student has to decide which one applies.

## What was verified

All 10 problems were machine-checked with SymPy — the eight direct computations
as exact rational arithmetic, the two equation problems as `solve` checks — and
the answer key's boxed answers were bound problem-by-problem to those verified
values, including the units. The six study-guide items (three examples, three
try-its) were verified the same way.

Five misconception traps are declared and were each machine-tested to be
distinguishable from the correct answer: adding denominators, subtracting
straight across, and reversing the fraction column instead of regrouping. They
print in the answer key as "common wrong answers", so a wrong answer on the page
tells you which mistake it was.

**Nothing is flagged for manual review.** The build finished all green. Two
numbers on the sheet are intentionally not part of any verified computation and
show up as expected flags in the consistency report: the wrong answer quoted in
the problem 9 error-analysis stem, and an intermediate improper fraction inside
one study-guide example.
