# Find and Fix: Parameters, Polar Bounds, and Speed — AP Calculus BC

Three PDFs are ready:

- **`ws_paramfix_curr494.pdf`** — the student worksheet, 8 error-analysis problems.
- **`ak_paramfix_curr494.pdf`** — the full step-by-step answer key.
- **`ss_paramfix_curr494.pdf`** — a 2-page study guide.

## What the worksheet does

Every problem shows a piece of student work that is wrong in one specific way,
and asks for two things: the corrected value, and a sentence naming the rule
that was broken. The eight errors are the three that dominate this unit:

- **Parameter errors** (1, 4, 7): reporting $dy/dt$ as $dy/dx$; differentiating
  the slope with respect to $t$ and forgetting the second division by $dx/dt$;
  and treating $dr/d\theta$ as the slope of a polar tangent line.
- **Polar bounds** (3, 5): integrating $r = 4\sin\theta$ over a full turn (which
  traces the circle twice), and guessing the limits of a rose petal instead of
  solving $r = 0$ for them.
- **Speed versus velocity** (2, 6, 8): adding velocity components instead of
  taking the magnitude; integrating the components separately for arc length;
  and computing speed from the *position* vector.

Problem 8 finishes with a speeding-up/slowing-down judgement, which is the
place the velocity/acceleration distinction actually pays off.

## Verification — what a machine checked, what you check

The answer key's "What is verified" note carries the same split.

- **9 of the 17 checks are machine-verified with SymPy**: every corrected value,
  including both polar area integrals (exact, $4\pi$ and $\tfrac{3\pi}{4}$), the
  arc-length integral in problem 6, and the parametric slope in problem 7 built
  from the converted $x$ and $y$ derivatives rather than asserted.
- **All 8 of those problems carry a machine-checked misconception trap.** Every
  wrong number printed in a stem (9, 7, $8\pi$, 12, $\tfrac{9\pi}{2}$, 12, $-1$,
  $\sqrt{45}$) was *computed* from the wrong method, and SymPy confirmed each is
  distinguishable from the right answer. Those appear in the answer key as
  "Common wrong answers" lines, so a paper showing 7 for problem 2 is immediately
  diagnosable as component-addition rather than arithmetic.
- **8 of the 17 are instructor-judged** — the (b) diagnosis on each problem.
  Each has a written rubric in the key stating what full credit requires.

So the honest split is **9 machine-checked, 8 instructor-judged**. For an
error-analysis sheet that is the correct shape: the diagnosis is the skill being
taught, and no CAS can read prose. Nothing is marked `[unchecked]`.

## Notes

- Angles are radians throughout; that is stated in the directions.
- Problem 4 has a free independent check worth showing a student: $x = t^2$ and
  $y = t^4$ means $y = x^2$, so $d^2y/dx^2$ must be 2 everywhere.
- The grade level and standards tagging (FUN-3.C for the derivative items,
  FUN-6 for the two area/arc-length items) print on the answer key only.
