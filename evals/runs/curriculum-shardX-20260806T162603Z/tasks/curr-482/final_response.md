# Separable Differential Equations with Initial Conditions — AP Calculus AB/BC

Three PDFs are ready:

- **`ws_sepde_curr482.pdf`** — the student worksheet, 10 problems.
- **`ak_sepde_curr482.pdf`** — the full step-by-step answer key.
- **`ss_sepde_curr482.pdf`** — a 2-page study guide to work alongside the sheet.

## What the worksheet covers

Every problem is a separable first-order equation, and the set walks up a clean
ramp rather than repeating one skeleton:

1. Problems 1–2 are pure separation-and-integration (write $\ln|y| = F(x)+C$,
   write $\tfrac12 y^2 = G(x)+C$) — no initial condition yet, so the mechanics
   are isolated.
2. Problems 3, 6 and 8 add an initial condition and ask for the particular
   solution plus one evaluated value. The three use different separation shapes
   ($2xy$, $3x^2/y$, $e^{x-y}$), so nothing is a re-run.
3. Problems 4, 7 and 9 turn the particular solution around: solve for *when* a
   value occurs (a bacteria colony, a draining tank) rather than plugging in.
4. Problem 5 and problem 10 are the two reasoning items — the $\pm$ branch
   ambiguity, and why the solution through $(0,\tfrac12)$ cannot be extended
   past $x=\pi$.

The three skills tested — separating and integrating, finding $C$ from the
start value, and using the particular solution — each get their own section in
the study guide with a rule box, a worked example, and a *different* try-it
problem with the answer printed upside down.

## Verification split — what a machine checked and what you check

**15 of the 17 answer checks are machine-verified with SymPy**; 2 are flagged
for you to judge. This matches the "What is verified" note printed at the top
of the answer key, and the two instructor-judged items are marked `---` in the
Quick Answers bank.

- **Machine-checked (15):** every antiderivative (SymPy differentiates the key's
  antiderivative back and compares it to the integrand), every rounded decimal
  (recomputed from the givens, not from my arithmetic), the exact solution
  $x = 4\ln 4$ of $12e^{x/4} = 48$, and the check that
  $y = 1/(1+\cos x)$ really does give $y(0) = \tfrac12$.
- **Instructor-judged (2):** problem 5(b) and problem 10(b), the two written
  explanations. No CAS can grade prose. The answer key prints a model response
  and a short rubric for each — for 5(b), full credit needs both the
  plus-or-minus ambiguity *and* the role of the initial value; for 10(b), the
  vanishing denominator *and* what it means for the interval of definition.

Nothing on the sheet is marked `[unchecked]`: every printed answer blank has a
verification entry behind it.

## Notes for whoever is helping

- The grade level prints only on the answer key (in its Curriculum block,
  tagged FUN-7), never on the student's copy.
- Problem 9's answer is asked for "to the nearest tenth of a minute" and comes
  out exactly 96.0 — that is not a rounding artefact, the algebra is clean.
- Problem 8 needs the hint that $e^{x-y} = e^x e^{-y}$; it is printed in the
  stem, since spotting the factorisation is a different skill from separating.
