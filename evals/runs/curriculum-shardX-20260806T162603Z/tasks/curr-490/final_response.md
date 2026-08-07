# Integrals in Context: Average Value, Accumulation, and Motion — AP Calculus AB/BC

Three PDFs are ready:

- **`ws_motion_curr490.pdf`** — the student worksheet, 10 problems.
- **`ak_motion_curr490.pdf`** — the full step-by-step answer key.
- **`ss_motion_curr490.pdf`** — a 2-page study guide.

## How the sheet is built

This is a review sheet, so it is deliberately **not** blocked by topic. Problems
1–3 are a short warm-up with one problem on each idea, and from problem 4 on the
three are interleaved so the student has to *choose* the method before writing
anything:

| | average value | accumulated change | motion |
|---|---|---|---|
| warm-up | 1 | 2 | 3 |
| mixed | 4, 7 | 5, 8 | 6, 9 |

Problem 10 is the synthesis: one velocity function, three questions off it —
total distance, average velocity, and why those are not the same as averaging
the fastest and slowest speeds.

The distinction the sheet is really drilling is the one students lose: integrate
a rate and you get a total; divide by the interval and you get an average;
integrate the *absolute value* of a velocity and you get distance rather than
displacement. Problems 3 and 6 sit deliberately close together for that reason,
and problem 9 pairs position with turning point so "where is it" and "how far
did it go" cannot be confused.

## Verification — what a machine checked, what you check

**13 of the 14 answer checks are machine-verified with SymPy**; 1 is flagged for
you to judge. The answer key's own "What is verified" note reports the same
split.

- **Machine-checked (13):** every definite integral recomputed from the
  integrand and limits, including the two absolute-value integrals (problems 6
  and 10a, where SymPy handles the sign change rather than trusting my split),
  the exact forms $\tfrac{2}{\pi}$, $18 + \tfrac{12}{\pi}$,
  $200(1 - e^{-1})$, $\tfrac{28}{3}$ and $\tfrac{4}{3}$, the turning times in
  problems 6 and 9, and the position $x(6) = 9$.
- **Instructor-judged (1):** problem 10(c), the written explanation. The answer
  key prints a model response and a rubric — full credit contrasts the two
  *weightings* (every instant equally vs. two instants), half credit for
  quoting the average-value formula alone.

Nothing is marked `[unchecked]`: every printed answer slot on the sheet has a
verification entry behind it, and where a problem prints two answer lines
(problems 6, 9, 10) each line has its own entry with its own unit.

## Notes

- Units are bound in both directions — litres, kilograms, metres and metres per
  second are declared in the verification data, printed on the worksheet's
  answer lines, and printed inside the boxed answers in the key.
- Problem 7 (the greenhouse) is the one worth talking through: the average of
  $18 + 6\sin(\pi t/12)$ over half a period is *not* 18, and the extra
  $12/\pi \approx 3.82$ is exactly the half-cycle where the sine is positive.
- The grade level and the FUN-6 tagging print on the answer key only.
