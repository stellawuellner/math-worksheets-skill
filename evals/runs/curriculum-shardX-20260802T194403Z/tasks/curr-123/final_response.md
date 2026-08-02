# Comparing Unlike Fractions — Grade 4–5 (curr-123)

Three PDFs are ready:

- **Worksheet** (`ws_fractions_curr123.pdf`, 4 pages) — 10 problems, every one set
  in a real situation with the whole and the units stated (same size water
  bottles, the same trail, the same book, cups in a recipe). A benchmark number
  line at the top is a value-free reference for the whole sheet. The problems
  rotate through four methods so your child has to *choose*, not repeat:
  compare with the $\tfrac12$ benchmark, compare on a common denominator, build
  an equivalent fraction, and order a set of three or four fractions. Difficulty
  ramps 1 → 5: it starts with fractions that sit on opposite sides of one half
  and finishes with four hikers' trail fractions that all need a common
  denominator of 24.
- **Answer key** (`ak_fractions_curr123.pdf`, 2 pages) — a quick-answer bank at
  the top for fast checking, then a full worked solution for each problem: which
  method was chosen and *why* it was the right one, the rewriting step in full,
  and the boxed comparison. Problems 8 and 10 add a grading note (problem 8
  shows a second route via a common denominator; problem 10 says to accept any
  correct common denominator).
- **Study guide** (`ss_fractions_curr123.pdf`, 2 pages) — one section per method
  with a rule box, a worked mini-example that names the strategy before doing
  any arithmetic, and a try-it whose answer is printed upside down inside the
  box. It closes with the two mistakes that cause most errors here: reading a
  bigger denominator as a bigger fraction, and comparing numerators alone.

## Verification

All 10 worksheet answers are machine-verified with SymPy (7 comparisons and 2
orderings through the `compare` checker, 2 equivalent fractions through the
`equiv` checker — problem 2 and 5). Nothing on this sheet is flagged manual: every
answer is a comparison or an equivalent fraction, and both are exactly checkable.
All 8 study-guide items (4 worked examples + 4 try-its) are verified the same way.

The build gate passed all 21 checks on the first run: template use, verification,
skill and facet coverage, layout and work space, the answer-key binding (each
boxed answer bound to its own verified problem), study-guide structure, and the
page budget.
