# Pythagorean Theorem: Which Side Goes Where? — Grade 8 / Pre-Algebra

Three PDFs are ready:

- **Worksheet** (`ws_pythag_curr244.pdf`, 5 pages) — 8 problems, every one built around
  the same diagnosis: *which given side is the hypotenuse, and does the substitution
  respect that?* A value-free reference triangle sits with the directions (legs $a,b$,
  right angle at $C$, hypotenuse $c$) so the labelling convention is shared and cannot be
  mistaken for any problem's givens. The directions also install the sanity check the
  whole sheet trains: a leg must come out shorter than the hypotenuse.
- **Answer key** (`ak_pythag_curr244.pdf`, 3 pages) — generated quick-answer bank with a
  "common wrong answers" line per declared trap, then full reasoning: the theorem is
  written before it is used, the substitution direction is justified, and each solution
  closes with the size check that would have caught the error.
- **Study guide** (`ss_pythag_curr244.pdf`, 2 pages) — three sections (hypotenuse from two
  legs, leg from a hypotenuse, coordinate distance), each with a rule box, a worked
  example whose first step names *why* that direction of the theorem applies, and a
  distinct try-it with the answer upside down inside the box.

## What was verified

**All 8 problems are machine-checked** — nothing on this sheet is left to manual review,
which suits the task's `machine_first` review mode:

| # | Check | Answer |
|---|---|---|
| 1 | hypotenuse from legs 6 and 8 | 10 cm |
| 2 | leg from hypotenuse 13, leg 5 | 12 cm |
| 3 | find-and-fix: 17 ft ladder, foot 8 ft out | 15 ft |
| 4 | distance $A(2,3)$ to $B(7,15)$ | 13 units |
| 5 | find-and-fix: legs 9 and 40, hypotenuse asked | 41 cm |
| 6 | find-and-fix: distance $P(-3,2)$ to $Q(5,8)$ | 10 units |
| 7 | solve $x^2 + 33^2 = 65^2$ (both roots, then reject one) | $x = 56$ or $x = -56$ |
| 8 | 80 m by 60 m field: two sides vs. the diagonal | 40 m shorter |

Declared units are bound in both directions (answer blank on the sheet, boxed answer in
the key), so an answer in the wrong unit cannot pass. Problem 7 is deliberately the one
with no unit: it asks for *every* solution of the equation and then for the reason the
negative root is discarded — the algebra/geometry distinction that the "just take the
square root" habit hides.

**Seven misconception traps are declared and machine-checked** to be distinguishable, and
each prints in the key's common-wrong-answers block:

- problem 1 — 14, the legs added instead of their squares;
- problems 2 and 3 — 13.93 and 18.79, the hypotenuse dropped into a leg slot (problem 3
  is the version where the answer is visibly absurd: the wall is taller than the ladder);
- problems 4 and 6 — 10.91 and 5.29, coordinate differences treated as a hypotenuse and
  subtracted;
- problem 5 — 38.97, the longest *given* side mistaken for the hypotenuse;
- problem 8 — 87.08, the same substitution error inside a two-step application.

Three problems (3, 5, 6) are explicit find-and-fix items, one more than requested, and
they cover both directions of the error: hypotenuse-used-as-leg and leg-used-as-hypotenuse.

Standards: every problem is tagged `8.G.B.7, 8.G.B.8`, taken verbatim from
`references/standards-map.md`.

## Gate chain

`BUILD PASSED` — **exit 0, all 21 gates green with no manual-review items**. That
includes both verification runs, skill and facet coverage, the quick-answer bank, layout
and unit binding, three compiles inside their page budgets (worksheet 5, key 3, guide 2),
per-problem answer-key binding, study-guide structure, and prose consistency (worksheet
27/27; study guide 23/24, the single flag being a printed exponent 2).
