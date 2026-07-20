# Standards Map & Difficulty Ladders

Tag every verify-JSON problem with `"standard"` (a code from THIS file — never
invent codes) and `"difficulty"` (1–5 per the ladders below). Ramp difficulty
across the worksheet; `verify.py` reports coverage and flags ramp drops.

## Common Core codes by topic (grades 5–8)

| Topic | Code |
|---|---|
| Fraction operations | 5.NF.A.1 / 6.NS.A.1 |
| Decimals & operations | 5.NBT.B.7 / 6.NS.B.3 |
| Ratios & unit rates | 6.RP.A.2, 6.RP.A.3 |
| Percent problems | 6.RP.A.3.c / 7.RP.A.3 |
| Integer operations | 7.NS.A.1, 7.NS.A.2 |
| One/two-step equations | 6.EE.B.7 / 7.EE.B.4 |
| Proportional relationships | 7.RP.A.2 |
| Exponents & scientific notation | 8.EE.A.1, 8.EE.A.4 |
| Linear equations & slope | 8.EE.B.5, 8.EE.B.6 |
| Systems of equations | 8.EE.C.8 (sub-codes 8.EE.C.8a–c for graphical/algebraic/word-problem emphasis) |
| Functions | 8.F.A.1–8.F.B.5 |
| Pythagorean theorem | 8.G.B.7, 8.G.B.8 |
| Volume | 8.G.C.9 |

## High school (CCSS-HS)

| Topic | Code |
|---|---|
| Quadratics: solve | HSA-REI.B.4 |
| Systems (linear/quadratic) | HSA-REI.C.6, HSA-REI.C.7 |
| Polynomial arithmetic/factoring | HSA-APR.A.1, HSA-SSE.B.3 |
| Polynomial zeros & graphs | HSA-APR.B.3 |
| Exponentials & logs | HSF-LE.A.4, HSF-BF.B.5 |
| Function composition/inverse | HSF-BF.A.1c, HSF-BF.B.4 |
| Trig functions & unit circle | HSF-TF.A.2, HSF-TF.B.5 |
| Trig identities | HSF-TF.C.8 |
| Law of sines/cosines | HSG-SRT.D.10, HSG-SRT.D.11 |
| Right-triangle trig | HSG-SRT.C.8 |
| Circles (arcs, sectors) | HSG-C.B.5 |
| Coordinate geometry proofs | HSG-GPE.B.4–B.7 |

## AP Calculus (CED unit codes)

| Topic | Code |
|---|---|
| Limits & continuity | LIM-1, LIM-2 |
| Derivative rules & chain rule | FUN-3.A–FUN-3.C |
| Implicit/inverse differentiation | FUN-3.D–FUN-3.E |
| Related rates | CHA-3.D |
| Optimization | FUN-4.B–FUN-4.C |
| Riemann sums & FTC | LIM-5, FUN-6 |
| u-substitution / parts (BC) | FUN-6.D–FUN-6.E |
| Differential equations | FUN-7 |
| Series (BC) | LIM-7, LIM-8 |

## Difficulty ladders (1–5)

Anchored to MATH-dataset level conventions: 1–2 routine single-step,
3 standard multi-step, 4 method-selection or unusual form, 5 synthesis.

- **Factoring:** 1 GCF/monic small ints · 2 monic any signs · 3 a≠1 grouping ·
  4 special forms (cubes, disguised quadratics) · 5 GCF-first + multi-technique
- **Linear equations/systems:** 1 one-step · 2 two-step · 3 variables both
  sides / substitution · 4 elimination with scaling, word setup · 5 3-variable
  or parameterized
- **Triangle trig:** 1 right-triangle ratio · 2 law of sines AAS · 3 law of
  cosines SAS/SSS · 4 applications (bearings, elevation) · 5 ambiguous SSA,
  multi-triangle composites
- **Derivatives:** 1 power rule · 2 product/quotient · 3 single chain ·
  4 nested chain + product mix · 5 implicit/related-rates synthesis
- **Word problems (any level):** base topic level +1 if multi-step story,
  +1 if distractor numbers present; cap 5

Worksheet default mix: start at 1–2, majority at 2–3, finish with one or two
4–5 challenge problems. A drill sheet may stay flat; say so in the header.

## Bloom tags (cognitive level)

Tag each problem `"bloom"`: **recall** (state/evaluate directly) · **apply**
(routine procedure) · **analyze** (multi-step, method selection, error-analysis
"find and fix the mistake" — still machine-verifiable: check the planted
conclusion is wrong AND the correction is right) · **justify** (explain/prove —
usually `manual`). Default mixes: drill = mostly apply; test-prep ≈ 20% recall,
50% apply, 20% analyze, 10% justify. Verification reports the mix.
