# Find and Fix: Separable Equations and Initial Conditions — AP Calculus AB/BC

Three PDFs are ready:

- **`ws_sepfix_curr484.pdf`** — the student worksheet, 8 error-analysis problems.
- **`ak_sepfix_curr484.pdf`** — the full step-by-step answer key.
- **`ss_sepfix_curr484.pdf`** — a 2-page study guide.

## What the worksheet does

Every one of the eight problems shows a piece of student work that is wrong
somewhere, and asks two things: **(a)** produce the corrected value, and
**(b)** name what rule was broken. That is the whole point of an error-analysis
sheet — a student who can only compute cannot yet grade.

The eight errors are deliberately the three that actually happen in this topic:

- **Separation and integration** (problems 1, 2, 6): dropping the $\tfrac12$ that
  $\int y\,dy$ carries; raising the power without dividing by it; and refusing to
  separate $x + xy$ because it "has a sum" when it factors as $x(1+y)$.
- **Where the constant goes** (problems 3, 7): writing $y = e^{F(x)} + C$ instead
  of $Ae^{F(x)}$, and reading the constant off $y$ rather than $y^2$.
- **Substituting the starting values** (problems 4, 5, 8): using the initial
  value additively, and reading $C$ off a numerator without the division.

Problem 7 puts two competing student solutions side by side; problem 8 is a
four-line solution with exactly one bad line to locate.

## Verification — and what only you can grade

The answer key's "What is verified" note says this too, so the two agree:

- **8 of the 16 checks are machine-verified with SymPy** — every corrected value
  in the (a) parts, recomputed from the givens.
- **6 of those 8 also carry a machine-checked misconception trap.** The wrong
  number printed in each stem (1613.715, 13.389, 4.123, 2002.46, 2, 5.325) was
  *computed* from the wrong method, not invented, and SymPy confirmed each one is
  far enough from the right answer that a student using the correct method can
  never land on it. Those traps are reprinted in the answer key as a "Common
  wrong answers" line, so when a paper shows 4.123 you know immediately it is
  the dropped one-half rather than an arithmetic slip.
- **8 of the 16 are instructor-judged** — the (b) diagnoses, one per problem.
  Prose cannot be CAS-checked. Each carries a written rubric in the answer key
  saying what full credit requires and, where useful, what earns half credit.

So the honest split is **half machine-checked, half yours**. That is the correct
outcome for an error-analysis sheet, not a shortfall: the diagnosis is the skill
being taught, and no automatic checker can read it. Nothing is marked
`[unchecked]` — every printed answer slot has an entry behind it.

## Notes

- Problem 4's corrected answer comes out to exactly 5, which is worth pointing
  out to a student who assumes a "hard" problem must have an ugly answer.
- Problem 5 is worth doing out loud: the sanity check (fifteen years of six
  percent growth adding $2.46 to a $2000 balance) is the transferable habit.
- The grade level and the FUN-7 tagging print on the answer key only.
