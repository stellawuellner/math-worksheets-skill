# Binomial Coefficients in Expansion and Probability — Precalculus / Advanced Statistics

Three PDFs are ready.

**Study guide (2 pages)** — four sections, each with a rule box, a two-step
worked example, and a try-it whose answer is printed upside down inside the box:

1. evaluating $\binom{n}{k}$ from the factorial formula, plus the symmetry rule
   and Pascal's rule
2. expanding with the binomial theorem — and the warning that a term's
   coefficient is $\binom{n}{k}$ *times* the powers of the constants
3. counting your way to a probability — favourable over total, both counted the
   same way, for draws without replacement
4. binomial probability for repeated independent trials —
   $\binom{n}{k}p^k(1-p)^{n-k}$, with an explicit note on when *not* to use it

The third and fourth sections are deliberately adjacent, because choosing
between them is the decision students get wrong most often.

**Worksheet (7 pages, 12 problems)** — the sheet is built around one idea: the
same number $\binom{n}{k}$ does two different jobs, and the student has to
notice which is wanted. Problems 1 and 2 are the warm-up (one coefficient, one
expansion). After that the four uses rotate: a committee-selection probability
(3), Pascal's rule with an explanation of where it lives in the triangle (4), an
expansion where both terms carry coefficients (5), a coin-flip probability read
off row 6 of the triangle (6), the coefficient of $x^5$ in $(x+3)^8$ (7 — where
answering $\binom{8}{5}=56$ instead of $1512$ is the designed trap), a
without-replacement marble problem (8), a free-throw binomial probability (9),
and the constant term of $(2x + 1/x)^6$ (10). Problem 11 is an error analysis:
Jo claims the probability of exactly 2 heads in 5 flips is $2/5$, and the
student has to produce $5/16$ and name the confusion. The synthesis challenge
(12) asks for the term of $(q+p)^8$ that answers a defect-rate question, its
exact value $5103/16384$, and an explanation of why the binomial coefficients in
that expansion *are* the counts of which components failed.

Work space runs 5–9 cm per problem, growing with the multi-part questions.

**Answer key (4 pages)** — quick answers at the top, a generated Curriculum
section, then a stepped solution per problem showing the cancellation, the
general term, or the two counts, as appropriate. Problem 7's solution names the
$56$-instead-of-$1512$ error explicitly, and problem 8's explains why that
situation is *not* the binomial formula.

**Verification.** All 12 problems were machine-checked with SymPy — 24 checks in
total, since most problems ask for the intermediate counts as well as the final
value. 22 passed automatically: every binomial coefficient was recomputed from
factorials, both expansions were checked symbolically, and every probability was
compared as an exact fraction.

**Flagged for manual review — two items**, both genuinely open writing:
problem 11(c) (describe Jo's mistake) and problem 12(c) (why the coefficients
are the counts). The key says what to accept for each rather than claiming they
were verified. Problem 4's "state the relationship" is answered in full in the
key; its three numeric values are machine-verified.

Standards: HSA-APR.C.5 (coefficients and expansions) and HSS-CP.A–HSS-CP.B
(probability). Difficulty ramps 1 → 5 across the sheet.
