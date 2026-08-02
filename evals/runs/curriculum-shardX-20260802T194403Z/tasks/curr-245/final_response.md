# Pythagorean Theorem and Coordinate Distance — Grade 8 / Pre-Algebra (curr-245)

Three PDFs are ready:

- **Worksheet** (`ws_pythag_curr245.pdf`, 5 pages) — 12 problems in an
  interleaved review format. Problems 1–2 are the warm-up (one hypotenuse, one
  missing leg); after that the four methods are mixed on purpose, so the student
  has to decide which one each situation calls for rather than repeat a
  procedure: hypotenuse from two legs, a missing leg from the hypotenuse,
  distance between two coordinate points, and multistep composites that use the
  theorem more than once. Every problem states its units. The set finishes with
  a synthesis challenge — the longest pole that fits corner-to-corner inside a
  120 × 90 × 80 cm crate, which needs the theorem twice (floor diagonal, then
  up to the far top corner).
- **Answer key** (`ak_pythag_curr245.pdf`, 3 pages) — a quick-answer bank for
  fast checking, then a full solution for every problem: which side is the
  hypotenuse and why, the equation, the arithmetic, and the boxed answer with
  its unit. Six problems carry a grading note naming the specific wrong answer
  the common error produces (for example 18.79 ft on problem 2 means the ladder
  was treated as a leg; 150 cm on problem 12 means the student stopped at the
  floor diagonal), so a wrong answer tells you which idea to reteach.
- **Study guide** (`ss_pythag_curr245.pdf`, 2 pages) — four sections, each with
  a rule box, a worked example whose first line explains *why* that method fits,
  and a try-it with its answer printed upside down. It makes the point that the
  distance formula is not a new formula, just the theorem applied to a triangle
  drawn on the grid, and closes with the self-check that catches most errors:
  if the answer comes out longer than the ladder or the string, the squares were
  added when they should have been subtracted.

## Verification

All 12 worksheet answers are machine-verified with SymPy: 8 through the `approx`
checker (each expression is a faithful transcription of the problem's givens),
2 through the `distance` checker straight from the coordinate pairs, and 2
through `solve` for the problems that ask for *both* points at a given distance
(problem 7: x = 0 and x = 12; problem 11: y = 10 and y = −14). Nothing is flagged
manual — every problem on this sheet has an exactly checkable numeric answer.
All 8 study-guide items (4 worked examples + 4 try-its) are verified the same way.

Build note: the first build failed at the answer-key compile gate — the generated
"common wrong answers" block ran off the page — so the misconception data was
moved into the answer key's per-problem grading notes instead. The final build is
green on all 21 gates, including the per-problem answer-key binding and the
unit binding (each declared unit appears on the worksheet's answer line and
inside the key's boxed answer).
