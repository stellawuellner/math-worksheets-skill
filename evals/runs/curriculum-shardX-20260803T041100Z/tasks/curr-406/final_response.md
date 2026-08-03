# End Behavior and Multiplicity: Sketching Polynomials (Precalculus)

Three PDFs: the student worksheet (10 problems, 5 pages), a step-by-step answer
key, and a two-page study guide.

## What the worksheet asks

The sheet is organised around the three decisions a sketch actually requires,
and it names them as such.

- **End behavior (1, 2, 6, 10)** — a reference table at the top gives the four
  degree-parity × leading-coefficient cases, and each problem asks for the two
  limits *plus* the degree and sign that justify them. Problem 2 makes the
  even-degree "ends agree" point explicit; problem 6 is odd degree with a
  negative leading coefficient, where the standard picture flips.
- **Zeros and multiplicity (3, 5, 8)** — read zeros from factored form and say
  crosses versus touches; problem 5 requires factoring first
  ($x^3 - 4x^2 + 4x = x(x-2)^2$); problem 8 is a quadratic in $x^2$ with four
  simple zeros $-2, -1, 1, 2$.
- **Sign, intercept, sketch (4, 7, 9)** — test values fix the sign of a whole
  interval. Problem 9 is the synthesis: sketch $(x+2)^2(x-3)$ on a supplied
  grid after finding the end behavior, the touch at $x = -2$, the crossing at
  $x = 3$ and the intercept $f(0) = -12$.
- **Problem 10** is error analysis on the most common end-behavior mistake:
  "even degree, so both ends rise" ignores the negative leading coefficient.

Difficulty ramps 1, 2, 2, 2, 3, 3, 3, 4, 4, 5; facets interleave after the
warm-up. Problem 9 declares `workspace_cm: 10.0` and carries a full unlabelled
coordinate grid, so the sketch has real room rather than being squeezed to save
a page.

## Verification

20 checks across the 10 problems: **18 machine-verified, 2 manual**. The build
exits 2 and names the manual items, which is the right outcome here:

- Every end-behavior claim is verified as a genuine `limit` at $\pm\infty$ —
  eight limit checks, so no arrow on the key can disagree with the mathematics.
- Zeros and factorings are verified with `zeros` and `factor`; the intercepts
  and sign test values with `eval`.
- **Manual:** the drawn curve in problem 9 and the written explanation in
  problem 10. Both carry the full expected description in the JSON `desc`
  (end behavior, touch/cross at each zero, intercept, sign intervals), so a
  human grader has an explicit target. A sketch cannot be CAS-checked and is
  not claimed as verified — problem 9's *numeric* anchor ($f(0) = -12$) is
  verified separately, and problem 10's two limits are verified even though the
  explanation is not.

`BUILD PASSED — 1 verification run flagged manual-review items (exit 2)`, and
prose consistency reports 100% on the worksheet.

## Study guide (2 pages)

Three sections: end behavior (with the same four-case table), zeros and what
multiplicity does at each, and signs/intercept/sketch order-of-work. Each has a
worked example that opens with a strategy line and a try-it with the answer
printed upside down inside the box.

## Notes

- Standards used verbatim from `references/standards-map.md`:
  `HSA-APR.B.3` ("Polynomial zeros & graphs") for the zeros, factoring and
  sketching problems, and `HSF-IF.A–HSF-IF.C` ("Function behaviour, notation,
  graphs") for the end-behavior problems. The task's `HSA-APR.B.3 / HSF-IF.C`
  maps onto exactly these two rows; no code was invented.
