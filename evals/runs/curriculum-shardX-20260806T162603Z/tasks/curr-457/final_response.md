Three PDFs — study guide, worksheet, answer key.

**Study guide (`ss_rules_curr457.pdf`, 2 pages).** Opens with the decision the
whole sheet turns on: which rule does this expression call for? Then one section
per rule — power (with the rewrite habit: $c/x^n$ is $cx^{-n}$, $\sqrt{x}$ is
$x^{1/2}$), product, and quotient — each with the formula, a worked example, and
a try-it whose answer is printed upside down inside the box. The watch-out box
names the two commonest slips, $u'v'$ for a product and $u'/v'$ for a quotient,
and why they are seductive: both give a tidier answer than the right one.

**Worksheet (`ws_rules_curr457.pdf`, 4 pages).** Ten problems, every one of them
a power, product, or quotient rule exercise, with a clean ramp from difficulty 1
to 5 and no repeated skeleton. Problems 1–2 are the power rule with a rewrite;
after that the three rules interleave (product, quotient, power, product,
quotient, product, quotient, quotient), so from problem 3 onward the student has
to choose the rule rather than repeat one. Problems 8–10 go further than a
derivative: find $f'(x)$, then evaluate it at a point. Problem 10 is the
challenge — a quotient whose derivative's numerator simplifies to
$x^2-2x-3$, which happens to vanish at $x=3$.

**Answer key (`ak_rules_curr457.pdf`, 4 pages).** Every solution names $u$ and
$v$ before applying the rule and shows the collection step, not just the result.
Two solutions also state the number a student would get from the classic wrong
method, so a wrong answer is diagnosable at a glance. Quick Answers bank at the
top with each part labelled, and a generated Curriculum block (FUN-3.B,
difficulty 1–5).

**What is verified.** The sheet asks for 14 graded responses. **Thirteen are
machine-checked** — every derivative was recomputed symbolically with SymPy and
compared against the printed key, and every evaluated slope was recomputed too.
**One is instructor-judged: problem 10(c)**, where the student explains what a
zero derivative says about the graph. It prints as `---` in the Quick Answers
bank, and the key gives the rubric: full credit is "horizontal tangent" tied to
the derivative being zero, and "the function is zero there" earns nothing —
$f(3)=9$, it is the slope that vanishes.

Two misconception traps are declared and were machine-checked as distinguishable
from the right answer: on problem 8, multiplying the two factors' derivatives
instead of using the product rule (gives 4 instead of 15); on problem 9, dividing
the numerator's derivative by the denominator's (gives 1 instead of 3/8). Both
print in the key's "Common wrong answers" block with the number to watch for.
