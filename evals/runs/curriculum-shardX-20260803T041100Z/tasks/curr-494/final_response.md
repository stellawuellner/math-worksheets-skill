Three PDFs are ready for an AP Calculus BC student on parametric, polar and
vector-valued calculus, focused on diagnosing parameter, polar-bound and
speed-versus-velocity errors.

- **Worksheet** (8 problems, `ws_parapolar_curr494.pdf`, 5 pages) — seven of the
  eight problems are find-and-fix items, and every planted solution is
  arithmetically clean and conceptually wrong, which is the point. Parameter
  errors: Ana computes (dx/dt)/(dy/dt) and gets −4 instead of −1/4; Elle
  substitutes t = 2 "because x = 2" on a curve where the point (2, −2) is reached
  at t = 1, and her 2.25 is the slope at a completely different place on the same
  curve. Polar bounds: Cal integrates ½r² from 0 to 2π on the three-petal rose
  r = 4cos 3θ and reports 25.13, six petal-areas; Ravi solves cos θ = +½ instead
  of −½ for the limaçon's pole crossings. Speed vs velocity: Bo adds x'(2) and
  y'(2) to get 13 where the magnitude is 12.04; Dev integrates the two components
  separately for a total distance; Nia reports a *negative* speed of −1.87, which
  is refutable before any arithmetic. Problem 8 is an open explanation
  distinguishing velocity, speed and dy/dx. Work space runs 5–7 cm.
- **Answer key** (`ak_parapolar_curr494.pdf`) — three to five numbered steps per
  problem, each opening by naming the error, then the corrected work, then the
  boxed answer, then an independent check. Several checks are the diagnostic
  habits themselves: the magnitude of a vector lies between its largest component
  and the sum of its components (which places Bo's 13 exactly at the unreachable
  upper bound), substituting a claimed root back into r, and the observation that
  Elle's parameter lands on the point (5, 2). It carries the generated
  quick-answer bank and the generated "Common wrong answers" block (−4, 13,
  25.13, 1.667, 2.25, −1.87), plus a full model answer and a full-credit checklist
  for the open item.
- **Study guide** (2 pages, `ss_parapolar_curr494.pdf`) — three skills matching
  the worksheet tags: the parameter is not a coordinate, speed is a magnitude
  rather than a sum, and polar limits come from solving r = 0. Each has a rule
  box, a two-step worked example and an upside-down try-it, plus a watch-out box
  reducing all three errors to one question each.

**Verification.** 7 of the 8 worksheet problems are machine-checked with SymPy —
two `eval` slope computations, two `approx` speeds, two `definite_integral`
evaluations (the petal area over its true limits, and the arc-length integral for
total distance), and a `solve_interval` for the pole crossings in exact radian
form. Problem 5 carries *two* entries under one id so both halves of the fix are
verified: the parameter values with x(t) = 2, and the slope at the correct one.
All 6 study-guide results are machine-checked. Problem 8 is a genuinely open
explanation and is declared `{"type": "manual"}`; the build correctly exits 2 with
one manual-review item and it is nowhere described as machine-verified.

Six planted wrong results are declared misconception traps; the verifier proved
each distinguishably wrong and derived from its stated wrong method.

**Standards — read this one.** `references/standards-map.md` has no row for
parametric or polar calculus. Rather than invent a code, the six derivative,
slope and speed problems are tagged `FUN-3.A–FUN-3.C` ("Derivative rules & chain
rule") and the three integral/bound problems `LIM-5, FUN-6` ("Riemann sums &
FTC"), both copied verbatim from that file. Those are exactly the two AP CED units
the task's own `FUN-3 / FUN-6` reference names, and the mathematics genuinely sits
in them — but a reader should know the map has no parametric/polar-specific row,
and adding one (CED unit 9, `CHA-3.G` / `CHA-5.D`) would be the honest fix. That
file is outside this task's write scope.

**Gate-log note.** Worksheet prose matches 29 of 32 numbers. The flags are Cal's
lower limit `0` in problem 3 (a planted wrong bound, deliberately not a JSON
given) and the `1` and `2` inside problem 8's ½r² reference, which is prose about
a formula with no computation attached. The study guide's flags are the
intermediate √13 and the ±π/4 limits written inside worked examples. No computed
value or figure label is unbound.
