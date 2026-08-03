# Derivative Applications — Diagnosing Related-Rates and Optimization Setup Errors

Three PDFs for an AP Calculus AB/BC student. The sheet is about the *setup*
rather than the differentiation: every problem targets one of four setup errors
named in the directions block (substituting too early, leaving a second variable
in, inverting a ratio, writing the wrong constraint).

- **Worksheet** (`ws_relatedrates_curr469.pdf`) — 8 problems, 4 pages.
  1–2 are the setup steps in isolation: differentiate $A = \pi r^2$ to get the
  factor the chain rule will attach to $dr/dt$, then eliminate a second variable
  ($h = 2r$) *before* differentiating. 3–4 are full related-rates problems whose
  numbers were chosen so the canonical error lands visibly off (balloon: $1.59$
  vs $0.318$; ladder with the inverted ratio: $-2.67$ vs $-1.500$). 5–6 are
  find-and-fix items — a student holds the conical tank's radius fixed at the rim
  value, and a student writes the closed-rectangle perimeter $2x + 2y = 200$ for
  a pen that only needs three sides. 7 is an optimization problem that ends in a
  rejected critical value, which is a domain-statement (setup) failure rather
  than a calculus one. 8 is an open explanation with `\noansline`. Work space is
  4–6 cm.
- **Answer key** (`ak_relatedrates_curr469.pdf`) — full reasoning, and every
  solution follows the same visible order: relate, eliminate, differentiate,
  *then* substitute. Each find-and-fix solution says what the wrong step
  *assumes* about the physical situation ("that the water's surface keeps the
  radius of the tank's rim as the level falls") and gives the direction of the
  resulting error, so the wrong answer is diagnostic rather than just wrong. The
  generated quick-answer bank under the title block prints all three declared
  traps.
- **Study guide** (`ss_relatedrates_curr469.pdf`) — two pages, three sections
  matching the three worksheet skills (differentiate the relation · set up a
  related-rates equation · set up an optimization problem). Each has a rule box,
  a two-step worked example, and a distinct try-it with the answer upside down.
  The first rule box states the setup order as a four-step pipeline, which is the
  single thing this topic most needs a student to internalise.

## Verification

9 machine checks cover 7 of the 8 problems: 4 `diff`, 3 `approx`, 2 `solve`
(problems 6 and 7 each carry a `diff` and a `solve` entry under one id, with
identical difficulty per the multi-part encoding). All 6 study-guide answers are
verified (2 `diff`, 2 `approx`, 2 `solve`).

**Problem 8 is `manual` by construction** — an "explain what went wrong" task
with no computable answer, declared `{"type": "manual", "desc": ...}` with
reviewer criteria (must separate varying quantities from genuine constants; must
state that substitution is legal only after differentiating). The build correctly
ends at exit 2 with one manual-review item.

Three misconception traps are declared and machine-checked as distinguishable
(one more on the study guide):

| Problem | Planted wrong result | Error it targets |
|---|---|---|
| 3 | $1.59$ | divided by $4\pi r$ instead of $4\pi r^2$ |
| 4 | $-2.67$ | inverted the ratio, $y/x$ instead of $x/y$ |
| 5 | $-1.27$ | held the radius fixed instead of substituting $r = h/2$ |

Both widened tolerances are inside the cap: `tol` of $0.001$ on values of
magnitude $0.318$ and $0.955$ is well under 1% of the expected value, so no
`tol_reason` was needed.

`bash scripts/build.sh` ends **BUILD PASSED** with exit 2 (manual-review item),
all 21 gates green. Worksheet prose consistency is 94%.

Standards codes are copied verbatim from `references/standards-map.md`:
`CHA-3.D` (Related rates) on problems 1–5 and `FUN-4.B–FUN-4.C` (Optimization)
on problems 6–8, which is exactly the task's `standard_refs`. Difficulty ramps
1, 2, 2, 3, 3, 3, 4, 4.

## Build notes

One gate failed on the first attempt: `answer-key-ss`. The study guide's first
worked example had verified `expected` of `"pi*h**2/9"`, and the binder's number
normaliser read the trailing `2/9` as the fraction $0.2222$ — a value the printed
box `\dfrac{\pi h^2}{9}` naturally does not contain, so the box read as
transcription drift. The fix was to re-parameterize that example (and its try-it)
so the derivative carries an integer coefficient — $2\pi r^3 \to 6\pi r^2$ and
$\tfrac{4}{3}\pi r^3 \to 4\pi r^2$ — which removes the ambiguous `**n/m`
substring entirely. **Worth recording for later agents: an `expected` string
ending in `**k/m` (a power immediately followed by a division) is read as a
fraction by the answer-key binder. Write such a coefficient as a leading factor,
not a trailing divisor.** Everything else was green first time.
