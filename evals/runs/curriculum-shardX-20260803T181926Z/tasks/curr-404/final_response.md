# Transformation Order and Inverse Domains — Precalculus

Three PDFs are ready.

**Study guide (`ss_transform_curr404.pdf`, 2 pages)** — three sections, each with
a rule box, a worked example and a try-it whose answer prints upside down in the
box:

1. **Transformations inside the function** — factor the inside before reading
   anything off it: $f(bx-c) = f(b(x - c/b))$. Inside operations act in the
   reverse of the written order and the opposite direction; outside operations do
   not.
2. **Composing in the right order** — in $f \circ g$ the function on the right
   runs first; compose symbolically before substituting, because the order is
   visible in the formula and invisible in the arithmetic. The try-it is
   deliberately the *other* order of the same pair, so the two answers sit side by
   side.
3. **Inverses and their domains** — swap and solve gives the formula, the range
   of the original gives the domain, and the non-negative side of a square root
   is what selects one branch of a $\pm$.

**Worksheet (`ws_transform_curr404.pdf`, 4 pages)** — 8 problems, all on the named
focus. Problems 1–3 set up the machinery (a single inside and outside shift;
$f(2x-6)$ factored so the real shift is 3 and not 6; both composites of the same
pair). Problems 4, 5 and 7 are find-and-fix items, one for each way the error
shows up: composing in the wrong order, reading a shift off an unfactored inside,
and writing an inverse with a $\pm$ and a domain of "all reals". Problem 6 is a
full inverse-with-domain problem. Problem 8 is a written explanation. Difficulty
ramps 1 → 4.

**Answer key (`ak_transform_curr404.pdf`, 5 pages)** — quick-answer bank at the
top, generated from the verification data, then full worked solutions. Each
find-and-fix solution names the failing line first. The key prints a "common wrong
answers" block for every planted number: *if they got 3.196: applied $f$ first and
$g$ second*; *if they got $-8$: shifted left 8 instead of left 4*; *if they got 0:
took the minus branch of the square root*. That last one is worth reading with a
student, because $f(0) = 5$ is genuinely true — the rejected branch is a real
number that satisfies the equation and still is not the inverse's output, since
$0 < 3$ puts it outside the restricted domain. The standards (HSF-IF.A–HSF-IF.C
and HSF-BF.A.1c, HSF-BF.B.4) and the difficulty range print in the key's
curriculum section only.

**What was machine-verified.** Fifteen machine checks, all passing. SymPy checked
every algebraic identity symbolically — the factored insides, both composites in
expanded form, the two completed-square forms — and independently recomputed the
numeric values, including $(f\circ g)(2) = \sqrt5 \approx 2.236$. Problem 7's
inverse is verified the honest way, by composing it back:
$\left(\left(3+\sqrt{x+4}\right)-3\right)^2-4$ simplifies to $x$. Three
misconception traps were declared and each confirmed *distinguishable*.

**Flagged for manual review.** Problem 8 is an open written response and is
labelled manual rather than claimed as verified. So is one part of every
inverse problem in a strict sense: the *domain statements* ($x \ge 1$, $x \ge -4$)
are reasoning about ranges, not values a CAS can bind, so the key states them
explicitly and explains where each restriction comes from — the algebra alone
would accept a larger set, which is exactly the error the sheet targets.
