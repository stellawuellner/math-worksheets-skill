# Finding and Verifying Inverse Functions — Algebra 2

Three PDFs are ready:

- **Study guide** (`ss_inverses_curr382.pdf`, 2 pages).
- **Worksheet** (`ws_inverses_curr382.pdf`, 5 pages, 12 problems).
- **Answer key** (`ak_inverses_curr382.pdf`, 3 pages) — every swap-and-solve step, plus the composition check.

## What the worksheet does

- **Find an inverse algebraically** (1, 2, 3, 6, 7, 10): $x+7$ and $5x$ as
  warm-ups, then $3x-8$ (two operations, undone in reverse order), then
  $\frac{x-4}{5}$, then $\sqrt{x-2}$ (where the inverse's domain is the real
  question), and finally the rational $\frac{2x+1}{x-3}$, where the whole
  problem turns on factoring $y$ out of both terms.
- **Verify a pair by composition** (4, 8): both directions computed, once as a
  straight verification and once as "is Sofia right?".
- **Inverse values, domain and restriction** (5, 9, 11, 12): $f^{-1}(11)$ from
  a formula; $x^2$ restricted to $x\ge0$; $f^{-1}(-4)$ computed two ways that
  must agree; and $x^2-4$, where the student must say why no inverse exists
  before restricting.

Difficulty ramps 1 → 5 and no two problems share a skeleton.

## What was verified

**17 machine checks across the 12 problems passed under SymPy**, and every
boxed answer in the key was bound to its own problem. The encoding is worth a
note, because it decides how much the gate is actually proving:

- The "find the inverse" problems are checked as `solve`: SymPy solves
  $x = f(y)$ **for $y$** and compares against the claimed inverse formula. So
  the verified answer is the inverse itself, not a downstream consequence — and
  the key's Quick Answers bank prints the real formulas ($x-7$, $\frac{x+8}{3}$,
  $5x+4$, $x^2+2$, $\frac{3x+1}{x-2}$) rather than a column of "$x$".
- The "verify a pair" problems are checked as `equiv`, one entry per direction,
  each confirming the composition simplifies to $x$. Here "$x$" *is* the answer.
- The value problems are `eval`, and problem 11 additionally carries a `solve`
  check so the two routes to $f^{-1}(-4)$ are independently confirmed to agree.

**One item is `manual`:** part (a) of problem 12 — explaining why $x^2-4$ has
no inverse on the reals. That is an argument, not a computation, so it is
declared `manual`; the key gives a model answer and a full-credit rubric.

Two traps were declared and machine-checked as distinguishably wrong, and print
in the key's "Common wrong answers" block: evaluating $f$ instead of $f^{-1}$
($43$ for $f^{-1}(11)$), and dividing before subtracting ($-6.33$ for
$f^{-1}(-4)$).

One solver limitation, tested rather than assumed: for the rational function in
problem 10, `solve` with the default real domain returns the **empty set** —
SymPy's real `solveset` gives up on a parameterised rational equation — so that
one entry declares `"domain": "complex"`. The single root it returns is real,
and a second `equiv` entry on the same problem confirms the composition
collapses to $x$ over the reals, so nothing is taken on trust.

## Standards and tagging

`HSF-BF.A.1c, HSF-BF.B.4` on every problem, copied verbatim as the one string
`references/standards-map.md` writes for "Function composition/inverse". Every
problem also carries a difficulty, a Bloom level (2 recall, 8 apply, 7 analyze,
1 justify), a skill tag and a facet tag; the three-facet plan is declared in the
verify JSON and its subtitle is bound to the worksheet title block.

## Study guide

Two pages, three sections matching the three skills, opening with a rule box
that states the two things students most often get wrong: $f^{-1}$ is not
$1/f$, and domain and range swap. Each section has a rule box, a worked example
whose first step chooses the method, and a try-it with the answer upside down
inside the box. The watch-out is the reverse-order rule: for $3x+5$ the inverse
is $\frac{x-5}{3}$, not $\frac{x}{3}-5$.

## Gate chain

`build.sh` finished **BUILD PASSED** (exit 2, manual-review item) on the first
attempt of the final design — no gate failed. All 21 gates green: ws 5/6 pages,
ak 3/6, ss 2/2.

Before that first build I revised the verification encoding: an earlier draft
checked the find-an-inverse problems only by `equiv` on the composition, which
passes the gate but makes every expected answer literally "$x$", so the
generated Quick Answers bank would have been useless for grading. Switching to
`solve` for $y$ fixed that. Worth flagging because the gate would not have
caught it — it is a quality failure, not a gate failure.
