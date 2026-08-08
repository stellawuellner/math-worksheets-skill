Here are the three PDFs for a 12-problem precalculus review set on **using binomial
coefficients in probability and algebraic expansion**.

**Worksheet — `ws_binomial_curr440.pdf` (5 pages).** Problems 1 and 2 are the warm-up: one
coefficient, one small expansion. After that the four subskills — evaluating $\binom{n}{k}$
and reading Pascal's triangle, expanding a binomial power, pulling out a single term, and
binomial probability — are deliberately interleaved so no two consecutive problems use the
same method and the student has to decide which tool the problem needs. Difficulty ramps
1 → 5 and the sheet closes with a synthesis item on $(2x+3)^7$ that requires the
coefficient *and* the reason the exponents pair the way they do.

The design deliberately reuses one context across methods: the same five free throws at
$p = 0.4$ appear in problem 7 (exactly 3) and problem 9 (at least 4), so the difference
between one binomial term and a sum of terms is visible in the student's own numbers rather
than asserted.

**Answer key — `ak_binomial_curr440.pdf` (4 pages).** Every problem restated and worked,
with a quick-answer bank, a curriculum block, and a "common wrong answers" list generated
from three machine-checked misconception traps: computing a permutation count instead of a
combination (problem 1), using the coefficient and forgetting the power (problem 4), and
dropping the coefficient so only one ordering is counted (problem 7).

**Study guide — `ss_binomial_curr440.pdf` (2 pages).** Four sections matching the four
subskills, each with the rule, a worked example that opens by naming why that method fits,
and a try-it with the answer printed upside down inside the box.

**What was verified, honestly.** The sheet asks for **16 separate responses**. **12 are
machine-checked** with SymPy — every binomial coefficient and single-term coefficient
recomputed from factorials, both full expansions checked as algebraic identities, and the
two rounded probabilities recomputed exactly and compared at the printed precision. **4 are
instructor-judged** and marked `---` in the quick-answer bank: the "why two terms" argument
in 9(b), the counting interpretation of the coefficients in 10(b), the row-sum argument in
11(b), and the exponent argument in 12(b). Those four are the reasoning that makes the
sheet more than arithmetic, and none of them is checkable by a computer algebra system —
so the key prints a full model argument and an explicit full-credit criterion for each. The
eight study-guide examples and try-its are machine-checked.

No response is marked `[unchecked]`: everything printed carries either a machine check or a
written rubric.
