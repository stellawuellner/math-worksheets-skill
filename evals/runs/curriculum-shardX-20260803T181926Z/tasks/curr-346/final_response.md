# Coordinate rigid transformations (High-school Geometry)

Three PDFs are ready:

- **`ws_transforms_curr346.pdf`** — the student worksheet, 8 problems, 5 pages.
- **`ak_transforms_curr346.pdf`** — the step-by-step answer key, 4 pages.
- **`ss_transforms_curr346.pdf`** — a 2-page study guide.

## What the worksheet does

Every problem puts the **coordinate rule beside the picture**: a labelled grid on the left
with the pre-image already plotted, and the algebra on the right. The student applies the
rule in symbols, then plots the image and checks that the two agree. That pairing is the
whole design — a sign error in the algebra and a miscount on the grid look completely
different, so the student can find their own mistakes without an answer key.

The eight problems ramp from single points to segments to reasoning:

1. Translate $P(-4,1)$ by $(x,y) \rightarrow (x+6,\,y-3)$.
2. Reflect $Q(6,-2)$ over the $y$-axis.
3. Rotate $R(2,7)$ by $90^\circ$ counterclockwise about the origin.
4. Translate the segment $\overline{AB}$ — and confirm with the distance formula that
   $A'B' = AB = 5$.
5. Reflect the segment $\overline{CD}$ over $y = x$ — again with a length check ($5$).
6. Rotate the segment $\overline{EF}$ by $180^\circ$ about the origin — length check ($4$).
7. Find and fix a mistake: Sam reflects $G(-6,3)$ over the $y$-axis and writes
   $(-6,-3)$. Both halves of that error (leaving $x$ alone, negating $y$) are declared
   misconception traps and were machine-checked to be distinguishably wrong.
8. Name the single rigid motion carrying $\triangle JKL$ onto $\triangle J'K'L'$, verify it
   on all three vertices, and justify the congruence *without* measuring three pairs of
   sides.

The three length checks in problems 4–6 are the evidence for problem 8's argument: a rigid
motion preserves distance, so congruence follows from naming the motion. That is the idea
the sheet is built to deliver, rather than a list of six rules to memorise.

## What was verified, and what was not

**Twenty-two machine checks across problems 1–7**, all passing: every image coordinate was
recomputed from the transformation rule, and the three preserved lengths were recomputed
from the image points with the distance formula. Nothing on the answer key was typed from
memory.

**Problem 8 is flagged for manual review** — it asks for a description and a justification,
which no computer algebra system can grade. The answer key names the motion
($90^\circ$ counterclockwise about the origin, $(x,y) \rightarrow (-y,\,x)$), shows all
three vertex checks, gives the congruence argument in full, and sets out a marking guide,
including what to say to a student who answers "translation".

## The study guide

Three sections — translations, reflections, rotations — each with the rules stated
compactly, a worked example whose first step explains *why* the rule applies, and a
distinct try-it with the answer printed upside down inside the box. A closing watch-out box
makes the rigid-motion point explicit. All twelve study-guide values were verified by the
same checker as the worksheet.

Standard covered: HSG-CO.A–HSG-CO.D. Difficulty ramps 1 → 5.
