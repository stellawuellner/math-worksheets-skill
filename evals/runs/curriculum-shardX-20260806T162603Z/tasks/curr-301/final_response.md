# Precise Definitions and Counterexamples — high-school geometry (8 problems)

Three PDFs are ready:

- **Worksheet** (`ws_definitions_curr301.pdf`, 6 pages) — 8 guided-concept problems on
  the two moves that make geometry definitions usable: reading a definition exactly, and
  disproving a sloppy claim with a counterexample. Each problem that needs a picture has
  its own labelled diagram (segment with a marked midpoint, an angle with its bisector,
  a linear pair, a perpendicular pair, two congruent segments). The diagrams carry
  labels only — every measurement is stated in the problem text, so no figure can be
  read as belonging to the problem beside it.
- **Answer key** (`ak_definitions_curr301.pdf`) — the equation each definition produces,
  worked line by line, plus a model answer *and* a grading note for every open item, so
  you know which part of a student's sentence is the part that must be there.
- **Study guide** (`ss_definitions_curr301.pdf`, 2 pages) — three sections: reading a
  definition exactly, turning a definition into an equation (midpoint, bisector,
  congruent segments), and building a counterexample. Each has a rule box, a short
  worked example, and a try-it with the answer upside down inside the box.

## What is verified, and what is not

**6 of the 13 responses are machine-checked with SymPy** — every algebraic answer:
problem 2 ($x = 5$), problem 4 ($x = 8$ and the $84^\circ$ whole angle), problem 5's
$x = 20$, and problem 7 ($x = 5$, $PQ = 11$ cm). The study guide's four worked examples
and both try-it answers are verified the same way.

**7 responses are flagged for your judgement** — problems 1, 3, 6 (both parts), 8 (both
parts) and part (a) of problem 5. These are definitions repaired in words and
counterexamples described in words; no computer algebra system can grade prose, and the
skill this sheet is built around lives precisely there. The answer key gives a model
answer for each, and states what a correct response *must* contain — for a
counterexample, a case that genuinely satisfies the "if" part plus an explicit reason
the "then" part fails. The Quick Answers bank marks these with `---`, and the key's
"What is verified" note names them. There are no `[unchecked]` marks: every printed
response is covered by either a machine check or a written rubric.

## Notes

Standards: HSG-CO.A (precise definitions of angle, perpendicular, segment) and
HSG-CO.C (angle relationships) — the codes and the difficulty range are printed in the
key's Curriculum block. Difficulty ramps 1 to 5, finishing with a synthesis item where
the student must both break a definition with a counterexample and then repair it.
