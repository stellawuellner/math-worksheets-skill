# Radical Equations and Extraneous Roots — Algebra 2

Three PDFs are ready:

- **Worksheet** (`ws_radeq_curr373.pdf`, 5 pages) — 10 problems, every one on
  solving a radical equation and testing the candidates it produces.
- **Answer key** (`ak_radeq_curr373.pdf`, 3 pages) — quick-answer bank, a
  "Common wrong answers" block, then a worked solution per problem that shows the
  isolate–square–check sequence, including the check that rejects a candidate.
- **Study guide** (`ss_radeq_curr373.pdf`, 2 pages) — three sections: isolate the
  radical and undo it; why every candidate must be tested; and solving a radical
  model for its input. Each has a rule, a worked example, and a try-it.

## Representations and applications

Three problems are real models with their units stated explicitly: fall time from
a bridge ($t = 0.45\sqrt{d}$ seconds, $d$ in metres), a skid-mark speed estimate
($s = \sqrt{21d}$ mph, $d$ in feet), and the horizon distance from a lookout
($D = 3.57\sqrt{h}$ km, $h$ in metres). No story detail that is not used by the
mathematics. The answer blanks on those problems carry the unit, and the key's
boxed answers carry it too — a gate binds the two, so a metres answer cannot ship
labelled in feet.

Three problems (3, 6, 9) are built around candidates that survive squaring but
fail the original equation. Each planted wrong answer set is declared as a
**machine-checked misconception trap**, so the verifier confirms the problem can
actually distinguish "kept the extraneous root" from the correct answer.

## Verification — the honest split

**16 verified responses across the 10 problems**:

- **15 are machine-checked** with SymPy — every solution set (SymPy solves the
  radical equation directly, so an extraneous root would show up as a
  disagreement), every model solve, the rounded horizon distance, and every
  substitution check.
- **1 is instructor-judged**, marked `---` in the quick-answer bank: **6(c)**,
  where the student has to say *why* the candidate $x = 2$ must be rejected. That
  is a written explanation; the key prints what a correct response must contain
  rather than claiming it was verified.

The key's "What is verified" note reports the same: 15 of 16, with problem 6
carrying the instructor-judged part. No `[unchecked]` marks.
