# Angle Pairs Formed by a Transversal (High-School Geometry)

Three PDFs: the student worksheet (8 problems, 4 pages), a step-by-step answer
key, and a two-page study guide.

## How the sheet is built

One diagram serves all eight problems: two parallel lines cut by a transversal,
with the eight angles numbered and **no measures marked on it**. Each problem
supplies its own measures in the text. That is deliberate — a numbered figure
carrying values for one problem sits a few lines above the next problem and gets
applied to it by mistake, so the shared reference figure is captioned as such
and no problem carries a figure of its own.

## What the worksheet asks

- **1** — name three pairs from position alone: corresponding, alternate
  interior, alternate exterior.
- **2, 3, 5** — chain two relationships to a missing measure. Problem 3 pairs a
  congruent relationship (alternate interior, $65^\circ$) against a
  supplementary one (same-side interior, $115^\circ$) on the same given, which
  is where the name does the work. Problem 5 goes alternate exterior, then
  linear pair.
- **4, 6, 7** — algebra from the pair name: congruent pairs give
  "set equal" ($3x+10 = 5x-24$, $x = 17$), same-side interior gives
  "sum to $180$" ($x = 25$), alternate exterior gives $x = 30$ with a linear-pair
  cross-check.
- **8** — justify: explain why $\angle 3$ and $\angle 6$ are supplementary,
  using a named pair and a stepping-stone angle.

Difficulty ramps 1, 2, 2, 3, 3, 3, 4, 4. Every problem asks for the pair name as
part of the answer, and the key marks a correct measure with a wrong name.

## Verification

14 checks across the 8 problems: **12 machine-verified, 2 manual**. The build
exits 2 and names them, which is the correct outcome:

- **Problem 1** (naming three pairs) and **problem 8** (the explanation) are
  `{"type": "manual"}` with the expected classifications and the full reasoning
  chain written into the `desc`, so a human grader has the target in front of
  them. Neither is a computation a CAS can confirm, and neither is claimed as
  verified.
- Everything else is verified: the congruent-pair copies, the
  $180^\circ$ subtractions, the three linear equations (`solve`) and the
  substitutions back to the measures (`eval`).

The answer key gives a model answer for problem 8 plus a second acceptable
chain, and states what must be present for full credit.

`BUILD PASSED — 1 verification run flagged manual-review items (exit 2)`.

## Study guide (2 pages)

The same reference diagram, with interior and exterior angles identified, then
three sections: naming the pair (the two position questions, and which names are
congruent versus supplementary), finding a missing measure by chaining
relationships, and setting up the equation an angle pair justifies. Each section
has a worked example opening with a strategy line and a distinct try-it.

## Notes

- **Standards code.** The task names `HSG-CO.C.9`, which
  `references/standards-map.md` does not carry as its own row. The map's
  congruence row is `HSG-CO.A–HSG-CO.D` (which contains CO.C.9), and that is the
  string tagged on every problem, verbatim. No code was invented.
- The worksheet's prose-consistency match rate (45%) is dominated by angle
  *indices* — the "5" in $\angle 5$ is a label, not a quantity, and the checker
  has no way to know that. Every actual measure on the sheet is a JSON given.
