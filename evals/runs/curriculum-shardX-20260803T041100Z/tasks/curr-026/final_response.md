# Subtraction Within 10 — Taking Away Objects and Writing Subtraction Equations

Three PDFs for a kindergarten / first-grade learner:

- **Worksheet** (`ws_subtraction_curr026.pdf`) — 8 problems, all in the requested
  focus. Every problem is a take-away situation attached to a concrete model
  (rows of counters, a row of stars, a full ten-frame, a draw-your-own picture)
  and every problem asks the child to connect that picture to the notation
  `start − taken away = left`. Problems 1–5 give the start number and the number
  taken away; problems 6–8 give the start and what is *left* and ask for the
  missing part, which is the harder direction of the same equation.
  Work space is 3–4.5 cm per problem so a five- or six-year-old has room to draw
  and cross out.
- **Answer key** (`ak_subtraction_curr026.pdf`) — full reasoning, not answers
  only: each solution says which group to count, shows the counting-on or
  counting-back route a child would actually use, and writes the whole equation.
  A generated quick-answer bank sits under the title block for fast grading, and
  it prints the three declared misconception traps ("if they got 5 …", "if they
  got 14 …", "if they got 6 …") so a wrong answer tells the adult *which* error
  it was.
- **Study guide** (`ss_subtraction_curr026.pdf`) — one page, three sections
  matching the three worksheet skills (take away with objects · write the
  equation for a story · find the missing part). Each section has a rule/model
  box, a two-step worked example, and a separate try-it with the answer printed
  upside down, plus one watch-out box for the two errors this topic produces.

## Verification

All 8 worksheet answers and all 6 study-guide answers are machine-verified with
SymPy — 5 `eval` checks (take-away arithmetic) and 3 `solve` checks (missing
part). **Nothing is flagged manual**; this topic has no genuinely open response,
so nothing needed to be. Three misconception traps are declared and were checked
to be distinguishable from the correct answers.

`bash scripts/build.sh` finished **BUILD PASSED** with all 21 gates green on the
first attempt. Standards tag is `K.OA.A / 1.OA.C.6 / 2.OA.B.2`, copied verbatim
from `references/standards-map.md` (the row that covers add/subtract within 20);
difficulty ramps 1, 1, 2, 2, 2, 3, 3, 4.

One note on the gate log: the study-guide prose report shows 87% number match.
The three flagged numbers are the spoken counting sequences inside the worked
examples ("6, 7, 8" when counting up from 5 to 8) — deliberate instructional
text, not givens, which is exactly the false-flag class that report documents.
