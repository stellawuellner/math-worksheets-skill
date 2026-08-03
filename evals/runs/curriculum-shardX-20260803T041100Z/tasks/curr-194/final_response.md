Three PDFs are ready for a Grade 6–7 learner on scale drawings, area, circles and
surface area, focused on diagnosing radius-versus-diameter and
area-versus-perimeter errors.

- **Worksheet** (8 problems, `ws_circles_curr194.pdf`, 4 pages) — problem 1 is a
  clean radius circumference so the correct habit is established before it is
  tested; problem 2 gives a diameter to an area formula that only accepts a
  radius. Problems 3 and 4 are the find-and-fix items: Rae computes 2πr and
  labels it cm², Marco multiplies 9 × 4 and orders 36 m of edging — each asks the
  student to *name* the quantity actually computed before redoing the work.
  Problem 5 is an L-shaped coordinate plot where the tempting move is to add the
  six side lengths; problem 6 hides the radius/diameter decision inside the
  phrase "from one edge, through the centre, to the opposite edge"; problem 7
  works backwards from a 44 m railing to the pool's area, the case where dropping
  the given number straight into πr² is off by a factor of forty. Problem 8 is an
  open explanation of why doubling a radius doubles a circumference but
  quadruples an area. Work space runs 4.4–6.5 cm and every problem carries an
  `\answerline` with its unit, because a length answered in m² is the
  misconception showing itself.
- **Answer key** (`ak_circles_curr194.pdf`) — three or four numbered steps per
  problem, the first always classifying the given number (radius or diameter?)
  and the question (length or covering?) before any substitution. Problem 5 is
  solved twice, by decomposition and by subtraction from the enclosing rectangle,
  so the student has an independent check. It carries the generated quick-answer
  bank and the generated "Common wrong answers" block (15.71, 615.75, 37.70, 36,
  34, 11.31, 6082.12), plus a full model answer and a full-credit checklist for
  the open item.
- **Study guide** (2 pages, `ss_circles_curr194.pdf`) — three skills matching the
  worksheet tags: halve a diameter before squaring it, decide between around-the-
  rim and across-the-face, and the same-rectangle-two-questions contrast for
  polygons. Each has a rule box, a two-step worked example and an upside-down
  try-it; the third section's try-it deliberately re-asks the example's rectangle
  as an area question. A watch-out box explains why the diameter slip multiplies
  an area by four rather than two.

**Verification.** 7 of the 8 worksheet problems are machine-checked with SymPy
(five `approx` circle computations, one `eval` perimeter, one `polygon_area`
shoelace on the L-shaped plot), and all 6 study-guide results are machine-checked.
Problem 8 is a genuinely open explanation, so it is declared `{"type": "manual"}`
and the build correctly exits 2 with one manual-review item; nowhere is it
described as machine-verified. Seven planted wrong answers are declared
misconception traps and each was proved distinguishably wrong by the verifier,
with its printed value derived from the wrong-method expression rather than typed
by hand.

**Standards.** Every problem is tagged `6.G.A / 7.G.B`, copied verbatim from
`references/standards-map.md` ("Area, surface area, volume (gr 6–7)"). The task's
own reference is the looser `6.G / 7.G`; the map's row is the more specific
spelling of the same codes, so no code was invented and none is missing.

**Gate-log note.** Three prose flags are expected false positives: the worksheet's
"problem 3" cross-reference in item 8, and the study guide's intermediate values
25, 14 and 6 written inside worked examples (π × 25, 14 + 6). No figure-label or
computed value is unbound; the worksheet matches 14 of 15 prose numbers.
