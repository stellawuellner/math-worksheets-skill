Three PDFs are ready for a precalculus student on the unit circle and
trigonometric graphs, focused on the two errors that produce believable-looking
wrong answers: **angle-mode errors** (a bare number read in the wrong unit, or a
conversion run the wrong way) and **quadrant-sign errors** (the reference angle's
value copied without the sign the quadrant demands).

- **Worksheet** (8 problems, `ws_unitcircle_curr419.pdf`) — the directions carry a
  value-free ASTC reference diagram, then: a warm-up exact value in quadrant III;
  Reva's calculator left in radian mode reporting sin 30° ≈ −0.99; Ari copying the
  reference-angle cosine for 4π/3; Sena's positive tan 150°; Bo converting 225° by
  multiplying by 180/π and landing on 12891.6; a degree-interval equation where
  Cal put a correct reference angle into the two quadrants where sine is
  *positive*; a radian-interval equation asking for the expected solution count and
  quadrants first; and a challenge on the bare number 3 (radians vs degrees) with
  the quadrant argument for the sign. Five are explicit find-and-fix items. Work
  space is 4.5–7 cm, declared with `workspace_cm`.
- **Answer key** (`ak_unitcircle_curr419.pdf`) — four to six numbered steps per
  problem, all built the same way: locate the quadrant, take the reference angle
  for the size, attach the quadrant's sign, then check. Each diagnosis names what
  the wrong method actually computed (30 radians is nearly five full turns; 180/π
  is the radians-to-degrees factor; a positive tangent in quadrant II contradicts
  sin/cos signs) and gives the size or sign check that would have caught it before
  any arithmetic. It carries the generated quick-answer bank and a "Common wrong
  answers" block (−0.99, 0.5, 0.58, 12891.6, 0.9986).
- **Study guide** (2 pages, `ss_unitcircle_curr419.pdf`) — three skills matching
  the worksheet tags: reference angle then quadrant sign (with ASTC and the
  coordinate reasoning behind it), getting the angle mode right (both conversion
  factors plus the 6.28-radian size check), and solving on an interval (size picks
  the reference angle, sign picks the quadrants). Each has a rule box, a two-step
  worked example, and an upside-down try-it, plus a watch-out box.

**Verification.** Problems 1–7 and part (b) of problem 8 are machine-checked with
SymPy: five `eval` exact values and conversions (answers verified in exact form —
−1/2, 1/2, −√3/3, 5π/4), two `solve_interval` checks (one in degrees on [0°, 360°),
one in radians on [0, 2π)), and one `approx` for cos 3. All 6 study-guide results
are machine-checked, including both interval solutions. Parts (a) and (c) of
problem 8 ask for explanations, so a second entry on problem 8 is declared
`{"type": "manual"}` and the build correctly exits 2 with one manual-review item;
no open response is described as machine-verified. Five planted wrong answers are
declared misconception traps (−0.99, 0.5, 0.58, 12891.6, 0.9986), each proved
distinguishably wrong and each really the output of the named wrong method.

Standards: every problem is tagged `HSF-TF.A.2, HSF-TF.B.5` from
`references/standards-map.md`.

**Build notes.** Two gates failed on the way to green, both fixed:
`verify-ws` rejected a trap whose printed value (12891.59) did not round-match its
own expression at the verifier's precision (12891.6) — the planted number is
derived, never typed; and `template-ss` rejected two `\skillheading` titles at 63
and 60 characters against the 57-character budget. A first-pass layout defect
found by inspecting the rendered page — the ASTC quadrant labels sat on top of the
circle — was also corrected by moving the labels outside it.
