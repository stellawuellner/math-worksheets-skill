# Multiplying by a One-Digit Number — Grade 4 (12 problems)

Three PDFs are ready:

- **`ws_multidigit_curr107.pdf`** — the student worksheet (4 pages, generous work space)
- **`ss_multidigit_curr107.pdf`** — a 2-page skills summary
- **`ak_multidigit_curr107.pdf`** — the full step-by-step answer key (3 pages)

## What the worksheet covers

Numbers grow from two digits to four across the sheet, and three methods interleave so the child has
to pick one rather than repeat one:

- **Standard algorithm (1, 2, 5, 7, 9)** — starting at $63 \times 4$ and finishing at
  $5{,}704 \times 9$. Two of these carry a zero digit inside the number, which is where most
  four-digit errors live.
- **Partial products (3, 4, 10)** — $214 \times 3$ written out by place value, a filled-in area model
  for $1{,}325 \times 4$, and then $3{,}208 \times 6$, where one partial product is $0$ and the child
  has to write it down rather than skip the column.
- **Estimate and apply (6, 8, 11, 12)** — round the large factor, estimate, then multiply exactly;
  a theatre-seats problem that goes the other way (exact first, then round the answer); and a
  reasonableness judgement on a bricks problem.

Every partial product has its own blank and its own check, so the *method* is verified and not just
the final total. Difficulty ramps 1 → 5.

## What is verified, and what is not

- **28 of the 30 checks are machine-verified** with SymPy, covering **10 of the 12 problems fully**.
  That count is high because every partial product, every rounded number and every intermediate
  estimate is checked separately — problem 4's area model alone carries five checks.
- **Two responses are instructor-judged**, marked `---` in the key's Quick Answers list: problem
  11(d), whether the exact answer is reasonable and why, and problem 12(b), why the tens digit of
  $1{,}608 \times 5$ is not zero. Both are reasoning, not arithmetic. The key gives a model answer
  for each and says what falls short — on 11(d), answering "yes" without comparing to the estimate is
  not full credit.
- Three **common wrong answers** are declared and machine-checked as genuinely wrong, and printed in
  the key: 242 on problem 1 (never carried the regrouped ten), 1,835 on problem 5 and 5,166 on
  problem 9 (dropped a zero digit out of the number, which is the same error twice at different
  scales). If a child's answer is one of those, the key names the misunderstanding.

## The study guide

Three sections: the standard algorithm with carrying, partial products as the no-carrying fallback,
and estimating before multiplying. Each has a rule box, a worked example whose first step says why
that method applies, and a try-it with the answer upside down inside the box. The watch-out box
addresses the sheet's main hazard directly: never drop a zero digit to make a number shorter — it
holds its column open, often for a carry.

The grade level and standards code (4.NBT.B.5) appear on the answer key only.
