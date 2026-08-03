# Grade 8 / Pre-Algebra — Putting Rational and Irrational Numbers in Order

Three PDFs are ready: the student worksheet, a full step-by-step answer key, and
a two-page study guide.

**What the worksheet covers.** Twelve problems on ordering lists that mix
fractions, decimals and square roots. Two short warm-ups come first (estimate
$\sqrt{50}$; compare $\sqrt 9$ with $2.9$ — a reminder that a perfect-square
root is rational). After that the three moves are interleaved so the student has
to pick one rather than repeat one: estimate a root, compare two quantities, or
order a whole list.

The numbers are chosen so careless rounding fails visibly. Problem 7 is
$\pi$ against $\frac{22}{7}$, which agree to two decimal places and separate at
the third. Problem 10 is $\sqrt{18}$ against $\frac{17}{4}$, which differ by
seven thousandths. Problem 11 puts four values inside a range of $0.02$, so two
decimal places genuinely cannot separate them. The synthesis problem adds
negatives, where the order reverses, and asks for a number-line sketch.

**What the answer key contains.** A worked solution for every problem, with the
trapping step ($36<40<49$, so $6<\sqrt{40}<7$) written out rather than a
calculator value asserted — that step is what makes an estimate checkable.
Answers are written back in the original symbols, not in decimals, because the
decimals were the tool and not the answer. Three problems carry a "common wrong
answers" block generated from declared misconception traps: halving the radicand
instead of taking the root (10 on problem 4), moving the decimal point (8.5 on
problem 8), and reading a fraction bar as a decimal point (17.4 on problem 10).
The key also carries the curriculum section listing the standards (8.NS.A,
8.EE.A) and the difficulty range; the grade level prints only there.

**What the study guide contains.** Three teaching sections — estimate a square
root, compare two quantities, and order a mixed list — each with a rule box, a
worked example whose first step states the strategy in words, and a try-it
problem with the answer upside down inside the box. The comparison section
teaches the squaring shortcut alongside the decimal method, since squaring
settles $\sqrt7$ versus $2.7$ with no estimating at all. The watch-out box
closes on the two errors that dominate this topic: treating $\frac{22}{7}$ as
equal to $\pi$, and rounding too early.

**Verification.** All 13 machine checks (12 problems, one with two parts) were
recomputed independently with SymPy and passed — every root estimate to the
stated precision, every comparison symbol, and every full ordering, including
the five-value list with negatives. All three declared misconception traps were
confirmed to give answers the problem's own check rejects. Nothing is flagged
for manual review; the number-line sketch in problem 12 is a presentation of the
ordering the key verifies, not a separate unverified claim.
