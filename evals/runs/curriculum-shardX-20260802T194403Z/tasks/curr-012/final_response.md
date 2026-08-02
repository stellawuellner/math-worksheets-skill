# Comparing Written Numerals 1–10 — Kindergarten/Grade 1

Three PDFs are ready for a procedural-fluency practice session on comparing
written numerals from 1 through 10.

- **Worksheet (4 pages, 10 problems).** The directions carry a worked pattern
  (`2 < 5`, read aloud) plus a value-free number line placed with the
  directions, so every problem shares one labelling convention and no problem
  carries a figure a neighbour could borrow. The ramp runs from writing a
  symbol between two single-digit numerals (1–3), to circling the greater or
  smaller of a pair (4–5), to the two-digit trap `10` vs `8` (6), to ordering
  three numerals (7, 9), and finishes with two count-on-then-compare problems
  (8, 10) where the student must finish counting before choosing a symbol.
  Each problem has 2.8–4 cm of work space and its own answer location; no two
  problems share a skeleton.
- **Answer key (2 pages).** Full reasoning per problem — the count-up argument
  ("you say 3 first, then 7"), why `10 > 8` is not about the leading digit,
  and, in problems 8 and 10, the explicit instruction to finish both counts
  before comparing. Every final answer is boxed and a generated quick-answer
  bank sits under the title for fast grading.
- **Study guide (2 pages).** Four skill sections — compare-with-symbols,
  greater-or-less, order-three-numerals, count-on-then-compare — each with a
  rule box, a worked example whose first step names the strategy, and an
  upside-down try-it the student attempts before the worksheet. A watch-out
  box flags the two errors this topic produces: judging `10` by its first
  digit, and comparing the starting number instead of the number landed on.

**Verification.** All 10 worksheet problems are machine-checked with SymPy
(13 checks: 10 `compare`, 3 `eval` for the count-on results) and all 8
study-guide boxes are machine-checked. Nothing is flagged manual — every
answer on this sheet is computable. The full gate chain passed green,
including per-problem binding of each printed boxed answer back to its
verified value, the skill/facet coverage gates, layout, and the page budgets.
