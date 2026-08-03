# Riemann Sums, Accumulation, and the Fundamental Theorem — AP Calculus AB/BC

Three PDFs are ready: the student worksheet, a full step-by-step answer key, and
a two-page skills summary.

## What the worksheet contains

10 problems on **connecting Riemann sums, accumulation, and FTC conclusions**,
in an interleaved-synthesis format. The sheet is built as one chain — a Riemann
sum estimates accumulated change, its limit is the definite integral, FTC 2
evaluates that integral from an antiderivative, and FTC 1 differentiates an
accumulation function — and the four facets rotate so the student has to
classify the question before choosing a tool:

| Facet | Problems | What it asks |
| --- | --- | --- |
| `antiderivative-form` | 1, 6 | general antiderivatives, power and trigonometric |
| `riemann-sum-estimate` | 2, 5, 9 | left sum and trapezoidal sum from a velocity table; right sum from a function |
| `ftc-definite-integral` | 3, 7, 10 | evaluate with $F(b)-F(a)$, including a negative (signed-area) result |
| `accumulation-function` | 4, 8, 10 | $F(x)=\int_a^x f(t)\,dt$: values, $F'$ by FTC 1, and initial-condition modelling |

Problems 2 and 5 share one velocity table (reprinted in full inside each
problem, so no reader can attach it to the wrong stem) and contrast a left sum
with a trapezoidal sum on identical data. Problem 7 lands on $-4$ deliberately,
so the key can distinguish signed area from geometric area. Problem 8 asks for
$g(4)$ and then $g'(3)$ *without integrating* — the FTC 1 conclusion. Problem 10
is the synthesis challenge: a rate $r(t)=4t+3$ with a 10-gallon initial amount,
where the integral gives 90 and the tank holds 100.

Difficulty ramps 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5 across the 14 verify
entries. Every problem is tagged `LIM-5, FUN-6`, taken verbatim from
`references/standards-map.md` — which is also the task's own `standard_refs`
string.

## What was verified, and what is flagged manual

**12 of the 14 verify entries are machine-verified; 2 are flagged
manual-review.** The build exits 2 for exactly that reason, which is the correct
outcome rather than a fault:

- **9(c)** — justify *why* a right Riemann sum overestimates for an increasing
  function, with an argument that works for any increasing function rather than
  a comparison of two numbers. This is a justification, not a computation, so it
  is `{"type": "manual"}`. The key supplies a model argument for the grader.
- **10(c)** — explain from the Fundamental Theorem why $\int_0^6 r(t)\,dt$ gives
  the *change* rather than the amount, and why the initial 10 gallons is added
  separately. Also `{"type": "manual"}`, with a model explanation in the key.

Everything computational is checked: `integrate` checks differentiate the
antiderivative back to the integrand, `definite_integral` recomputes each exact
value, and the Riemann sums are `eval` checks whose `at` bindings are the table
readings printed on the sheet, so the figures and the arithmetic share one
source.

Four misconception traps are declared and machine-checked, and each prints in
the answer key's "Common wrong answers" bank:

- P2 — right endpoints in place of left (100 instead of 80)
- P5 — trapezoid without doubling the interior readings (55 instead of 90)
- P7 — $F(0)-F(2)$ instead of $F(2)-F(0)$ (+4 instead of $-4$)
- P9 — left endpoints in place of right (3.75 instead of 5.75)

The study guide's 8 boxes (4 worked examples + 4 try-its) are all
machine-verified.

## Study guide

Two pages, one section per worksheet skill: Riemann sums as estimates (with the
increasing/decreasing over- and under-estimate rule stated as a rule, since the
worksheet asks the student to justify it), antiderivatives, FTC 2 evaluation,
and accumulation functions with FTC 1 and the $A(t)=A(0)+\int_0^t r$ modelling
form. Each section has a rule box, a worked example opening with a strategy
step, and a distinct try-it.

## Notes

- **One gate failed on the first attempt:** `compile-ss` — the study guide ran 3
  pages against its hard 2-page cap. Fixed per SKILL.md's stated priority order:
  the watch-out box was cut first, and two formula boxes were tightened from
  displayed to inline math. No try-it and no worked example was touched.
- The prose-consistency report leaves a few soft flags on intermediate values
  inside worked examples (e.g. the partial sum 20 before multiplying by
  $\Delta x$). Those are subexpressions of the entry's own computation, the
  documented false-flag case.
