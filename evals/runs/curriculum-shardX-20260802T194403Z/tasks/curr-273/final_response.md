Three PDFs are ready for an Algebra 1 student on arithmetic sequences as linear
functions, focused on writing recursive formulas.

- **Worksheet** (10 problems, `ws_recseq_curr273.pdf`) — every problem asks for
  both lines of the recursive rule ($a_1$ and $a_n = a_{n-1} + d$) and then a
  numerical answer, so the formula is the work and the number is checkable. The
  representations rotate: two listed sequences (one with a negative common
  difference), three applications with units stated (a tank in liters, a chair
  stack in centimeters, a savings balance in dollars), two given recursive rules
  to run forward or backward, a table with $a_3$ and $a_7$ known and $a_1$
  missing, a recursive-to-explicit conversion, and a closing synthesis on a
  theater's rows that ends in a 15-term sum.
- **Answer key** (`ak_recseq_curr273.pdf`) — three labelled steps per problem
  (find $d$, write both lines, count the $n-1$ steps and compute), plus a
  quick-answer bank and a generated "Common wrong answers" block for the three
  designed traps (adding instead of subtracting a negative $d$; multiplying by
  $n$ instead of $n-1$, in two different contexts).
- **Study guide** (2 pages, `ss_recseq_curr273.pdf`) — four skills matching the
  worksheet's facets: recursive rule from a listed sequence, from a situation,
  using a recursive rule to reach a later term, and converting recursive to
  explicit ($d$ is the slope, $a_1 - d$ the intercept). Rule box, two-step worked
  example and upside-down try-it in each, plus a watch-out on the $n$ vs. $n-1$
  step count.

**Verification.** All 10 worksheet answers are machine-checked with SymPy
(7 `eval` term computations, 2 `solve` "which term" equations, 1 `series` partial
sum of 15 terms), and all 8 study-guide results are verified the same way.
Nothing is flagged manual. Three misconception traps were declared and proved
distinguishably wrong. The two unit-carrying answers (580 L, 183 cm) are bound in
both directions, the facet plan is bound to the printed subtitle, and the full
gate chain is green.

*Note on the standards tag:* `references/standards-map.md` has no dedicated
arithmetic-sequence code, so every problem carries `HSF-BF.A.1c` verbatim from
that file --- the nearest entry inside the HSF-BF.A family the task names. No
code was invented.
