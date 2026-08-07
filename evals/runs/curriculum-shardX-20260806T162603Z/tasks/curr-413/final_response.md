# Exponential models — fitting and interpreting (Precalculus)

Three PDFs are ready.

**Study guide (`ss_expmodels_curr413.pdf`, 2 pages)** — four sections, each with a
rule box, a worked example that opens by naming *why* that tool applies, and a
try-it whose answer is printed upside down inside the box: fitting $y = ab^x$ to
two data points, reading the growth/decay rate off the base, solving for time
with logarithms, and rewriting a model with a new base (including base $e$).
Hand this to your student first.

**Worksheet (`ws_expmodels_curr413.pdf`, 5 pages)** — 10 applied problems, every
one stating its variable and its units: a savings account, a bacteria culture, a
drug dose, a town population, a car's value, a continuously compounded
investment, a radioactive tracer, a city's water use, two analysts modelling one
fund, and a cooling cup of coffee. The four methods are interleaved after the
first problem, so the student has to choose the method rather than repeat it.
Difficulty ramps 1 → 5, finishing with the coffee problem, where the room
temperature has to be subtracted before anything decays exponentially.

**Answer key (`ak_expmodels_curr413.pdf`, 4 pages)** — full worked solutions, a
Quick Answers bank for fast grading, and a Curriculum section listing the
standards (HSF-LE.A.4, HSF-BF.B.5) against the problems that exercise them.
Four problems also print a "common wrong answer" line naming the misconception
the numbers were chosen to expose (linear-instead-of-exponential decay,
$\ln A/\ln B$ instead of $\ln(A/B)$, dropping the half-life divisor, and
forgetting the ambient temperature).

## What is verified, honestly

The sheet asks for **20 responses across the 10 problems**.

- **18 are machine-checked** by SymPy before anything compiled — every growth
  factor, every rate, every time, every balance, plus the algebraic identity
  $300(1.06)^{2t} = 300(1.1236)^t$ in problem 9, which is checked as an identity
  in $t$, not at a sample value.
- **2 are instructor-judged** and marked `---` in the Quick Answers bank:
  problem 8(c) ("explain why 9% a year for 10 years is not a 90% drop") and
  problem 9(c) ("justify that the two models agree for every $t$"). Both are
  written explanations, so no computer algebra system can grade them. The answer
  key prints a grading rubric for each — 8(c) needs the *multiplicative* reason,
  not just the number 61.1%; 9(c) needs the law of exponents rather than a check
  at one value of $t$.

That is the same split the key's own "What is verified" note reports. Nothing on
this sheet is marked `[unchecked]`: there is no printed answer blank that the
verification data does not cover.

The four declared misconception traps were each re-computed and confirmed to land
on a value the problem's own check rejects, so each trap really does distinguish
the error it names.
