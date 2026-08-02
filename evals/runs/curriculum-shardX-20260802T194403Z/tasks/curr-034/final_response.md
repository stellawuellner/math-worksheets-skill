Three PDFs are ready for a K/Grade-1 learner on teen numbers, focused on
catching and correcting a swapped tens-and-ones representation.

- **Worksheet** (6 problems, `ws_teenplace_curr034.pdf`) — a ten-frame warm-up
  that names which digit counts tens, three find-and-fix items (Leo writes 61
  for 1 ten and 6 ones; Nina writes 81 for eighteen; Ana writes 71 for one full
  ten-frame and 7 dots), and two compare-the-swapped-pair items (1 ten 3 ones
  vs. 3 tens 1 one; and Jo's swapped number vs. the number she meant). Every
  problem has 3 cm of building/drawing space and its own answer blank.
- **Answer key** (`ak_teenplace_curr034.pdf`) — three numbered reasoning steps
  per problem (name the tens, name the ones, write tens-first), a quick-answer
  bank for grading, and a generated "Common wrong answers" block that tells the
  grader exactly what a 41 / 61 / 81 / 71 means.
- **Study guide** (2 pages, `ss_teenplace_curr034.pdf`) — three skills
  (read 1 ten and some ones; fix a swapped number; compare a swapped pair),
  each with a rule box, a two-step worked example, and an upside-down try-it,
  plus a watch-out box on why teen numbers are *said* ones-first but *written*
  tens-first.

**Verification.** All 6 worksheet answers and all 6 study-guide results were
machine-checked with SymPy (4 `eval` place-value computations and 2 `compare`
relations on the worksheet). Nothing is flagged manual. The four planted wrong
answers (41, 61, 81, 71) are declared misconception traps, so the verifier
proved each planted result is distinguishably wrong and that the printed wrong
number really is what the swapped method computes. The full gate chain is green,
including the per-problem binding of every printed answer to its verified value.
