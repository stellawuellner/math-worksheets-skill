# Sums of Radicals: What Combines and What Does Not — Grade 8 / Pre-Algebra

Three PDFs are ready.

**Study guide (`ss_radicals_curr204.pdf`, 2 pages)** — three sections, each with a
rule box, a worked example and a try-it whose answer is printed upside down in
the box:

1. **Simplifying one radical** — roots split over *products* ($\sqrt{ab} =
   \sqrt{a}\sqrt{b}$) and there is no rule for $\sqrt{a+b}$. This is the legal
   rule the invalid one is copied from, so it is stated first.
2. **Combining like radicals** — simplify each term first, because unlike
   radicands often match once simplified; then add coefficients only.
3. **Testing a claim with decimals** — how to kill a plausible-looking rule in
   one line, and why perfect squares make the sharpest counterexample.

**Worksheet (`ws_radicals_curr204.pdf`, 4 pages)** — 8 problems, every one on the
same focus. Problems 1–3 build the machinery (simplify $\sqrt{72}$; combine like
radicals; $\sqrt{8}+\sqrt{18}$, where the radicands only match after
simplifying). Problems 4, 5 and 7 are find-and-fix items carrying the three
distinct forms of the error: adding radicands under one root
($\sqrt9+\sqrt{16}=\sqrt{25}$), adding coefficients *and* radicands
($4\sqrt5+3\sqrt2 = 7\sqrt7$), and collecting radicands in a case where the terms
genuinely do combine but by a different route ($\sqrt2+\sqrt8$). Problem 6 is a
three-term simplification, and problem 8 is a written explanation. Difficulty
ramps 1 → 4.

**Answer key (`ak_radicals_curr204.pdf`, 4 pages)** — quick-answer bank at the
top, generated from the verification data, then full worked solutions. Each
find-and-fix solution names the invented rule before giving the correct work, and
the key prints a "common wrong answers" line for every planted number — for
example, *if they got 5.10: added the radicands and took one square root, writing
$\sqrt{26}$*. Problem 6's note is worth reading: the wrong answer 6 and the right
answer 6.93 are close enough that estimating alone will not catch it. The
standard (8.NS.A) and difficulty range print in the key's curriculum section
only; the student's pages carry no grade label.

**What was machine-verified.** Eleven machine checks, all passing. Exact radical
forms were checked symbolically with SymPy (so $\sqrt{72} = 6\sqrt2$ and
$\sqrt{12}+\sqrt{27}-\sqrt3 = 4\sqrt3$ are verified as *identities*, not as
decimals), the decimal values were recomputed independently, and the two
comparisons were evaluated as orderings. Five misconception traps were declared
and each confirmed *distinguishable*: the wrong method must land on a visibly
different number, or the problem cannot teach the error it targets.

**Flagged for manual review.** Problem 8 is an open written response and is
labelled manual rather than claimed as verified. The key supplies a model answer
— including the reason the rule fails, that squaring $\sqrt a + \sqrt b$ leaves
an extra $2\sqrt{ab}$ — and tells a reviewer what to look for: identical
radicands *after simplifying* named as the condition, a counterexample whose
arithmetic is carried out, and no claim that the rule works for perfect squares,
since the perfect-square case is precisely the counterexample.
