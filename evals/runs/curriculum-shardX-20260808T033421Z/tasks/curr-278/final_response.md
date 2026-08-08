# Writing Growth and Decay Models from Data — Algebra 1

Three PDFs are ready:

- **Worksheet** (`ws_growthdecay_curr278.pdf`) — 10 problems, every one of them building a model
  $y = a \cdot r^{\,t}$ from real data and then using it. Four extract the multiplier from data
  (two tables, a pair of readings three hours apart, and a two-day bacteria count); three convert
  a stated percent into a multiplier and predict (a culture growing 8% an hour, a car losing 15% a
  year, a town losing 3% a year); three solve for the time (a doubling population, a halving drug
  dose, and a half-life problem that closes with a written explanation). Units are stated in every
  stem. Difficulty ramps 1 → 5.
- **Answer key** (`ak_growthdecay_curr278.pdf`) — every solution names how the multiplier was
  obtained, shows the power before the multiplication, and checks the answer by walking the
  halvings or doublings. A "Common wrong answers" note explains the \$7200 a student gets by taking
  15% of the original price four times instead of compounding. Quick Answers and a Curriculum block
  sit at the top.
- **Study guide** (`ss_growthdecay_curr278.pdf`) — 2 pages: the multiplier from a table, the
  multiplier from a percent (with the "percent of the original" error called out), and solving
  doubling / half-life models by matching powers. Rule box, worked example with a stated strategy
  step, and a try-it per section.

## What is verified, honestly

- **18 machine checks passed.** Every multiplier, every percent conversion, all four rounded
  two-decimal predictions (455.63, 396.72, 9396.11, 8849.09), the cube-root multiplier in problem
  5, and all three solve-for-the-time answers were recomputed by SymPy and matched the key.
- **1 response is instructor-judged**: problem 10(c), "explain why halving is not the same as
  removing a fixed number of grams". It carries a `manual` entry and a printed rubric, and the
  key's "What is verified" note names problem 10 as the only `---`.
- **1 misconception trap** was machine-tested for distinguishability: simple rather than
  compound depreciation, which lands on \$7200 instead of \$9396.11.
- All six study-guide examples and try-its were verified.

Nothing is marked `[unchecked]`.
