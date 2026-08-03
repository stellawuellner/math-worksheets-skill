Three PDFs are ready for a Grade-8 / pre-algebra learner on slope and rate of
change, focused on diagnosing the two set-up errors that keep the right digits
and still give a wrong answer: the **inverted** ratio (run over rise) and the
**sign-reversed** ratio (differences taken in opposite orders).

- **Worksheet** (8 problems, `ws_slopeerrors_curr219.pdf`) — a warm-up that makes
  the student label rise and run before dividing, then five find-and-fix items
  where another student's work is printed in full and must be diagnosed *by its
  set-up*, not by re-checking arithmetic: Devi's sign reversal on (−3, 5) and
  (2, −5); Mika's inverted ratio on (1, 4) and (5, 6); Ty's mixed order on
  (5, 9) and (1, 1); Jo's inverted candle rate; and Priya's inverted equation for
  a missing coordinate. Two table items (a draining tank) separate the signed
  *change* from the signed *rate of change*. The closing challenge solves for the
  missing coordinate a and asks for the diagnosis of Priya's −11. Work space is
  5–6.5 cm per problem, declared with `workspace_cm`.
- **Answer key** (`ak_slopeerrors_curr219.pdf`) — four to six numbered steps per
  problem. Each find-and-fix solution first *names what each of the student's
  differences actually measured*, then names the error class, then rebuilds the
  computation in one consistent order, and finishes with an independent check (a
  predicted sign, a single table step, a multiply-back, or a recomputed slope).
  It carries the generated quick-answer bank and a generated "Common wrong
  answers" block covering 0.5, 2, 18, 3, −2 and −0.67.
- **Study guide** (2 pages, `ss_slopeerrors_curr219.pdf`) — three skills matching
  the worksheet tags: slope from two points (rise on top, same order top and
  bottom, predict the sign first), rate of change from a table (later minus
  earlier in both), and rate of change in a story (read the units of your fraction
  back, and multiply the rate by the elapsed time). Each has a rule box, a
  two-step worked example, and an upside-down try-it, plus a watch-out box on why
  re-checking arithmetic can never find either of these two errors.

**Verification.** All 8 worksheet answers and all 6 study-guide results are
machine-checked with SymPy: four `slope` checks from raw coordinate pairs, one
`read_data` signed difference computed from the same table the worksheet prints,
two `eval` rate computations, and one `solve` for the missing coordinate.
Nothing is flagged manual — every item on this sheet has a single checkable
value, so nothing is described as verified that is not. Seven planted wrong
answers are declared misconception traps (0.5, 2, 2, 18, 3, −2, −0.67), and the
verifier proved each is distinguishably wrong and really is what the inverted or
sign-reversed method computes; the tank givens were chosen so the sign-reversed
rate (+3) is a plausible-looking number the correct check still rejects.

Standards: every problem is tagged `8.EE.B.5, 8.EE.B.6` from
`references/standards-map.md`. The full gate chain is green.
