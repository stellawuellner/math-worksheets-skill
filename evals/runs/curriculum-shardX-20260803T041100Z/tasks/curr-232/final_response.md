# Evaluating functions from rules, tables, and graphs (Grade 8 / Pre-Algebra)

Three PDFs are ready for an eighth-grade or pre-algebra learner.

**Worksheet — 12 problems.** One shared coordinate plane, **Graph A**, sits with
the directions (not beside any single problem, so it can never be mistaken for one
problem's givens); it shows $f(x)=2x-1$ solid and $g(x)=-x+5$ dashed, and the
directions name exactly which problems use it. The set interleaves four kinds of
task after a short warm-up:

- *From a rule* (1, 2, 4, 9) — including $f(-3)$ for $x^2-5$, where the sign must go
  inside the parentheses before squaring.
- *From a table* (3, 6, 10) — read a listed output; find the **input** with the
  smallest output (an input, not a height); and find how much larger $C(6)$ is than
  $C(2)$ in a joining-fee cost table.
- *From a graph* (5, 7) — read $f(3)$ off the solid line and $g(1)$ off the dashed one.
- *Comparing two functions at one input* (8, 11, 12).

Difficulty ramps 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 5. Problems 3, 6, and 10 print a
table inside the problem block, so each declares extra `workspace_cm` rather than
having the sheet compressed to fit a page target; the worksheet runs 6 pages.

**Answer key.** Every solution shows the substitution or the read, not just the
result: which column of the table was read, which line on the graph, and (for the
graph problems) a cross-check against the algebraic rule. Problem 2 carries a
declared misconception trap — the $-3^2-5=-14$ sign error — printed in the key's
quick-answer bank so the grader can name the mistake.

**Flagged for manual review: problem 12** is a written explanation of why the two
graphs meet at $x=2$ and what that means for comparing $f$ and $g$ on either side.
That is genuinely open reasoning, so it is declared `manual` rather than
machine-verified; the key gives a three-bullet model answer plus what to accept.
The build therefore exits 2 with one manual item, which is the correct outcome, not
a failure.

**Study guide (2 pages).** Three skill sections, each with a rule box, a worked
example, and a distinct upside-down try-it:

1. Evaluate a function from its rule (substitute in parentheses; $f(3)$ is not $f\cdot 3$).
2. Read a value from a table or a graph — the try-it includes a small graph to read.
3. Compare two functions at the same input, and what a crossing point means.

**Verification.** 11 of 12 worksheet answers are machine-checked with SymPy
(`eval`, `read_data`, and `compare` checks); the twelfth is the declared manual
explanation. All 6 study-guide results are machine-checked. The full gate chain is
green: every printed boxed answer binds back to its verified value, and each table
and graph is drawn from the same `data` array its check reads, so the display and
the answer cannot disagree.

Standards tag: `8.F.A.1–8.F.B.5`, taken verbatim from the skill's standards map.
