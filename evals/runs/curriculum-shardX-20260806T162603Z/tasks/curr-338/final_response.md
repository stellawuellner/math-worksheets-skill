# Circle Equations in Context — 8 problems

Three PDFs are ready:

- **`ws_circleeq_curr338.pdf`** — the student worksheet (4 pages).
- **`ak_circleeq_curr338.pdf`** — the full step-by-step answer key.
- **`ss_circleeq_curr338.pdf`** — a 2-page skills summary.

## What the worksheet covers

Every problem is a real site plan with its units stated in the stem — a splash
pad, a cell tower, a garden bed, a drone no-fly zone, a lighthouse, a running
track, a flood-warning zone, a reservoir — and nothing in a stem is decoration.
The three skills are interleaved rather than blocked:

- **Writing** a circle equation (problems 1, 3, 6, 8): from a centre and a point
  on the edge, from the endpoints of a diameter, from a tangent line, and from a
  diameter plus a scale-up.
- **Reading** one (problems 2, 5): pulling out the radius, and substituting a
  point to decide inside / on / outside.
- **Completing the square** (problems 4, 7) to recover a hidden centre and
  radius.

The ramp runs from a one-step translation to a final problem that chains a
midpoint, a distance, a scale factor and an equation.

## What is verified, and what is not

The sheet asks for **20 separate responses** across the 8 problems.

- **19 are machine-checked.** Every radius, every substituted value, every
  midpoint and distance, and both completed-square rewrites were recomputed with
  SymPy. The rewrites are checked as algebraic identities, so a rearrangement
  that is off by any amount fails — not just a wrong final number. Declared
  units (km, m) are bound in both directions: the sheet's answer lines and the
  key's boxes must carry the same unit the JSON verified.
- **1 is instructor-judged: problem 7(c)**, the written argument about whether
  the city centre lies inside the flood zone. The distance (8.06 km) *is*
  machine-checked; the reasoning that compares it with the radius is not. The
  key prints `---` for it in the Quick Answers bank and supplies a model
  response with a full / half / no-credit rubric.

There are no `[unchecked]` marks — every printed blank has either a verified
value or a written rubric.

## A note on the standards tag

The task listed HSG-C.B.5 (arcs and sectors). The problems here are all
equation-of-a-circle work, so they are tagged **HSG-GPE.A.1** — "derive the
equation of a circle given centre and radius; complete the square to find the
centre and radius" — which is the row in the standards map that actually matches
the requested focus. The tag appears in the answer key's Curriculum section.

## The study guide

Three sections — writing, reading, and completing the square. Each opens with a
rule box, then a worked example whose first step says *why* that tool is the
right one, then a try-it with the answer printed upside down inside the box. The
closing watch-out box flags the two errors this topic produces most: reading the
right-hand side as $r$ instead of $r^2$, and adding a completing term to only one
side of the equation.
