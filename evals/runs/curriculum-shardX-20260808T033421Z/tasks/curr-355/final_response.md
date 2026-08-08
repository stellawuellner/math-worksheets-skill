# Complex Solution Sets — Algebra 2 interleaved review

Three PDFs are ready:

- **`ss_cxsolve_curr355.pdf` — Skills Summary (2 pages).** Four sections, each
  with a rule box, a worked example and a try-it whose answer prints upside down
  inside the box: square roots of negatives, the quadratic formula with a
  negative discriminant, finding *all* solutions of a higher-degree equation,
  and checking a proposed solution / reporting the full set.
- **`ws_cxsolve_curr355.pdf` — Student worksheet (5 pages), 12 problems.**
  The first four are a short warm-up; after that the four methods are
  deliberately interleaved, so no two consecutive problems use the same one and
  the student has to decide whether to isolate a square, use the formula, or
  factor first. The set closes with one synthesis challenge: build a monic real
  quadratic from the single root $4 - i$ and justify why $4 + i$ must be its
  partner. Difficulty runs 1 → 5.
- **`ak_cxsolve_curr355.pdf` — Answer key (3 pages).** Every solution shows the
  method choice and the discriminant, not just the roots, and each one says how
  many solutions the degree demands. The Quick Answers bank, curriculum block
  (HSN-CN.C.7 and HSN-CN.C.9) and a "Common wrong answers" section sit at the
  top.

## What is verified, and what is not

The set carries **15 declared responses across 12 problems. 13 are machine
checked** — every solution set was recomputed with SymPy over the complex
numbers, which means the check confirms *completeness* as well as correctness:
a key that listed only the real roots of $x^4 - 81 = 0$ would fail the gate, not
pass it. The study guide's four worked examples and four try-its were verified
the same way.

**2 responses are instructor-judged**, printed as `---` in the key:

- **Problem 5(b)** — explaining what was missing from an incomplete solution set
  and why the equation must have that many solutions.
- **Problem 12(b)** — justifying why $4 + i$ must be the second root of a real
  quadratic.

Both are written arguments; the key states what full credit requires and what
does not earn it (asserting the conjugate-pair rule with no reason attached).

## Notes

- Three misconception traps are declared and machine-checked to be
  distinguishably wrong, and they are the three incompleteness errors this topic
  produces: reporting only the positive imaginary root, stopping after the real
  roots of a quartic, and dividing only the radical part of the quadratic
  formula by $2a$.
- The grade level appears on the answer key only.
