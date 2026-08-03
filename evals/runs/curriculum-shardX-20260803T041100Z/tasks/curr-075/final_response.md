# Matching Division Stories, Drawings, and Equations — Grades 2–3

Three PDFs are ready: the student worksheet, a full step-by-step answer key, and
a two-page skills summary.

## What the worksheet contains

12 problems on **matching division stories, drawings, and equations**, in an
interleaved-synthesis format. Four subskills are tagged as facets and rotate
after the first two warm-up problems, so the student has to decide *which*
translation is being asked for rather than repeating one move:

| Facet | Problems | What it asks |
| --- | --- | --- |
| `story-to-equation` | 1, 4, 8, 12 | read a story, write the division equation, answer it |
| `drawing-to-equation` | 2, 6, 10 | read an equal-groups or array picture, write the equation |
| `equation-to-story` | 5, 9 | decide which of two stories the equation actually tells |
| `equation-fact-family` | 3, 7, 11 | find a missing factor or missing divisor and write the family |

Both meanings of division are exercised deliberately: sharing (partitive:
problems 1, 5, 12) and grouping/measurement (problems 4, 8, 9). Problem 12 is
the synthesis challenge — 5 packs of 6 pencils shared among 3 tables, which
cannot be divided until the total is built by multiplying first.

Difficulty ramps 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 5. Standards are tagged from
`references/standards-map.md` only: `3.OA.A.3 / 4.OA.A.2` for the story and
picture problems, `3.OA.C.7` for the fact-family problems. The task's own
`standard_refs` string `3.OA.A.2–3.OA.A.4` is not a row in that file, so the two
rows that do cover this content were used verbatim rather than inventing a code.

Reference figures carry no numbers (a value-free "what a division sentence
says" card with the directions), and the three counter drawings are unlabelled
dot pictures, so no figure can be misread as belonging to a neighbouring
problem.

## What was verified

**All 12 worksheet answers are machine-verified by SymPy — 0 manual items.**
Nine are `eval` checks of the division itself; three are `solve` checks of the
missing-number equations, including problem 11 where the *divisor* is unknown
(`45 ÷ ? = 9`).

Four misconception traps are declared and machine-checked, and each one is
printed in the answer key's "Common wrong answers" bank so a grader can
diagnose instead of just marking:

- P4 — subtracting instead of dividing (would give 18)
- P8 — multiplying instead of dividing (would give 256)
- P10 — reporting the number of rows (4) instead of the number in each row
- P12 — dividing one pack only (would give 2)

The study guide's 8 boxes (4 worked examples + 4 try-its) are verified by their
own JSON, so the examples the student learns from are gated too. Nothing on
either document is claimed as verified without a check behind it.

## Study guide

Two pages, one section per worksheet skill: story→equation, drawing→equation,
equation→story, and fact families. Each section is a rule box, a worked example
with a strategy step before any arithmetic, and a distinct try-it whose answer
is printed upside down inside the box. A closing watch-out box names the two
errors the traps target.

## Notes

- Nine problems declare a `workspace_cm` larger than the printed work-space
  argument. That is deliberate: the drawings and displayed equations sit in the
  *stem*, which the page-budget model cannot see, so the extra centimetres are
  declared in the JSON to charge the budget honestly rather than compressing
  the sheet. The first build failed exactly here (7 pages against a 6-page
  ceiling) and was fixed by declaring the stem content, not by shrinking room
  to write.
- The worksheet runs 7 pages because grade 2–3 students draw their groups; the
  page budget was computed, not capped.
