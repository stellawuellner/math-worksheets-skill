# Signed Rational Numbers — Diagnosing Subtraction and Negative-Sign Errors

Three PDFs for a sixth- or seventh-grade learner. The whole sheet is built
around one habit ("rewrite every subtraction as an addition of the opposite")
and the three errors that habit prevents.

- **Worksheet** (`ws_signednumbers_curr169.pdf`) — 8 problems. 1–3 evaluate
  subtractions chosen so each canonical sign error lands visibly off the correct
  value, including one with decimal rationals ($-3.5 - 2.25$) so the topic is
  rational numbers and not just integers. 4–5 compare and order signed
  expressions, which is where "subtracting a negative equals adding a positive"
  becomes a statement the student has to commit to rather than a rule they
  recite. 6–8 are find-and-fix items: Dana's $-4 - (-9) = -13$, Marcus's
  $-7 - 4 = -3$, and a three-term challenge where a single dropped double
  negative produces $-12.75$. Each asks the student to *name the rule that was
  broken* before recomputing. Work space is 3.5–5 cm.
- **Answer key** (`ak_signednumbers_curr169.pdf`) — reasoning, not answers. Every
  solution rewrites the subtraction first, then explains the sign of the result
  in number-line terms, and each of the three find-and-fix solutions ends with a
  size check the student can use as a standalone diagnostic ("subtracting a
  negative always makes the result larger, so any answer below $-4$ is wrong
  before the arithmetic is checked"). The generated quick-answer bank sits under
  the title block and prints all six declared traps.
- **Study guide** (`ss_signednumbers_curr169.pdf`) — two pages, three sections
  matching the three worksheet skills (subtract signed numbers · compare two
  signed expressions · find and fix a sign error). Each has a rule box, a
  two-step worked example, and a distinct try-it with the answer upside down.
  The third section's rule box is a diagnostic table: what a too-far-left,
  too-far-right, or correct-size-but-positive answer each tells you about which
  sign was mishandled.

## Verification

All 8 worksheet answers and all 6 study-guide answers are machine-verified with
SymPy — 6 `eval` and 2 `compare` checks on the worksheet (one relation, one
three-value ordering), 4 `eval` + 2 `compare` on the guide. **Nothing is flagged
manual**; every task on this sheet has a single checkable value or relation.

Eight misconception traps are declared and machine-checked as distinguishable
(six on the worksheet, two on the study guide's error-analysis items):

| Problem | Planted wrong result | Error it targets |
|---|---|---|
| 1 | $-11$ | merged the two negatives into $-8 + (-3)$ |
| 2 | $7$ | computed $12 - 5$ to avoid a negative |
| 3 | $-1.25$ | changed the operation without changing the sign |
| 6 | $-13$ | added two negatives instead of subtracting a negative |
| 7 | $-3$ | turned $-7 - 4$ into $-7 + 4$ |
| 8 | $-12.75$ | dropped the double negative |

`bash scripts/build.sh` ends **BUILD PASSED**, all 21 gates green, and both
prose-consistency reports are at 100% (every number printed on either document
traces to a JSON given, an `at` binding, or a declared trap value).

Standard code `7.NS.A.1, 7.NS.A.2` is copied verbatim from
`references/standards-map.md` (the "Integer operations" row), which is exactly
the task's `standard_refs`. Difficulty ramps 1, 2, 2, 2, 3, 3, 3, 4.

## Build notes

No gate failed. The first build passed all 21 gates; the only change afterwards
was declaring the study guide's two planted wrong results ($2$ and $-7.75$) as
traps, which the prose report had correctly flagged as numbers not traceable to
the JSON. That moved the study-guide prose match from 89% to 100% and made the
two error-analysis items machine-checked rather than merely printed.
