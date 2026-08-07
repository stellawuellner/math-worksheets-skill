# Solving SAS and SSS triangles with the law of cosines (Precalculus)

Three PDFs are ready.

**Study guide (`ss_lawcos_curr427.pdf`, 2 pages)** — four sections, each a rule
box, a worked example whose first step explains *why* the law of sines cannot
start the problem, and a try-it with the answer upside down inside the box: SAS
for the third side, SSS rearranged for an angle (with the read-the-sign habit),
the two-step SAS-then-angle route, and applied distance-and-turn problems.

**Worksheet (`ws_lawcos_curr427.pdf`, 7 pages)** — 12 problems on a clean ramp
from a single SAS substitution to a two-step obtuse-angle application, and no two
share a skeleton: SAS third side, SSS angle, SAS with a different vertex
labelled, SSS solving for a different angle, SAS-then-law-of-sines, and three
applied problems in metres (two paths from a car park, three survey markers, two
drone flight lines). **Every problem carries its own to-scale triangle**,
generated from the same verified data the answer key uses, so the picture cannot
disagree with the answer.

**Answer key (`ak_lawcos_curr427.pdf`, 4 pages)** — worked solutions that name
which arrangement (SAS or SSS) is in play and why, with a sanity check attached
to several (the largest angle faces the longest side; an obtuse included angle
must make the third side longer than either leg). Two problems print a "common
wrong answer" line. Plus a Quick Answers bank and a generated Curriculum section
(HSG-SRT.D.10, HSG-SRT.D.11).

## What is verified, honestly

The sheet asks for **14 responses across the 12 problems**.

- **12 are machine-checked** by SymPy — one per problem. Each is verified by
  solving the whole triangle from its three given values rather than re-running
  the formula I wrote, so a mis-assigned side or a wrong included angle would
  fail the check. The same `given` data drives the printed figures.
- **2 are instructor-judged** and marked `---` in the Quick Answers bank:
  problem 9(b), explaining what the negative cosine revealed before the inverse
  cosine was taken, and problem 12(b), explaining why the law of sines could not
  be the first step. Both are conceptual prose. The key prints a rubric for each;
  12(b) requires the *missing matched pair* reason, not merely naming the law of
  cosines.

That matches the key's own "What is verified" note. Nothing is marked
`[unchecked]`.

Two declared misconception traps were recomputed and confirmed distinguishable:
problem 1's (dropping the $-2ab\cos C$ term, i.e. treating the triangle as
right-angled) and problem 12's (using the $48^\circ$ reference angle instead of
the obtuse $132^\circ$, which flips the sign of the middle term).
