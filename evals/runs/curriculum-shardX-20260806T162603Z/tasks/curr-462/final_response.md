Three PDFs — study guide, worksheet, answer key.

**Study guide (`ss_invderiv_curr462.pdf`, 2 pages).** Three sections, each a rule
box + worked example + try-it with the answer printed upside down inside the box:
the three inverse-trig rules with the chain rule already built in, the
inverse-function rule $\left(f^{-1}\right)'(b)=1/f'(a)$ with the order of
operations spelled out, and inverse trig inside a product. The middle section
makes the point that matters most here — you never need a formula for $f^{-1}$,
which is exactly why the rule is worth having.

**Worksheet (`ws_invderiv_curr462.pdf`, 4 pages).** Ten problems, all on
differentiating inverse and inverse-trigonometric functions, ramping from
difficulty 1 to 5 with no repeated skeleton. The three subskills interleave from
problem 3 onward — inverse-trig, inverse-trig, inverse-function, product,
inverse-trig, inverse-function, chain, inverse-trig, product, inverse-function —
so the student has to identify the structure before reaching for a rule.
Problems 2 and 7 are a deliberate pair: $\arctan(x^2)$ and $(\arctan x)^2$, the
same two ingredients composed in opposite orders. Problem 10 is the challenge:
$f(x)=2x+\sin x$, whose inverse has no formula at all, so the inverse-function
rule is the only way in.

**Answer key (`ak_invderiv_curr462.pdf`, 4 pages).** Each solution names $u$ and
$u'$ before applying a rule, and the inverse-function problems state explicitly
which number gets substituted where. Several solutions close with the number a
student would get from the standard slip. Quick Answers bank at the top with each
part labelled, and a generated Curriculum block (FUN-3.E, difficulty 1–5).

**What is verified.** The sheet asks for 14 graded responses. **Thirteen are
machine-checked** — every derivative was recomputed symbolically with SymPy and
compared against the printed key, and every inverse-derivative value was
recomputed from the reciprocal formula at the correct input. **One is
instructor-judged: problem 10(c)**, the argument for why $f(x)=2x+\sin x$ has an
inverse on all of $\mathbb{R}$. It prints as `---` in the Quick Answers bank, and
the key gives the rubric: full credit needs $f'(x)=2+\cos x \ge 1 > 0$ *and* the
step from strictly increasing to one-to-one; "it passes the horizontal line test"
with no reason earns nothing.

Two misconception traps are declared and were machine-checked as distinguishable
from the correct answer, and both print in the key's "Common wrong answers"
block: on problem 3, evaluating $f'$ at the output 4 instead of the input 1
(gives 50 rather than 1/5); on problem 6, taking the reciprocal of the input 2
instead of the reciprocal of the derivative (gives 1/2 rather than 1/8).
