# Evaluating and Graphing Exponential Functions — Algebra 1

Three PDFs are ready:

- **Worksheet** (`ws_expgraph_curr277.pdf`) — 12 fluency problems on $a \cdot b^{\,x}$. Six are
  straight evaluations (including $b^0$, a decimal base, a negative exponent, and a doubling model
  with the exponent $t/3$); three build a table and plot it on a grid supplied on the page — one
  growth curve, one decay curve, one with a solve-and-explain tail; three solve equations by
  rewriting both sides as powers of the same base. Difficulty ramps 1 → 5 and the three types are
  interleaved rather than blocked.
- **Answer key** (`ak_expgraph_curr277.pdf`) — every answer worked out with the power computed
  before the multiplication, exact fractions kept as fractions ($\tfrac12$, $\tfrac29$), the
  matching-powers step written out for each equation, and a check. A "Common wrong answers" note
  covers the declared negative-exponent misconception. Quick Answers and a Curriculum block sit at
  the top.
- **Study guide** (`ss_expgraph_curr277.pdf`) — 2 pages: evaluating a power rule, table-to-graph
  (with the shape facts: crosses the vertical axis at $a$, never reaches the horizontal axis), and
  solving by matching powers, plus a watch-out box on the two commonest slips
  ($4 \cdot 2^x \ne 8^x$, $3^{-2} \ne -9$).

## What is verified, honestly

- **30 machine checks passed.** Every table entry, every evaluation, both rounded two-decimal
  answers (1072.08 and 1587.40), and all four exponential equations were recomputed by SymPy and
  matched the key. The exact fractional values are checked as fractions, not decimals.
- **1 response is instructor-judged**: the closing part of problem 10, "explain why this curve
  never touches the horizontal axis". It carries a `manual` entry and a printed rubric, and the
  key's "What is verified" note names problem 10 as the only `---`.
- **1 misconception trap** was machine-tested: reading $2 \cdot 3^{-2}$ as $-18$ rather than
  $\tfrac{2}{9}$.
- All six study-guide examples and try-its were verified.

Nothing is marked `[unchecked]`.
