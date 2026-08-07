Three PDFs are ready — study guide, worksheet, answer key.

**Study guide (`ss_limits_curr452.pdf`, 2 pages).** Three sections, each a rule
box + worked example + try-it with the answer printed upside down inside the box:
reading a limit from one side (rewrite the absolute value or piecewise rule for
that side first), telling a hole from a vertical asymptote at a zero of the
denominator, and end behavior as $x$ grows large. The watch-out box carries the
one that trips almost everyone: $\sqrt{x^2}=|x|$, not $x$.

**Worksheet (`ws_limits_curr452.pdf`, 4 pages).** Ten problems on one-sided,
infinite, and end-behavior limits, with a clean ramp from difficulty 1 to 4 and
no two problems sharing a skeleton. The three subskills are blocked for the first
three problems and then interleaved, so from problem 4 on the student has to
decide which question the notation is actually asking before touching the
algebra. Problem 5 is a piecewise shipping cost with a genuine jump; problem 7
puts a hole and an asymptote in the same function; problem 10 is the challenge,
the $\sqrt{9x^2+4}/(3x-1)$ sign trap at both ends.

**Answer key (`ak_limits_curr452.pdf`, 4 pages).** Worked solutions throughout —
the case split for each absolute value, the factor-and-cancel that separates hole
from asymptote, and the divide-by-the-highest-power step written out rather than
asserted. A Quick Answers bank at the top gives each part its own label ("(a)
from the left = $-\infty$"), so you can grade a two-part problem without decoding
which number goes where. A generated Curriculum block lists the AP codes (LIM-1,
LIM-2) against the problems that use them.

**What is verified.** The sheet asks for 16 graded responses. **Fifteen are
machine-checked** — each limit, including every one-sided and infinite one, was
recomputed with SymPy and compared to the printed key. **One is
instructor-judged: problem 5(c)**, where the student has to explain whether the
two-sided limit exists. It shows as `---` in the Quick Answers bank, and the key
spells out the rubric: the conclusion must be "does not exist" *and* must give
the reason that 5 and 8 disagree. A bare "DNE" earns nothing, and neither does
answering 8 because $f(2)=8$.

Two misconception traps are declared and were machine-checked as distinguishable
from the correct answer: on problem 3, using the ratio of the constant terms
instead of the leading terms; on problem 8, dividing leading coefficients without
first comparing the degrees (gives 5/2 instead of 0). The second prints in the
key's "Common wrong answers" block with the number to watch for.
