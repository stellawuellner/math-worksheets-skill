# Finding unit rates with whole-number quantities (Grades 6–7)

Three PDFs, all gated:

- **Worksheet** `ws_unit_rates_curr156.pdf` — 10 guided concept-practice
  problems, 5 pages. Every problem pairs a story with its own **ratio table**
  containing an explicit "per one" column, so the model and the notation sit
  side by side; each problem then gets 3.5–4 cm of work space and a unit-bearing
  answer line.
- **Answer key** `ak_unit_rates_curr156.pdf` — quick-answer bank plus a full
  solution per problem. Each solution first names which quantity the word
  *per* makes the divisor, then scales the table, then states the rate with
  units.
- **Study guide** `ss_unit_rates_curr156.pdf` — 2 pages, four skill sections
  (divide to get a unit rate · read a rate out of a ratio table · compare two
  rates fairly · scale up from a unit rate), each with a rule box, a worked
  example that opens with a strategy step, and a distinct try-it.

## Facet plan

Declared facets: `unit-rate-from-two-quantities` (2 problems),
`rate-table-model` (3), `compare-unit-rates` (3), `apply-unit-rate` (2). The
worksheet subtitle is composed from that list and bound verbatim to the title
block by the facet gate. Max same-facet run after the warm-up: 1, so the
student has to choose the method rather than repeat it. Every facet has a
matching worked example in the study guide.

## Verification

- Worksheet JSON: **10 of 10 machine-verified**, 0 manual — six `eval`, one
  `approx` (the 3.50 dollars-per-pound comparison), two `solve` (proportions
  cross-multiplied), matching the task's `approx`/`eval`/`solve` targets.
- Study-guide JSON: **8 of 8 machine-verified** (4 examples + 4 try-its).
- Nine problems declare an `answer_unit`, each bound in both directions: an
  `\answerline` on the sheet and the same unit printed inside the key's boxed
  answer.
- **3 traps declared, all confirmed distinguishable**: inverting the division
  (pounds ÷ dollars = 0.29), comparing lap totals instead of laps per minute,
  and picking the smaller total price (18) without dividing. They print in the
  key's "common wrong answers" block.
- Difficulty ramp `[1, 1, 2, 2, 2, 3, 3, 3, 4, 4]`; standard
  `6.RP.A.2, 6.RP.A.3` taken verbatim from `references/standards-map.md`.

`BUILD PASSED` — all 21 gates green, first attempt. The residual prose flags in
the report are the literal `1` heading each table's "per one" column and the
story quantities the check does not itself divide (e.g. Store A's 5 pounds,
whose rate the student computes but the JSON entry checks Store B's); both are
the expected false-flag class the checker documents.
