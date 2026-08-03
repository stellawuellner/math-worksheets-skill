Here are the three PDFs for the Algebra 2 complex-number review.

**Worksheet — `ws_complexsets_curr355.pdf` (5 pages, 12 problems).**
The focus is stated on the sheet: solve the equation and report the *complete*
complex solution set. Two short warm-ups get the arithmetic in hand (a complex
product, and a power of the imaginary unit), and the remaining ten problems all
end in a solution set. After the warm-up the methods are deliberately
interleaved — square roots, factoring, quadratic formula, and substitution
checks alternate, so your student has to decide which tool the equation wants
rather than repeating one procedure twelve times. Problem 12 is the synthesis
challenge: one non-real zero of a quartic is given, and the student has to use
the conjugate-pair fact to recover the whole solution set, including the
repeated real zero.

**Answer key — `ak_complexsets_curr355.pdf` (4 pages).**
Every problem is worked out step by step, not just answered: the first step of
each solution says *why* that method was chosen. A quick-answer bank sits at the
top for fast grading, followed by a Curriculum section listing the standards
covered (HSN-CN.A/B for the arithmetic warm-ups, HSN-CN.C.7–C.9 for the
solution-set work) and the difficulty range. Two problems carry a "common wrong
answers" note so that if the answer comes out wrong you can tell *which*
misconception produced it.

**Study guide — `ss_complexsets_curr355.pdf` (2 pages).**
Four sections, one per skill the worksheet tests: multiplying complex numbers,
quadratics with complex solutions, testing a proposed solution, and reporting a
complete solution set. Each section is a rule box, a worked example, and a
try-it problem whose answer is printed upside down inside the box so the student
can attempt it first and then check.

**What was verified.** All 12 worksheet answers and all 8 study-guide answers
were recomputed independently with SymPy — every root set was checked over the
complex domain, so "did they list *all* the solutions" is machine-checked, not
just "is this one root right". Nothing on this sheet is flagged for manual
review: there are no open-response items, so every answer key value is a
verified value.

Two misconception traps are declared and machine-checked as well: problems 5 and
9 are built so that the classic error — treating $i^2$ as $+1$ when squaring —
lands on 32 instead of 0, visibly wrong rather than accidentally close. Problem 9
puts that wrong value in the stem and asks the student to find the mistake.
