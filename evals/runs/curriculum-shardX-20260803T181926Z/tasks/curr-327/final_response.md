# Parallel and Perpendicular Slopes — High-School Geometry practice set

Three PDFs are ready:

- **`ss_slopes_curr327.pdf` — Skills Summary (2 pages).** Three sections, each with a
  rule box, a worked example, and a "try it" whose answer is printed upside down
  inside the box: (1) the slope formula and the **parallel** test (equal slopes),
  (2) the **perpendicular** test (opposite reciprocals, product `-1`) *plus* the
  vertical-line exception the product rule cannot handle, and (3) how to turn a
  coordinate claim into a proof — which slopes to compute, what each comparison
  entitles you to conclude, and the reminder that the arithmetic alone is not a
  proof. A watch-out box names the two half-done opposite reciprocals (sign
  forgotten, fraction not flipped).
- **`ws_slopes_curr327.pdf` — Student worksheet (5 pages), 10 problems.** Every
  problem uses slopes to settle a parallel or perpendicular question. The set opens
  with two single-segment warm-ups that also ask for the parallel/perpendicular
  partner slope, then two "are these two segments parallel / perpendicular?" items,
  then the vertical-segment special case, then a parallelogram (four slopes), a right
  triangle plus its area, a rectangle test with diagonal midpoints, a square proof
  with slopes *and* distances, and finally a full midsegment coordinate proof.
  Difficulty ramps 1 → 5; work space runs 4.5–8 cm and every problem has its own
  answer line.
- **`ak_slopes_curr327.pdf` — Answer key (4 pages).** Every slope is computed from
  the formula with the substitution shown, and each conclusion states the theorem it
  rests on rather than just asserting the shape. Problem 8 is worth flagging: the
  figure looks like a rectangle but is not — the key shows why (the adjacent slopes
  multiply to `+1`) and identifies what it actually is. It opens with a quick-answer
  bank and a generated Curriculum section listing the specific standards used
  (HSG-GPE.B.4 for the proofs, B.5 for the slope criteria, B.6 for midpoints,
  B.7 for area and distance) with the difficulty range.

**Verification.** 27 machine checks — every slope, midpoint, distance and area on the
sheet — were recomputed independently with SymPy and passed.

**Two items are flagged for manual review, correctly:**

1. **Problem 5**, the written explanation of why the opposite-reciprocal rule must be
   read carefully when one segment is vertical. The slope itself (undefined) is
   machine-checked; the reasoning is not something a CAS can grade. The key gives a
   model explanation and says any equivalent wording is acceptable.
2. **Problem 10(c)**, the coordinate proof itself. All four numbers it rests on (both
   midpoints and both slopes) are machine-verified; the proof write-up is the open
   part. The key prints a complete model proof to compare against, including the
   step students most often omit — saying why the two segments are distinct lines and
   not the same line.
