# Sign and Conjugate Errors — Algebra 2 error-analysis set

Three PDFs are ready:

- **`ss_signfix_curr354.pdf` — Skills Summary (2 pages).** Three sections with a
  rule box, a worked example and a try-it: products and the sign of $i^2$,
  distributing a subtraction sign, and choosing the right conjugate. Each rule
  box names the specific way the rule is broken, so the guide reads as a
  checking tool rather than a formula dump. The watch-out box says where to look
  first when auditing someone else's division.
- **`ws_signfix_curr354.pdf` — Student worksheet (4 pages), 8 problems.**
  **Four** of the eight are find-and-fix items — a printed student solution
  containing exactly one mistake — well past the two the brief asked for. Each
  asks two things: work it correctly, and name the error. The other four are
  clean computations that set up the same three error types. Difficulty runs
  1 → 5, ending with a three-line solution where the student must identify which
  line is the *first* one that is wrong.
- **`ak_signfix_curr354.pdf` — Answer key (3 pages).** Every solution is worked
  through, and every diagnosis has an explicit rubric: what full credit
  requires, and what earns nothing. The Quick Answers bank, curriculum block
  (HSN-CN.A.2 and HSN-CN.A.3) and a "Common wrong answers" section sit at the
  top.

## What is verified, and what is not

The set carries **12 declared responses across 8 problems. 8 are machine
checked** — every corrected value was recomputed with SymPy, and the build
refuses to emit a PDF if a printed answer disagrees.

**4 responses are instructor-judged** (problems 3, 5, 6 and 8), and the answer
key prints `---` for them. These are the *diagnosis* halves of the find-and-fix
items: "name the error", "say which line is first wrong and state the rule".
Naming an error is prose, so no computer algebra system can grade it. The key
gives a rubric for each one, including what does not earn credit — writing the
corrected value again without saying what went wrong.

**Every planted wrong result is a declared, machine-checked trap.** Seven traps
are declared across the sheet, and the verifier proves each one is
*distinguishably* wrong: it computes the value a student following that
misconception would get and confirms the problem's own check rejects it. So the
planted errors are not merely plausible-looking — they provably cannot be
confused with the correct answer.

## One limitation worth knowing

The verification system can bind a planted wrong *number* into the printed stem
only when that number is real. Four of the seven traps on this sheet produce
complex wrong results (for example $3 - 4i$ on problem 3), and those numbers
are typed into the stem rather than generated from the trap. The trap's
*distinguishability* is still machine-checked in every case; only the printed
digits of a complex wrong value are hand-entered. The two real-valued wrong
results (11 and 21) are generated and appear in the key's "Common wrong answers"
block.

The grade level appears on the answer key only.
