Three PDFs — study guide, worksheet, answer key.

**Study guide (`ss_limiterr_curr454.pdf`, 2 pages).** Three sections, each a rule
box + worked example + try-it with the answer upside down inside the box. Section
1 is the pre-flight check (substitute into the *denominator* first; $0/0$ is a
message, not a value). Section 2 is the sign rule for infinite limits — read two
signs, not one. Section 3 teaches how to write a find-and-fix answer: a complete
one has a *fix* and a *diagnosis*, and "it's wrong" is not a diagnosis.

**Worksheet (`ws_limiterr_curr454.pdf`, 4 pages).** Eight problems, all on the
two error families named in the request. **Four are find-and-fix items**
(problems 2, 5, 7, 8) — each prints a real student's work and asks for the
correct value *and* the name of the mistake. The other four build the diagnostic
habit directly: problem 1 is a limit where substitution *is* legal and asks how
you could tell; problems 3 and 6 contrast an odd-power denominator (opposite
signs on the two sides) with a squared one (same sign on both). Problem 8 is the
challenge, where dropping the absolute-value bars hides a genuine
does-not-exist. Difficulty ramps 1 → 4.

**Answer key (`ak_limiterr_curr454.pdf`, 3 pages).** Each solution redoes the
limit properly and then states the diagnosis in the terms a grader can mark
against. Quick Answers at the top, plus a generated Curriculum block (LIM-1,
difficulty 1–4) and a "Common wrong answers" block listing the planted errors and
the numbers they produce.

**What is verified — please read this part.** The sheet asks for 16 graded
responses. **Eleven are machine-checked** with SymPy: every limit value,
including the infinite ones and both one-sided branches of the challenge. **Five
are instructor-judged** — problems 1(b), 2(b), 5(b), 7(b) and 8(b), which are the
written diagnoses. That is exactly as it should be for an error-analysis sheet:
the diagnosis is prose and no computer algebra system can grade it. Each shows as
`---` in the Quick Answers bank, and the answer key carries a written rubric for
each one, including what *not* to accept (for instance, "they forgot a minus
sign" without naming which quantity is negative).

**Five misconception traps are declared and machine-checked** as genuinely
distinguishable from the correct answer, so every planted wrong result on the
sheet is derived rather than typed: reading $0/0$ as 0 (problem 2), cancelling
$x^2$ across an addition (problem 4), deciding an infinite limit from the
numerator's sign alone (problems 5 and 7), and dropping the absolute-value bars
(problem 8).
