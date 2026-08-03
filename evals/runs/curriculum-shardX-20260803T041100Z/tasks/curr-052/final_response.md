# Place Value to 1,000 — Standard, Word, and Expanded Form (Grade 2–3)

Three PDFs are ready.

- **Worksheet** (`ws_place_value_curr052.pdf`, 4 pages) — 10 problems in a
  procedural-fluency format. A short directions box shows the same number
  (546) written all three ways, so the sheet opens with the worked pattern
  rather than a definition. Problems 1–3 are the warm-up (one conversion in
  each direction); after that the four methods are mixed so the student has
  to decide what each problem is asking for: standard → expanded, expanded →
  standard, number name → standard, and comparing two numbers that are written
  in *different* forms. No two problems share a skeleton — 907 hides a zero in
  the tens place, 600 + 5 hides one in the expanded form, problem 7 is an
  error-analysis item, problem 8 orders three numbers given three different
  ways, and the closing challenge adds ten and asks for the new number in both
  forms.
- **Answer key** (`ak_place_value_curr052.pdf`, 2 pages) — a quick-answer bank
  for fast checking, then a reasoned solution for every problem: which place
  each digit sits in, why a zero place is dropped from the sum but kept in the
  standard form, and the boxed final answer. Three problems carry a grading
  note naming the specific wrong answer a common error produces (90 + 7 on
  problem 4 means the 9 was read as 9 tens; 6015 on problem 7 means chunks are
  being stacked side by side instead of assigned to places).
- **Study guide** (`ss_place_value_curr052.pdf`, 2 pages) — four sections, each
  with a rule box, a worked example whose first line says *why* that method
  applies, and a try-it with the answer printed upside down inside the box. It
  closes with the zero-place watch-out, which is the single largest source of
  errors at this grade.

## Verification

All 10 worksheet problems are machine-verified with SymPy: 8 through the `eval`
checker (each expanded form is evaluated and compared against the standard form
it must equal, with the place values lifted into named givens so the checker
sees them) and 2 through the `compare` checker (one relation, one three-way
ascending order). Problem 7's misconception is declared as a machine-checked
trap: the verifier confirms 6015 is a value the problem's own check rejects, so
the planted wrong answer is genuinely distinguishable, and it is printed in the
key's "common wrong answers" block.

One item is flagged for manual review and is labelled as such in the key:
problem 9(a) asks for the number name of 470 written out in words. Spelling and
hyphenation are read by a teacher, so that half is encoded as `manual` rather
than claimed as verified; 9(b), the expanded form, is machine-checked. That is
why the build exits 2.

All 8 study-guide items (4 worked examples + 4 try-its) are verified the same
way, and every worksheet facet has a matching worked example in the guide.

**Standard used:** `2.NBT.A`, taken verbatim from `references/standards-map.md`
(row "Place value (tens/ones, to 1000)").

## Build

Green on the first build — all 21 gates pass, including the per-problem
answer-key binding, the example/try-it pairing in the study guide, and the
page budget (worksheet 4 pages, key 2, guide 2 against its hard 2-page cap).
