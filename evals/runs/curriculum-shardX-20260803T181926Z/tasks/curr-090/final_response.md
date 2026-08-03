# Two-Step Measurement Stories — Grades 2–3

Three PDFs are ready:

- **`ws_measure_curr090.pdf`** — the student worksheet, 12 problems, 5 pages.
- **`ak_measure_curr090.pdf`** — the step-by-step answer key, 3 pages.
- **`ss_measure_curr090.pdf`** — a 2-page study guide to keep beside the worksheet.

## What the worksheet covers

Every problem is a **two-step** measurement story, and every one asks for an answer
in a stated unit. Four kinds are interleaved so your child has to decide what to do
rather than repeat the same move twelve times:

- **Time** (4 problems) — adding up stretches of minutes, and finding what is left of
  a movie.
- **Money** (4 problems) — dollars-and-cents change, counting quarters and dimes into
  cents, and buying several identical things.
- **Mass** (2 problems) — grams and kilograms in the same problem.
- **Liquid volume** (2 problems) — litres and millilitres in the same problem.

The first four problems block together by kind (that is the warm-up); after that the
kinds rotate. Problems 6, 9 and 10 deliberately mix units inside one story
(2 L and 350 mL, 3 kg and 450 g), so the child has to convert before computing —
that conversion is the step most often skipped. The last problem is the synthesis
one: six groups, two different supplies, and change from \$50.

Every problem has a printed answer line with the unit already on it
(minutes, cents, g, mL), so the answer is written where a grader will look and in
the unit the question asked for.

## What was verified

All 12 answers were recomputed by the checker (SymPy) from the numbers in the story
before the PDFs were built — 12 of 12 machine-verified, nothing left to check by
hand. The units are verified too, in both directions: the unit on the worksheet's
answer line and the unit inside the boxed answer in the key both have to match the
verification data, so a millilitre problem cannot be answered in litres.

Four **misconception traps** are declared and machine-checked, and the answer key
prints them under **Common wrong answers**:

- Problem 2: a child who takes away only the 40 minutes gets 55, not 30.
- Problem 6: using "100 mL in a litre" instead of 1000 gives a negative answer.
- Problem 9: removing only one book gives 2550 g, not 2100 g.
- Problem 11: counting only the ride *to* school gives 175 minutes, not 350.

So if the answer that comes back is 175, you know exactly which half of the story
was missed — that is a different conversation from "wrong".

## The study guide

Four short sections, one per measurement kind. Each has the plan in words
(step 1 / step 2), the conversion fact it needs (1 kg = 1000 g, 1 L = 1000 mL,
1 hour = 60 minutes), one worked example that says *why* the first move is the first
move, and a try-it problem with the answer printed upside down so the child attempts
it before checking.
