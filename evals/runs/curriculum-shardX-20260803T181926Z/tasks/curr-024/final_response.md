Three PDFs are ready for a kindergarten or first-grade learner on addition within
10, focused on finding and fixing a counting-on error.

- **Worksheet** (6 problems, `ws_countingon_curr024.pdf`, 4 pages) — every
  problem is a find-and-fix item built on the same real error: counting the
  starting number as the first hop, which always makes the total exactly one too
  small. Sam counts "six, seven, eight" for $6 + 3$ and writes 8 instead of 9;
  Mia says "four, five" for $4 + 2$ and writes 5 instead of 6; Ravi starts at the
  smaller number for $3 + 5$, loses a hop and writes 7 instead of 8; Jo counts
  the *words* she says going from 5 up to 9 and writes 5 when the answer is the
  4 hops she took; Ana starts at 2 for $2 + 7$ and writes 8 instead of 9, when
  turning it around leaves only two hops; and Ben makes the start-number slip
  twice in a row (9 for $6 + 4$, 7 for $2 + 6$), so the child has to notice that
  *both* answers are one low. Every problem carries a value-free counter picture
  — filled dots for what the child has, open dots for what is added — so the
  answer can be checked by counting the page. Work space runs 5–6.5 cm per
  problem, with a full answer line.
- **Answer key** (`ak_countingon_curr024.pdf`, 3 pages) — three to six numbered
  steps per problem, always in this order: name the mistake in child-facing
  words, count on correctly with the hops numbered out loud, box the answer, then
  check it a *different* way (recount the picture, use fingers, or add the answer
  back to the part). It carries the generated quick-answer bank and the generated
  "Common wrong answers" block (8, 5, 7, 5, 8, 9, 7), and each solution closes
  with the diagnostic a parent can actually use: an answer exactly one too small
  means the start number was counted as a hop, and the fix is the start number,
  not more counting practice.
- **Study guide** (2 pages, `ss_countingon_curr024.pdf`) — three skills matching
  the worksheet tags: say the first number then start hopping (the start number
  is free), start from the bigger number (fewer hops, fewer chances to lose one),
  and count on to find a missing part (count hops on fingers, not words, then add
  it back to check). Each has a rule box, a two-step worked example and an
  upside-down try-it, plus a watch-out box on the "exactly one too small"
  signature.

**Verification.** All 6 worksheet problems are machine-checked with SymPy — seven
`eval` checks (five totals, one missing part, and a second total under problem 6,
which asks about two of Ben's answers) plus a `solve` check of $5 + n = 9$ for the
missing-part problem, so both the counting model and its equation are bound.
Nothing on this sheet is left to manual review: every item has a single numeric
answer, so no problem is described as verified when it is not. All 6 study-guide
results are machine-checked too.

Seven planted wrong results are declared misconception traps (8, 5, 7, 5, 8, 9,
7). The verifier proved each one distinguishably wrong and derived from the
stated wrong method rather than typed by hand — each trap expression is literally
"one less than the true total", which is what the count-on error does.

**Standards.** Every problem is tagged `K.OA.A / 1.OA.C.6`, the on-grade portion
of the "Add/subtract within 20" row in `references/standards-map.md` (that row
reads `K.OA.A / 1.OA.C.6 / 2.OA.B.2`; the grade-2 code is dropped as off-grade
for this sheet). It matches the task's own standard reference exactly. No code
was invented.

**Gate-log note.** Prose matched 19 of 19 numbers on the worksheet and 18 of 18
on the study guide, with no figure-label flags — the counter pictures are
deliberately value-free, so the printed dots are a model to count rather than
labels that could disagree with the answer key. The grade level appears only on
the answer key, in the generated Curriculum section; nothing the child holds says
"Kindergarten" or "Grade 1".
