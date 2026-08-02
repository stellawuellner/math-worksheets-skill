Three PDFs are ready for a high-school geometry student on **one-way property
implications between quadrilaterals** — the fact that "square ⇒ rhombus" does
not run backwards, and what extra property is needed before it does.

- **Worksheet — 6 problems, misconception and error-analysis format.** Four of
  them present a named student's claim that runs an implication backwards and
  ask for the computation that settles it plus a written diagnosis: Priya
  concludes "square" from four congruent sides (2), Sam concludes "rhombus" from
  perpendicular diagonals (4), Sam concludes "square" from congruent diagonals
  in a parallelogram *and* slips in the algebra (5). Problem 1 uses the angle
  algebra of a rhombus; problem 3 is the pure implication audit (always true /
  not always true, with a counterexample); problem 6 is the challenge where the
  diagonal test finally *does* certify a square. Coordinate problems come with a
  blank plotting grid beside the work space.
- **Answer key — computation and diagnosis kept separate.** Part (a) of each
  problem is worked in full; part (b) gives the model sentence, plus an explicit
  "accept / do not accept" note so a grader knows that "she just miscalculated"
  is not the diagnosis. The quick-answer bank at the top also prints the common
  wrong answers that the three declared misconception traps generate.
- **Study guide — 2 pages, four sections**: the upgrades that genuinely work
  (parallelogram + congruent diagonals ⇒ rectangle, etc.), testing a claim with
  side lengths, the diagonal test for the most specific name, and killing a
  converse with a counterexample (kite, isosceles trapezoid). Each section has a
  rule box, a worked example whose first step says why that test is the decisive
  one, and a try-it with the answer upside down inside the box.

**Verification:** 9 computed quantities on the worksheet (diagonal and side
lengths by the distance type, the two algebra answers) and all 8 study-guide
answers were recomputed by SymPy. The three planted wrong results — 8.49 for
BD, 6.71 for BC, x = 3 — are declared as misconception traps and were each
machine-checked to be *distinguishably* wrong, i.e. the problem's own check
rejects them. The six written diagnoses (one per problem, including all of
problem 3) are labelled `manual` and are **not** claimed as verified; the build
therefore exits 2 and says so, which is the correct outcome for reasoning
answers. Final verdict: **BUILD PASSED — 1 verification run flagged
manual-review items (exit 2)** (worksheet 4 pages, key 3, guide 2).

One note for the record: `references/standards-map.md` has no code for
quadrilateral property relationships, so every problem is tagged with the
closest code the map actually contains, `HSG-GPE.B.4–B.7` (coordinate geometry
proofs), which is the mode most of the sheet uses. No code was invented.
