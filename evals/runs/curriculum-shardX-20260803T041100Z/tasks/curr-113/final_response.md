# Whole-Number Division: Interpreting Remainders — Grades 4–5

Three PDFs are ready:

- **Worksheet** (`ws_remainders_curr113.pdf`, 3 pages) — 10 problems, all set in
  real contexts (bagging apples, seating students, cutting ribbon, filling album
  pages, shelving books). A boxed decision guide at the top names the only three
  things a remainder can mean, and the directions ask the student to write the
  division, the quotient and the remainder *before* deciding. 6–6.5 cm of work
  space per single-part problem; the three two-part problems give 4.5–5 cm per part.
- **Answer key** (`ak_remainders_curr113.pdf`, 2 pages) — quick-answer bank on top,
  then per problem: the division, the multiply-back check (`8 × 34 = 272`,
  `275 − 272 = 3`), and — the point of the sheet — a sentence saying *why* the
  question makes the remainder dropped, rounded up, or reported.
- **Study guide** (`ss_remainders_curr113.pdf`, 2 pages) — four sections. The first
  three all run off the **same** division, `74 ÷ 8 = 9 R 2`, so the student sees one
  computation give three different correct answers (9, 10, 2) depending on the
  question. The fourth teaches estimating the quotient as a reasonableness check.
  Each section: rule box → two-step worked example → try-it with the answer printed
  upside down inside the box.

## Design

Facets declared and tagged on every problem: `drop-the-remainder` (3),
`round-up-the-quotient` (4), `remainder-is-the-answer` (4),
`estimate-the-quotient` (2). They are interleaved after the warm-up — the gate
reports a maximum same-facet run of 2 — so the student must decide the meaning
each time instead of repeating a pattern. Difficulty ramps 1 → 4.

Problem 10 is an error-analysis item: Maya's division is correct
(`314 ÷ 6 = 52 R 2`) but she reports 52 boxes, leaving 2 marbles unboxed. The
wrong answer 52 is **declared as a machine-checked trap**, so the verifier proved
the problem distinguishes it from the correct 53, and the answer key prints it in
the "common wrong answers" block for the grader.

## Verification

**13 SymPy checks over 10 problems — 13 verified, 0 manual.** Every quotient
(`floor(a/b)`), every rounded-up count (`ceiling(a/b)`) and every leftover
(`a − b·floor(a/b)`) is recomputed independently; the two-part problems carry a
check per part, so a right part (a) cannot cover a wrong part (b). Problem 7's
estimate is verified with the `estimate` type (round each operand to the nearest
ten, then divide: `240 ÷ 40 = 6`), not by trusting a written-down number. The
build gate also binds every boxed answer in the key and the guide back to its own
problem's verified value.

Nothing here is open-ended, so nothing is flagged for manual review.

**Standards note:** all problems are tagged `4.NBT.B.5 / 4.NBT.B.6`, taken
verbatim from `references/standards-map.md` ("Multi-digit multiplication &
division"). Nine of the ten problems use a one-digit divisor, which is squarely
4.NBT.B.6; problem 7 uses a two-digit divisor (40 seats), whose own code
(5.NBT.B.6) has no row in the standards map — rather than invent one I left it on
the multi-digit division row and am flagging it here.

Gate verdict: **BUILD PASSED — all gates green**.
