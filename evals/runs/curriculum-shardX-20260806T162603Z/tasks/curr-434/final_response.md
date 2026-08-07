Here are the three PDFs for an 8-problem precalculus error-analysis set on **diagnosing
quadrant and parameter-orientation errors**.

**Worksheet — `ws_polarerrors_curr434.pdf` (5 pages).** Every problem shows one student's
work with exactly one thing wrong in it. Part (a) asks for the corrected value; part (b)
asks the student to name the error in a sentence or two — that diagnosis is the point of
the sheet, so it is asked explicitly rather than left implied. The eight items cover the
four ways this topic goes wrong: the arctangent key reporting a first- or fourth-quadrant
angle for a left-hand point (problems 1–2), a negative $r$ converted with its sign dropped
(problems 6–7), orientation destroyed by eliminating the parameter (problems 3–4), and a
domain quietly lost in the same elimination (problems 5, 8). Difficulty ramps 1 → 5.

**Answer key — `ak_polarerrors_curr434.pdf` (3 pages).** Each problem restated, with the
corrected computation worked line by line and a written model diagnosis for part (b),
followed by a sentence saying what a response must contain to earn full credit. The key
opens with a quick-answer bank, a curriculum block, and a "common wrong answers" list.

**Three planted wrong results are machine-checked traps**, as asked. The $-0.79$ in
problem 1, the $1.05$ in problem 2, and the $x = 2$ in problem 6 are not hand-typed
numbers — each is computed from the wrong method's own expression and then tested to
confirm the problem's correct-answer check *rejects* it. A trap the problem could not
distinguish would have failed the build, so each planted error is guaranteed to be
visibly, checkably wrong.

**Study guide — `ss_polarerrors_curr434.pdf` (2 pages).** Four sections, one per error
class, each with the rule that prevents it, a worked example, and a try-it.

**What was verified, honestly.** The sheet asks for **20 separate responses**. **12 are
machine-checked** with SymPy: every corrected angle, coordinate and parameter value, plus
the four zero-angles of the rose in problem 7. The remaining **8 are instructor-judged** —
one per problem, the part (b) diagnosis — and they are marked `---` in the quick-answer
bank. That is unavoidable and correct: "name the error" is prose, and no computer algebra
system can grade it. Because this is an error-analysis sheet, every problem carries one
such response; the answer key prints a full model diagnosis and an explicit full-credit
criterion for each, so grading is a comparison rather than a judgement call. The eight
study-guide examples and try-its are machine-checked.

There are no `[unchecked]` marks: nothing on the sheet prints an answer that carries
neither a machine check nor a stated rubric.
