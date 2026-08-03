# Arithmetic Sequences as Linear Functions — Algebra 1

Three PDFs are ready: the student worksheet, a full step-by-step answer key, and
a two-page skills summary.

## What the worksheet contains

12 problems on **modeling discrete linear change and finite arithmetic sums**,
in an interleaved-synthesis format. The sheet is organised around a single
distinction the student has to make on every problem — is the question asking
for *a term*, for *which term*, or for a *total*? Four facets rotate from
problem 3 onward:

| Facet | Problems | What it asks |
| --- | --- | --- |
| `explicit-formula-from-context` | 1, 5, 10, 12 | use $a_n = a_1+(n-1)d$, including negative $d$ and a two-known-terms case |
| `sequence-as-linear-function` | 2, 7 | evaluate the sequence written as $f(n) = dn + c$ and say where the slope and constant come from |
| `find-term-number` | 4, 8 | solve the explicit formula for $n$ |
| `finite-arithmetic-sum` | 3, 6, 9, 11, 12 | $S_n = n(a_1+a_n)/2$, in context (seating, savings, production) |

Problem 3 develops the sum formula from the pairing argument rather than
handing it over. Problem 10 gives two non-consecutive terms ($a_4 = 14$,
$a_9 = 34$) so the student has to count steps instead of reading $d$ off
consecutive values. Problem 12 is the synthesis challenge and carries two verify
entries on one id: week-20 output (405 units) and the 20-week total (5250
units), then a written explanation of why multiplying the best week by 20
overestimates.

Difficulty ramps 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 5. Every problem is tagged
`HSF-BF.A.2, HSF-LE.A.2`, taken verbatim from `references/standards-map.md`
(the task's `standard_refs` shorthand `HSF-BF.A / HSF-LE.A` is not itself a row
in that file, so the full row it corresponds to was used rather than inventing a
code). Nothing depends on geometric sequences, sigma manipulation, or any
Algebra 2 prerequisite.

## What was verified

**All 12 worksheet problems (13 verify entries) are machine-verified — 0 manual
items.** Term values are `eval` checks of $a_1+(n-1)d$ and of $mn+b$; the
which-term problems are `solve` checks; every total is a genuine `series` check
(SymPy sums the term expression over the stated range rather than trusting the
closed form written in the key).

Six misconception traps are declared and machine-checked, and each prints in the
answer key's "Common wrong answers" bank:

- P1 — using $n$ instead of $n-1$ (38 instead of 33)
- P5 — adding a common difference that the story said was a decrease (53 instead
  of $-13$)
- P6 — first row times number of rows, ignoring the growth (216 instead of 348)
- P9 — number of terms times the *last* term (1580 instead of 820)
- P11 — 15 rows all filled to the back row's size (930 instead of 615)
- P12 — 20 weeks all at the week-20 rate (8100 instead of 5250)

The study guide's 8 boxes (4 worked examples + 4 try-its) are verified by their
own JSON, including two `series` checks.

## Study guide

Two pages, one section per worksheet skill: the explicit formula, solving for
$n$, summing a finite arithmetic sequence, and the sequence-as-linear-function
view. The fourth section makes the discrete/continuous connection explicit — the
common difference *is* the slope, and the constant in $f(n) = dn + (a_1-d)$ is
the "term zero" value, not $a_1$. Each section has a rule box, a worked example
opening with a strategy step, and a distinct try-it.

## Notes

- Build passed on the first gate run; no gate failures to report.
- The prose-consistency report flags the listed opening terms of the example
  sequences in the study guide (the "5, 8, 11, …" style leads). Those are
  derived from the entry's own $a_1$ and $d$ rather than being separate JSON
  givens, which is the documented false-flag case for that heuristic.
