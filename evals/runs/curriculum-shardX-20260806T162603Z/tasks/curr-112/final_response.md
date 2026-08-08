# Dividing by a One-Digit Number — Grade 4 (12 problems)

Three PDFs are ready:

- **`ws_longdivision_curr112.pdf`** — the student worksheet (4 pages)
- **`ss_longdivision_curr112.pdf`** — a 2-page skills summary
- **`ak_longdivision_curr112.pdf`** — the full step-by-step answer key (3 pages)

## What the worksheet covers

Dividends grow from two digits to four, and three methods interleave so the child chooses rather than
repeats:

- **Long division (1, 2, 4, 6, 8, 12)** — from $84 \div 4$ up to $5{,}207 \div 9$, with and without
  remainders. Problems 4 and 8 ask for the quotient and the remainder in separate blanks, so the two
  are named rather than run together as "59 r 3".
- **Partial quotients (3, 7, 10)** — $258 \div 6$ and $4{,}872 \div 7$ are scaffolded chunk by chunk
  (take out 40 groups, then 600 groups), with each intermediate step given its own blank. Problem 7,
  $618 \div 6$, is the zero-in-the-quotient case, and the child has to explain why that zero must be
  written.
- **Estimate and check (5, 9, 11)** — round the dividend, estimate, then divide exactly and see which
  side of the estimate the answer lands on. Problem 11 runs the operation backwards: $1{,}908$
  divided by an unknown one-digit number gives exactly $212$ — find the divisor.
- **12** closes with $7{,}236 \div 4$ plus the reasoning question: how could you tell *before*
  dividing that the quotient would have four digits?

Every answer key solution ends with the multiply-back check, which is the habit the sheet is trying
to build. Difficulty ramps 1 → 5.

## What is verified, and what is not

- **25 of the 27 checks are machine-verified** with SymPy, across all 12 problems, and **10 of the 12
  problems are fully machine-checked**. Every quotient, every remainder, every partial quotient and
  every rounded number was recomputed independently of the answer key.
- **Two responses are instructor-judged**, marked `---` in the key's Quick Answers list: problem 7(b),
  why the zero in the quotient has to be written, and problem 12(b), how to predict the number of
  digits before dividing. The key gives model answers for both and says what falls short — on 12(b),
  simply stating 1,809 is not full credit, because the question asks for the reasoning that comes
  first.
- Two **common wrong answers** are declared and machine-checked as genuinely wrong, and printed in the
  key: 13 on problem 7 and 189 on problem 12. Both are the same error at different scales — dropping
  the zero out of the quotient — and the multiply-back check catches both immediately.

## The study guide

Three sections: long division as the four repeating moves (divide, multiply, subtract, bring down),
partial quotients as the take-out-easy-chunks alternative, and estimate-first/check-after. Each has a
rule box, a worked example that opens by saying why that method applies, and a try-it with the answer
upside down inside the box. The watch-out box states the sheet's main hazard: a $0$ in the quotient
is a digit, not a gap.

The grade level and standards code (4.NBT.B.6) appear on the answer key only.
