# Distinguishing Exponential from Linear Change — Algebra 1

Three PDFs are ready: the student worksheet (6 pages), a step-by-step answer
key, and a two-page skills summary.

## What the worksheet contains

10 problems in a guided concept-practice format, all of them on the same
decision: is the step an **addition** (constant difference, linear) or a
**multiplication** (constant ratio, exponential)? Four subskills are tagged as
facets and interleave after a two-problem warm-up:

| Facet | Problems | What it asks |
| --- | --- | --- |
| `table-differences-ratios` | 1, 2, 6 | build both the difference row and the ratio row, then decide |
| `write-the-rule` | 4, 7, 9 | turn a description or two points into `a + dn` or `a·rⁿ`, then use it |
| `compare-growth` | 5, 10 | evaluate a linear and an exponential model at the same input and measure the gap |
| `context-classify` | 3, 8 | read a real situation, classify it, then compute |

Three design choices carry the focus rather than decorating it:

- **Problem 6 is neither.** The table 2, 8, 18, 32 has neither a constant
  difference nor a constant ratio, and the student proves it by computing two
  unequal ratios (4 and 2.25). Without this problem, "not linear" quietly means
  "exponential" for the rest of the sheet.
- **Problem 8 puts the two models on the same object** — 12 percent of the
  car's *current* value versus a flat 2400 dollars a year — so the distinction
  decides the answer instead of being announced.
- **Problem 10 is the classic overtaking case**, and part (b) deliberately asks
  the student to notice that on day 10 the doubling plan is still 200 times
  behind.

Models per the `concept-models` mode: value tables with a difference row and a
ratio row to fill in (P1, P2, P6), a value-free reference card giving both rule
shapes, and rule-versus-rule comparisons written out before any number is
computed.

Difficulty ramps 1, 2, 2, 2, 3, 3, 3, 4, 4, 5.

## What was verified

**All 10 worksheet problems are machine-verified by SymPy — 0 manual items**, as
12 checks: five `eval`, three `approx`, one `slope`, one `solve`, and two
multi-entry problems (6 and 9) where a single problem carries two verified
parts under one id. That covers the task's `eval`, `solve`, and `approx`
verification targets.

Three misconception traps are declared, machine-checked as distinguishable, and
printed in the answer key's "Common wrong answers" bank. Each one *is* the
linear/exponential confusion in a different disguise:

- P5 — computing `100·1.5·5` instead of `100·1.5⁵` (would give a 400-dollar gap)
- P8 — taking 12 percent of the *original* price every year (would give −2400,
  flipping which dealer looks better)
- P10 — `0.01·2·19` instead of `0.01·2¹⁹` (would leave the doubling plan 999.62
  dollars behind)

The study guide's 8 boxes (4 worked examples + 4 try-its) are verified by their
own JSON. Nothing is claimed as verified without a check behind it; the
"explain in one sentence" parts are worked as reasoning in the key and are not
presented as machine-checked.

## Study guide

Two pages, one section per worksheet skill: decide from a table, write the rule
from a description, compare the two models at one input, and classify a real
situation. Each section is a rule box, a worked example that opens with a
strategy sentence, and a distinct try-it. Sections 3 and 4 are built as
contrasts — the try-it in section 4 is the *linear* twin of the exponential
example (a tank draining 20 litres an hour against a phone losing 20 percent a
year), so the student meets the distinction rather than being told it.

## Notes on standards

The task's `standard_refs` value is `HSF-LE.A`, and the exact code for this
focus is **HSF-LE.A.1** ("distinguish between situations that can be modeled
with linear functions and with exponential functions"). **That code has no row
in `references/standards-map.md`** — the file's HSF-LE entries are `HSF-LE.A.4,
HSF-BF.B.5` (exponentials and logs) and `HSF-BF.A.2, HSF-LE.A.2` (sequences and
series). No code was invented. Every problem is tagged
`HSF-BF.A.2, HSF-LE.A.2`, copied verbatim from the map, which is a genuine fit
rather than a nearest-neighbour reach: HSF-LE.A.2 is constructing linear and
exponential functions from a graph, description, or two input-output pairs
(problems 1–4, 7, 9 do exactly that), and HSF-BF.A.2 is arithmetic versus
geometric sequences, which is what a constant difference row versus a constant
ratio row *is*. The missing HSF-LE.A.1 row is flagged here so it can be added
centrally.

## Other notes

- `workspace_cm` (6–8 cm) was declared on every problem before the first
  compile, because the value tables, bulleted two-model descriptions, and
  displayed rules live in the stem, which the page budget charges a flat 0.6 cm
  for. The sheet runs 6 pages against a computed 6-page budget.
- The build passed after one verify-only fix: problem 9's `solve` on
  `500r³ − 4000` was refused until `"domain": "real"` was declared, because the
  cubic has two complex roots and the verifier will not guess whether the key
  meant to list them. All 21 gates then passed on the next run.
- Prose-consistency match rates (67% worksheet, 68% study guide) are the
  expected false flags: table entries the student reads but the check does not
  consume, and shown intermediate values such as 1.5⁶ = 7.59375 and 0.8³ =
  0.512.
