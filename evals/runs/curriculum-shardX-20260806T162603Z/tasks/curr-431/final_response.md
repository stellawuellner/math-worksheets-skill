# Converting between rectangular and polar coordinates (Precalculus)

Three PDFs are ready.

**Study guide (`ss_polar_curr431.pdf`, 2 pages)** — four sections, each a rule box,
a worked example whose first step names the decision being made, and a try-it with
the answer upside down inside the box: polar to rectangular (the safe direction,
since the signs of sine and cosine carry the quadrant for you); rectangular to
polar; choosing the angle by quadrant, with the exact rule for when to add
$180^\circ$; and the fact that one point has many polar names, including the
negative-$r$ one.

**Worksheet (`ws_polar_curr431.pdf`, 6 pages)** — 10 problems, opening with a
labelled but **value-free** reference diagram of the right triangle that every
conversion formula is read from, so the model and the notation sit on the same
page. The four subskills interleave after the warm-up. The set deliberately
includes the awkward cases: a negative $r$ (problem 6), a point on an axis where
the $\tan^{-1}$ formula does not apply at all (problem 9), two quadrant
corrections (5 and 8), and a radar context in kilometres for the synthesis
problem. Answers are exact — radicals and fractions — except where decimals are
asked for. Difficulty ramps 1 to 5.

**Answer key (`ak_polar_curr431.pdf`, 3 pages)** — worked solutions that state the
quadrant *before* using the calculator and say what the correction was for, plus a
Quick Answers bank and a generated Curriculum section (HSF-IF.C.7).

## What is verified, honestly

The sheet asks for **24 responses across the 10 problems**.

- **21 are machine-checked** by SymPy: every $r$, every $x$ and $y$, every angle.
  The quadrant-corrected angles are checked as the full corrected expression
  ($180^\circ$ plus the inverse tangent), not as a bare number, so the correction
  itself is what is verified. Problem 9(b) is a genuine round-trip check —
  $7\sin 270^\circ$ must return the given $y = -7$ — rather than a restatement of
  the angle.
- **3 are instructor-judged** and marked `---` in the Quick Answers bank:
  problem 5(c), explaining why the calculator's $-60^\circ$ is wrong and why
  adding $180^\circ$ fixes it; problem 9(c), explaining why the $\tan^{-1}$
  formula cannot be used when $x = 0$; and problem 10(d), explaining why the
  negative-$r$ name locates the same aircraft. These are the reasoning the sheet
  is for, so each carries a rubric in the key — 5(c) requires the
  $180^\circ$-period justification, not just the corrected number.

That matches the key's own "What is verified" note. Nothing is marked
`[unchecked]`.
