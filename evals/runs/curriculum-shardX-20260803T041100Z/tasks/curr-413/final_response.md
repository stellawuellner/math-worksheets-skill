# Fitting and Interpreting Exponential Models — Precalculus

Three PDFs are ready:

- **Worksheet** (`ws_expmodels_curr413.pdf`, 5 pages) — 10 problems on real models:
  a streaming service's subscriber count, a bacteria culture, a drug level in the
  bloodstream, algae coverage measured on two dates, a town's population, and a
  decaying chemical sample. A header box states the whole toolkit ($a$ is the value
  at $t=0$, $b$ is the per-step multiplier, $b = 1 \pm r$, divide two equations to
  cancel $a$, take logs to free $t$, $b^t = e^{(\ln b)t}$). Every problem states its
  units, its time origin and the rounding it wants. 5.5–6.5 cm of work space per
  single-part problem, 4–4.5 cm per part elsewhere.
- **Answer key** (`ak_expmodels_curr413.pdf`, 2 pages) — quick-answer bank, then
  each solution worked in full: the equation set up from the data, the division or
  logarithm step, the arithmetic with intermediate values shown, the rounded answer,
  and a substitution check where one exists.
- **Study guide** (`ss_expmodels_curr413.pdf`, 2 pages) — four sections matching the
  four facets: fitting $a$ and $b$ from two points, interpreting $a$ and $b$,
  solving for time with logarithms, and rewriting the base (to $e$, and to a new
  time step). Each has a formula box, a two-step worked example, and a try-it.

## Design

Facets declared and tagged on every check: `fit-from-two-points`,
`interpret-parameters`, `solve-for-time`, `rewrite-base`, interleaved with a maximum
same-facet run of 2. Difficulty ramps 1 → 5, ending with a two-part problem that
fits a decay model from two measurements and then solves for the time at which it
crosses a threshold.

Problems 1–4 and 7–8 deliberately revisit the *same two models* from different
angles (state the rate, solve for time, convert the base to $e$, convert the rate to
monthly), which is the interpretation work the focus asks for rather than repeated
algebra on fresh numbers.

Problem 9 is error analysis: a student reads $P(t) = 500(1.08)^t$ as "gains 8 people
a year". The student computes the year 0→1 increase (40 people) and the year 5→6
increase (58.77 people); the two answers make the misconception impossible to hold.
The wrong answer 8 is **declared as a machine-checked trap**, so the verifier proved
the problem distinguishes it, and the key prints it in the common-wrong-answers
block.

## Verification

**17 SymPy checks over 10 problems — 17 verified, 0 manual.** Fits are verified by
`solve` on the actual model equation (`240·b³ = 810` → `b = 1.5`, real domain);
interpretations by `eval` (`b − 1`, `1 − b`); times by `solve` on the exponential
equation itself where it is exact (`240(1.5)^t = 1215` → `t = 4`) and by `approx` on
the log expression where the answer is a rounded decimal; base changes by `equiv`,
which proves `1.5^t` and `e^{t\ln 1.5}` are the *same function* rather than trusting
a stated $k$. The one answer carrying a measurement unit (10.75 hours) declares
`"answer_unit": "hours"`, gate-bound to the sheet's `\answerline` and the key's box.

Nothing on this sheet is open-ended, so nothing is flagged for manual review.

Standard `HSF-LE.A.4, HSF-BF.B.5` (exponentials and logs) on every problem, taken
verbatim from `references/standards-map.md`.

Gate verdict: **BUILD PASSED — all gates green**.
