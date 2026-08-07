# Generating and Comparing Two Patterns — Grades 4–5

Three PDFs: the student worksheet, a full step-by-step answer key, and a two-page study
guide.

**Worksheet (10 problems).** The sheet is built around two representations of the same
idea and one real application.

- A **Two Rules Table** at the top holds patterns A (start at 0, add 4) and B (start at
  0, add 8) with the first three terms filled in and the rest blank to complete.
  Problems 1–5 and 10 all work from it: generate the 6th term of each, compare the two
  step sizes, find the gap between the 10th terms, and write the matching 4th terms as
  an ordered pair.
- A **savings application** (problems 6 and 7): Maya has 12 dollars and adds 3 a week,
  Liam has 4 and adds 5. When are they equal, and how much do they have then? This is
  the case where the pattern that starts behind finishes ahead, which is exactly what
  the step-size rule alone cannot tell you.
- A **second table** (problems 8 and 9) holding patterns P and Q, used to write an
  ordered pair from matching terms and to compare the two patterns' means.
- **Problem 10** closes by asking for the relationship between matching terms of A and B
  *and* why it must hold for every term, not just the ones checked.

Units are stated where they exist (weeks, dollars) and there is no irrelevant story
detail — every number in a stem is a number the problem uses.

**Answer key.** Each solution generates the terms in full before computing, so a parent
can see the pattern being built rather than a formula being applied. The off-by-one that
sinks most students (term 6 is *five* steps out) is named in problem 1 and used
consistently after that.

**Study guide (2 pages).** Four sections: generating a term without listing them all,
relating one rule to the other (and the warning that the step-ratio shortcut only works
when both patterns start at the same place), comparing matching terms, and writing two
patterns as ordered pairs. Each has a rule box, a worked example whose first step names
the strategy, and a try-it with the answer upside down inside the box.

## What is verified, honestly

The sheet asks for 15 separate responses across the 10 problems.

- **14 are machine-checked** with SymPy: every generated term, the step-size ratio, the
  gap between the 10th terms, both ordered pairs, the savings equation (solved as
  12 + 3w = 4 + 5w), the equal total of 24 dollars, and both means. The two tables'
  values live in the verification data, so the printed tables and the answers come from
  one source, and the key was bound back to those verified values by the build.
- **1 is instructor-judged** and prints as `---` in the Quick Answers bank: problem
  10(c), the explanation of why every term of B is double the matching term of A. The
  key states what full credit requires — the *reason* (same start, twice the step, so
  twice the total added after any equal number of steps), not just the doubling noticed
  in a few pairs.

Nine of the ten problems are fully machine-checked end to end.
