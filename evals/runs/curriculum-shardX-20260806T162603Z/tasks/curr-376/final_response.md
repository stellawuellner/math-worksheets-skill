# Exponential Form and Logarithmic Form — Algebra 2

Three PDFs are ready:

- **Worksheet** (`ws_logform_curr376.pdf`) — 10 problems, all on converting
  between $b^{\,y} = x$ and $\log_b x = y$.
- **Answer key** (`ak_logform_curr376.pdf`) — quick-answer bank, then a worked
  solution per problem that shows the switched form before the arithmetic.
- **Study guide** (`ss_logform_curr376.pdf`, 2 pages) — four sections:
  exponential to logarithm, logarithm back to a power, evaluating a logarithm,
  and solving by switching form. Each carries a rule, a worked example that names
  its strategy first, and a try-it.

## The model

The worksheet opens with a small table that puts the same three facts side by
side in words, in exponential form, and in logarithmic form, ending in the
general row $b^{\,y} = x \leftrightarrow \log_b x = y$. Every problem then points
back at it: the base never moves, and the logarithm *is* the exponent. Problems 4
and 5 extend the model to negative exponents, problem 7 to a fractional one, and
problem 9 flips the unknown to the base itself. Problem 8 attaches the model to a
doubling bacteria count so the conversion answers a question with a unit.

## Verification — the honest split

**13 verified responses across the 10 problems**:

- **12 are machine-checked** with SymPy. Note what is actually checked: a
  conversion is verified by recomputing the logarithm as $\ln x / \ln b$ (or the
  power $b^{\,y}$) and comparing with the value the key prints — so a key that
  wrote the base and the exponent the wrong way round would fail the gate, not
  pass it.
- **1 is instructor-judged**, marked `---` in the bank: **10(c)**, where the
  student must explain why no $x \le \tfrac13$ can solve $\log_2(3x-1) = 4$. The
  key prints what a correct response must contain.

The key's "What is verified" note reports the same 12 of 13, naming problem 10.
No `[unchecked]` marks.
