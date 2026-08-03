# Explaining legal equation transformations (Algebra 1)

Three PDFs, all gated:

- **Worksheet** `ws_legal_steps_curr256.pdf` — 10 guided concept-practice
  problems, 6 pages. Every problem carries a **Step / Reason table** — the
  standard two-column justification model — that the student fills in, plus
  3.5–4 cm of work space and an answer line. A value-free "reason bank"
  (Addition/Subtraction, Multiplication/Division, Distributive, combining like
  terms, "not a legal step") sits with the directions, before the first
  problem, so the naming task is well defined.
- **Answer key** `ak_legal_steps_curr256.pdf` — quick-answer bank plus a full
  solution that names the property on every line, and for the error-analysis
  problems states *which line* first broke and *what* was done instead.
- **Study guide** `ss_legal_steps_curr256.pdf` — 2 pages, four skill sections
  (name the property behind a step · decide whether two equations match ·
  find the step that is not legal · multiply an inequality by a negative),
  each with a rule box, a worked example opening on a strategy step, and a
  distinct try-it.

## Facet plan

`name-the-property` (4 problems), `judge-equivalence` (2),
`find-the-illegal-step` (3), `inequality-sign-rule` (2). The subtitle is
composed from that list and bound verbatim to the title block. Max same-facet
run: 2.

## Verification

- Worksheet JSON: **12 checks over 10 problems, 12 passed, 0 manual.** Problems
  1 and 4 carry two entries each under one id — the solve, plus the
  substitution check that proves the transformation preserved the solution set,
  which is the actual point of the topic. Types used: `solve`, `inequality`,
  `equiv`, `eval` — the task's three targets plus the substitution checks.
- Study-guide JSON: **8 of 8 verified** (4 examples + 4 try-its).
- Problem 7 is the strongest item: dividing $x^2 = 4x$ by $x$ loses the root
  $x = 0$. The key names the missing nonzero condition and recovers both roots
  by factoring; the JSON verifies `[0, 4]`.
- **3 traps declared, all confirmed distinguishable**: undoing multiplication
  before addition (8 instead of 22 on the check), changing the right side only
  (6 instead of 12), and substituting into the *changed* equation rather than
  the original (5 instead of 4).
- Difficulty ramp `[1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4]`.

## Standards note

Every entry in both verification files is tagged **`HSA-REI.A.1`**, verbatim
from the "Justifying steps in solving equations" row of
`references/standards-map.md`. That is precisely this sheet's subject: A-REI.A.1
asks the student to explain each step in solving an equation as following from
the previous step and to justify a solution method, which is what the Step /
Reason table makes them do on every problem — including the equivalence
judgements (is this rewrite legal), the find-the-illegal-step items, and the
inequality items, where the step being justified is multiplying or dividing by
a negative. Problem 7 also touches HSA-REI.B.4, but what it assesses is the
illegality of dividing both sides by $x$, so it stays with A-REI.A.1. The
earlier build left the field off because that row did not yet exist in the map
and the nearest in-map codes (`6.EE.B.7 / 7.EE.B.4`, `8.EE.C.7`) are off-grade
for Algebra 1.

## Gate history

First build **failed** at `verify-ss`: the try-it for the inequality section
declared `["-oo", -4, "loopen"]` for the strict inequality $-5x > 20$.
`loopen` closes the upper end, but a strict relation leaves both ends open —
the verifier reported `Interval.open(-oo, -4)` against an expected
`Interval(-oo, -4)`. Changed to `"open"` and the build went green. (The
worksheet's own $\ge$ problem legitimately uses `loopen`, which is what makes
the pair a useful worked contrast.)

Final run: `BUILD PASSED`, all 21 gates green.
