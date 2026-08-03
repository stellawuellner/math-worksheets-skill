# Convergence and Taylor Series --- Inconclusive Tests and Omitted Endpoints (AP Calculus BC)

Three PDFs are ready: the student worksheet, a full step-by-step answer key, and
a two-page study guide.

## What is on the worksheet (8 problems)

Both errors this sheet targets are errors of *logic*, not of algebra, so every
problem asks the student to name the test used and say exactly what it licenses.

1. **Warm-up** --- $a_n = \frac{4n+1}{n+7}$ has $\lim a_n = 4 \neq 0$, so the
   series diverges by the $n$th-term test. The one direction that test can prove.
2. **Find and fix** --- Devi computes $\lim 1/\sqrt{n} = 0$ (correct) and
   concludes convergence (not). The limit is **0**; the test says nothing there;
   the $p$-series test settles it as divergent. This series is the standing
   counterexample to Devi's rule.
3. **Find and fix** --- a geometric series where the ratio test correctly gives
   convergence but the student divides by $r$ instead of $1 - r$ and reports 6.
   The exact sum is **3**.
4. $\sum \frac{1}{n(n+1)}$, where the ratio test returns exactly 1 and settles
   nothing. Partial fractions and a telescoping partial sum give **1**; a
   classmate's 0.5 is the first term promoted to an answer.
5. (a) Both ratio-test limits for $\sum 1/n$ and $\sum 1/n^2$ are **1**.
   (b) Explain why $L = 1$ can never be evidence either way, and name the test
   that settles each. *(Part (b) open --- manual review.)*
6. A power series centred at $c = 2$ with radius $r = 3$: the endpoints are
   **-1 and 5**. An answer of 3 treats the radius as a coordinate --- the centre
   shift was dropped.
7. **Find and fix** --- a student reports an open interval "because the ratio test
   gave a strict inequality". Substituting the left endpoint gives
   $\sum (-1)^n/n$, whose exact sum is **$-\ln 2$**, so the left endpoint *does*
   belong. The key also explains why the sum must be negative.
8. **Challenge** --- write the complete interval with the right bracket at each
   end, justify each end by name, and explain why no ratio-test computation can
   ever decide an endpoint. *(Open --- manual review.)* The answer is $[-1, 5)$;
   the asymmetry is the whole point.

All eight problems bear on the two named errors. Problems 2, 3 and 7 are the
find-and-fix items.

## What was machine-verified

Nine of the eleven checks were verified independently by the SymPy verifier
before anything printed: all four limits, all three infinite sums (including the
telescoping series and the alternating harmonic series, which is checked as the
exact value $-\ln 2$, not a decimal), and both interval endpoints. The two items
labelled **manual review** are 5(b) and 8 --- the explanations --- and each gets a
full model answer plus a "look for" list in the key, including the answers that
restate the rule without explaining it.

Four declared misconception traps were proved distinguishably wrong by the
verifier and print in the key's "Common wrong answers" block:

- geometric sum as $a/r$ instead of $a/(1-r)$ (6 instead of 3);
- the first term reported as the sum of the series (0.5 instead of 1);
- the radius reported as an endpoint (3 instead of -1 and 5);
- the alternating sum kept positive ($\ln 2$ instead of $-\ln 2$).

## The study guide

Two pages, three sections, each with a rule box, a worked example, and a separate
try-it whose answer is printed upside down inside the box:

1. the $n$th-term test goes one way --- a non-zero limit proves divergence, a zero
   limit licenses nothing;
2. when the ratio test says nothing --- $L = 1$ is compatible with both outcomes,
   so switch tools, plus the geometric sum formula and the slip that ruins it;
3. endpoints of the interval --- $c \pm r$, why the ratio test is guaranteed to be
   silent at both ends, and why one end may be included while the other is not.

## Note

The course label prints on the answer key only, in the generated Curriculum
section (LIM-7, LIM-8; difficulties 1--5).
