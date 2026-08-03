# Precalculus — Transformations, Compositions and Inverses Together

Three PDFs are ready: the student worksheet, a full step-by-step answer key, and
a two-page study guide.

**What the worksheet covers.** Twelve problems that treat transformations,
compositions and inverses as one topic rather than three. The sheet is built on
a claim it then keeps demonstrating: a transformation *is* a composition with a
simple linear map, and an inverse is the composition that undoes one. Problem 5
makes that explicit — composing $g(x)=x^2$ with $f(x)=x+4$ produces exactly the
horizontal shift rule.

Two short warm-ups come first, then the three methods alternate one at a time so
the student must choose rather than repeat. The set includes a rational-function
inverse (clear the denominator, collect the $y$ terms), a
$(f\circ g)^{-1}=g^{-1}\circ f^{-1}$ problem worked both ways so the two answers
can be compared, and a transformation read from a two-row table rather than a
formula. The synthesis problem restricts $f(x)=(x-1)^2$ to $x\ge 1$, asks why
that restriction creates an inverse, and closes by computing
$f^{-1}(f(5))$ — the reflection across $y=x$ done in numbers.

**What the answer key contains.** A worked solution for every problem in
numbered steps that begin with the reasoning move, not the algebra. Where a
misconception is likely the key names it: shifting right when the rule says
$f(x-2)$, distributing an outside minus to only the first term, and applying a
vertical shift before the stretch. Two of those are declared misconception traps
and appear in the key's "common wrong answers" bank (2 on problem 7, $-2$ on
problem 11). The key also carries the quick-answer bank and a curriculum section
with the standards and difficulty range; the course level prints there only.

**What the study guide contains.** Three teaching sections — transform a rule,
compose two functions, invert a function — each with a rule box, a worked
example whose first step states the strategy in words, and a try-it problem with
the answer upside down inside the box. The composition try-it deliberately asks
for $(g\circ f)(2)$ after the example did $(f\circ g)(2)$, so the student
discovers the two differ. The watch-out box closes on the two persistent errors:
reading $f^{-1}$ as a reciprocal, and forgetting that undoing a composition
reverses the order.

**Verification.** 15 machine checks were recomputed independently with SymPy and
all passed, including three inverse round-trips ($f(f^{-1}(x))$ simplified back
to $x$, one of them for the rational function) and both declared misconception
traps. Two items are flagged for manual review, correctly: the written
description of the three transformations in problem 11(b), and the explanation
in problem 12(a) of why restricting the domain creates an inverse. Both have the
expected answer and a grading note in the key.

**One note on standards tagging.** `references/standards-map.md` has rows for
function composition and inverses (HSF-BF.A.1c, HSF-BF.B.4) and for function
behaviour and graphs (HSF-IF.A–HSF-IF.C), but no row for HSF-BF.B.3, which is
the CCSS code that actually covers graph transformations
($f(x)+k$, $kf(x)$, $f(kx)$, $f(x+k)$). The transformation problems here are
tagged HSF-IF.A–HSF-IF.C, which is in the map and covers graphing function
behaviour, rather than inventing a code.
