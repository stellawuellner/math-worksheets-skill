# Solving Exponential and Logarithmic Equations — Algebra 2

Three PDFs are ready:

- **Worksheet** (`ws_expleq_curr378.pdf`) — 10 problems on solving exponential
  and logarithmic equations.
- **Answer key** (`ak_expleq_curr378.pdf`) — quick-answer bank, a "Common wrong
  answers" block, and a worked solution per problem.
- **Study guide** (`ss_expleq_curr378.pdf`, 2 pages) — four sections: match the
  bases; take a logarithm of both sides; logarithmic equations (with the domain
  check); and growth and decay models. Each has a rule, a worked example that
  names its strategy first, and a try-it.

## Representations and applications

Three problems are real models with the units stated: a bacteria culture tripling
hourly ($N = 500 \cdot 3^t$, $t$ in hours), an account compounding annually
($A = 2000(1.06)^t$ dollars, answer to the nearest cent), and a tracer decaying
with a 12-day half-life ($A = 100(0.5)^{t/12}$ mg, answer in days). The decay
problem is the one that genuinely needs logarithms, so the method choice is
motivated rather than decorative. No story detail that the mathematics does not
use.

The method choice is the point elsewhere too: problems 1, 5 and 9 have a common
base and are solved exactly with no logarithm; problems 4 and 8 do not, so a
logarithm and a rounded decimal are the honest answer. Problem 7 plants the
classic extraneous candidate $x = -2$ — declared as a machine-checked trap, so
the verifier confirms the problem can distinguish "solved the quadratic and kept
both roots" from the correct answer.

## Verification — the honest split

**12 verified responses across the 10 problems**:

- **11 are machine-checked** with SymPy — every exact solve (with the real-domain
  restriction set, so a spurious complex branch cannot slip through), every
  rounded decimal, and the model evaluations.
- **1 is instructor-judged**, marked `---` in the bank: **10(c)**, the domain
  condition on the two logarithm inputs and why a candidate outside it must be
  discarded. The key prints what a correct response must contain.

The key's "What is verified" note reports the same 11 of 12, naming problem 10.
No `[unchecked]` marks.
