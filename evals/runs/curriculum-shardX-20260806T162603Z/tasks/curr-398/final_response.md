# Ellipses and hyperbolas in real structures

Three PDFs for your Algebra 2 student, all on **analyzing ellipse and hyperbola vertices,
foci and asymptotes**:

- **`ws_conicapp_curr398.pdf`** — the student worksheet, 10 problems, 6 pages.
- **`ak_conicapp_curr398.pdf`** — the full step-by-step answer key, 4 pages.
- **`ss_conicapp_curr398.pdf`** — a 2-page study guide.

## Every problem is a real object, with its units on the page

The applications are the ones these curves actually describe, and each states the origin,
the orientation and the unit before asking anything: a whispering gallery floor (metres), a
semi-elliptical bridge arch (feet), a cooling-tower waist (metres), a planetarium dome
(metres), a hyperbolic mirror and a lamp's shadow line (centimetres), an elliptical garden
bed (feet). There is no decorative story detail — every number printed in a stem is a number
the mathematics uses.

The units are carried through: each answer blank is labelled with its unit, and the key
prints the unit inside the boxed answer, so "24" and "24 ft" are not treated as the same
answer.

## What the ten problems cover

| Problems | Feature |
|---|---|
| 1, 3 | ellipse axes and vertices (including the height of an arch at a stated distance from the centre) |
| 2, 6, 9, 10 | ellipse foci — separation, the constant-sum property, and designing a gallery to a required focus separation |
| 4, 7 | hyperbola vertices and foci |
| 5, 8 | hyperbola asymptotes |

Two traps are built into the applications rather than announced: problem 9 gives the *full*
axes of a garden bed, so they must be halved before the focus formula is used, and problems 5
and 8 use hyperbolas with opposite orientations, where the asymptote slope is $b/a$ in one
case and $a/b$ in the other.

## What was verified, and what was not

The key's generated note says it exactly: **15 of the 17 answers are machine-checked with
SymPy; 2 are instructor-judged.**

- **Machine-checked (15):** every axis length, focal distance, vertex distance, asymptote
  slope and arch height was recomputed independently from the printed givens, including the
  exact surd $6\sqrt{3}$ in problem 3 — no decimal rounding was accepted in its place.
- **Instructor-judged (2):** the written parts of **5(b)** (what the asymptotes describe
  about the tower wall) and **10(b)** (why pushing the foci apart forces a lower ceiling).
  Both are marked `---` in the Quick Answers bank rather than given a value, and the key
  states what full credit needs. For 5(b) the key names the specific misconception to catch:
  calling the asymptotes the *edges* of the tower, or a line the wall touches.

## Study guide

Four sections, each with a rule box, a worked example whose first step names the decision
being made, and a try-it with the answer upside down inside the box: ellipse axes and
vertices (with the doubling that most answers lose), ellipse foci and the constant-sum
property, hyperbola vertices and foci (subtract versus add), and asymptote slopes with the
orientation rule stated both ways. All 14 of its worked values are machine-verified.
