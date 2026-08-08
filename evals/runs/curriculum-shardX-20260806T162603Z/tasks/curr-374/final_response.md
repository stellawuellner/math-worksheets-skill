# Radicals Do Not Split Across a Sum — Algebra 2 (error analysis)

Three PDFs are ready:

- **Worksheet** (`ws_radsum_curr374.pdf`) — 8 problems, all built around the
  single misconception that $\sqrt{a+b} = \sqrt{a}+\sqrt{b}$ (and its exponent
  twin, $(a+b)^{1/2} = a^{1/2}+b^{1/2}$).
- **Answer key** (`ak_radsum_curr374.pdf`) — quick-answer bank, a "Common wrong
  answers" block, and a worked solution per problem.
- **Study guide** (`ss_radsum_curr374.pdf`, 2 pages) — three sections: test a
  suspect rule with numbers; the rules that *do* hold (products and quotients);
  and how to spot the split-over-a-sum step in someone else's work.

## The find-and-fix items

Four problems (1, 3, 6, 7) present the error and ask the student to compute the
correct value first and then name what went wrong:

- **Problem 3:** "$\sqrt{x^2+9} = x+3$, because the root goes onto each piece."
- **Problem 6:** "$\sqrt{4+x^2}$ simplifies to $2+x$."
- **Problem 7:** "$\sqrt{x}+\sqrt{9} = 5$, so $\sqrt{x+9} = 5$, so $x = 16$."

Every planted wrong result is declared as a **machine-checked misconception
trap**: the verifier recomputes the wrong method ($\sqrt{x^2}+\sqrt{9}$,
$\sqrt{4}+\sqrt{3^2}$, and the merged-radical solve) and confirms the problem's
own check rejects it. All three passed the distinguishability check and print in
the key, so a grader seeing 7, 5 or 16 knows immediately which step produced it.

Problems 1, 4 and 8 make the point numerically instead: the student computes both
sides and sees $5 \ne 7$, $10 \ne 14$, $8.66 \ne 6.24$ for themselves.

## Verification — the honest split

**20 verified responses across the 8 problems**:

- **16 are machine-checked** with SymPy — every numerical evaluation, every
  simplified radical (checked as an algebraic identity), the rounded decimals,
  and the corrected solve in problem 7.
- **4 are instructor-judged**, marked `---` in the bank: **1(c), 3(c), 6(c) and
  7(b)** — the written diagnoses. The key prints a grading rubric for each.

The key's "What is verified" note reports the same 16 of 20, naming problems 1, 3,
6 and 7. No `[unchecked]` marks.
