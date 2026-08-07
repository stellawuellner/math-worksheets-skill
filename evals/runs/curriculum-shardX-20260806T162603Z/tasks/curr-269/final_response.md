# Function Notation Is Not Multiplication — Algebra 1

Three PDFs are ready:

- **Worksheet** (`ws_fnotation_curr269.pdf`) — 8 error-analysis problems. Each one shows
  work that reads $f(x)$ as "$f$ times $x$" (dragging the function's name into the
  arithmetic, splitting $f(2+3)$ into $f(2)+f(3)$, dividing by $f$ to solve, using a
  zero-product argument on $A(t)=0$). The student repairs the computation *and* names the
  error. Two problems sit in context — a print-shop cost $C(n)$ and a draining tank $A(t)$
  — so the notation has something to mean. Difficulty ramps 1 → 5.
- **Answer key** (`ak_fnotation_curr269.pdf`) — every value worked out with the
  substitution shown explicitly, plus a written grading rubric for each diagnosis, plus a
  "Common wrong answers" note on the three problems where I designed the numbers so the
  misconception lands on a visibly different answer ($10/3$, $48$, $t=0$).
- **Study guide** (`ss_fnotation_curr269.pdf`) — 2 pages: reading the notation as an
  instruction, substituting a negative input, and solving for the input (the
  "find $f(0)$ vs. solve $f(x)=0$" distinction). Each section has a rule box, a worked
  example, and a try-it with the answer upside down inside the box.

## What is verified, honestly

This is a misconception sheet, so almost every problem has two responses — a number and a
sentence — and they are verified differently:

- **11 numeric answers machine-checked.** Every corrected value on the sheet
  (all the evaluations and both solve-for-the-input answers) was recomputed by SymPy and
  matched the key.
- **8 diagnoses are instructor-judged.** One per problem: "name the error", "explain why
  the claim fails", "say what the notation instructs you to do". No CAS grades a sentence.
  The answer key prints the rubric for each.
- Because every problem carries one of those written parts, the key's "What is verified"
  note reads **0 of 8 problems *fully* machine-checked** and lists all eight as
  instructor-judged. That is accurate and is not a defect: it means the numbers are
  checked and the reasoning still needs your eyes.
- Three misconception traps were machine-tested for distinguishability, so the wrong
  method provably lands on a different number than the right one.
- All six study-guide examples and try-its were verified.

No answer is marked `[unchecked]`.
