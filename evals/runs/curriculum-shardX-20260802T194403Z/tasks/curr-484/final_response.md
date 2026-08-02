# Diagnosing Separation and Initial-Condition Errors (AP Calculus AB/BC)

Three PDFs are ready for an AP Calculus student working on separable
differential equations. The sheet is built around the three places these
problems actually break: integrating before the variables are separated, losing
the constant of integration, and applying the initial condition at the wrong
moment.

- **Worksheet (4 pages, 8 problems).** Problems 1-2 establish the general and
  particular solution of the same equation. Problems 3-6 are find-and-fix items,
  each showing a named student's real work: Wren integrates `xy dx` with y
  treated as a constant, Dev writes `y = e^(3x) + C` after exponentiating, Rosa
  square-roots `y^2/2 = x^2/2 + C` term by term *and* applies the initial
  condition too late, and Sam loses the minus sign from the integral of y to the
  negative second power. Problem 6 also asks what the corrected solution does as
  x approaches 1 — the sign error changes the qualitative behaviour, not just a
  digit. Problem 7 asks explicitly when the initial condition may be applied.
  Problem 8 refutes "a constant is a constant, add it anywhere" with a derivative
  test.
- **Answer key (3 pages).** Each solution names the first wrong line, states the
  rule it breaks, then works the correct solution and checks it by substitution.
  Problem 4's key includes the one-line derivative test that would have caught
  the error before any arithmetic. Problem 8 carries a model argument plus
  explicit accept/reject guidance.
- **Study guide (2 pages).** Three sections: integrating both sides when the
  right-hand side has no y, separating the variables (with the two integrals
  students lose most often, including the minus sign on the integral of y to the
  negative second power), and where the constant of integration goes — why
  exponentiating turns `+C` into the factor `A = e^C`. Each has a rule box, a
  worked example whose first step names the decision, and a try-it.

## Verification

**7 of 8** worksheet problems were machine-checked with SymPy. Problem 8 is an
argued justification, so it is declared `{"type": "manual"}` rather than claimed
as verified — the build exits 2 and says so, which is correct for an open
response. All **6** study-guide boxes (3 worked examples + 3 try-its) are
machine-verified.

**Five misconception traps are declared and machine-checked**, one for every
planted wrong result on the sheet: 8 (constant dropped), 4 (integrated without
separating), 23.09 (constant added after exponentiating), 7 (square root taken
term by term), and 0.67 (minus sign lost). Verification proves each is a value
the problem's own check rejects, so each find-and-fix item genuinely
discriminates its error; the answer key prints them as a "common wrong answers"
block for grading. The full gate chain is green.
