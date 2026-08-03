# Diagnosing Separation and Initial-Condition Errors (AP Calculus AB/BC)

Three PDFs are ready for an AP Calculus student working on separable
differential equations. The sheet is built around the three places these
problems actually break: integrating before the variables are separated, losing
or misplacing the constant of integration, and applying the initial condition at
the wrong moment.

- **Worksheet (6 pages, 8 problems).** Problems 1–2 establish the general and
  the particular solution of the same equation, and ask explicitly at which step
  the initial condition may first be used. Problems 3–6 are **four find-and-fix
  items**, each showing a named student's real work: Wren integrates $2xy\,dx$
  with $y$ treated as a constant; Dev exponentiates $\ln|y| = 5x + C$ into
  $e^{5x} + C$; Rosa takes the square root of $y^2/2 = x^2/2 + C$ term by term;
  and Sam loses the minus sign from $\int y^{-2}dy$. Problem 6 also asks what the
  corrected solution does as $x \to 0.5$ — the sign error hides a finite-time
  blow-up, so it changes the qualitative behaviour, not just a digit. Problem 7
  is a clean $u$-substitution solution that asks why applying the condition
  before integrating is meaningless. Problem 8 refutes "a constant is a constant,
  add it anywhere" with a derivative test. Work space is 6–8 cm, declared as
  `workspace_cm` so the page budget charges for separating, integrating, solving
  for the constant and checking by substitution.
- **Answer key (3 pages).** Each solution names the first wrong line, states the
  rule it breaks, then works the correct solution and checks it by substituting
  back into the differential equation. Problem 8 carries a model argument plus
  explicit accept/reject guidance for the grader. The generated quick-answer bank
  and a **"Common wrong answers"** block sit under the title.
- **Study guide (2 pages).** Three sections matching the worksheet's three
  facets: separate before integrating, where the constant of integration goes
  (why $+C$ becomes the factor $A = e^C$), and when to apply the initial
  condition (including that the radical applies to the whole side). Each has a
  rule box, a worked example whose first step names the decision, and a try-it,
  plus a watch-out on the one-line differentiate-and-compare check.

## Verification

**7 of 8** worksheet problems are machine-checked with SymPy — 1 `integrate`,
1 `eval` and 5 `approx`. Problem 8 is an argued justification, so it is declared
`{"type": "manual"}` rather than claimed as verified; the build therefore exits 2
and says so, which is the correct outcome for an open response, not a failure.
All **6** study-guide boxes (3 worked examples + 3 try-its) are machine-verified.

**Six misconception traps are declared and machine-checked** — one for every
planted wrong result on the sheet, plus two on the non-error items: 20 (constant
dropped before evaluating), 4 (integrated without separating), 153.41 (constant
added after exponentiating), 7 (square root taken term by term), 1.33 (minus sign
lost), and 4.83 (antiderivative reported instead of the particular solution).
Verification proves each is a value the problem's own check rejects, so every
find-and-fix item genuinely discriminates the error it targets, and the key
prints them as a grading block.

The facet plan is bound to the printed subtitle, every worksheet facet has a
study-guide worked example, and the facet rotation keeps the maximum same-facet
run at 1. Standards are tagged `FUN-7` — the differential-equations row of
`references/standards-map.md`, verbatim; no code was invented. Gate chain green
with one manual-review item (exit 2).
