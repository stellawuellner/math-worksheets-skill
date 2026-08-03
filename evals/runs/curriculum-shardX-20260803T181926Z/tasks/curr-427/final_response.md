# Law of Cosines: SAS and SSS Triangles — Precalculus (12 problems)

Three PDFs are ready:

- **Worksheet** (`ws_lawcos_curr427.pdf`, 8 pages) — 12 problems, each with its own
  to-scale triangle figure generated directly from the verified data, so no figure
  can disagree with its problem.
- **Answer key** (`ak_lawcos_curr427.pdf`, 4 pages) — the substitution line, the
  arithmetic, and a sense-check for every problem, plus the generated quick-answer
  bank, curriculum section, and "common wrong answers" notes.
- **Study guide** (`ss_lawcos_curr427.pdf`, 2 pages) — three sections (SAS side,
  SSS angle, bearings), each with a formula box, a worked example, and a try-it.

## What the worksheet covers

- **SAS (problems 1, 3, 5, 8, 11)** — find the third side from two sides and the
  included angle. Problem 8's included angle is obtuse, so the cosine term *adds*;
  problem 5 also asks for the area from the same two sides and angle; problem 11
  continues into finding an angle once all three sides are known.
- **SSS (problems 2, 4, 7, 10)** — rearrange for $\cos$ of the named angle.
  Problem 2's cosine is negative, which settles obtuseness with no ambiguity;
  problem 7 asks for the exact fraction $\cos A = \tfrac{13}{14}$ before the
  decimal angle.
- **Navigation (problems 6, 9, 12)** — two bearings from one point, a course change
  in flight, and a survey traverse. Each has to be turned into an SAS triangle
  first; answers carry km or mi and the worksheet's answer lines print the unit.

Difficulty ramps 1 → 5 and no two consecutive problems use the same method after
the opening pair.

## Verification

15 of the 16 machine checks passed under SymPy: every triangle is re-solved from
its givens and compared to the key within 0.01, the area is recomputed
independently, and $\cos A$ is checked as an exact fraction. The three figures'
labels are generated from the same data the checker used.

**Flagged for your review (1 item):** problem 12(b), which asks the student to
*explain* why the law of sines cannot start the problem. That is a reasoning
answer, so it is marked manual rather than claimed as verified; the key gives a
model response and says what to credit. Problem 12(a), the distance, is fully
verified.

Three misconception traps are declared and machine-confirmed distinguishable, and
they print in the key:

- writing $+2ab\cos C$ instead of $-2ab\cos C$ (gives 14.41 rather than 7.24),
- subtracting the wrong squared side in the SSS rearrangement (gives 32.16 rather
  than 45.21),
- adding the two distances instead of using the law of cosines (95 km rather than
  55.86 km).

## Notes for the adult

Every figure is drawn to scale from the problem's own numbers, so a student whose
answer contradicts the picture has made an arithmetic error, not a reading error.
The course level prints on the answer key only.
