# Factoring Special Forms: Squares — Algebra 1

Three PDFs are ready:

- **Study guide** (`ss_special_factoring_curr288.pdf`, 2 pages) — the two patterns, three worked examples, three try-its.
- **Worksheet** (`ws_special_factoring_curr288.pdf`, 4 pages, 10 problems).
- **Answer key** (`ak_special_factoring_curr288.pdf`, 2 pages) — full reasoning plus a quick-answer bank.

## What the worksheet does

All ten problems are the two special forms and nothing else, so the sheet is
about *recognising which pattern applies* rather than grinding factor pairs.

- **Difference of squares** (1, 3, 5, 8, 10): plain $x^2 - 49$; then $9x^2 - 16$
  where the coefficient has to be recognised as a square; then a patio
  application ($x^2 - 16$ paved area); then an error-analysis item; then
  $x^4 - 81$, which is a difference of squares twice over and stops at a sum of
  squares.
- **Perfect-square trinomial** (2, 4, 7): positive middle term, then a negative
  middle term with a leading coefficient, then a mosaic whose area
  $x^2 + 14x + 49$ factors to give its side length.
- **Common factor first** (6, 9): $2x^2 - 50$ and $18x^2 - 32$, neither of which
  is a difference of squares until the common factor comes out. This is the
  single most common "factor completely" miss.

The two patterns alternate rather than being blocked, so no student can coast on
"this page is all differences of squares". Difficulty ramps 1 → 4.

The sheet opens with one **value-free area-model reference figure** (a square of
side $x + a$ cut into four regions), captioned so it cannot be read as any one
problem's givens. It is the geometric reason the identities hold, and it is the
only figure on the sheet — no problem carries its own valued figure, so nothing
can be misattributed.

## What was verified

**Eleven machine checks passed** across the ten problems, using SymPy's
`factor`, `expand` and `equiv`. Problem 8 carries two checks: the planted wrong
answer $(x-3)^2$ is expanded to $x^2 - 6x + 9$ (proving it is *not* $x^2 - 9$)
and the correct factorization is verified independently — so the error analysis
is machine-checked in both directions rather than asserted.

**One item is flagged for manual review**: the one-sentence explanation in
problem 8 of which pattern the student confused. That is an open response and is
declared `manual` rather than claimed as verified, so the build ends at exit 2
with it named. The key gives the accept criteria for that sentence.

No misconception traps are declared: `traps` are allowed only on types with a
single comparable numeric answer, and every problem here has a symbolic answer.
The error-analysis problem carries the equivalent teaching value in a form the
verifier can actually check.

## Standards and tagging

`HSA-SSE.B.3` — from the "Polynomial arithmetic/factoring" row of
`references/standards-map.md`, used verbatim, on all ten problems. Each problem
also carries a difficulty (ramp 1,1,2,2,2,3,3,3,4,4), a Bloom level (5 apply,
6 analyze, 1 justify) and one of three skill tags; the three-facet plan is
declared in the verify JSON and its subtitle is bound verbatim into the
worksheet title block.

## Study guide

Two pages, three sections matching the three skills, each with a rule box, a
worked example whose first step names the trigger for the pattern, and a try-it
with the answer upside down inside the box. The formula box lists the squares
worth knowing on sight, including $4x^2 = (2x)^2$ and $x^4 = (x^2)^2$, because
recognition is what this topic rewards. The watch-out box carries the exact
mistake problem 8 dissects: $x^2 - 9 \neq (x-3)^2$.

## Gate chain

`build.sh` finished **BUILD PASSED** (exit 2 — green with one manual-review
item): template shells, both verification files, skill and facet coverage,
subtitle binding, figure scope and work space, three compiles inside their page
budgets (4 / 2 / 2 pages), per-problem answer-key binding, study-guide
structure, and prose consistency (100% on the worksheet). No gate failed on the
first attempt.
