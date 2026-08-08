# The Zero That Holds a Place — Grade 2 error analysis

Three PDFs are ready:

- **Worksheet** (`ws_zeroexp_curr054.pdf`) — 8 misconception-focused problems on
  zero-placeholder errors in expanded form, including three find-and-fix items:
  Nia's 830 = 800 + 3, Owen's 402 = 400 + 20, and Kai's claim that 506 and 56 are
  equal. The rest practice the two directions the errors come from (expanded form
  of 507/640, standard form of 600 + 3 and 200 + 9), ending with a two-part
  challenge (5 hundreds, no tens, 3 ones).
- **Answer key** (`ak_zeroexp_curr054.pdf`) — worked reasoning per problem, a
  quick-answers bank, and a "common wrong answers" block built from the seven
  declared misconception traps (57, 63, 29, 803, 420, 604, 53) so grading doubles
  as diagnosis. Curriculum section tags 2.NBT.A.
- **Study guide** (`ss_zeroexp_curr054.pdf`) — three sections: expanded form with
  an empty place, keeping the placeholder in standard form, and a
  find-the-error checklist with a worked fix (Jade's 520 = 500 + 2).

**Verification split:** 9 of 12 responses are machine-verified with SymPy — every
corrected expanded form (checked as an identity, e.g. 800 + 30 = 830), every
standard-form answer, and the comparison 506 > 56. All seven planted wrong results
are machine-checked traps, proven to give visibly wrong values. **3 responses are
instructor-judged**: the written diagnoses in problems 4, 5, and 7 (naming the
error / explaining the zero) — the key prints a model diagnosis for each, and its
"What is verified" note marks the same three. All study-guide examples and
try-its are machine-verified, including the two error-analysis boxes.
