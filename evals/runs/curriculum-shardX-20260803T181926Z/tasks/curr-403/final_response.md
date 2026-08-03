# Finding Inverses with Domain Restrictions — Precalculus

Three PDFs are ready:

- **`ws_inverses_curr403.pdf`** — the student worksheet (5 pages, 10 problems)
- **`ss_inverses_curr403.pdf`** — the study guide / skills summary (2 pages)
- **`ak_inverses_curr403.pdf`** — the full step-by-step answer key (4 pages)

## What the worksheet covers

The sheet is built around the thing students skip: **an inverse is not finished
until its domain is stated.** Every problem asks for the formula *and* the
domain, and nine of the ten involve a restriction that actually changes the
answer.

1. **Invert and state the domain** (problems 1, 2, 7) — a linear warm-up, then
   $\sqrt{x-4}$ where the squaring step is exactly what forces a domain, then
   $\sqrt{2x-6}+1$ where the operations have to be peeled off in reverse.
2. **Restrict a quadratic and pick the branch** (3, 5, 6, 9) — a right branch, a
   left branch (where the $\pm$ must resolve to minus), a downward parabola
   restricted to $x \le 0$, and problem 9, which asks the student to *find* the
   restriction from the vertex rather than being handed it.
3. **Verify by composition** (4, 8) — a rational function whose inverse has an
   excluded value coming from a horizontal asymptote, and an error-analysis item
   where Priya undoes the shift but squares where she should take a root.

Every problem also asks for a numeric round trip ($f^{-1}(a)$ checked against
$f$ of the answer), which is what makes the algebra self-checking. Difficulty
ramps 1 → 5.

## What was verified, and what is not

Nineteen machine checks cover problems 1–9 — the two composition identities, the
vertex equation, and the sixteen round-trip evaluations — and **all nineteen
passed**. Because each inverse formula is tested at a value in both directions,
a wrong formula could not have survived the gate.

**Problem 10 is deliberately labelled for manual review.** It asks the student
to explain *why* one-to-one is required, using $f(x)=x^2-4$ at $x=3$ and
$x=-3$, and to describe a restriction that repairs it. That is open reasoning,
so no computer-algebra check can grade it. The answer key carries a full model
answer and a grading note listing what full credit requires — a concrete pair of
inputs sharing an output, the statement that a function cannot return two
values, a named restriction, and the resulting domain and range. A student who
only writes "it fails the horizontal line test" has restated the condition, not
explained it.

One misconception trap was declared and machine-checked as distinguishably
wrong: Priya's rule giving $77$ where the true value is $-1$ (problem 8). It is
printed in the key's common-wrong-answer block.

The study guide's three worked examples and three try-it items were verified the
same way (eight more checks, all passed).

## Using them

Give the study guide first. It opens with the two facts the whole topic rests
on — when an inverse exists, and the domain/range swap — then gives a rule, a
worked example and a try-it for each of the three skills, with the try-it
answers printed upside down inside their boxes. The watch-out box flags the two
standing errors: reading $f^{-1}$ as $1/f$, and writing an inverse formula
without its domain.

The answer key opens with a quick-answer bank for fast grading and a curriculum
section listing the standards (HSF-BF.B.4, with HSF-IF.A–HSF-IF.C on the
domain/range items) and the difficulty range.
