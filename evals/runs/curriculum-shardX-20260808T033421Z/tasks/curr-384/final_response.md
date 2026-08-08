# Find-the-mistake set: composition order and inverse domains

Three PDFs for your Algebra 2 student, all built around the two errors the task named —
running a composition in the wrong order, and accepting an "inverse" nobody checked:

- **`ws_compinv_curr384.pdf`** — the student worksheet, 8 problems, 5 pages.
- **`ak_compinv_curr384.pdf`** — the full step-by-step answer key, 4 pages.
- **`ss_compinv_curr384.pdf`** — a 2-page study guide.

## How the worksheet is built

Every problem sits on one of the two named misconceptions, and four of the eight are
explicit find-and-fix items where a wrong answer is printed and the student has to produce
the correct one **and** name the move that produced the wrong one:

- **Problem 1** sets the trap up honestly: compute both compositions of the same two rules at
  the same input, and watch them disagree (17 versus 27).
- **Problem 2** (find and fix) — a quoted answer of $-2$ that is the other composition.
- **Problem 3** — a claimed inverse that "divides instead of multiplying and leaves the
  constant alone"; the round trip comes back 21 instead of 5, refuting it.
- **Problem 4** — the classic unverified domain: $\sqrt{x-1}$ against $x^2+1$, which returns
  $3$ when you feed it $-3$.
- **Problem 5** (find and fix) — a composed *rule*, $x^2-4$, that is the other order.
- **Problem 6** — find an inverse and then state the restriction the formula must carry.
- **Problem 7** (find and fix) — "just turn it upside down", the reciprocal-is-not-inverse error.
- **Problem 8** — the synthesis: the two compositions of $x+3$ and $x^2$ agree at exactly one
  input, and the student has to find it and say why there cannot be a second.

## Planted wrong answers are machine-checked

Every wrong number printed on the sheet is declared as a misconception trap and recomputed
by the verifier, which also confirms that each one is *distinguishably* wrong — a trap the
problem's own check would accept is rejected as a bad problem design. Four traps are
declared (problems 2, 4, 5, 7), and the answer key prints them in a **Common wrong answers**
block, so grading tells you which error a student made rather than just that they missed it:

- $-2$ on problem 2 — reversed composition.
- $-3$ on problem 4 — assuming a square root returns the original input.
- $45$ on problem 5 — squaring before subtracting.
- $0.125$ on problem 7 — flipping the fraction instead of solving for the input.

## What was verified, and what was not

The key's "What is verified" note is generated from the same data and says it plainly:
**13 of the 19 answers are machine-checked with SymPy; 6 are instructor-judged.**

- **Machine-checked (13):** every corrected value, every composed rule, every inverse
  formula, and the single input in problem 8 were recomputed independently. A printed answer
  that disagreed would have blocked the build.
- **Instructor-judged (6):** the diagnosis half of problems 2, 4, 5, 6, 7 and 8 — "explain
  which composition was carried out", "justify the restriction", "why can they agree only
  once". Error analysis is two responses, not one: the correction is a value and can be
  checked; the diagnosis is prose and cannot. Each is marked `---` in the Quick Answers bank,
  and the key prints a grading note saying what a correct response must contain and what to
  reject (for instance, "arithmetic slip" is not a diagnosis).

## Study guide

Three sections, each with a rule box, a worked example whose first step says why the method
applies, and a try-it with the answer upside down inside the box: reading a composition
inside out, the two-sided test for a claimed inverse, and the domain an inverse inherits from
the range of the original. All 8 of its worked answers are machine-verified.
