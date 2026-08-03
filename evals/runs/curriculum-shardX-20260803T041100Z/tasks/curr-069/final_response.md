# Foundations of Multiplication — Rows, Groups, and the Total

Three PDFs for a second- or third-grade learner, all aimed at one confusion:
answering "how many rows?" when the question asked "how many in all?"

- **Worksheet** (`ws_multiplication_curr069.pdf`) — 8 problems. Every problem
  forces the rows / in-each-row / total distinction: 1–3 read an array or a
  garden into `rows × in each row = total`; 4–5 are find-and-fix items where a
  named student has reported the row count (Jonah: "5 stickers, because I count
  5 rows") or has added instead of multiplied (Mia: `2 + 8 = 10`); 6–8 run the
  same relationship backwards, giving the total and asking for the missing rows
  or group size, which is where the rows-versus-total mix-up does the most
  damage. Problem 8 additionally asks the student to say in one sentence what
  the mistaken student mixed up. Work space is 3–4.5 cm per problem.
  A directions block up front names the three different questions explicitly
  and gives the size check ("the total is almost always bigger than the number
  of rows").
- **Answer key** (`ak_multiplication_curr069.pdf`) — reasoning, not answers.
  Each solution names the two counts before it multiplies, shows the actual
  skip-counting route a 7–8 year old would use (4, 8, 12, 16, 20), and checks
  the missing-number problems by multiplying back. The generated quick-answer
  bank sits under the title block and prints the four declared misconception
  traps, so a wrong paper tells the adult *which* error it was.
- **Study guide** (`ss_multiplication_curr069.pdf`) — one page, three sections
  matching the three worksheet skills (read an array as multiplication · fix a
  rows-versus-total mistake · find the missing rows or group size). Each has a
  rule/model box, a two-step worked example, and a separate try-it with the
  answer printed upside down, plus one watch-out box with the "say out loud what
  your answer counts" habit.

## Verification

All 8 worksheet answers and all 6 study-guide answers are machine-verified with
SymPy: 5 `eval` checks (array totals) and 3 `solve` checks (missing factor) on
the worksheet, 4 `eval` + 2 `solve` on the guide. **Nothing is flagged manual** —
this topic has no genuinely open response, so nothing needed to be.

Four misconception traps are declared and machine-checked as distinguishable
from the correct answer:

| Problem | Planted wrong result | Error it targets |
|---|---|---|
| 2 | 4 | wrote the number of rows instead of the total |
| 3 | 9 | added 6 + 3 instead of multiplying |
| 4 | 5 | reported the number of rows as the total |
| 5 | 10 | added 2 + 8 instead of multiplying |

`bash scripts/build.sh` ends **BUILD PASSED**, all 21 gates green.

Standards codes are copied verbatim from `references/standards-map.md`:
`3.OA.C.7` (times tables / multiply-and-divide facts) for the array-reading
problems and `3.OA.A.3 / 4.OA.A.2` (multiplication/division word problems) for
the story and missing-number problems. The task's `standard_refs`
("3.OA.A.1–3.OA.A.3") is not a row in that file, so the two closest real rows
were used rather than an invented code. Difficulty ramps 1, 2, 2, 3, 3, 3, 3, 4.

One note on the gate log: the study-guide prose report shows 73% number match.
Every flagged number is a spoken skip-counting sequence inside a worked example
("4, 8, 12, 16, 20"), which is instructional text rather than a given — the
documented false-flag class for that heuristic report. The worksheet's own prose
report is 100%.

## Build notes

One gate failed on the first attempt: `compile-ws`, an overfull `\hbox`
(203pt) where the directions block's closing `\noindent\rule{\linewidth}` was
absorbed into the preceding prose paragraph. Adding the paragraph break before
the rule fixed it; everything else was green first time.
