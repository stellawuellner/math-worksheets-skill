# Ordering Three Amounts from Least to Greatest — Kindergarten/Grade 1

Three PDFs are ready:

- **Worksheet** (`ws_ordering_curr013.pdf`, 2 pages) — 8 problems, every one of
  them ordering three quantities from least to greatest. Each problem ends with
  the same three-blank answer strip (`least ___ ___ ___ greatest`) so the child
  always knows what "finished" looks like, and each has 3–4.5 cm of work space
  for writing the three counts down before ordering them.
- **Answer key** (`ak_ordering_curr013.pdf`) — a quick-answer bank at the top for
  grading at a glance, then a worked explanation per problem: how each amount was
  found (count the dots, count on from a full ten-frame, add the "3 more"), then
  the tens/ones reasoning that decides the order.
- **Study guide** (`ss_ordering_curr013.pdf`, 1 page) — three skill sections, each
  with a rule box, a two-step worked example and a try-it whose answer is printed
  upside down inside the box.

## What the problems cover

| # | Representation / context | Skill |
|---|---|---|
| 1 | Apples drawn on three plates | count-then-order |
| 2 | Three number cards (7, 4, 9) | order-three-numbers |
| 3 | Three ten-frames | count-then-order |
| 4 | Three cube trains | count-then-order |
| 5 | Books on three library shelves | order-three-numbers |
| 6 | Buttons in three jars (41 / 14 / 40) | order-three-numbers |
| 7 | Stickers, one amount given as "3 more than" | compute-then-order |
| 8 | Three team scores, two of them two-part totals | compute-then-order |

Difficulty ramps 1, 1, 2, 2, 2, 3, 3, 4. Problem 6 deliberately uses 41/14/40 —
the classic digit-reversal error — and the study guide's watch-out box names it.
Problems 7 and 8 hide one or two amounts inside the story, so the child must
work the totals out *before* ordering; that is the step the answer key shows
explicitly.

## Verification

Every problem is machine-checked with SymPy — **11 checks over 8 problems, 11
verified, 0 manual**. Problems 7 and 8 carry more than one check each: the
hidden totals (`8+3=11`, `10+5=15`, `9+3=12`) are verified as separate `eval`
entries, and the ordering itself as a `compare` entry, so a right order built
from a wrong total cannot pass. The build gate also binds every printed boxed
answer in the key and the study guide back to the verified values, so no
transcription drift is possible.

Standards: `K.CC.A.1–K.CC.C.7` (comparing and ordering numbers, which is where
K.CC.C.6–C.7 live in the shipped standards map) and, for the two problems that
add first, `K.OA.A / 1.OA.C.6 / 2.OA.B.2`. Both codes are taken verbatim from
`references/standards-map.md`.

Nothing on this sheet is open-ended, so nothing is flagged for manual review.
Gate verdict: **BUILD PASSED — all gates green**.
