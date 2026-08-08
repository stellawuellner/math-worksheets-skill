# Handling the ambiguous SSA case completely (Precalculus)

Three PDFs are ready.

**Study guide (`ss_ssa_curr428.pdf`, 2 pages)** — four sections, each a rule box,
a worked example whose first step names what is being decided, and a try-it with
the answer upside down inside the box: the height test $h = b\sin A$ and its four
outcomes; the $a \ge b$ case where only one triangle fits and the obtuse partner
can be discarded on sight; the $h < a < b$ case where **two** answers must be
reported; and reporting both cases in a real measurement, where the ambiguity is
a property of the data rather than a mistake.

**Worksheet (`ws_ssa_curr428.pdf`, 8 pages)** — 10 problems, all SSA, with units
stated throughout (cm for the abstract triangles, metres for the applied ones).
The set covers all three outcomes rather than just the interesting one: three
height-test problems (two of which have **no** solution), two one-triangle
problems, two two-triangle problems, and three applied problems — a coastguard
fix, a fence-line survey, and a pair of pole cables. **Every problem carries its
own figure**, generated from the same verified data as the answers: the
two-triangle problems get the two-apex swing figure with both possible positions
drawn, and the height-test problems get the right triangle that defines $h$.
Difficulty ramps 1 to 5.

**Answer key (`ak_ssa_curr428.pdf`, 3 pages)** — worked solutions that run the
height test *first* and say what it decided, then solve; each two-triangle answer
also states why the obtuse partner survives ($A + B_2 < 180^\circ$), and each
one-triangle answer states why it does not. Plus a Quick Answers bank and a
generated Curriculum section (HSG-SRT.D.11).

## What is verified, honestly

The sheet asks for **18 responses across the 10 problems**.

- **14 are machine-checked** by SymPy: every height, every angle, every side.
  The obtuse second solutions are checked as their own explicit computations
  ($180^\circ$ minus the inverse sine), not merely accepted as "the other
  triangle" — which matters, because SymPy's triangle solver will accept either
  branch of an ambiguous case, so a check that only asked "is this a valid
  triangle" would pass an answer that reported the wrong one.
- **4 are instructor-judged** and marked `---` in the Quick Answers bank:
  problems 1(b), 4(b) and 7(b), the "how many triangles, and why" counts, and
  10(c), the physical interpretation of the two cable anchors. These are the
  *reasoning* the sheet exists to teach — a count with no justification is worth
  little — so they are graded by a person against the rubrics printed in the key,
  each of which requires the comparison ($a$ against $h$, and $a$ against $b$) and
  not just the verdict.

That matches the key's own "What is verified" note. Nothing is marked
`[unchecked]`.

One practical note: the sheet runs 8 pages because ten figures plus real working
room need that much. I checked the rendered pages for label collisions and
adjusted the coastguard problem's measurements after the automated overprint
check found the angle label sitting on a side label in the original data.
