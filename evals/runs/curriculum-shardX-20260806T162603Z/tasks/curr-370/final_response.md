# Reading a Rational Graph — Algebra 2 (interleaved synthesis review)

Three PDFs are ready:

- **Worksheet** (`ws_ratgraph_curr370.pdf`, 6 pages) — 12 problems on analysing
  rational graphs: intercepts, holes, vertical asymptotes, horizontal asymptotes.
- **Answer key** (`ak_ratgraph_curr370.pdf`, 4 pages) — quick-answer bank, a
  "Common wrong answers" block, then a full worked solution per problem.
- **Study guide** (`ss_ratgraph_curr370.pdf`, 2 pages) — four sections (simplify
  and keep the domain; intercepts; holes vs vertical asymptotes; horizontal
  asymptotes from the degrees), each with a rule, a worked example that names its
  strategy before computing, and a try-it.

## How it is sequenced

Problems 1–4 are the warm-up: one subskill each, in order. From problem 5 on the
four subskills are fully interleaved — no two consecutive problems use the same
one — so the student has to decide which tool a problem needs rather than repeat
a procedure. Problem 12 is the synthesis challenge: one function, five parts,
requiring every subskill at once (simplify, intercepts, hole height, asymptote,
and a written justification).

Five misconception traps are declared and machine-checked as distinguishable —
counting a canceled factor's zero as an asymptote (problems 3, 5), reading the
hole's height off the original quotient (problem 7), and using constant terms
instead of leading coefficients for a horizontal asymptote (problems 4, 8). They
print in the key so a wrong answer immediately identifies the error.

## Verification — the honest split

**25 verified responses across the 12 problems**:

- **23 are machine-checked** with SymPy — every simplification (checked as an
  identity), every intercept, every excluded value, every asymptote, and every
  hole height (computed as a limit).
- **2 are instructor-judged**, marked `---` in the quick-answer bank: **11(c)**
  (what the degrees tell you about the horizontal asymptote) and **12(e)** (why
  $x=3$ is a hole and not an asymptote). Both are written explanations, so the
  key prints a grading rubric rather than claiming machine verification.

The key's "What is verified" note reports the same 23 of 25, naming problems 11
and 12. No `[unchecked]` marks.
