# Synthesis Review: Vector Motion, Polar Curves, and Accumulation — AP Calculus BC

Three PDFs are ready:

- **`ws_pvsyn_curr495.pdf`** — the student worksheet, 10 problems.
- **`ak_pvsyn_curr495.pdf`** — the full step-by-step answer key.
- **`ss_pvsyn_curr495.pdf`** — a 2-page study guide.

## How the sheet is built

This is a review sheet, so it is deliberately not blocked by topic. Problems
1–3 are a warm-up with one problem on each of the three ideas, and from
problem 4 on they are interleaved, one after another, so the student has to
identify what is being asked before reaching for a formula:

| | vector motion | polar intersections | accumulated quantities |
|---|---|---|---|
| warm-up | 1 | 2 | 3 |
| mixed | 4, 7 | 5, 8 | 6, 9 |

Problem 10 is the synthesis challenge: one velocity vector, and three questions
off it — total distance, position, and why those two are different numbers.
The speed there simplifies exactly to $t^2 + 1$, so the arc length comes out to
a clean 12 metres and the comparison with $\sqrt{117}$ is easy to see.

## Verification — what a machine checked, what you check

The answer key's "What is verified" note reports the same split.

- **16 of the 18 checks are machine-verified with SymPy.** That includes both
  polar intersection solves (found over a full turn, not guessed), the area
  between $r = 4\cos\theta$ and $r = 2$ in exact form
  $\tfrac{4\pi}{3} + 2\sqrt3$, the arc length $10\sqrt5 - 2$, the exponential
  accumulation $60(1 - e^{-1})$, and every coordinate of every position asked
  for — computed from the antiderivative, not asserted.
- **2 are instructor-judged:** problem 8(c) (why solving the two polar
  equations simultaneously misses the pole) and problem 10(c) (why path length
  exceeds displacement). Both carry a written rubric in the answer key.

Nothing is marked `[unchecked]`. Where a problem prints two answer lines
(problems 4, 8, 9, 10) each line has its own verification entry, and where the
two lines carry different units — problem 9 answers in litres and in minutes —
each unit is declared and bound to its own line.

## Notes

- Angles are radians throughout, stated in the directions.
- Problem 8(c) is the one worth discussing aloud: both curves reach the pole,
  but at different values of $\theta$, which is why a polar point has to be
  checked separately from the algebra. Students lose this point routinely on
  the exam.
- The grade level and standards tagging print on the answer key only.
