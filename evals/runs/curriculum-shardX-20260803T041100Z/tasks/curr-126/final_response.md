# Adding and Subtracting Fractions with Like Denominators (Grades 4–5)

Three PDFs, all built and gated together.

- **Worksheet** (`ws_fractions_curr126.pdf`) — 10 problems, all on like
  denominators. Every problem is anchored to a bar model: the bar is drawn cut
  into exactly the denominator's number of equal parts, and the student shades or
  crosses out before writing the number sentence, so the notation is always read
  off the picture. Coverage: 5 addition, 3 subtraction, 2 missing-numerator
  (work-backwards) problems, interleaved after the warm-up so no method runs more
  than twice in a row. Problems 3, 4 and 7 land on answers that must be
  simplified; problem 5 crosses one whole (9/8); problem 10 is a find-and-fix-the-
  mistake item built around the classic 3/7 + 2/7 = 5/14 error. 3.5–5 cm of work
  space per problem, 3 pages.
- **Answer key** (`ak_fractions_curr126.pdf`) — reasoning, not answers: each
  solution says why the denominator does not change, shows the numerator
  arithmetic on its own line, and shows the simplifying division separately when
  one is needed. A generated quick-answer bank sits under the title block and
  prints the three declared misconception traps, so a grader seeing 9/16 or 16/12
  knows immediately which rule broke.
- **Study guide** (`ss_fractions_curr126.pdf`) — 2 pages, three sections that
  match the three worksheet skills (add · subtract-and-simplify · missing
  numerator). Each has a rule box with the general form a/n ± b/n, a two-step
  worked example, and a distinct try-it with the answer printed upside down,
  plus one watch-out box on the add-the-denominators error.

## Verification

All 10 worksheet answers and all 6 study-guide answers are machine-verified with
SymPy: 8 `eval` checks (exact rational arithmetic, so 6/12 and 1/2 are proven
equal rather than assumed) and 2 `solve` checks for the missing-numerator
problems. **No problem is flagged manual** — every item on this sheet has a
single exact rational answer, so nothing needed to be. Three misconception traps
are declared and were confirmed distinguishable from the correct answers.

`bash scripts/build.sh` returned **BUILD PASSED**, all 21 gates green on the
first attempt. Facet plan (`add-like`, `subtract-like`, `missing-addend-like`) is
declared in the verify JSON, every problem is tagged with one, the subtitle is
bound to that plan, and each facet has its own worked example in the study guide.
Standard `4.NF.B.3` is taken verbatim from `references/standards-map.md`
("Fractions: add/subtract like denominators"); difficulty ramps
1, 1, 2, 2, 2, 3, 3, 3, 4, 4.

Gate-log note: the worksheet prose report flags one number, the 14 in problem
10's printed wrong answer 5/14. That number is the planted error the problem asks
the student to find, so it is correctly absent from the verified givens.
