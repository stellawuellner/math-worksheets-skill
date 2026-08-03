# Integration by Parts, Chosen Strategically — AP Calculus AB/BC (10 problems)

Three PDFs are ready:

- **Worksheet** (`ws_parts_curr477.pdf`, 6 pages) — 10 problems, every one of them
  a decision about which factor becomes $u$, with 7–10 cm of work space each.
- **Answer key** (`ak_parts_curr477.pdf`, 4 pages) — the $u$/$dv$ choice stated and
  justified before any computation, then the full derivation, plus the generated
  quick-answer bank and curriculum section.
- **Study guide** (`ss_parts_curr477.pdf`, 2 pages) — four skill sections, each with
  a rule box, a worked example, and a separate try-it with the answer printed
  upside down.

## What the worksheet covers

The sheet is built around the strategic question rather than the mechanics:

1–2. Standard $u = $ algebraic choices: $\int xe^x\,dx$, $\int x\cos x\,dx$.
3. $\int \ln x\,dx$ — one factor, so the split is forced ($dv = dx$).
4. $\int x^2 e^x\,dx$ — parts does not finish it; recognise the simpler leftover and repeat.
5. $\int_0^1 xe^{2x}\,dx$ — parts inside a definite integral, exact answer $(e^2+1)/4$.
6. $\int x\ln x\,dx$ — students must say in one line why $u = \ln x$ and not $u = x$.
7. $\int x\sec^2 x\,dx$ — choose $dv$ as the factor whose antiderivative is already known.
8. $\int e^x\sin x\,dx$ — the cycling case: name the integral $I$ and solve for it.
9. $\int_0^\pi x^2\cos x\,dx$ — two rounds plus exact boundary evaluation, answer $-2\pi$.
10. $\int_1^\infty \frac{\ln x}{x^2}\,dx$ — improper: a separate part (a) for the limit of the boundary term, part (b) for the value.

## Verification

All 11 machine checks passed under SymPy (problem 10 carries two: the limit and
the integral). Antiderivatives are checked by differentiating them back to the
integrand, definite and improper integrals by exact evaluation, and the limit
symbolically. Nothing is flagged for manual review.

Two misconception traps are declared and confirmed distinguishable from the
correct answer, and they print in the key:

- adding the second antiderivative term instead of subtracting it in problem 5,
- keeping the plus sign in the second round of parts in problem 9, which turns
  $-2\pi$ into $+2\pi$.

## Notes for the adult

Problem 7's answer is $x\tan x + \ln|\cos x| + C$; the absolute value matters and
the key says so. Problem 10 deliberately splits the limit from the integral so a
student who substitutes $\infty$ into the antiderivative loses only part (a). The
course level prints on the answer key only.
