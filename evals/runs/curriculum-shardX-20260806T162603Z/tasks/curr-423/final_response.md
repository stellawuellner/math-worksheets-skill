# Solving trigonometric equations on a restricted interval (Precalculus)

Three PDFs are ready.

**Study guide (`ss_trigeqn_curr423.pdf`, 2 pages)** — four sections, each a rule
box, a worked example whose first step names *why* that method applies, and a
try-it with the answer upside down inside the box: linear equations in one ratio
(with the quadrant table), equations that factor (and the warning never to divide
by a trigonometric factor), identity-first quadratics, and multiple angles, where
the interval must be widened *before* solving.

**Worksheet (`ws_trigeqn_curr423.pdf`, 5 pages)** — 10 problems, all on stated
restricted intervals, with the four methods interleaved after the first two
warm-ups so the student must choose a method rather than repeat one. Three carry
a real context with explicit units: a press cam's crank angle in degrees, a buoy
whose height in metres is a function of hours after midnight, and a searchlight
whose brightness in lux depends on the beam angle. Difficulty ramps 1 to 5,
finishing with a difference-of-squares equation whose solution count is the point.

**Answer key (`ak_trigeqn_curr423.pdf`, 3 pages)** — worked solutions, including
the interval-widening step written out for both multiple-angle problems, a Quick
Answers bank, and a generated Curriculum section (HSF-TF.B.5 and HSF-TF.C.8).

## What is verified, honestly

The sheet asks for **14 responses across the 10 problems**.

- **12 are machine-checked** by SymPy. Every solution list is checked for
  *completeness* on its stated interval, not merely for containing correct
  angles — which matters here, because the characteristic error on problems 4, 7
  and 9 is finding half the solutions, and a check that only confirmed the roots
  it was handed would pass that. The two "rewrite using a Pythagorean identity"
  parts (5a, 8a) are verified as **identities in $\theta$**, so a factorisation
  that happens to agree at a few angles would not pass.
- **2 are instructor-judged** and marked `---` in the Quick Answers bank:
  problem 6(b), interpreting what the two buoy times mean physically, and problem
  10(b), explaining why the factored equation has four solutions where the linear
  one has two. Both are prose. The key prints a rubric for each — 6(b) requires
  saying which crossing is rising and which is falling; 10(b) requires the
  two-cases-times-two-quadrants argument, not just "one list is longer".

That is the same split the key's "What is verified" note reports. Nothing is
marked `[unchecked]`.
