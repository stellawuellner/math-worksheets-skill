Here are the three documents for the Algebra 1 interleaved review on solving
quadratic equations — specifically, picking an efficient method and reading what
the roots mean.

**Worksheet — 12 problems.** Every problem has a **Method** line: the student
commits to square roots, factoring, or the quadratic formula *before* solving,
which is the skill the sheet is actually training. After a short warm-up
(1–2) the three methods are interleaved with the context problems so no two
consecutive problems reward the same reflex: square roots (1, 4, 9), factoring
(2, 6, 10), quadratic formula (3, 7), and interpret-the-roots word problems
(5, 8, 11, 12). Notable items: problem 6 (`3x² = 12x`) punishes dividing by x;
problem 8 produces a negative root that must be rejected as a width; problem 11
needs the formula and a rounded answer, with the negative time thrown out; and
problem 12 is the synthesis — break-even roots for a downward parabola, then a
judgement about whether n = 20 breaks even. Three problems carry verified units
(seconds, seconds, metres) with matching answer lines.

**Answer key — step by step.** Each solution opens by saying *why* that method
was the efficient one (no linear term → square roots; perfect-square
discriminant → it will factor; stalled factor hunt → formula), then works the
algebra, then interprets. Problems 5, 8, 11, 12 each explain what happens to the
rejected or second root, and the key includes two "common wrong answer" notes
(dividing by x; taking the negative time branch).

**Study guide — 2 pages.** A method-selection decision box up top (including the
discriminant test), then four sections — square roots, factoring, the quadratic
formula, and reading roots in context — each with a rule box, a worked example
whose first step is the choose-the-method sentence, and a try-it with the answer
printed upside down inside the box.

**Verification.** All 12 worksheet answers are machine-checked with SymPy:
11 `solve` root-set checks (including the exact radical pair −2 ± √3 and the
fractional pair 1/3, −3/2) and one `approx` check for the rounded landing time
2.62 s. All 8 study-guide results are checked the same way, and every declared
unit is bound in both directions (answer line on the sheet, unit inside the
boxed answer in the key). Two written parts are *not* machine-verified and are
labelled as such on the page: the explanation of why the negative time is
rejected in problem 11, and part (b) of problem 12 (whether the manager is
right). Their numerical companions are verified. The full gate chain is green.
