# Rigid Motions on the Coordinate Plane — 8 problems

Three PDFs are ready:

- **`ws_rigidmotion_curr346.pdf`** — the student worksheet (5 pages), opening with
  a rules table that pairs each motion with its coordinate rule.
- **`ak_rigidmotion_curr346.pdf`** — the full step-by-step answer key.
- **`ss_rigidmotion_curr346.pdf`** — a 2-page skills summary.

## What the worksheet covers

The guiding idea is that a slide, a flip and a turn are all *the same kind of
thing*: a rule on coordinates that never changes a distance. Every stem states the
rule in notation, and two problems come with a printed coordinate grid so the
student can see the motion and the algebra side by side.

1. A translation, plotted on the grid.
2. A reflection in $y = -x$ (swap and negate).
3. A half turn about the origin.
4. A translated segment — find the image point, then measure the segment before
   and after and see the two lengths agree.
5. A reflection in the vertical line $x = 2$, then the distance from the point to
   its image.
6. A quarter turn about $(1, 2)$ — the offset form, not the origin shortcut.
7. A composition (reflection then translation), with a grid, ending in an argument
   about why the length cannot change.
8. The challenge: measure a segment, half-turn it, measure again, and say why the
   agreement was guaranteed.

## What is verified, and what is not

The sheet asks for **23 separate responses** across the 8 problems.

- **21 are machine-checked** with SymPy. Every image coordinate is checked as its
  own value — an $x$-coordinate and a $y$-coordinate are two answers, not one —
  and every length is recomputed with the distance formula from the raw
  coordinates.
- **2 are instructor-judged**: 7(c) and 8(d), the written arguments about why
  rigid motions preserve length. Both are marked `---` in the Quick Answers bank,
  and the key gives a model response and a full / half / no-credit rubric for each.
  The key's own "What is verified" note says 21 of 23.

There are no `[unchecked]` marks.

## The study guide

Opens by defining a rigid motion as a distance-preserving move, then three
sections — translations, reflections, rotations. The reflection section lists all
five rules the sheet uses with a check ("the mirror sits halfway between a point
and its image"); the rotation section gives the offset form for a centre other
than the origin. Each section has a worked example whose first step names the
reason for choosing that rule, and a try-it with the answer upside down inside the
box. The closing watch-out box separates $y = x$ from $y = -x$, the mix-up this
topic produces most.
