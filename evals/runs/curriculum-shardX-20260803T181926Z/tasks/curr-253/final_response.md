# Rewriting Expressions with Distributive Structure — Algebra 1

Three PDFs are ready:

- **`ws_distributive_curr253.pdf`** — the student worksheet (4 pages, 10 problems)
- **`ss_distributive_curr253.pdf`** — the study guide / skills summary (2 pages)
- **`ak_distributive_curr253.pdf`** — the full step-by-step answer key (3 pages)

## What the worksheet covers

All ten problems are the same idea seen from four directions, so the student has
to *decide* which direction a problem is asking for rather than repeat one
procedure:

1. **Distributing over a sum** (problems 1–3) — a mural's area $6(2x+5)$, a gym
   billing $9(4x+15)$ dollars, and $6$ boards of $(2x-9)$ inches, which is the
   first one where a sign has to travel with the second term.
2. **Expanding two binomials** (5, 9) — a patio $(x+3)$ by $(x+8)$ ft, and a rug
   $(2x+3)$ by $(x+6)$ ft where the leading coefficient is no longer 1.
3. **Factoring out the greatest common factor** (4, 7, 10) — including one with
   a variable in the GCF, $15x^2 + 10x = 5x(3x+2)$.
4. **Checking equivalence** (6, 8) — one "is this claim true" rewrite, and one
   error-analysis problem where a student's wrong form $10x - 3$ is tested
   against the original at $x = 4$.

Problem 10 is the closing challenge: distribute twice, combine, then factor the
result — the whole sheet in one problem.

Every problem states its units and givens explicitly; the area problems carry
ft$^2$ / cm$^2$ answer lines, and the money problems say "in dollars" in the
stem. Difficulty ramps 1 → 5 across the sheet.

## What was verified

Every answer was checked independently by SymPy before anything compiled — 11
checks across the 10 problems (problem 10 is checked twice, once for the
combined form and once for the factored form). **All 11 passed; nothing is
flagged for manual review**, because every task on this sheet has a
machine-checkable answer.

The declared misconception trap on problem 8 (distributing to the first term
only, giving $37$ instead of $25$) was machine-checked as *distinguishably*
wrong, so the problem really does catch the error it was designed around. That
wrong answer is printed in the key's "common wrong answers" block for grading.

The study guide's four worked examples and four try-it items were verified the
same way (8 more checks, all passed), and the gate chain confirms that every
skill the worksheet tests has a matching worked example and try-it in the guide.

## Using them

Give the study guide first — it has the rule, an area model, a worked example
and a try-it for each of the four skills, with the try-it answers printed upside
down inside their boxes so the student can self-check. The answer key shows the
reasoning for every problem, not just the answers, plus a quick-answer bank at
the top for fast grading and a curriculum section listing the standard
(HSA-APR.A.1) and difficulty range.
