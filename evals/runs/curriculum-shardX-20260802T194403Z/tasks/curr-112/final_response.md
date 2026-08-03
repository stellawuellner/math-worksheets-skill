# Whole-Number Division: Up to Four Digits by One-Digit Divisors (Grades 4–5)

Three PDFs are ready for a fourth- or fifth-grade student practising long
division with one-digit divisors.

- **Worksheet (12 problems).** The ramp runs 1 → 5. Problems 1–3 are three-digit
  warm-ups, including $618 \div 6$, where the tens place needs a $0$ in the
  quotient. Problem 4 estimates $2{,}835 \div 7$ with the compatible number
  $2{,}800$ and problem 5 divides it exactly, so the estimate has something to be
  checked against. Problem 6 is the first remainder. Problem 8 works backwards
  from a quotient to the missing dividend. Problems 10 and 11 are deliberately
  the same division, $3{,}275 \div 6$, asked two different ways — how many *full*
  boxes, and how many pencils are *left over* — because deciding what the
  remainder means is the skill, not the arithmetic. Problem 12 chains two
  divisions. Every problem has at least 4.5 cm of ruled-off work space plus its
  own answer line.
- **Answer key.** Every solution is worked place by place ("28 hundreds $\div$ 7
  = 4 hundreds; 3 is smaller than 7, so write 0 in the tens place"), and each
  ends with a multiplication check. The generated quick-answer bank sits directly
  under the title block for fast grading, followed by a **Common wrong answers**
  block built from the declared traps.
- **Study guide (2 pages).** Four sections — the divide/multiply/subtract/bring
  down cycle, four-digit dividends and zeros in the quotient, remainders and what
  they mean in a story, and estimating with compatible numbers. Each section has
  a rule box, a worked example that opens by saying *why* that method applies,
  and a try-it with the answer printed upside down inside the box.

## Verification

All **12 of 12** worksheet problems and all **8** study-guide boxes (4 worked
examples + 4 try-its) were machine-checked with SymPy. Nothing on this sheet is
open-ended, so nothing is flagged `manual`.

**Seven misconception traps are declared and machine-checked** (problems 3, 5, 6,
9, 10, 11, 12): the dropped zero in the quotient at three different place values
(13, 45, 69), the remainder written as a decimal digit (129.1), rounding the
leftover up to an extra box (546), reporting the quotient where the leftover was
asked for (545), and stopping after the first of two divisions (594). Each was
proved distinguishably wrong by the problem's own check, and each prints in the
key's "Common wrong answers" block so a wrong paper names its own error.

Every standard is tagged `4.NBT.B.6` from `references/standards-map.md`.

The full gate chain — template use, both verification files, skill and facet
coverage, subtitle binding, layout and work space, answer-line binding,
compilation page budgets, per-problem answer-key binding, study-guide structure,
and prose consistency — is green: **BUILD PASSED, all gates green (exit 0)**, on
the first attempt. The answer key carries the quick-answer bank with no
`\raggedright` or `\emergencystretch` around it and compiles with no overfull box.
