Three PDFs — study guide, worksheet, answer key.

**Study guide (`ss_deriv_curr456.pdf`, 2 pages).** Three sections, each with a
rule box, a worked example, and a try-it whose answer is printed upside down
inside the box: the derivative as the limit of secant slopes (with the reminder
that you may never substitute $h=0$ before the $h$ downstairs cancels), average
rate versus instantaneous rate and how the wording tells you which is being
asked, and how to read a derivative value in three parts — sign for direction,
size for speed, units as output-per-input.

**Worksheet (`ws_deriv_curr456.pdf`, 3 pages).** Eight problems on interpreting
the derivative as a limit and as an instantaneous rate. Problems 1 and 3 are
deliberately the same cart: problem 1 asks for the average velocity from $t=1$ to
$t=3$ (7 m/s, read from a table of positions) and problem 3 asks for the
instantaneous velocity at $t=3$ (9 m/s, from the limit). Seeing the two numbers
side by side is the concept. Problems 2, 4 and 6 build the limit definition
across three function shapes — polynomial, reciprocal, radical — so the algebra
that cancels the $h$ has to change each time. Problems 7 and 8 move to the
derivative *function* and then back to meaning. Difficulty ramps 1 → 4.

**Answer key (`ak_deriv_curr456.pdf`, 3 pages).** Every difference quotient is
worked line by line to the point where the $h$ cancels, and several solutions add
a sanity check (the negative slope of $1/x$ at 2, the shallow slope of $\sqrt{x}$
at 9). Quick Answers bank at the top with each part labelled, plus a generated
Curriculum block (FUN-3.A, FUN-3.B; difficulty 1–4).

**What is verified.** The sheet asks for 12 graded responses. **Ten are
machine-checked** with SymPy — every limit, every derivative function, and every
evaluated slope, recomputed independently and compared with the printed key.
**Two are instructor-judged: problems 5(b) and 8(c)**, the sentences interpreting
what a derivative value means. They print as `---` in the Quick Answers bank, and
each carries a rubric in the key naming what full credit needs (direction, size,
rate units, and the word *instant*) and what to reject — "20 litres" with no rate
unit, or "the ball has gone down 10 metres", which confuses a rate with a
displacement.

Two misconception traps are declared and were machine-checked as distinguishable:
on problem 1, dividing $s(3)$ by 3 instead of using the change over the change
(gives 6 rather than 7); on problem 3, reporting the average velocity 7 where the
instantaneous 9 was asked for. The second is the exact confusion the pairing of
problems 1 and 3 is designed to surface, and it prints in the key's "Common wrong
answers" block.
