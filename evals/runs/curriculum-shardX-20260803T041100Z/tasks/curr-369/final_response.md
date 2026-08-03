# Rational Functions — Canceled-Factor Holes vs Vertical Asymptotes

Three PDFs for an Algebra 2 student. Every problem turns on the same decision:
a denominator zero is a break in the domain either way, and only the factoring
tells you which kind.

- **Worksheet** (`ws_rationalfunctions_curr369.pdf`) — 8 problems built as a
  chain. 1–4 take one function, $f(x) = \frac{x^2-9}{x^2+x-12}$, all the way
  through: factor without cancelling, reduce and name the restriction that
  reducing destroys, find the *height* of the hole, then solve for the surviving
  factor's asymptote. 5–6 are find-and-fix items — Nina calls both denominator
  zeros asymptotes, Ray sees one matching factor in a perfect-square denominator
  and calls it a hole — so the sheet covers both directions of the confusion
  rather than only one. 7 puts a hole and an asymptote in the same function and
  asks which factor produced each. 8 is an open explanation with `\noansline`
  (the paragraph is the answer). Work space is 4–5.5 cm; the page budget puts the
  sheet at 3 pages.
- **Answer key** (`ak_rationalfunctions_curr369.pdf`) — reasoning throughout.
  Each solution factors before deciding, and the find-and-fix solutions name the
  mishandled *factor* (not just the wrong number) and state the rule that would
  have caught it ("a factor produces a hole only when it cancels completely;
  compare multiplicities, do not just look for a match"). Problem 8 carries a
  full model answer with a table-of-nearby-values contrast and explicit reviewer
  criteria. The generated quick-answer bank under the title block prints the
  three declared traps.
- **Study guide** (`ss_rationalfunctions_curr369.pdf`) — two pages, three
  sections matching the three worksheet skills (factor and reduce · locate holes
  and vertical asymptotes · tell a hole from an asymptote). Each has a rule box,
  a two-step worked example, and a distinct try-it with the answer upside down.
  The third section's rule box is the multiplicity comparison written as two
  side-by-side templates, which is the part students most often skip.

## Verification

11 machine checks cover 7 of the 8 problems: 3 `factor`, 4 `equiv`, 3 `solve`,
3 `limit` (multi-part problems 1, 5, 6 and 7 each carry two entries under one
id, with identical difficulty per the multi-part encoding). All 6 study-guide
answers are verified (4 `equiv`, 2 `limit`).

**Problem 8 is `manual` by construction** — it is an "explain why" task, so it is
declared `{"type": "manual", "desc": ...}` with the reviewer's criteria in the
`desc` (must contrast a limit that exists with one that grows without bound;
must not claim the function is defined at the hole). The build correctly ends at
exit 2 with one manual-review item.

Three misconception traps are declared and machine-checked as distinguishable
(one more on the study guide):

| Problem | Planted wrong result | Error it targets |
|---|---|---|
| 3 | $0$ | original numerator over reduced denominator |
| 5 | $10$ | stopped at the reduced numerator, never divided |
| 7 | $-5$ | same error, where it also flips the sign |

`bash scripts/build.sh` ends **BUILD PASSED** with exit 2 (manual-review item),
all 21 gates green. Study-guide prose consistency is 100%; the worksheet is at
92%, the two flagged numbers being the $9$ and $12$ of the function printed in
problem 4's stem, whose own check is the surviving factor $x + 4$ rather than the
whole quotient.

## Standards note

The task's `standard_refs` is `HSA-APR.D / HSF-IF.C`. **`references/standards-map.md`
has no `HSA-APR.D` row** (its HSA-APR rows are A.1, B.3 and C.5), so no code was
invented for it. Every problem is tagged `HSF-IF.A–HSF-IF.C`, copied verbatim
from the "Function behaviour, notation, graphs" row, which is the half of the
task's reference the map does carry and which covers rational-function behaviour
and graphs. Difficulty ramps 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4 across the
entries (1, 2, 2, 2, 3, 3, 4, 4 by problem).

## Build notes

No gate failed. The build was green on the first attempt.
