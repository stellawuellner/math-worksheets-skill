# Finding the Fault in a Proof — high-school geometry (6 problems)

Three PDFs are ready:

- **Worksheet** (`ws_proof_faults_curr304.pdf`, 6 pages) — 6 error-analysis problems. Each
  shows a student's actual work (four of them as printed two-column proofs, one as a quoted
  argument) and asks the student to name the faulty line, say what is wrong with its reason,
  and repair it. Three items are full find-and-fix: after diagnosing the break, the student
  redoes the arithmetic and gives the true value. The faults alternate between **circular
  reasoning** (the reason is the claim), **an unsupported statement** (the reason is the
  picture, or a theorem whose hypothesis is not met), and **a broken algebraic step**.
- **Answer key** (`ak_proof_faults_curr304.pdf`, 3 pages) — for every item, which line
  fails, why the cited reason does not do the job, and the correct repair; the three
  numeric items are re-solved line by line with a substitution check. The Quick Answers
  bank also prints a "common wrong answers" line for each planted error, so if a student
  hands back 5, 2, or 10 you can read off exactly which misconception produced it.
- **Study guide** (`ss_proof_faults_curr304.pdf`, 2 pages) — three sections: spotting
  circular reasoning (follow each reason backwards; a chain must end at a given), finding
  and fixing a broken step, and catching an unsupported statement. Rule box, worked
  example, and try-it in each.

## What is verified, and what is not

**3 of the 12 responses are machine-checked with SymPy** — the three corrected values
($x = 8$, $x = 4$, $x = 20$). Note that the key's "What is verified" note says *no problem
is fully machine-checked*, and that is right: every one of the six problems also carries a
written diagnosis, so none of them is verified end to end. In addition, **all three planted wrong answers are
machine-checked as traps**: the verifier recomputes each wrong method, confirms it really
produces the number printed in the problem (5, 2, 10), and confirms that number is
distinguishably wrong. So the planted errors are not hand-typed — they are derived, and
the sheet cannot contain a "mistake" that is accidentally correct.

**9 responses are flagged for your judgement** — every diagnosis: naming the faulty line
and explaining what is wrong with its reason, plus each written repair. That is the
substance of this worksheet and it is prose, so no computer algebra system can grade it.
The answer key states, for each one, exactly which elements a correct diagnosis must
contain (for example, in problem 6: rejecting "vertical angles" on adjacency grounds
*and* naming the Linear Pair Postulate). The Quick Answers bank marks these `---`; no
`[unchecked]` marks appear.

## Notes

Standards: HSG-CO.C for the geometric proof faults, HSA-REI.A.1 for the two items about
justifying steps in solving an equation. Difficulty ramps 2 to 5, ending with a proof that
cites a real theorem whose hypothesis is not satisfied — the hardest fault to see, because
the reason column looks entirely legitimate.
