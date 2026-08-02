# Parametric, Polar, and Vector-Valued Calculus — AP Calculus BC (curr-495)

Three PDFs are ready:

- **Worksheet** (`ws_parapolar_curr495.pdf`, 5 pages) — 10 problems in
  interleaved-synthesis format. After a three-problem warm-up (parametric slope,
  speed of a moving particle, total distance travelled) the four subskills are
  rotated so the student has to identify what is being asked before setting
  anything up: a slope $\frac{dy/dt}{dx/dt}$, a magnitude $|\mathbf v|$, a polar
  intersection, or an accumulation. Problem 4 finds where a cardioid meets a
  circle and problem 8 reuses those angles as the limits of the area integral,
  so the sheet builds one idea across two problems. It closes with a synthesis
  challenge on distance vs. displacement and a speeding-up/slowing-down
  justification.
- **Answer key** (`ak_parapolar_curr495.pdf`, 3 pages) — a quick-answer bank,
  then a full solution per problem: the set-up, the substitution or identity
  that makes the integral doable, exact value, and the three-decimal form in the
  box. Several solutions carry grading notes on the errors these problems target
  — integrating a rose over $[0,2\pi]$ (four petals, four times the area),
  reversing the limits on the inside/outside area, confusing speed with
  $\frac{dy}{dx}$, and "acceleration is positive so it is speeding up".
- **Study guide** (`ss_parapolar_curr495.pdf`, 2 pages) — four sections
  (parametric slope, vector motion, polar intersections, accumulated
  quantities), each with a formula box, a worked example that states the
  strategy before computing, and a try-it with the answer printed upside down.
  It also flags the two things students most often skip: checking the pole
  separately when intersecting polar curves, and choosing limits that trace the
  region exactly once.

## Verification

9 of the 10 worksheet problems are machine-verified with SymPy: 4
`definite_integral` checks (distance travelled, one rose petal, the
inside-circle/outside-cardioid region, and the arc length — all evaluated
exactly, then compared against the printed three-decimal answers), 1
`solve_interval` for the polar intersection (verified complete on $[0,2\pi)$),
1 `diff` for the product-rule velocity, 1 `eval` for the parametric slope, 1
`approx` for the speed, and 1 `solve` for the horizontal-tangent parameter.

Problem 10 is flagged **manual review**, correctly: it asks for an explanation
of why total distance differs from displacement plus a justification of speeding
up at $t=1$. The answer key gives the model response, both correct set-ups, the
dot-product argument ($\mathbf v(1)\cdot\mathbf a(1) = 4 > 0$), the accepted
alternative argument, and what not to accept.

All 8 study-guide items (4 worked examples + 4 try-its) are machine-verified.

Build note: the first run failed the layout gate — the two-part synthesis
problem gave its parts no work space or answer location of their own. Both parts
now carry their own writing space inside the problem's unbreakable block. The
final build is green on all 21 gates (exit 2 for the single manual item).
