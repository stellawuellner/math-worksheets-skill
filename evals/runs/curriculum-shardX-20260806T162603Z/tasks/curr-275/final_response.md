# Modeling Discrete Linear Change and Arithmetic Sums — Algebra 1

Three PDFs are ready:

- **Worksheet** (`ws_arithmodel_curr275.pdf`) — 12 problems, all set in situations that change by
  the same amount at every stage: stacking chairs, gym fees, a training plan, a draining tank,
  theatre rows, a savings account, a plumber's call-out, a brick pile, a data allowance, two job
  offers, and a concert hall. Three question types are interleaved rather than blocked, so the
  student has to decide each time whether the question wants a **value** at a stage, the **stage
  number** at a value, or a **running total** — the three are never more than two problems apart.
  Difficulty ramps 1 → 5.
- **Answer key** (`ak_arithmodel_curr275.pdf`) — each problem starts by naming what $n$ counts,
  then shows the step count, the term rule or the pairing $S_n = \tfrac{n}{2}(a_1 + a_n)$, and a
  check. A "Common wrong answers" block covers the three declared misconceptions. Quick Answers
  and a Curriculum block sit at the top.
- **Study guide** (`ss_arithmodel_curr275.pdf`) — 2 pages: turning a situation into a term rule
  (including the trap where a one-off fee is not part of the step), finding the stage number, and
  adding a finite run. Rule box, worked example with a stated strategy step, and a try-it per
  section.

## What is verified, honestly

- **14 machine checks passed.** Every stage value, every stage number, and all five running totals
  were recomputed by SymPy — the sums as genuine symbolic summations, not by re-applying the same
  formula the key uses — and matched the printed answers.
- **1 response is instructor-judged**: problem 12(c), "explain why doubling the number of rows more
  than doubles the capacity". The key prints the rubric and, for reference, the actual 48-row
  total. The key's "What is verified" note names problem 12 as the only `---`.
- **3 misconception traps** were machine-tested for distinguishability, including the sum error of
  multiplying the average by the number of gaps instead of the number of rows.
- All six study-guide examples and try-its were verified.

Nothing is marked `[unchecked]`.
