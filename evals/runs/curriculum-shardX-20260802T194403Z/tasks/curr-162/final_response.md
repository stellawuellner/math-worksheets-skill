# Percent Applications — Grades 6–7 procedural fluency

Three PDFs are ready:

- **Worksheet** — `ws_percent_curr162.pdf` (5 pages, 12 problems)
- **Answer key** — `ak_percent_curr162.pdf` (3 pages, proportion set-up and check for every
  problem)
- **Study guide** — `ss_percent_curr162.pdf` (2 pages, 3 skill sections)

## What the worksheet does

Everything hangs on one relationship, printed at the top of the sheet as a "pattern to
copy":

    part / whole = percent / 100

The sheet opens with two worked models built from the *same three numbers* (27, 45, 60) —
one where the percent is missing, one where the whole is missing — so the student sees
that the only real decision is which slot is empty. From there the twelve problems drill
that decision:

- **percent-rate-from-parts** (1, 2, 4, 6, 9) — part and whole given, find the rate
- **whole-from-part-and-rate** (3, 5, 7, 10, 12) — part and percent given, find the whole
- **rate-from-change** (8, 11) — percent increase and percent decrease, where the whole is
  the *original* amount

The two families alternate rather than sitting in blocks (max run of a single method is
2), so the student cannot coast on one procedure. Difficulty ramps
1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 5. Problem 9 uses a non-integer rate (5.40 tax on 80 →
6.75%) and problem 12 is the synthesis item: after a 20% increase the gym has 168 members,
so 168 is 120% of the old membership, not the part that was added.

No two problems share a skeleton — the contexts run through seats, a quiz, a hiking club,
penalty kicks, a markdown, a survey, a defect rate, bakery sales, sales tax, an election,
a price drop, and membership growth.

## Verification

- **All 12 problems are machine-verified** — nothing is flagged manual. Rates are checked
  as `eval` of `100·part/whole`, wholes as `solve` of the proportion equation, and the
  non-integer tax rate as `approx`. The build reports `BUILD PASSED — all gates green`.
- Problem 9 also carries a **declared misconception trap**: dividing whole by part
  (100·80/5.40 ≈ 1481.48). The verifier confirmed the problem's own check rejects that
  value, and the answer key prints it in the "common wrong answers" bank so a grader who
  sees 1481 knows exactly which move the student made.
- The answer key's boxed final answers are each bound back to their own problem's verified
  value, so a shuffled or drifted key could not have compiled.

## Study guide

Three sections mirroring the three worksheet skills, each with a rule box that says *which
slot is missing*, a worked example whose first step names that decision, and a try-it with
the answer printed upside down inside the box. All six study-guide computations are
verified. The watch-out box covers the three errors this topic produces most: inverting the
ratio, using the new amount as the whole in a percent change, and trying to undo a 20%
increase by taking 20% off the new total.
