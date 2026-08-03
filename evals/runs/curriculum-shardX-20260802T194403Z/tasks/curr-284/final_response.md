# Sign Errors in Parabola Transformations — Algebra 1 error analysis

Three PDFs are ready:

- **Worksheet** — `ws_parabola_curr284.pdf` (4 pages, **8 problems**)
- **Answer key** — `ak_parabola_curr284.pdf` (3 pages, with the quick-answer bank and a
  machine-checked "Common wrong answers" list)
- **Study guide** — `ss_parabola_curr284.pdf` (2 pages, 3 skill sections)

## What the worksheet does

Everything on the sheet turns on one idea, stated in a box at the top: in
$y = a(x-h)^2 + k$ the vertex sits at the $x$ that makes the squared factor **zero**, so
the horizontal shift runs opposite the printed sign, and a negative $a$ reflects the
parabola without moving it.

The eight problems interleave three skills (max same-skill run of 1):

- **vertex-from-form** (1, 3) — locate the vertex and the $x$-intercepts from vertex form.
- **transform-to-equation** (2, 5, 7) — write the equation from a description
  (left/right, reflection, stretch), then test your own equation by substituting at a
  point where a flipped sign gives a visibly different number.
- **find-and-fix** (4, 6, 8) — diagnose a planted sign error.

Three find-and-fix items, exceeding the two requested: Jamal reports a maximum of $-137$
for $y = -(x-6)^2 + 7$ because he used $x = -6$; Mia calls $(x + 7)$ a shift right and
reports a minimum of 191; and problem 8 is an open study-card audit — three sign rules,
exactly one correct, each to be labelled, explained and rewritten.

Difficulty ramps 1, 2, 2, 3, 3, 3, 4, 5.

## Verification and traps

- **7 of 8 problems machine-verified** — vertex values as `eval` at the true vertex,
  $x$-intercepts as `zeros`.
- **Five misconception traps are declared and machine-checked**, on every problem whose
  answer is a single comparable value and whose design plants a specific misreading:
  **102** (read $x-5$ as vertex $-5$), **61** (wrote $(x-4)^2$ for a left shift),
  **$-137$** (substituted $x = -6$, taking the printed sign literally),
  **24** (dropped the reflection), **191** (read $x+7$ as right 7). The verifier proved
  each planted value is one the problem's own check rejects, and they print in the key's
  "Common wrong answers" block so the grader sees *which* misreading produced each wrong
  number. Two further traps (254, $-320$) are declared on the study guide's find-and-fix
  example and try-it. (`zeros` problems 3 and 7 and the `manual` problem 8 take no traps:
  the trap field is only allowed on single-comparable-answer types.)
- **1 problem flagged manual** — problem 8 is written reasoning about three rules, so it is
  declared `{"type": "manual"}`. The key supplies a model answer for each rule plus an
  explicit full-credit standard. Build result: **BUILD PASSED — 1 verification run flagged
  manual-review items (exit 2)**, which is the correct outcome for an open-response item.

Standards are taken verbatim from `references/standards-map.md`: `HSA-SSE.B.3` on the
vertex-form and transformation problems, `HSA-APR.B.3` on the two $x$-intercept problems.

## Study guide

Three sections matching the three worksheet skills. Section 3 gives a three-check audit
routine for someone else's work — the thing this worksheet actually asks for — and its
worked example and try-it are themselves find-and-fix items with declared, verified traps.
The watch-out box names why these errors survive: a wrong $h$ still produces a real point
on the parabola, just not the vertex.

## Gate chain

Green on the first attempt. The answer key `\input`s the generated quick-answer bank
directly under `\aktitleblock` with **no `\raggedright` and no `\emergencystretch`** — the
previous artifact wrapped that `\input` in `{\raggedright ... \par}` to survive the
`\commonerror` overflow; that workaround is gone. All five `\commonerror` lines set and the
key compiles clean at 3 pages with no overfull box, so the fix holds with the largest trap
block on this sheet.

One heuristic note, not a gate failure: `check_prose_consistency.py` reports the negative
trap values ($-137$ on the worksheet, $-320$ in the study guide) as "missing from JSON"
prose numbers even though both are declared trap `value`s. Positive trap values are matched
correctly, so the sign appears to be dropped when trap values are folded into the givens
set. Everything still passes; flagging it only because trap values are documented as
counting as JSON givens for that checker.
