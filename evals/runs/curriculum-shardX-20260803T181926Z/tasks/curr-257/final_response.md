# Multi-Step Linear Equations with Rational Coefficients — Algebra 1

Three PDFs are ready: the student worksheet, a full step-by-step answer key, and a
two-page study guide.

**Worksheet (6 pages, 12 problems).** Every problem has fractional (rational)
coefficients and needs more than one move to solve. The ramp runs from two-step
equations with a single fraction (1–2), through clearing two denominators with the
LCD and distributing a fraction over a binomial (3–4), to equations with the
variable on both sides (5, 8), inequalities with rational coefficients (6, 9), and
finishes with two challenge problems: a fraction inside a fraction (11) and three
fractional terms across both sides (12). No two problems share a skeleton. Problem
10 asks only for the cleared integer equation, which is where students see *why*
multiplying by the LCD is legal. Each problem has 5–8 cm of work space and its own
answer blank.

**What was verified.** All 12 answers were checked independently with SymPy before
anything was typeset: 9 `solve` checks, 2 `inequality` checks (the solution set,
including the reversed symbol in problem 9), and 1 `equiv` check proving the cleared
equation in problem 10 really is equivalent to the original. The answer key's boxed
answers were then machine-bound to those verified values problem by problem, so a
typo in the key cannot survive. **Nothing on this sheet is flagged for manual
review** — every answer is machine-checkable, and every one passed.

**Answer key (3 pages).** Each problem is restated and solved in numbered steps
(what the move is *and* why), with a substitution check back into the original
equation. A quick-answer bank for fast grading sits under the title, and the
generated Curriculum section lists the course level, the standard, and the
difficulty range — the grade level appears only here, never on the student's pages.

**Study guide (2 pages).** Three sections, each with a rule box, a worked example,
and a try-it whose answer is printed upside down inside the box: clearing fractions
with the LCD, variable on both sides, and inequalities with rational coefficients.
The six study-guide answers were verified by the same gate as the worksheet.

**One note on tagging.** All 12 problems are tagged `HSA-REI.A.1` (justifying the
steps of an equation solution), which is the closest row in the skill's standards
map. There is no row in that map for HSA-REI.B.3 (solving linear equations *and
inequalities* in one variable), which is the exact code for problems 6 and 9; rather
than invent a code, I used the in-map cluster code and am flagging the gap.
