Here are the three PDFs for a 12-problem precalculus review set on **connecting the
numerical, graphical and algebraic ideas of a limit**.

**Worksheet — `ws_limitviews_curr445.pdf` (6 pages).** Problems 1 and 2 are the warm-up:
the same limit reached once by algebra and once by a table. After that the four views —
algebra, a table of values, a graph, and a series sum as the limit of its partial sums —
are interleaved so no two consecutive problems use the same one and the student has to
decide which view the problem is asking for. Difficulty ramps 1 → 5.

Several problems are built to force the connection rather than assert it. Problem 2 has the
student compute $f(3.9)$ and $f(4.1)$ *and* the exact limit, so the table and the algebra
answer the same question. Problem 5 pairs the fourth partial sum with the infinite sum, so
$S_4 = 45/8$ and the sum $6$ sit next to each other. Problem 10 has the student watch
$(1+1/n)^n$ climb toward $e$ and then say why a table cannot prove it. Three problems come
with a blank coordinate grid to sketch on, and the closing synthesis item asks for a limit
that exists at a point where the function is nonetheless discontinuous.

**Answer key — `ak_limitviews_curr445.pdf` (4 pages).** Every problem restated and worked
line by line — conjugates, factorings and the telescoping partial sum written out — with a
quick-answer bank, a curriculum block, and a "common wrong answers" list from two
machine-checked traps (reading $0/0$ as $0$, and "cancelling" inside a radical).

**Study guide — `ss_limitviews_curr445.pdf` (2 pages).** Four sections, one per view, each
with the rule, a worked example that opens by naming why that view applies, and a try-it.

**What was verified, honestly.** The sheet asks for **25 separate responses**. **19 are
machine-checked** with SymPy: every limit computed symbolically (including the one-sided
pair in problem 3), both series sums, and all six table values recomputed exactly and
compared at four decimal places. **6 are instructor-judged** and marked `---` in the
quick-answer bank: the three sketch-and-conclude items (problems 3, 7 and 12), the
partial-sum argument in 9(b), the "why a table is not a proof" item in 10(c), and the
"why cancelling is legal" item in 11(b). Those are hand-drawn graphs and written reasoning,
which no computer algebra system can grade — so for each one the key prints a full model
answer, including exactly which points must be open and which closed, plus an explicit
full-credit criterion. The eight study-guide examples and try-its are machine-checked.

No response is marked `[unchecked]`.
