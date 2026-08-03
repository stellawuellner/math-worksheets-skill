Three PDFs are ready for a kindergarten/Grade-1 learner on composing and
decomposing numbers to 10, focused on repairing a number-bond fact family that
is either missing a fact or says the same fact twice.

- **Worksheet** (6 problems, `ws_numberbonds_curr019.pdf`) — every problem shows
  its own number bond, so the whole and the parts are always visible. A warm-up
  finds a missing part (whole 6, part 4); three find-and-fix items follow: Mia
  writes 12 for the missing part of a bond with whole 9 and part 3 (she added
  instead of taking away), Ben writes the take-away fact 9 − 7 = 2 twice, and Ana
  repeats the adding fact 6 + 4 = 10 where the second take-away fact belongs.
  Problem 5 fills the blank in the fourth fact of Jo's family, and the challenge
  has Sam's family with *both* take-away facts missing (two answers). Work space
  runs 3.5–4.5 cm per problem, declared as `workspace_cm` where a problem needed
  more than the type default.
- **Answer key** (`ak_numberbonds_curr019.pdf`) — four to five numbered reasoning
  steps per problem (name the whole and the parts, decide add or take away,
  compute, check by adding the parts back), a generated quick-answer bank for
  fast grading, and a generated "Common wrong answers" block that tells the
  grader what a 12, a repeated 9 − 7 = 2, or a repeated 6 + 4 = 10 means.
- **Study guide** (2 pages, `ss_numberbonds_curr019.pdf`) — three skills matching
  the worksheet tags: find the missing part, spot a fact written twice, write the
  whole family of four facts. Each has a rule/model box (including a labelled
  blank bond), a two-step worked example, and an upside-down try-it, plus a
  watch-out box on why turning an *adding* fact around makes a new fact but
  writing the same take-away fact twice does not.

**Verification.** All 7 worksheet checks (problem 6 carries two, one per missing
fact) and all 6 study-guide results were machine-checked with SymPy: two `solve`
missing-number checks and five `eval` part/whole computations on the worksheet.
Nothing is flagged manual — every item on this sheet has a single checkable
number. The three planted wrong answers (12, the repeated 9 − 7 = 2, the repeated
6 + 4 = 10) are declared misconception traps, so the verifier proved each planted
result is distinguishably wrong and that the printed wrong number really is what
the wrong method computes. The full gate chain is green, including the
per-problem binding of every printed answer to its verified value and the
figure-label check on all six bonds.

Standards: every problem is tagged `K.OA.A` from `references/standards-map.md`.
