# Identities, Multiple Angles, and Exact Solutions — Precalculus

Three PDFs, all gated green:

- **Worksheet** (`ws_trigidentities_curr425.pdf`, 7 pages) — 12 problems mixing
  three jobs that look alike on the page: simplify/verify (no equation to
  solve), convert a multiple angle, and produce a complete exact solution set on
  $[0, 2\pi)$. The directions make the discrimination explicit, and consecutive
  problems never call for the same first move.
- **Answer key** (`ak_trigidentities_curr425.pdf`, 3 pages) — every solution
  opens by naming *which identity and why that one*, which is the real content
  here (e.g. problem 8's key explains that $\cos 2x = 2\cos^2 x - 1$ is chosen
  precisely because it makes $1 + \cos 2x$ collapse; problem 10's warns against
  dividing by $\sin x$ and losing two roots). A generated "Common wrong answers"
  bank carries the declared traps.
- **Study guide** (`ss_trigidentities_curr425.pdf`, 2 pages) — three sections:
  the basic identities with an order-of-moves rule, the double-angle formulas
  with explicit guidance on *choosing among the three cosine forms*, and the
  four-step routine for a complete exact solution set. Each has a worked example
  and a distinct try-it with the answer upside down.

## What the sheet actually exercises

| Facet | Problems |
|---|---|
| `simplify-with-identities` | 1, 2, 6, 9 |
| `multiple-angle-formulas` | 3, 5, 8, 11 |
| `exact-solution-sets` | 4, 7, 10, 12 |

Max same-facet run = 1 — fully interleaved. Difficulty ramp
`1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5`. Problem 12 is the synthesis and needs all
three moves in sequence: a Pythagorean substitution to reach one function, a
factorisation, then a complete sweep of the interval.

## Verification

- **12 of 12 worksheet problems machine-verified — 0 manual.** Six `equiv`
  (identity simplifications, checked as function equality, not string matching),
  two `eval` (double-angle values from a given ratio, exact fractions), and four
  `solve_interval` on $[0, 2\pi)$ — where SymPy checks *completeness* of the
  root list, not merely that the listed roots are roots. All three verification
  targets named by the task are used.
- **6 of 6 study-guide boxes machine-verified** (3 worked examples + 3 try-its).
- Two misconception traps declared and machine-checked: $\sin 2\theta$ read as
  $2\sin\theta$ (gives $1.2$, outside the range of sine) and $\cos 2\theta$ read
  as $2\cos\theta$ (gives $-0.77$ against the correct $-119/169$).
- Every `solve_interval` expression is stated in **factored** form in the JSON,
  which is what lets the verifier confirm the solution set is complete rather
  than returning MANUAL on an expanded trig quadratic. The worksheet still
  presents the unfactored equation; the key does the factoring.
- Worksheet prose–JSON binding is 25/25 (100%).
- Standards: `HSF-TF.C.8` on the eleven identity/multiple-angle/equation
  problems and `HSF-TF.A.2, HSF-TF.B.5` on problem 4 (a plain unit-circle
  equation needing no identity), both verbatim from
  `references/standards-map.md`.

Nothing here is genuinely open-ended, so nothing is flagged for manual review.

**First-attempt gate failure (one):** `compile-ws` — the sheet ran 7 pages
against a computed 6-page budget. The correct fix was *not* to shrink the work
space: these are multi-line algebraic manipulations and each problem block runs
7–9.5 cm. Instead I declared `workspace_cm` per problem so the page budget
charges for the room the problems actually need; the budget rose to 7 pages and
the sheet passed unchanged. Worth noting for the skill: the default budget for
`equiv` (5 cm) and the displayed-equation stems it does not charge for are what
made a correctly-sized identity sheet look over budget.
