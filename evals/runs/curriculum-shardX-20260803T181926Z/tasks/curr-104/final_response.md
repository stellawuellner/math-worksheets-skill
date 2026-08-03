# Multi-digit place value and rounding — boundary and placeholder errors (Grades 4–5)

Three PDFs are ready:

- **Worksheet** (`ws_rounding_curr104.pdf`, 4 pages) — 8 problems, all on the two
  errors that break rounding: reading the wrong deciding digit at a boundary, and
  losing the zeros that hold a place. Rounding 3,472 and 2,961 (which rolls over into
  the thousands), two find-the-mistake items, comparing 4,806 with 4,860, estimating
  a sum by rounding each addend, "10 more than 4,995", and a challenge that rounds
  2,548 to three different places.
- **Answer key** (`ak_rounding_curr104.pdf`, 2 pages) — every solution names the
  deciding digit, says which places become zeros, and ends with a sense check. It
  opens with a quick-answer bank, a generated Curriculum section
  (4.NBT.A.1–A.3 / 5.NBT.A.1–A.2, difficulty 1–4), and a "common wrong answers" line
  for each of the five declared traps.
- **Study guide** (`ss_rounding_curr104.pdf`, 2 pages) — three sections: the
  three-step rounding routine, the exact-halfway case (and why you must always round
  the original number), and zeros as place holders including carrying on a rollover.
  Each has a rule box, a worked example that starts by naming the strategy, and a
  try-it with the answer upside down.

**Find-and-fix items (2, as requested).** Problem 3 plants Jo's 4,700 for
"round 4,750 to the nearest hundred" — the halfway case treated as a round-down — and
problem 4 plants Ravi's "50" for 5,048, the placeholder error in its purest form.
Both planted numbers are declared as machine-checked misconception traps, as are
three more: 2,900 on problem 2, 4,905 on problem 7, and 2,600 on the challenge (the
double-rounding error). SymPy confirmed each wrong number is what that wrong method
produces and that the problem's own check rejects it.

**What was verified.** All 10 machine-checkable answers were recomputed by SymPy —
every rounding (using the half-up school convention), the comparison, the estimated
sum, and the +10 rollover. Three items are flagged for **manual review**: the
one-sentence explanations in problems 3, 4 and 8 (which digit decides at an exact 5,
why the zeros must stay, and why rounding twice fails). Each has a model answer and a
credit note in the key. Layout, work space, answer blanks, page budget, and the
binding of every boxed answer to its verified value all passed the build gates.
