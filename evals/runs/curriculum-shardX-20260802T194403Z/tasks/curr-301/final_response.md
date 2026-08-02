# Precise Definitions and Counterexamples — High School Geometry

Three PDFs are ready: the student worksheet, a full step-by-step answer key, and
a two-page study guide.

**Worksheet (`ws_definitions_curr301.pdf`, 5 pages, 8 problems).** The sheet is
built on one idea: a definition has to be true of everything it names *and of
nothing else*, and the way you show it fails the second half is to exhibit a
counterexample. To keep that from being an argument about pictures, every
problem is set on the coordinate plane, so a definition becomes something the
student can **compute**. A reference table in the directions makes that
translation explicit — definition in words, definition in coordinate notation.

- Problem 1: a vague midpoint definition, repaired and then applied.
- Problem 2: "isosceles" and the difference between *at least two* and *exactly
  two* congruent sides.
- Problem 3: a slope computation that shows "the line through the midpoint" is
  not enough to define a perpendicular bisector.
- Problem 4: converse of a true conditional, killed by a non-square rectangle.
- Problem 5: equal lengths do not imply parallel.
- Problem 6: the perpendicular definition used *backwards* — solve for the
  coordinate that makes it hold.
- Problems 7 and 8: the two open items — repair a definition (kite vs. rhombus)
  and construct a labelled counterexample on the supplied grid (congruent
  diagonals do not force a rectangle).

**Answer key (`ak_definitions_curr301.pdf`).** Every solution shows the
arithmetic and then says what it *proves about the definition*, which is the
part students skip. The two open problems get complete model answers plus
explicit grading guidance — what must be present (specific vertices, the two
computed lengths, the named failing condition) and what to reject.

**Study guide (`ss_definitions_curr301.pdf`, 2 pages).** Three sections: turning
a definition into a coordinate test, killing a claim with one counterexample
(including the converse warning), and repairing a loose definition. Each has a
rule box, a worked example that opens by naming the strategy, and a try-it with
its answer printed upside down inside the box.

## Verification

- **6 of 8** worksheet problems are machine-verified with SymPy from raw
  coordinates — `midpoint` (1), `distance` (2, 4), `slope` (3, 5) and `solve`
  (6). The script computes each value from the given points, so the printed
  answer key cannot drift from the figure data.
- **Problems 7 and 8 are flagged `manual`** and labelled as such. Both ask for a
  written definition or a student-constructed counterexample, which no CAS can
  check; the build reports them as manual-review items (exit 2), and the key
  supplies model answers and accept/reject criteria for the human grader.
- All 6 study-guide boxes (3 worked examples + 3 try-its) are machine-verified.
- Difficulty ramps 1 → 5 with no drops; bloom mix 2 apply / 4 analyze /
  2 justify.

**One note on the standards tag.** The task references HSG-CO.A / HSG-CO.C, but
those codes do not appear in this skill's `references/standards-map.md`, and the
skill forbids inventing codes. Because every problem here is carried out with
coordinates, the sheet is tagged `HSG-GPE.B.4–B.7` (coordinate geometry proofs),
which is in the map and genuinely describes the work.
