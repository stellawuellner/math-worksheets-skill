# Volumes from Known Cross Sections and Cylindrical Shells — AP Calculus AB/BC

Three PDFs are ready:

- **`ws_volumes_curr488.pdf`** — the student worksheet, 8 problems.
- **`ak_volumes_curr488.pdf`** — the full step-by-step answer key.
- **`ss_volumes_curr488.pdf`** — a 2-page study guide.

## What the worksheet covers

All eight problems are volume computations, and each one names its units:
metres, centimetres or feet, so every answer comes out in a stated cubic unit
and the answer line on the sheet prints that unit. The set alternates between
the two techniques so the student has to decide which is in play:

- **Known cross sections** (1, 2, 4, 7): squares, semicircles and equilateral
  triangles built on a base region. The point of the mix is that the base only
  gives the *side*; the named shape turns it into an area.
- **Cylindrical shells** (3, 5): revolution about the $y$-axis, radius $x$,
  height read straight off the curve.
- **Choosing and adapting the setup** (6, 8): why shells avoid the algebra a
  washer setup would need, and what the radius becomes when the axis moves off
  the $y$-axis to the line $x = 4$.

Problem 7 asks for the intersection of $y = x$ and $y = x^2$ first — a
deliberate two-step, because the limits are the part students most often
guess. Problem 8 is the hardest and asks for an endpoint check on the radius,
which is the habit that prevents the single most common shell error.

## Verification — what a machine checked, what you check

**9 of the 11 answer checks are machine-verified with SymPy**; 2 are flagged
for you to judge. The "What is verified" note printed at the top of the answer
key says the same thing.

- **Machine-checked (9):** every definite integral was recomputed by SymPy
  from the integrand and limits printed in the key — including the exact forms
  $\tfrac{64}{3}$, $\tfrac{81\pi}{16}$, $\tfrac{16\sqrt3}{3}$,
  $\tfrac{972\pi}{5}$ and $\tfrac{1}{30}$ — plus the intersection
  $x = 0, 1$ in problem 7, solved rather than asserted.
- **Instructor-judged (2):** problem 6(b) and problem 8(b), the two written
  explanations. Each carries a rubric in the answer key — 6(b) must name the
  *variable of integration* as the reason, not just "shells are easier"; 8(b)
  must say the radius is a distance from the axis and check it at both
  endpoints.

Every printed answer slot has a verification entry behind it, so nothing is
marked `[unchecked]` in the Quick Answers bank.

Units are checked in both directions: the unit each problem declares is the
unit printed on the worksheet's answer line *and* inside the boxed answer in
the key, so a cubic-metre problem cannot be answered in cubic centimetres
without a gate catching it.

## Notes

- Exact answers are asked for first and decimals second, on purpose — a
  decimal alone hides whether the student integrated or estimated.
- The study guide's three sections mirror the three skills, and each try-it is
  a fresh re-parameterisation (different limits or a different axis), not the
  worked example with new numbers pasted in.
- The grade level and the FUN-6 tagging print on the answer key only.
