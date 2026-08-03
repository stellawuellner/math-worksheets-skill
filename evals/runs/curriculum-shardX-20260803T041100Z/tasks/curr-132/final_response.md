# Multiplying fractions and mixed numbers (Grades 4–5)

Three PDFs are ready for a fourth- or fifth-grade learner practising fraction
multiplication.

**Worksheet — 12 problems, 6 pages.** Four different problem shapes are
interleaved after a short blocked warm-up, so the student has to choose a method
rather than repeat one:

- *Fraction × fraction* (1, 2, 4, 9) — including two where cancelling a common
  factor before multiplying keeps the arithmetic small.
- *Fraction × whole number* (3, 8) — the whole number rewritten as $n/1$; problem 8
  is a "12 batches of 3/8 cup" story.
- *Mixed numbers* (5, 7, 10, 12) — convert to improper fractions first; problem 10
  is a doormat-area question answered in square feet, and problem 12 is a two-step
  trail problem (fraction of the *remaining* distance).
- *Missing factor* (6, 11) — $\tfrac34 \times x = \tfrac9{20}$ and
  $x \times 2\tfrac12 = 4$, solved by multiplying by the reciprocal.

Difficulty ramps 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 5. Work space runs 5–8 cm per
problem; problems 10 and 12 carry unit-labelled answer lines (ft² and km).

**Answer key.** Each solution shows the setup, the cancelling or conversion step,
and the simplification — not just a boxed number. Problems 6 and 11 include the
check step (multiply the answer back in). Problem 10 carries a declared
misconception trap: multiplying whole parts and fraction parts separately gives
2.375 instead of 4.125, and the key's quick-answer bank prints that wrong value so
the grader can name the error. The key also gives a size estimate showing why 2.375
cannot be right.

**Study guide (2 pages).** Three skill sections, each with a rule box, a worked
example, and a distinct upside-down try-it:

1. Multiply fractions and whole numbers (multiply across; cancel first; "of" means ×).
2. Multiply mixed numbers (convert, then multiply; estimate to check).
3. Find a missing factor (divide by a fraction = multiply by the reciprocal).

**Verification.** All 12 worksheet answers and all 6 study-guide results were
machine-checked with SymPy (`eval`, `solve`, and `approx` checks) — nothing is
flagged for manual review. The full gate chain is green: every printed boxed answer
binds back to its verified value, both declared units bind in both directions
(sheet answer line ↔ JSON ↔ key box), every facet tested on the sheet has a worked
example in the guide, and 100% of the worksheet's stem numbers trace back to the
verification data.

Standards tag: `5.NF.A.1 / 6.NS.A.1 / 5.NF.B`, taken verbatim from the skill's
standards map.
