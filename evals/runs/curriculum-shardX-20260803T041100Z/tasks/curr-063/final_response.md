# Estimating Differences and Checking Reasonableness — Grades 2–3

Three PDFs were generated and every gate in the build chain is green.

- **Worksheet** (`ws_estimate_differences_curr063.pdf`) — 10 problems, all set in
  realistic contexts with the unit named in the stem (books, passengers, apples,
  seats, cans, pages, eggs, tickets, stickers). Every problem exercises the
  requested focus: five ask for an estimated difference by rounding (to the
  nearest hundred or the nearest ten), three ask the student to estimate *and*
  compute exactly and then judge whether the exact answer is reasonable, and two
  check a stated difference by adding it back. Difficulty ramps 1 → 4 and the
  facets are interleaved after the warm-up, so the student has to choose the
  method rather than repeat one.
- **Answer key** (`ak_estimate_differences_curr063.pdf`) — full reasoning for
  every problem: which digit decides the rounding, the trade-by-trade
  regrouping for each exact subtraction, and the comparison sentence that
  settles reasonableness. It opens with the generated quick-answer bank, which
  also prints the two declared misconception traps for the grader.
- **Study guide** (`ss_estimate_differences_curr063.pdf`) — 2 pages, three skill
  sections (estimate by rounding · is my answer reasonable? · check by adding),
  each with a rule box, a worked example whose first step names the strategy,
  and a distinct try-it whose answer is printed upside down inside its box, plus
  one watch-out box on the tens-digit rounding rule.

## Verification

All 13 verify entries (10 problems; problems 5, 6 and 8 carry two entries each
because they are two-part) are machine-checked by SymPy: `estimate` for the
rounding problems, `eval` for exact differences and for check-by-adding sums.
**Zero entries are `manual`** — the reasonableness judgments are all anchored to
a checkable number, so nothing was left unverifiable. The study guide's six
boxes (three examples, three try-its) are verified the same way.

Two misconception traps are declared and were proved distinguishable:

- Problem 7: rounding 349 up to 400 by looking at the ones digit → 500 instead
  of 600.
- Problem 9: taking the smaller digit from the larger in each column instead of
  regrouping → 655 instead of 545. This is the planted wrong answer the
  worksheet asks the student to refute with an estimate.

Standard `3.NBT.A.2` (from `references/standards-map.md`, row "Multi-digit
add/subtract") is tagged on all entries.

## Notes for the reviewer

Nothing is flagged for manual review. The prose-consistency checker reports a
few unmatched numbers in the answer key's column-by-column arithmetic and in the
worksheet's `itemsep` length — expected false flags, not content defects.
