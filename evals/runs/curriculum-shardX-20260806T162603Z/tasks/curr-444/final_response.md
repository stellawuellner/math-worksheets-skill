Here are the three PDFs for an 8-problem precalculus error-analysis set on **diagnosing
index-shift and convergence-condition errors**.

**Worksheet — `ws_serieserrors_curr444.pdf` (5 pages).** Every problem shows one student's
work with exactly one thing wrong in it: part (a) asks for the correct value, part (b) asks
the student to name the error. The eight items cover the four ways this material goes
wrong — miscounting which terms a sum actually contains (problems 1 and 5), shifting an
index without moving both limits (2 and 8), applying $a/(1-r)$ outside $|r| < 1$ or with the
wrong first term (3 and 6), and mishandling the limit of a rational or alternating sequence
(4 and 7). Difficulty ramps 1 → 5.

**Six of the planted wrong answers are machine-checked misconception traps.** The $21$ in
problem 1, the $363$ in problem 2, the $-2$ in problem 3, the $1$ in problem 4, the $140$ in
problem 5, the $1.67$ in problem 6 and the $6$ in problem 8 are not hand-typed: each is
computed from the wrong method's own expression, and the build confirms that the problem's
correct-answer check *rejects* it. A planted error the problem could not distinguish would
have failed the build.

**Answer key — `ak_serieserrors_curr444.pdf` (3 pages).** Every problem restated, the
correct value worked line by line, and a written model diagnosis for part (b) followed by a
sentence naming what a response must contain for full credit. Problem 8's solution goes one
step further and shows that the student's $6$ is exactly the sum of the *longer* series,
which is usually the moment the error clicks. The key opens with a quick-answer bank, a
curriculum block, and the generated "common wrong answers" list.

**Study guide — `ss_serieserrors_curr444.pdf` (2 pages).** Four sections, one per error
class, each with the rule that prevents it, a worked example, and a try-it.

**What was verified, honestly.** The sheet asks for **17 separate responses**. **9 are
machine-checked** with SymPy: every corrected sum (finite and infinite), both limits, and
the two sequence terms in problem 7. The other **8 are instructor-judged** — one per
problem, the part (b) diagnosis — and are marked `---` in the quick-answer bank. On an
error-analysis sheet that is the whole point: naming a mistake is prose, and no computer
algebra system can grade prose. The key prints a full model diagnosis and an explicit
full-credit criterion for each of the eight, so grading is a comparison. The eight
study-guide examples and try-its are machine-checked.

No response is marked `[unchecked]`.
