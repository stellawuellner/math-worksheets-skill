# Radicals, Rational Exponents, Domains, and Approximate Solutions — Algebra 2

Three PDFs are ready: the student worksheet, a full step-by-step answer key, and
a two-page skills summary.

## What the worksheet contains

12 problems on **combining radical equations, domains, and approximate
solutions**, in an interleaved-synthesis format. Four facets rotate from problem
3 onward, so the student has to classify the task (rewrite / combine / solve /
approximate) before reaching for a method:

| Facet | Problems | What it asks |
| --- | --- | --- |
| `rational-exponent-form` | 1, 5, 9 | evaluate $a^{m/n}$, including a negative rational exponent |
| `simplify-and-combine-radicals` | 2, 6, 11 | simplest radical form, combining like radicals, adding rational exponents |
| `radical-equation-with-domain` | 3, 7, 10, 12 | isolate, state the domain and sign condition, square, test every candidate |
| `approximate-radical-solution` | 4, 8, 12 | simplify first, then round to two decimals |

The domain thread is explicit rather than incidental. Problem 7 ($\sqrt{2x+3}=x$)
and problem 10 ($\sqrt{x+5}=x-1$) each produce two candidates from the squared
quadratic and each rejects one, and the key distinguishes the two separate
conditions: the radicand must be non-negative *and* the other side must be
non-negative. Problem 10's rejected candidate $x=-1$ is deliberately inside the
radical's domain, so being in the domain cannot be mistaken for sufficiency.

Problem 12 is the synthesis challenge and carries two verify entries on one id.
Equation (i) $\sqrt{2x+7}=x+2$ has the rational solution 1; equation (ii)
$\sqrt{2x+7}=x+1$ differs by one constant, has solutions $\pm\sqrt{6}$, and
requires both an extraneous-root decision and a two-decimal approximation
(2.45). Part (c) asks why squaring is what makes the check necessary.

Difficulty ramps 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 5. Standards come from
`references/standards-map.md` verbatim: `HSN-RN.A.1, HSN-RN.A.2` for the
radical/rational-exponent problems and `HSA-REI.A.2` for the equation problems
(the row that explicitly names extraneous roots). The task's shorthand
`HSN-RN / HSA-REI.A` is not itself a row, so the two full rows it corresponds to
were used rather than inventing a code.

## What was verified

**All 12 worksheet problems (13 verify entries) are machine-verified — 0 manual
items.** `eval` covers the rational-exponent evaluations, `equiv` proves the
simplified and combined forms are genuinely the same expression (not just
plausible), `solve` returns the surviving root set for each radical equation —
SymPy's real-domain solve rejects the extraneous candidates independently of the
key's reasoning — and `approx` recomputes each decimal.

Four misconception traps are declared and machine-checked, and each prints in
the answer key's "Common wrong answers" bank:

- P4 — halving the radicand ($2\sqrt{10}\approx 6.32$ instead of $2\sqrt5$)
- P8 — $\sqrt2+\sqrt8$ read as $\sqrt{10}\approx 3.16$ instead of 4.24
- P9 — a negative exponent read as a negative answer ($-4$ instead of $0.25$)
- P12 — keeping $-\sqrt6$ ($-2.45$) despite the negative right-hand side

The study guide's 8 boxes (4 worked examples + 4 try-its) are verified by their
own JSON, including two radical equations with extraneous candidates.

## Study guide

Two pages: rational exponents, simplifying and combining, a five-step solving
procedure with the substitution check as a numbered step rather than advice, and
approximation technique (simplify first, approximate last, bracket between
perfect squares). Each section has a rule box, a worked example whose first step
is a strategy sentence, and a distinct try-it.

## Notes

- Build passed on the first gate run; no gate failures to report.
- The prose-consistency report flags a few intermediate values in the study
  guide's worked examples (the bracketing values 9 and 16 for $\sqrt{11}$, the
  simplified $3\sqrt2$ inside a combining example). Those are derived from the
  entry's own expression rather than separate givens — the documented
  false-flag case for that heuristic.
