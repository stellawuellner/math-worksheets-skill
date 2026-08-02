Three PDFs are ready for an Algebra 2 student on **diagnosing reversed
composition and unverified inverse domains**, in an error-analysis format.

- **Worksheet (`ws_composinv_curr384.pdf`, 4 pages)** — 8 problems. Problems 1–2
  compute $(f \circ g)(3)$ and $(g \circ f)(3)$ for the same pair so the student
  produces the counterexample themselves ($15$ vs $2$). Problem 3 reads an inverse
  value as a solve. **Two find-and-fix items**: problem 4 (Nia computes
  $(f\circ g)(4)$ as $7$ by composing in reverse; correct answer $-5$) and problem
  6 (Sam's $h^{-1}(x) = 3-\sqrt{x}$ returns $-1$, outside the restricted domain
  $x \ge 3$; correct value $7$). Problem 5 verifies an inverse by composition,
  problem 7 uses the two solutions of $x^2 = 9$ to show $x^2$ has no inverse
  unrestricted, and problem 8 closes with an open justification about a one-sided
  composition check. Difficulty ramps 1 → 5; every problem has 5–7 cm of work space.
- **Answer key (`ak_composinv_curr384.pdf`, 2 pages)** — quick-answer bank, a
  generated **"Common wrong answers"** block (7 → composed in reverse order;
  $-1$ → kept the minus branch), and a three-step solution per problem. The two
  find-and-fix items include the exact one-sentence diagnosis to accept, and
  problem 8 carries a full model answer plus the $\sqrt{x^2} = |x|$ reasoning.
- **Study guide (`ss_composinv_curr384.pdf`, 2 pages)** — three sections, each a
  rule box + worked example with a strategy first step + upside-down try-it: read
  composition inside-out (with a watch-out box on the substitute-into-the-outer-
  function error), verify a proposed inverse by composing **both** ways, and treat
  the domain as part of the inverse (one-to-one, branch choice, domain/range swap).

**Verification.** 7 of the 8 worksheet answers are machine-checked with SymPy
(4 `eval`, 2 `solve`, 1 `equiv`), and all 6 study-guide results (3 worked examples
+ 3 try-its) as well. Problem 8 is a genuine explanation and is declared `manual`;
it is flagged for human review in the gate log and is **not** claimed as verified.
Both planted wrong results are declared as misconception traps and were
machine-checked: $g(f(4)) = 7$ and $3 - \sqrt{16} = -1$ each compute to a value the
problem's own check rejects, so the printed wrong numbers are derived rather than
typed. The build passed with exit 2 (one manual-review item), the correct outcome.
