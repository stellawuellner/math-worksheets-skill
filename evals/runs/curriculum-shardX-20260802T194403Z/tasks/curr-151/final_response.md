Three PDFs are ready for a Grade 6/7 learner on ratios and equivalent ratio
tables, focused on writing and interpreting ratios in multiple forms.

- **Worksheet** (10 problems, `ws_ratioforms_curr151.pdf`) — every problem hands
  the student a model and asks for notation. A tile strip drives the three
  written forms (4 to 6, 4:6, 4/6) and then the part-to-whole form; two ratio
  tables (flour/water, pencils/price) build equivalent ratios by scaling both
  rows; a tape diagram turns 3:5 plus a box value into a total; a part-to-part
  2:7 statement is turned into a fraction of the whole class; two mixes are
  compared by the *value* of their ratios; and the closing synthesis splits
  45 L of paint in the ratio 3 to 2. Each problem has 5-6 cm of work space.
- **Answer key** (`ak_ratioforms_curr151.pdf`) — three labelled reasoning steps
  per problem (read the model, connect it to notation, compute/check), a
  quick-answer bank, and a generated "Common wrong answers" block naming four
  designed-for errors (inverted ratio, one tape strip instead of both,
  part-to-part in place of part-to-whole, halving instead of 3 + 2 shares).
- **Study guide** (2 pages, `ss_ratioforms_curr151.pdf`) — four skills matching
  the worksheet's four facets: reading a ratio off a model, part-to-part vs.
  part-to-whole, equivalent ratio tables, and the value of a ratio. Each has a
  rule box, a two-step worked example, and an upside-down try-it, plus a
  watch-out on the a:b vs. a/(a+b) confusion.

**Verification.** All 10 worksheet answers are machine-checked with SymPy
(5 `eval` ratio computations, 3 `solve` proportions, 1 `compare` of two ratio
values, 1 unit-carrying `eval`), and all 8 study-guide results are verified the
same way. Nothing is flagged manual. Four misconception traps were declared and
proved distinguishably wrong by the verifier. The declared facet plan is bound
to the printed subtitle, every worksheet facet has a study-guide worked example,
and the "27 L" answer is unit-bound in both directions (worksheet answer line
and boxed key answer). Full gate chain green.
