# Composite Solids, Density and Design — 10 problems

Three PDFs are ready:

- **`ws_composite_curr345.pdf`** — the student worksheet (4 pages), with the
  formula list in the directions so no problem depends on memory alone.
- **`ak_composite_curr345.pdf`** — the full step-by-step answer key.
- **`ss_composite_curr345.pdf`** — a 2-page skills summary.

## What the worksheet covers

This is an interleaved review, so the work is deciding *what the situation asks
for*, not repeating one formula. Problems 1–4 are a short warm-up; after that the
four subskills alternate:

- **Composite volume** (1, 2, 5) — a plain cylinder, a block with a hole drilled
  through it, and a cylinder capped by a hemisphere.
- **Composite surface area** (3, 8) — an open-topped tank (no lid) and a
  cone-on-cylinder hopper (no buried disc).
- **Density and mass** (4, 6, 9) — mass from volume, volume from mass, and a
  composite volume converted to mass.
- **Design constraints** (7, 10) — a required capacity that fixes a dimension.

Problem 10 is the synthesis challenge: solve for the height a fixed capacity
forces, cost that design in steel, then argue what happens if the radius doubles.

## What is verified, and what is not

The sheet asks for **12 separate responses**.

- **11 are machine-checked** with SymPy — every volume, surface area, mass and
  height, each recomputed from the raw dimensions rather than from a rounded
  intermediate. Declared units (m³, m², cm³, cm², g, kg, m) are bound in both
  directions: the sheet's answer lines and the key's boxes must carry the unit the
  JSON verified, so a cubic-metre problem cannot be answered in square metres.
- **1 is instructor-judged: problem 10(c)**, the argument about doubling the
  radius. The key prints `---` for it in the Quick Answers bank and gives a model
  response with the numbers worked through, plus a full / half / no-credit rubric.
  The key's own "What is verified" note says 11 of 12.

There are no `[unchecked]` marks.

## Grading help

Four problems carry declared misconception traps, all confirmed distinguishable
by the verifier and printed in the key under **Common wrong answers**:

- 0.48 m³ — the drilled hole never subtracted (problem 2)
- 100.53 m² — a lid counted on an open-topped tank (problem 3)
- 339.29 m³ — a whole sphere used where a hemisphere belongs (problem 5)
- 47520 cm³ — mass multiplied by density instead of divided (problem 6)

## The study guide

Four sections — composite volume, composite surface area, density, and designing
to a constraint. Each has a rule box that says how to *decide* (add or subtract;
which faces are actually outside; which form of the density relationship), a
worked example whose first step is that decision, and a try-it with the answer
printed upside down inside the box.
