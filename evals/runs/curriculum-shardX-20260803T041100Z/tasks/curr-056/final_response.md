# Adding two-digit numbers with place-value strategies (Grades 2–3)

Three PDFs are built and gated:

- **Worksheet** `ws_place_value_addition_curr056.pdf` — 8 guided concept-practice
  problems, 5 pages, every problem carrying its own model and 4–4.5 cm of work
  space. Every problem is a two-digit + two-digit addition attacked with a
  place-value strategy, so the focus coverage is 8/8.
- **Answer key** `ak_place_value_addition_curr056.pdf` — the generated
  quick-answer bank plus a full spoken-aloud solution per problem (name the
  tens, name the ones, put them back together), including why a trade happens
  and why the compensation in problem 7 must be given back while the one in
  problem 5 must not.
- **Study guide** `ss_place_value_addition_curr056.pdf` — 2 pages, four skill
  sections (break apart into tens and ones · jump tens then ones on a number
  line · make a friendly ten and adjust · round to ten to check), each with a
  rule box, a two-step worked example, and a distinct try-it whose answer is
  printed upside down inside the box.

## Models used (concept-models mode)

Every problem carries a drawn model wired to notation: base-ten blocks
(problems 1, 3), an open number line with jumps (2, 4), a friendly-ten hop
with the compensation arrow labelled (5, 7), a rounding number line (6), and a
student's incorrect written work for the error-analysis problem (8). Because
`check_layout`'s figure-scope rule is all-or-nothing, all eight problems carry
a valued figure rather than some.

## Verification

- Worksheet JSON: **8 of 8 machine-verified**, 0 manual. Seven `eval` checks
  and one `estimate` (round each operand to the nearest ten, then add) — the
  two verification targets the task asked for.
- Study-guide JSON: **8 of 8 machine-verified** (4 worked examples + 4
  try-its, bound positionally).
- **3 misconception traps declared, all confirmed distinguishable** by
  `verify.py`: adding exactly instead of estimating (92), rounding 58 down to
  the ten below (80), and — on the error-analysis problem — writing the tens
  sum and the ones sum side by side to get 613. The traps print in the answer
  key's "common wrong answers" block.
- Difficulty ramp `[1, 2, 2, 3, 3, 3, 4, 4]`; bloom mix recall/apply/analyze;
  standard `2.NBT.B.5 / 3.NBT.A.2` from `references/standards-map.md`, verbatim.

`BUILD PASSED` — all 21 gates green, first attempt. The only report-level note
is a heuristic prose flag: the rounding number line in problem 6 is labelled
50 and 60, and 60 is not one of that problem's JSON givens. That is the
model's decade endpoint, not a drifted value.
