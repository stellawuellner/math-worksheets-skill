Three PDFs are ready for a kindergarten / first-grade learner on **add-to
result-unknown stories within 10**.

- **Worksheet (`ws_addstories_curr023.pdf`, 3 pages)** — 8 problems, every one an
  add-to story where the *total* is the unknown. Two are modelled on ten-frames,
  two ask the student to write the number sentence itself (`4 + 5 = \_\_`), and
  the set closes with a two-change story and a "is Ben right?" check where the
  planted total (8) is the classic count-on-off-by-one error. Every problem has
  3–4 cm of drawing/counting room and its own answer line.
- **Answer key (`ak_addstories_curr023.pdf`, 2 pages)** — a quick-answer bank for
  grading, then a two- or three-step solution per problem: name the start, the
  change and the unknown, then show the count-on out loud ("6, 7, 8"). Problem 8
  also names *why* a child lands on 8 instead of 9.
- **Study guide (`ss_addstories_curr023.pdf`, 2 pages)** — three skills, each with
  a rule box, a worked example with a strategy step, and an upside-down try-it:
  turning the story into a number sentence, counting on from the bigger part, and
  showing the story on a ten-frame. A watch-out box flags the "don't say the
  starting number as your first count" error.

**Verification.** All 8 worksheet answers were machine-checked with SymPy
(6 `eval`, 2 `solve`) and all 6 study-guide results (3 worked examples + 3
try-its) as well — 14 machine-verified items, 0 manual. The declared misconception
trap on problem 8 (`4 + 3 + 2 - 1 = 8`) was machine-checked to be distinguishable
from the correct answer, and it prints in the key as a "common wrong answers"
line. The full gate chain passed green, including the per-problem binding of
every printed boxed answer back to its verified value.
