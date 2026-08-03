# Equivalent Expressions: Expanded and Factored Forms — Grades 6–7

Three PDFs are ready: the student worksheet, a full step-by-step answer key, and
a two-page skills summary.

## What the worksheet contains

12 problems on **rewriting expressions in equivalent expanded and factored
forms**, in an interleaved-synthesis format. The sheet is built on the single
idea that $a(b+c) = ab+ac$ is one property read in two directions, and the four
tagged facets rotate from problem 3 onward so the student must decide which
direction is being asked for:

| Facet | Problems | What it asks |
| --- | --- | --- |
| `distribute-to-expand` | 1, 3, 7, 11 | expand, including negative multipliers and three-term parentheses |
| `factor-out-gcf` | 2, 6, 10, 12 | factor completely, including a two-variable case |
| `combine-like-terms` | 4, 8 | collect after expanding |
| `check-equivalence-by-substitution` | 5, 9, 12 | test a claimed equivalence with a value |

Problems 5 and 9 are error-analysis: a named student's wrong expansion is given
and one substitution settles it, which is also the sheet's chance to teach that
a single counterexample disproves equivalence while a single agreement proves
nothing. Problem 12 is the synthesis challenge and carries two verify entries on
one problem id — factor $18x+24$ completely, then substitute $x=2$ into the
factored form and reconcile it with the original.

Difficulty ramps 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 5. Every problem is tagged
`6.EE.A / 7.EE.A`, taken verbatim from `references/standards-map.md` — which is
also the task's own `standard_refs` string, so no gap here. Nothing on the sheet
requires binomial multiplication or any Algebra 1 prerequisite.

## What was verified

**All 12 worksheet problems (13 verify entries) are machine-verified — 0 manual
items.** `expand` and `factor` checks are structural (SymPy confirms the
rewritten form is genuinely equivalent to the original, not merely
plausible-looking), `equiv` covers the collect-like-terms answers, and `eval`
covers the substitution tests.

Three misconception traps are declared and machine-checked, and each prints in
the answer key's "Common wrong answers" bank:

- P5 — distributing to the first term only ($3x+4$, giving 19 instead of 27)
- P9 — expanding $4(2x-5)$ as $8x-5$ (giving 27 instead of 12)
- P12 — factoring 6 out of $18x$ only and leaving 24 inside (giving 180 instead
  of 60)

The study guide's 8 boxes (4 worked examples + 4 try-its) are verified by their
own JSON.

## Study guide

Two pages, one section per worksheet skill: expanding, factoring out the GCF,
collecting like terms, and testing equivalence by substitution. Each section is
a rule box, a worked example whose first step is a strategy sentence, and a
distinct try-it with the answer printed upside down inside the box. The
equivalence section states the asymmetry explicitly (disagreement disproves,
agreement does not prove) and warns against testing at $x=0$ or $x=1$.

## Notes

- Build passed on the first gate run; no gate failures to report.
- One soft prose flag in the study guide (a `9` appearing as a factor inside a
  worked example's arithmetic rather than as a JSON given). It is a derived
  intermediate value, which the checker documents as an expected flag.
