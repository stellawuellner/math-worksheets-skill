# Reading and Comparing Multi-Digit Whole Numbers — Grades 4–5

Three PDFs are ready:

- **Worksheet** (`ws_placevalue_curr101.pdf`, 4 pages) — 10 problems, each with a
  place-value model to think with and room to work.
- **Answer key** (`ak_placevalue_curr101.pdf`, 2 pages) — a quick-answer bank at the top for
  fast grading, then the reasoning behind every answer, not just the answer.
- **Study guide** (`ss_placevalue_curr101.pdf`, 2 pages) — four rules, four worked examples,
  four try-it items to attempt before starting the worksheet.

## What the worksheet practices

Four skills, interleaved after a short warm-up so the child has to decide which idea applies:

1. **What a digit is worth** (problems 1, 2, 8) — reading a place-value chart, the ten-times
   relationship between neighbouring places, and one "find the mistake" problem.
2. **Expanded and word form** (3, 5) — rebuilding a standard numeral, including the zeros
   that hold empty places.
3. **Comparing and ordering** (4, 6, 10b) — compare from the left, first differing place
   decides.
4. **Rounding to estimate** (7, 9, 10a) — round to the nearest thousand, then estimate a sum.

Difficulty ramps 1 → 4: problem 1 is a chart read, problem 10 is a two-part synthesis where
two populations round to the same thousand and the child must notice that rounding cannot
answer "which is greater".

Models used: place-value charts (problems 1 and 4), a "which thousands does it sit between"
table (problem 7), and expanded-form notation tied back to the chart. Every model is
connected to the numeral it represents.

## Verification

All 10 problems are machine-checked with SymPy through the skill's gate chain — 12 checks in
total (problems 1 and 10 have two parts, each checked separately):

- digit values and expanded/word form as `eval` checks,
- comparisons and the three-number ordering as `compare` checks,
- rounding and the estimated sum as `estimate` checks (which round each operand first, then
  evaluate — the same procedure the student is asked to follow).

**Nothing is flagged manual**: every printed answer on this sheet is machine-verifiable, and
`build.sh` reports `BUILD PASSED — all gates green` (exit 0). The answer key and study guide
were each bound back to their verification data problem by problem, so a printed answer
cannot drift from a verified one.

One note on the gate log: the prose-consistency report shows a low match rate. That checker
reads numerals with a regex that has no notion of thousands separators, so `34{,}650` reads
as "34" and "650" and is reported as not found. It is a heuristic report, not a gate; every
numeral printed on these sheets is exactly the numeral in the verification JSON.
