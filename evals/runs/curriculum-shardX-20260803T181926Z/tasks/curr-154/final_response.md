# Ratios and equivalent ratio tables — reversed and non-equivalent ratios (Grades 6–7)

Three PDFs are ready:

- **Worksheet** (`ws_ratios_curr154.pdf`, 4 pages) — 8 problems, every one about
  order or equivalence: writing a ratio in the requested order, testing $4:6$
  against $6:9$, three find-the-mistake items (a reversed girls-to-boys ratio, an
  "add 2 to both parts" table, and an upside-down rate), an equivalent-ratio table
  to complete, a unit-rate comparison of two cars, and a challenge that finds and
  repairs the one column of a ratio table that does not belong.
- **Answer key** (`ak_ratios_curr154.pdf`, 2 pages) — each solution shows the
  reasoning and then a sense check (a girls-to-boys ratio must exceed 1; a printer
  prints more than one page a minute), which is the habit that catches a reversed
  ratio without redoing the arithmetic. It opens with a quick-answer bank and a
  generated Curriculum section (6.RP.A.2, 6.RP.A.3, difficulty 1–4), and prints a
  "common wrong answers" line for each declared trap.
- **Study guide** (`ss_ratios_curr154.pdf`, 2 pages) — three sections: order is part
  of the answer (with the greater-than-1 sense check), scale both parts by the same
  factor (and why adding fails), and three interchangeable tests for equivalence.
  Each has a rule box, a worked example that opens with the strategy, and a try-it.

**Find-and-fix items (3, more than the two requested).** Problems 3, 5 and 7 carry
planted wrong work, and each planted result is declared as a machine-checked
misconception trap: the reversed ratio $12/18$, the added-instead-of-scaled 8 scoops,
and the reversed rate 0.125 pages per minute. SymPy confirmed each is exactly what
the wrong method computes and that the problem's own check rejects it.

**What was verified.** All 9 numeric and relational checks across the 8 problems were
recomputed by SymPy and passed — including the two comparison answers ($=$ and $<$),
which are checked as relations, not just as numbers. Three items are flagged for
**manual review**: the one-sentence explanations in problems 3, 5 and 7 (why order
matters, why adding does not preserve a ratio, which number goes on top). Each has a
model answer plus a note on what earns credit in the key. Layout, work space, answer
blanks, page budget, and the binding of every boxed answer to its verified value all
passed the build gates.
