Three PDFs are ready for an AP Calculus AB/BC student on definite integrals and
the Fundamental Theorem, focused on diagnosing bounds, sign and
variable-of-integration errors.

- **Worksheet** (8 problems, `ws_ftcerrors_curr474.pdf`, 5 pages) — seven of the
  eight problems are find-and-fix items, one per named error family. Bounds:
  Jae evaluates $\int_5^2 2x\,dx$ as $5^2 - 2^2 = 21$ instead of $-21$; a student
  given $\int_1^6 f = 10$ and $\int_1^4 f = 3$ answers $\int_6^4 f = 7$ instead
  of $-7$; Kwame differentiates $G(x) = \int_x^5 (t^2+1)\,dt$ without flipping the
  bound and gets $5$ rather than $-5$; Ines substitutes $u = x^2+1$ but evaluates
  the $u$-antiderivative at the $x$-bounds, getting $2$ instead of $78$. Sign:
  Ravi drops the parentheses around $F(1)$ and gets $10$ instead of $18$; Lena
  uses $+\cos x$ as the antiderivative of $\sin x$ and gets $-0.5$ instead of
  $0.5$. Variable of integration: Noor substitutes the upper bound straight into
  the integrand of $\int_0^2 (3t^2+2)\,dt$ and gets $14$ instead of $12$ — the
  answer that equals $f$(upper bound), which is that error's fingerprint. Problem
  8 is an open explanation. Work space runs 5–7.5 cm per problem.
- **Answer key** (`ak_ftcerrors_curr474.pdf`, 4 pages) — four numbered steps per
  problem: name the slip in words, redo the work, box the answer, then run an
  *independent* check — the reversal rule, splitting the integrand, a size bound
  from the integrand's range, the positive-integrand sign test, an explicit
  computation of $G(x)$, and expanding $x(x^2+1)^3$ termwise to confirm 78 without
  substituting at all. It carries the generated quick-answer bank and the
  generated "Common wrong answers" block (21, 10, 14, 7, −0.5, 5, 2), plus a
  model answer and a full-credit checklist for the open item.
- **Study guide** (2 pages, `ss_ftcerrors_curr474.pdf`) — three skills matching
  the worksheet tags: bound order carries a sign (reversal, additivity, and
  converting bounds under substitution), subtract the whole lower value (the
  parentheses rule plus the trig antiderivative signs), and the variable of
  integration is a dummy (FTC Part 1). Each has a rule box, a two-step worked
  example and an upside-down try-it, plus a watch-out box on the diagnostic value
  of a right-magnitude/wrong-sign answer.

**Verification.** 7 of the 8 worksheet problems are machine-checked with SymPy:
five `definite_integral` evaluations (including the backwards-bounds one, the
$\sin$ integral over $[0, \pi/3]$, and the substitution problem), an `integrate`
check that $x^3 - 4x$ really is an antiderivative of $3x^2 - 4$, and two `eval`
checks for the two problems whose answers are built from given integral values or
FTC Part 1. Problem 2 carries two entries under one id so the antiderivative and
the evaluated integral are both bound. All 6 study-guide results are
machine-checked. Problem 8 is a genuinely open explanation and is declared
`{"type": "manual"}`; the build exits 2 with one manual-review item, and it is
nowhere described as machine-verified.

Seven planted wrong results are declared misconception traps (21, 10, 14, 7,
−0.5, 5, 2). The verifier proved each one distinguishably wrong and derived from
the stated wrong method rather than typed by hand.

**Standards.** Problems are tagged `LIM-5, FUN-6` ("Riemann sums & FTC") and the
substitution problem `FUN-6.D–FUN-6.E` ("u-substitution / parts (BC)"), both
copied verbatim from `references/standards-map.md`. Together they cover the
task's `LIM-5, FUN-6` reference; no code was invented.

**Gate-log note.** Worksheet prose matched 27 of 31 numbers. The flags are the
intermediate values 27 and 12 quoted inside Ravi's wrong line in problem 2 (both
are pieces of the trap expression rather than top-level givens) and the bound
labels 1 and 4 naming the two given integrals in problem 4. Study-guide flags are
intermediate values inside worked examples (16, 6, 8). No computed final value is
unbound.
