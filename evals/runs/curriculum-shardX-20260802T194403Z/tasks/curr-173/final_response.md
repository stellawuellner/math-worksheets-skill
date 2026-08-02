Here are the three documents for the Grade 6–7 expressions workshop on the
distributive property and combining like terms.

**Worksheet — 10 problems, each paired with a representation.** Every problem
prints the expression *and* a model that stands for it: an area model for
distribution (1, 6, 8), a tape diagram for repeated groups (2, 5), a
like-terms sorting table (3, 4), a distribute-and-subtract table (7), and a
givens/cost table for the application (9). Givens and units are stated in the
stem (metres, minutes, markers, square inches, dollars). The four subskills are
interleaved after the warm-up so the student has to choose a method: distribute
over a sum → combine like terms → distribute then combine → factor out the
greatest common factor. Problem 9 is a two-part application (simplify, then
evaluate at x = 7); problem 10 is a find-and-fix-the-error challenge on the
classic `3(2x − 5) = 6x − 5` slip.

**Answer key — step by step.** Each solution explains *why* the step is legal,
not just what was written: the area model justifies distribution, the sign
rule is spelled out for `−3(x − 2)`, factoring is presented as the area model
run backwards, and two solutions include a substitution check (m = 10 in
problem 4, x = 7 in problem 9) that shows equivalent expressions agree at every
value.

**Study guide — 2 pages, four sections** matching the four worksheet subskills.
Each has a rule box (with the reason behind the rule), a worked example whose
first step names why that method applies, and a try-it whose answer is printed
upside down inside the box. A watch-out box flags the incomplete-distribution
error.

**Verification.** All 10 worksheet answers are machine-checked with SymPy:
3 `expand` checks, 4 `equiv` equivalence checks, 2 `factor` checks, and 1
`eval` (the x = 7 evaluation, 78 dollars). All 8 study-guide results are checked
the same way. Nothing is flagged manual. One caveat worth naming: problem 10
also asks the student to *say* which number Jamal failed to multiply — that
written explanation is teacher-judged, and only the corrected expression
(6x − 15) is machine-verified. The answer key says so on the page. The full gate
chain is green, including facet coverage (each of the four facets has a
study-guide worked example) and per-problem binding of every boxed answer to its
verified value.
