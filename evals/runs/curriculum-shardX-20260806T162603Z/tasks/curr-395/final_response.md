# Interleaved review: binomial coefficients and expansion structure

Three PDFs for your Algebra 2 student, all on **using binomial coefficients and sequence
structure in expansions**:

- **`ws_binom_curr395.pdf`** — the student worksheet, 12 problems, 5 pages.
- **`ak_binom_curr395.pdf`** — the full step-by-step answer key, 4 pages.
- **`ss_binom_curr395.pdf`** — a 2-page study guide.

## Why the order matters

This is an interleaved review. Problems 1 and 2 are the warm-up — two straight expansions,
one with a positive second term and one with a negative one. After that the four subskills
alternate, so the student has to decide what a question is actually asking before starting:

| Subskill | Problems |
|---|---|
| expand a binomial power completely | 1, 2, 6, 11 |
| pick out one named term or coefficient | 3, 7, 10 |
| read and use a binomial coefficient (Pascal structure) | 4, 8, 12 |
| sum across an expansion (series) | 5, 9 |

The distinction that gets drilled by the interleaving is *do not expand when you do not have
to*: problems 3, 7 and 10 each want a single coefficient, and expanding $(3x-2)^5$ to find
one term is the slow, error-prone route. Problem 11 breaks the skeleton again by making the
first term $x^2$, so the exponents double.

Problem 12 is the synthesis challenge: expand $(1+x)^4$, use it to evaluate $3^4$ by
substitution, then run the same idea backwards to find the exponent whose coefficients add to
512.

## What was verified, and what was not

The key's generated note says it exactly: **14 of the 16 answers are machine-checked with
SymPy; 2 are instructor-judged.**

- **Machine-checked (14):** every expansion was independently re-expanded and compared term
  by term, every coefficient recomputed from the factorial formula, both sums re-summed, and
  the exponent in 12(c) solved independently. A printed answer that disagreed would have
  blocked the build.
- **Instructor-judged (2):** the written explanations in **8(b)** (why $\binom{9}{3}$ and
  $\binom{9}{6}$ must be equal, *without* computing the second) and the written half of
  **12(c)** (why substituting $x=1$ gives the coefficient sum). Both are reasoning asks, so
  they are marked `---` in the Quick Answers bank rather than given a value, and the key says
  what a full-credit response needs. For 8(b) in particular the key is explicit that
  computing $\binom{9}{6}=84$ and noting the match is a *check*, not an explanation, and
  earns partial credit only — that distinction is the whole point of the problem.

## Study guide

Four sections, each with a rule box, a worked example whose opening step explains the choice
of method, and a try-it with the answer upside down inside the box: expanding a power,
picking out one named term (including how to find the index $k$ from the power you want),
reading a binomial coefficient and its symmetry, and summing across an expansion. All 8 of
its worked answers are machine-verified.
