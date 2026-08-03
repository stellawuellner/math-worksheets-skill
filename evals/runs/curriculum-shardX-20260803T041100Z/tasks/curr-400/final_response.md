# Modeling Loci and Intersections with Conic Sections (Algebra 2)

Three PDFs are ready.

- **Worksheet** (`ws_conics_curr400.pdf`, 6 pages) — 12 problems in an
  interleaved-synthesis format. The directions box states the two moves the
  whole sheet runs on: a locus is a sentence about distance (write the
  distances, set them equal, square, simplify), and an intersection is a system
  (substitute, solve one variable, substitute back and report ordered pairs).
  Problems 1–4 are the blocked warm-up — two circle items, then two parabola
  items — after which the four methods rotate with no same-method run longer
  than two. The set builds to real modelling: completing the square to recover a
  center and radius, a circle meeting a parabola in **three** points (one of
  them tangential), a line meeting a parabola in **one** repeated root so the
  student has to say what tangency means, a full focus-directrix derivation of
  $x^2 = 20y$, a circle meeting a hyperbola in four points, an Apollonius locus
  ("always twice as far from $A$ as from $B$" turns out to be a circle), and a
  satellite-dish synthesis where the same intersection point is measured against
  both the focus and the directrix.
- **Answer key** (`ak_conics_curr400.pdf`, 5 pages) — the generated
  quick-answer bank, then a full solution per problem. Each intersection
  solution names *which* substitution to make and why (eliminating $x^2$ rather
  than $x$ when a parabola is involved), and each solution ends with the check
  that matters for that case: why three intersections and not four, what a
  repeated root says about a tangent line, why $y = -10$ is rejected on the
  dish, and why the Apollonius ratio produces a circle rather than a
  perpendicular bisector. Three problems carry a named common wrong answer
  (101 from adding the center coordinates instead of subtracting, 12 from
  dividing by $p$ instead of $4p$, and $r \approx 3.32$ from reading the
  original constant as $r^2$).
- **Study guide** (`ss_conics_curr400.pdf`, 2 pages) — four sections matching
  the four worksheet skills (circles from a distance condition, parabolas from
  a focus and directrix, a line meeting a conic, two conics meeting). Each has
  a rule box, a worked example whose first step names why that tool applies, and
  a try-it with the answer upside down inside the box. The line-conic box makes
  the root count explicitly geometric (secant / tangent / miss), and the
  conic-conic box warns that a candidate value forcing $x^2 < 0$ yields no real
  point.

## Verification

17 of the 19 checks are machine-verified with SymPy: 5 `system` checks (a line
with a circle, a circle with a parabola giving three points, a tangent line with
one repeated root, a circle with a hyperbola giving four points, and the
dish-and-ring synthesis), 3 `solve` checks, 8 `eval` checks (point-on-circle
test, focus-directrix evaluation, and the center/radius components recovered by
completing the square), and 1 `distance` check for the focus measurement in the
synthesis. Problems 6, 9, 11 and 12 carry more than one verify entry under one
problem id, so a multi-part answer is verified part by part rather than as a
whole.

Two items are labelled for manual review, and the key says so at the point of
use:

- problem 9(a) — derive $x^2 = 20y$ from the equidistance condition. The
  derivation is written work; the points it produces in part (b) are
  machine-checked.
- problem 12(c) — explain what the two equal distances say about every point of
  the dish. Parts (a) and (b) are machine-checked; the explanation is prose.

Both are encoded as `{"type": "manual", ...}` rather than claimed as verified,
which is why the build exits 2. All 8 study-guide items (4 worked examples +
4 try-its) are fully machine-verified, and each of the four worksheet facets has
a matching worked example.

Three misconception traps are declared and machine-proved distinguishable from
the correct answers.

**Standards used and one honest gap.** The task's reference is
`HSG-GPE.A / HSF-IF`, but **`references/standards-map.md` has no row for
HSG-GPE.A** — the conic-derivation cluster (derive the equation of a circle by
completing the square; derive a parabola from a focus and directrix). I checked
the file directly: its only GPE row is "Coordinate geometry proofs |
HSG-GPE.B.4–B.7", and there is no row containing "conic", "parabola",
"ellipse" or "hyperbola". Rather than invent a code or stretch a neighbouring
one, the three problems that are *purely* conic-equation derivation — problem 3
(parabola from focus and directrix), problem 6 (completing the square to
center-radius form), and problem 12(c) (the focus-directrix property in words)
— carry **no `standard` field**, and this note is the record of why. The
remaining problems use codes taken verbatim from the map:
`HSA-REI.C.7` for the five intersection systems (row "Systems
(linear/quadratic)"), `HSA-REI.B.4` for the two quadratic solves (row
"Quadratics: solve"), and `HSG-GPE.B.4–B.7` for the items that use coordinates
and the distance formula to establish a geometric fact — the point-on-circle
test, the equidistance locus, the Apollonius locus, and the focus/directrix
distance measurements (row "Coordinate geometry proofs"). Adding an
`HSG-GPE.A.1–A.3` row to the map would let those three problems be tagged
properly.

## Build

All 21 gates green on the first build (exit 2 for the two declared manual
items). The four- and three-point intersection systems were verified against
`run_verify.sh` before any LaTeX was written, because `system` passes only when
the listed solutions match SymPy's *full* solution set — the dish-and-ring
system in particular has two rejected complex branches, and it was worth
confirming the checker agrees they are not solutions before building a problem
around that fact. Page counts: worksheet 6 (budget 7), answer key 5 (budget 7),
study guide 2 against its hard 2-page cap.
