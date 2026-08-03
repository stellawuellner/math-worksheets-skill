# Using Twos, Fives, and Tens as Anchor Facts — Grades 2–3

Three PDFs are ready: the student worksheet (5 pages, with real drawing room),
a full step-by-step answer key, and a two-page skills summary.

## What the worksheet contains

8 problems in a guided concept-practice format, every one of them built on the
same move: start at a fact you can *count* (twos, fives, tens) and take one step
to the fact you need. Four subskills are tagged as facets and rotate from the
first problem on, so the student has to choose an anchor rather than repeat one
procedure:

| Facet | Problems | The step from the anchor |
| --- | --- | --- |
| `doubles-anchor` | 1, 4 | skip-count by twos; double a two-fact to get a four-fact |
| `tens-anchor` | 2, 5 | skip-count by tens; take one whole group off a ten-fact to get a nine-fact |
| `fives-anchor` | 3, 7 | add one more group to a five-fact; split a seven-fact into 5 + 2 |
| `anchor-division` | 6, 8 | count *up* on an anchor and score the jumps |

Every problem carries a concrete or visual model tied to notation, as the task's
`concept-models` mode asks: a skip-count ladder with blanks (P1), six ten-frames
to total (P2), equal-group drawings with the extra group circled (P3, P4), a
7 × 7 array cut into a 5-part and a 2-part (P7), and count-up ladders for the
two division problems.

Difficulty ramps 1, 2, 2, 2, 3, 3, 4, 5. Every problem is tagged `3.OA.C.7`,
which is the row `references/standards-map.md` gives for "Times tables /
multiply & divide facts" and is exactly the task's own `standard_refs` code — no
code was invented and none was missing.

## What was verified

**All 8 worksheet answers are machine-verified by SymPy — 0 manual items.** Six
are `eval` checks written so the *anchor relation itself* is the expression
(`a*b + a` for "one more group", `a*b - a` for "one group less", `2*(a*b)` for
doubling, `a*5 + a*2` for the 5 + 2 split), so the check tests the method the
sheet teaches and not just the product. Two are `solve` checks of the division
problems. That matches the task's `eval` + `solve` verification targets.

Three misconception traps are declared, machine-checked as distinguishable, and
printed in the answer key's "Common wrong answers" bank:

- P4 — adding one more 2 instead of doubling the product (would give 14)
- P5 — subtracting 1 instead of one whole group of 7 (would give 69)
- P7 — adding one extra group of 7 to the five-fact instead of two (would give 42)

All three target the same underlying error, which is the one this focus lives or
dies on: confusing *one more group* with *one more counter*.

The study guide's 8 boxes (4 worked examples + 4 try-its) are verified by their
own JSON, so the examples the student learns from are gated too. Nothing is
claimed as verified without a check behind it.

## Study guide

Two pages, one section per worksheet skill: double a two-fact, take a group off
a ten-fact, add a group to a five-fact, and divide by counting up on an anchor.
Each section is a rule box, a worked example that opens with a strategy sentence
before any arithmetic, and a distinct try-it (new numbers, same skeleton) whose
answer prints upside down inside the box. The closing watch-out box names the
group-versus-counter error the traps target.

## Notes

- Every problem declares a `workspace_cm` (6–8 cm) larger than a bare
  computation would need. That is deliberate and was declared before the first
  compile: the ladders, ten-frames, and array drawings live in the *stem*, which
  the page-budget model charges a flat 0.6 cm for, and grade 2–3 students draw
  their groups. The sheet runs 5 pages against a computed 5-page budget; nothing
  was compressed to save paper.
- The build passed on the first run — all 21 gates green, no manual-review
  items. Prose-consistency warnings on the worksheet (73% match) are the
  expected false flags: skip-count sequence entries and the anchor products
  (40, 12, 35) the student is told and then steps from.
