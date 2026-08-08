# Diagnosing Transformation-Order and Inverse-Domain Errors — three PDFs

An 8-problem precalculus error-analysis set, plus the worked answer key and a
two-page study guide.

| File | What it is |
|---|---|
| `ss_transformerrors_curr404.pdf` | Study guide (2 pages) |
| `ws_transformerrors_curr404.pdf` | Student worksheet, 8 problems (5 pages) |
| `ak_transformerrors_curr404.pdf` | Step-by-step answer key (3 pages) |

**Every problem is a find-and-fix.** Each shows a specific wrong claim or a
wrong answer, and asks for two things: the correct value, and a written
diagnosis naming the rule that was broken. Both halves are graded, and the
sheet says so in the directions — "they got a different number" is a check, not
a diagnosis.

The eight problems cover the three errors that produce almost all of these
mistakes:

* **Inside vs outside** (#1, #6) — `f(x)+5` against `f(x+5)`, and the claim that
  `f(2x)` stretches horizontally when it in fact compresses. #6 makes the
  student produce the evidence: the same height that was reached at x = 16 is
  now reached at x = 8.
* **Order of operations** (#2, #4, #7) — shifting before stretching (so the
  shift gets multiplied), and reflecting after a vertical shift (so the shift
  gets negated).
* **Inverse domain** (#3, #5, #8) — √x offered as the inverse of x² with no
  restriction, a domain claim of "all reals" on an inverse whose inputs are the
  range of the original, and finally a restricted parabola where the branch
  decides the sign of the square root.

**Four planted wrong answers are declared as machine-checked traps** (#2, #4,
#7, #8). For each, the verifier independently computed the value the named wrong
method produces — 2, −6, −5 and 5 — and confirmed the problem's own check
rejects it. Those appear in the key under "Common wrong answers", so a student
handing back −6 on #4 is instantly identifiable as having multiplied the shift.

**How much is machine-checked — honestly.** There are 19 responses across the 8
problems. **11 were recomputed with SymPy** and matched against the key.
**8 are instructor-judged** — the written diagnosis on every single problem,
marked `---` in the Quick Answers bank. That is the correct split for an
error-analysis sheet: the diagnosis is the point of the exercise, and no
software can grade prose. The key prints a grading note for each one, saying
what a correct diagnosis must name and what partial answers to reject.

All six study-guide items are fully machine-verified.
