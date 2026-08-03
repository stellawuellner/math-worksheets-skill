# Dividing Complex Numbers with Conjugates — Algebra 2

Three PDFs are ready:

- `ws_complexdiv_curr353.pdf` — the student worksheet, 10 problems, 4 pages
- `ak_complexdiv_curr353.pdf` — the full step-by-step answer key, 3 pages
- `ss_complexdiv_curr353.pdf` — a 2-page skills summary / study guide

## What the worksheet asks

The sheet is a representations-and-applications workshop built around one move:
a quotient of complex numbers is not in standard form until the denominator is
real, and multiplying top and bottom by the conjugate is what makes it real.

Nine of the ten problems are divisions. The set ramps through four distinct
methods, interleaved so the student has to choose rather than repeat:

1. **Why the conjugate works** (problem 1) — multiply $7+2i$ by its conjugate
   and see the imaginary part cancel.
2. **Pure imaginary denominators** (problems 2 and 7) — dividing by $2i$ and by
   $3i$, where the conjugate is just the opposite imaginary number.
3. **Binomial denominators** (problems 3, 4, 6, 8 and 10) — the standard case,
   ending with a real numerator ($25/(3+4i)$) and a synthesis problem where the
   division is hidden inside solving $(3+2i)x = 4+7i$ and finding the zero of
   $f(x) = (1-i)x - (6+2i)$.
4. **Circuit applications** (problems 5 and 9) — Ohm's law for AC, $V = I \cdot Z$,
   with voltage in volts, current in amps and impedance in ohms. Both problems
   state every given with its unit and ask for the answer in a named unit; the
   worksheet prints a unit-labelled answer line for each.

Difficulty ramps 1, 1, 2, 2, 3, 3, 3, 4, 4, 5.

## What was verified

Every one of the ten problems is machine-checked by SymPy (11 checks — problem
10 carries two, one `solve` and one `zeros`, both over the complex domain).
**Nothing on this sheet is flagged for manual review**; the build finished with
all gates green.

Three misconception traps are declared and machine-proved to be
distinguishable, and they print in the answer key as "common wrong answers":

- treating $i^2$ as $+1$ (gives 45 instead of 53 on problem 1),
- using $1/i = i$ instead of $1/i = -i$ (gives $-2+3i$ instead of $2-3i$ on
  problem 2),
- dividing real-by-real and imaginary-by-imaginary (problem 6 is written around
  this error and asks the student to explain why it fails).

The answer key repeats each problem, shows the conjugate chosen, the expanded
numerator, and the final division of both parts, then boxes the answer; several
solutions end with a multiplication check. The units (ohms, amps) are carried
inside the boxed answers and are gate-bound to the verification data.

## The study guide

Four sections, each with a rule box, a worked example whose first step says
*why* that tool applies, and a try-it item with the answer printed upside down
inside the box: why a conjugate clears a denominator, dividing by a pure
imaginary number, dividing by a full complex denominator, and the circuit model
$V = I \cdot Z$.

All standards tags are HSN-CN.A.3 (use conjugates to find quotients of complex
numbers).
