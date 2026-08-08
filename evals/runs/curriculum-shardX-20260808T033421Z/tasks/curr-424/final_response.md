# Find and fix: illegal cancellation and lost solutions (Precalculus)

Three PDFs are ready.

**Study guide (`ss_trigcancel_curr424.pdf`, 2 pages)** — three sections, each a
rule box, a worked example whose first step names the trap being avoided, and a
try-it with the answer upside down inside the box: factor rather than cancel; the
three places solutions go missing (one square root, an un-widened multiple-angle
interval, a factor wrongly declared impossible); and testing for extraneous roots
after squaring.

**Worksheet (`ws_trigcancel_curr424.pdf`, 5 pages)** — 8 find-and-fix problems.
Each shows work a student handed in, and asks for the complete correct solution
set and then a written diagnosis. Four are cancellation errors (dividing by
$\sin\theta$, by $\cos\theta$, cancelling a factor out of only part of a term,
and the synthesis problem 8 which does it *and* forgets to widen). Three are
lost-solution errors (one square root, an un-widened doubled angle, a factor
wrongly discarded). One is the mirror fault — squaring, which *invents* a root.
Difficulty ramps 1 to 5.

**Answer key (`ak_trigcancel_curr424.pdf`, 4 pages)** — full worked solutions,
including the substitute-back test written out for problem 4, a Quick Answers
bank, and a Curriculum section for HSF-TF.C.8.

## What is verified, honestly

The sheet asks for **17 responses across the 8 problems**, and the split is close
to even:

- **9 are machine-checked** by SymPy: every corrected solution set (checked for
  *completeness* on its interval, which is exactly the property every one of
  these problems is about), the algebraic simplification in 6(a), verified as an
  identity in $\theta$ rather than at a sample angle, and its value in 6(b).
- **8 are instructor-judged** and printed as `---` in the Quick Answers bank —
  one per problem, the written diagnosis. Naming an error is prose. The answer
  key prints a rubric for each; problem 8's requires **two** faults named *and*
  the missing solutions attributed to the right one.

That matches the key's own "What is verified" note. Nothing is marked
`[unchecked]`.

**Every planted wrong answer is a declared, machine-checked misconception trap** —
eight of them, one per problem. The verifier recomputed each and confirmed it is
distinguishable from the correct answer, and it reports *how*: seven traps drop
specific solutions (it names which), and problem 4's trap adds one. That is the
whole pedagogy of this sheet made mechanical.
