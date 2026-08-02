Three PDFs are ready for an AP Calculus AB/BC student on **differentiating
inverse and inverse-trigonometric functions**:

- **Worksheet — 10 problems, procedural-fluency ramp, no repeated skeleton.**
  It opens with the worked pattern for $\frac{d}{dx}\arctan(u)$ and then moves
  through: a linear inner function (1), a quadratic inner function (2), the
  inverse-function derivative $(f^{-1})'(a) = 1/f'(b)$ in two forms — one where
  $b$ must be solved for from a cubic (3) and one where $b$ is read off by
  inspection (7) — the product rule with $\arctan$ (4) and with $e^x$ (8), the
  $\arccos$ sign trap (5), a radical inner function whose denominator collapses
  (9), and two second derivatives (6, 10). Difficulty runs 1 → 5.
- **Answer key — the chain-rule factor written out every time.** Each solution
  names the inner function $u$ (or the rule being combined) before
  differentiating, since $u'$ is the mark most often lost. Three problems carry
  a note on the classic wrong answer: $\sqrt{1-x^2}$ instead of $\sqrt{1-x^4}$
  in problem 2, $1/f'(4) = 1/50$ instead of $1/f'(1)$ in problem 3, and the
  structural check on where the $16$ comes from in problem 10. A quick-answer
  bank sits at the top for grading.
- **Study guide — 2 pages, four sections**: the three arc-derivative formulas
  with the chain rule, the inverse-function derivative with its four-step order
  of work, products with an arc-function, and second derivatives via rewriting
  as a power. Each has a rule box, a worked example whose first step says why
  that tool applies, and a try-it with the answer upside down inside the box.

**Verification:** every printed answer is machine-checked. The ten worksheet
answers were recomputed by SymPy — eight as symbolic derivatives (`diff`,
including two second derivatives), one as an exact real root (`solve`, with the
real domain declared so the two complex roots of the cubic cannot be silently
dropped), and two as exact evaluations (`eval`) — and so were all eight
study-guide answers. Nothing on this sheet is an open response, so nothing is
flagged manual. Prose numbers bind 12/12 to the verification data on the
worksheet and 25/25 on the study guide. Final verdict: **BUILD PASSED — all
gates green** (worksheet 4 pages, key 3, guide 2).
