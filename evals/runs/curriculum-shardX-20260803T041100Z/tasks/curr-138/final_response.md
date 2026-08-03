# Multiplying and Dividing Decimals by Place-Value Reasoning — three PDFs

**Worksheet** (`ws_decimals_curr138.pdf`, 10 problems, ~4 pages). Every problem
multiplies or divides decimals and asks for the *place-value* thinking, not just
the algorithm (10 of 10 on the requested focus). Four planned facets, declared
in the JSON and interleaved after the warm-up (longest same-facet run: 2):

- **power-of-ten-shift** (2) — 100 paper clips at 1.24 g, with a place-value chart to fill in; a 4.5 m ribbon cut into 10 pieces
- **multiply-decimals** (3) — 0.4 L of stock for 6 batches (in tenths); a 0.25 m by 0.4 m tile with a hundredths area model; the error-analysis problem
- **divide-decimals** (4 entries over 3 problems) — a 4.8 m rope into 0.6 m pieces; 9 books massing 7.2 kg; the two-part juice-machine problem
- **estimate-and-compare** (2) — estimate a 6.8 m by 4.2 m garden bed by rounding; decide which of `0.6 x 12` and `12 / 0.6` is greater *without computing*

Difficulty ramps 1, 1, 2, 2, 2, 3, 3, 3, 4, 4. Problem 9 is error analysis
(Sam's 4.9 m² for 1.4 m by 0.35 m); problem 10 is a two-part application with
its own answer blank per part. Work space is 5–6 cm per problem, and seven
problems carry a unit-tagged answer line (g, m, L, m², kg) bound to the JSON's
`answer_unit`.

**Answer key** (`ak_decimals_curr138.pdf`). Each solution says the place-value
reason first (digits shift two places left; 48 tenths ÷ 6 tenths; hundredths ×
tenths = thousandths), then computes, then checks by multiplying back. The
generated quick-answer bank sits under the title, and it prints the three
declared traps for the grader: 0.0124 (shifted the wrong way), 0.125 (divided
the smaller by the larger), 4.9 (counted only one decimal place).

**Study guide** (`ss_decimals_curr138.pdf`, 2 pages). Four sections, one per
facet/skill — powers of ten, multiplying two decimals, dividing by a decimal,
estimating and judging size — each with a rule box, a two-step worked example,
and an upside-down-answer try-it, plus a watch-out box on decimal-point
placement.

## Verification

All 11 worksheet verification entries (problem 10 is two parts) and all 8
study-guide results were machine-checked with SymPy: **19 verified, 0 manual**.
The three declared misconception traps were proved distinguishably wrong. The
full gate chain is green (`BUILD PASSED`), including the facet-coverage and
subtitle-binding gates, per-problem answer binding, and unit binding in both
directions.

Standard: `5.NBT.B.7` from `references/standards-map.md` (row "Decimals &
operations"), which is the code the task's `standard_refs` names. Prose-checker
flags are TeX box dimensions and intermediate whole-number products (6 x 3, 35
x 7) inside worked steps — no story number is unaccounted for.
