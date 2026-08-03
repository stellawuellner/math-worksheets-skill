Three PDFs are ready for an Algebra 1 student on solving quadratic equations,
focused on diagnosing incomplete root sets and quadratic-formula sign errors.

- **Worksheet** (8 problems, `ws_quadroots_curr294.pdf`, 4 pages) — seven of the
  eight problems present someone else's work and ask the student to name the
  mistake in words before fixing it, which is the skill the focus names. The two
  headline find-and-fix items are problem 3 (Rio substitutes c = 6 instead of
  c = −6 and reports a discriminant of −23, concluding "no real solutions" about
  an equation that factors) and problem 4 (Mia reasons that "b is already
  negative" so the numerator opens with −4, landing on 0.58 instead of
  1 + √10⁄2). Around them: Toby stops at the principal square root of 49; Jae
  divides x² = 3x by x and deletes the root x = 0; Sam takes only the positive
  branch of (x − 3)² = 25 and loses x = −2; Kai reads roots straight out of
  (2x + 3)(x − 4) with the printed signs; and problem 7 attacks the opposite
  error — a student who *invents* a second root for the perfect square
  4x² − 12x + 9, where the discriminant is 0. Problem 8 is an open explanation of
  why ± is not optional. Work space runs 5–7 cm.
- **Answer key** (`ak_quadroots_curr294.pdf`) — three to five numbered steps per
  problem. Each solution first names the fault in plain words ("Jae divided away
  the very solution x = 0"), then shows the corrected work, then boxes the
  complete solution set, and several close with an independent check (substitution
  or a second method — problem 5 is redone by expanding and factoring, problem 7
  by recognising (2x − 3)²). It carries the generated quick-answer bank and the
  generated "Common wrong answers" block (−23, 0.58, 288), plus a full model
  answer and a full-credit checklist for the open item.
- **Study guide** (2 pages, `ss_quadroots_curr294.pdf`) — three skills matching
  the worksheet tags: every square root gets a ±, substitute signs rather than
  digits into the formula, and read a factored equation correctly (opposite sign,
  and a coefficient means two moves). Each has a rule box, a two-step worked
  example and an upside-down try-it, plus a watch-out box making the point that a
  one-root answer is a claim requiring a zero discriminant, not a default.

**Verification.** 7 of the 8 worksheet problems are machine-checked with SymPy —
four `solve` root sets (including the two-element sets a student most often
truncates), two `eval` discriminant/formula computations, and problem 7 carries
*two* entries under one id so both its discriminant (0) and its double root (3/2)
are verified rather than only one of them. All 6 study-guide results are
machine-checked. Problem 8 is a genuinely open explanation and is declared
`{"type": "manual"}`; the build correctly exits 2 with one manual-review item and
the problem is nowhere described as machine-verified.

Three planted wrong results are declared misconception traps (−23, 0.58, 288) and
the verifier proved each distinguishably wrong and derived from its stated wrong
method. Note a real constraint here: `verify.py` allows `traps` only on types with
a single comparable answer, so the four `solve` problems — whose misconception is
a *missing* root rather than a wrong number — cannot carry one. Their planted
wrong answers are instead bound as prose numbers drawn from the JSON `expected`
set, and the key names each error explicitly.

**Standards.** Every problem is tagged `HSA-REI.B.4`, taken verbatim from
`references/standards-map.md` ("Quadratics: solve"), which is also the code the
task names.

**Gate-log note.** The only unmatched prose number in either document is `0` — the
right-hand side of every "… = 0" equation, which the JSON stores as an expression
rather than an equation. Worksheet prose matches 28 of 31 numbers; no computed
value or figure label is unbound.
