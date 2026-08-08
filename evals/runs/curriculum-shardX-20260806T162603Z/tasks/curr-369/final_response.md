# Holes and Vertical Asymptotes — Algebra 2 (error-analysis practice)

Three PDFs are ready:

- **Worksheet** (`ws_holesasym_curr369.pdf`, 4 pages) — 8 problems, all on
  telling a canceled-factor hole from a vertical asymptote.
- **Answer key** (`ak_holesasym_curr369.pdf`, 4 pages) — quick-answer bank,
  a **"Common wrong answers"** block listing the five planted misconceptions,
  then a full worked solution per problem.
- **Study guide** (`ss_holesasym_curr369.pdf`, 2 pages) — three sections: factor
  and cancel; hole or asymptote; and finding the height of a hole. Each has a
  rule box, a worked example that names the strategy first, and a try-it.

## The error-analysis items

Problems 5 and 6 print work a student actually handed in and ask for the correct
answer *and* the name of the error — the two classic mistakes in this topic:

- **Problem 5:** "the numerator is zero at $x=2$, so the hole is at height 0."
- **Problem 6:** "the bottom is zero at $x=2$ and $x=-2$, so both are vertical
  asymptotes."

Both planted wrong results are declared as **machine-checked misconception
traps**: the verifier recomputes each wrong method and confirms the problem's own
check rejects it, so the item genuinely distinguishes the error. Five traps in
all are declared (problems 3, 5, 6 and two on problem 8), and every one passed
the distinguishability check. They print in the key so a grader sees at a glance
what a given wrong answer means.

## Verification — the honest split

There are **17 verified responses across the 8 problems**:

- **13 are machine-checked** with SymPy — every simplification (checked as an
  algebraic identity, not by pattern-matching your form), every domain
  restriction, every asymptote, and every hole height (computed as a limit).
- **4 are instructor-judged**, marked `---` in the quick-answer bank: problems
  **2(b), 5(b), 6(c) and 7(c)**. These are the written diagnoses — which
  discontinuity is which and why, and naming each student's error. The key prints
  a grading rubric for each instead of claiming it was checked.

The key's "What is verified" note says the same: 13 of 17 answers machine-checked,
with problems 2, 5, 6 and 7 carrying an instructor-judged part. No `[unchecked]`
marks.
