# Putting the Circle Theorems Together — 10 problems

Three PDFs are ready:

- **`ws_circlethm_curr340.pdf`** — the student worksheet (4 pages), opening with a
  value-free labelled reference diagram so the vocabulary is never ambiguous.
- **`ak_circlethm_curr340.pdf`** — the full step-by-step answer key.
- **`ss_circlethm_curr340.pdf`** — a 2-page skills summary.

## What the worksheet covers

This is an interleaved review, so the point is **method choice**, not repetition.
Problems 1–3 are a short blocked warm-up; after that the four subskills are
shuffled so no method runs more than twice in a row:

- **Central and inscribed angles** (1, 2, 6) — including a cyclic quadrilateral.
- **Chord, secant and tangent lengths** (4, 8) — intersecting chords, then the
  tangent-secant relation where the tangent must be *squared*.
- **Arc length and sector area** (3, 7, 9) — the same fraction of a circle,
  applied to circumference and to area.
- **The circle's equation inside a configuration** (5, 10) — a tangent point read
  off a centre-radius equation, and a completed square used to settle a chord
  question.

Problem 10 is the synthesis challenge: complete the square, use the radius to
find how far a 16-unit chord sits from the centre, then argue why a 24-unit chord
cannot exist at all.

## What is verified, and what is not

The sheet asks for **16 separate responses** across the 10 problems.

- **15 are machine-checked** with SymPy — every angle, every length, both
  rounded arc/sector values, and the completed-square rewrite (checked as an
  algebraic identity, so any error in the rearrangement fails, not just a wrong
  final number). The declared units (cm, cm², m) are bound in both directions:
  the sheet's answer lines and the key's boxes carry the same unit the JSON
  verified.
- **1 is instructor-judged: problem 10(c)**, the written argument that no chord
  can exceed the diameter. The key prints `---` for it in the Quick Answers bank
  and supplies a model response with a full / half / no-credit rubric.

There are no `[unchecked]` marks.

## Grading help

Two problems carry declared misconception traps, printed in the key under
**Common wrong answers**:

- Problem 7 — if the answer is about **25.13**, the arc-length formula was used
  where the sector-area formula was needed.
- Problem 8 — if the answer is **1.5**, the tangent length was used instead of
  its square.

Both were machine-checked to be distinguishably wrong, so neither can be
confused with a correct response.

## A note on the standards tag

The standards map carries a single high-school circles row, **HSG-C.B.5**, and no
separate row for the inscribed-angle family (HSG-C.A). Every problem is therefore
tagged HSG-C.B.5, which is the closest on-grade code the map actually contains —
I did not invent a code for the angle theorems. The tag appears in the answer
key's Curriculum section.

## The study guide

Four sections, one per subskill, each with a rule box that says how to *recognise*
which theorem applies (vertex at the centre or on the circle; crossing point
inside or outside), a worked example whose first step is the choice of tool, and a
try-it with the answer upside down inside the box.
