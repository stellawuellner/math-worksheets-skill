# Limits and Continuity: Substitution and One-Sided Signs — AP Calculus AB/BC

Three PDFs are ready.

**Study guide (`ss_limits_curr454.pdf`, 2 pages)** — three sections, each a rule
box, a worked example and a try-it whose answer prints upside down in the box:

1. **Reading what substitution reports** — a real number means continuity;
   $0/0$ is *indeterminate*, not undefined, and only tells you to rewrite
   (factor, conjugate, common denominator) and substitute again.
2. **One-sided signs at an infinite limit** — nonzero-over-zero is infinite, and
   which infinity is decided by two signs: the numerator at the point and the
   denominator on the side being approached. "From the right, so $+\infty$" is
   the specific habit this section breaks.
3. **Making a piecewise function continuous** — set the two branch values equal
   at the joint and solve for the constant; the constant is not the branch
   value.

**Worksheet (`ws_limits_curr454.pdf`, 4 pages)** — 8 problems, all on the same
focus. Problems 1–3 build the substitution diagnosis: one where substitution is
legitimate, one $0/0$ repaired by factoring, one repaired by the conjugate.
Problems 4, 5, 6 and 7 are find-and-fix items with a specific wrong claim
attached: that $1/(x-2) \to \infty$ two-sidedly; that $|x|/x$ cancels to 1; that
approaching from the right always gives $+\infty$ (it does not, when the
numerator is negative); and that the continuity constant can be read off one
branch. Problem 8 is a written explanation. Difficulty ramps 1 → 4.

**Answer key (`ak_limits_curr454.pdf`, 4 pages)** — quick-answer bank at the top
(generated from the verification data), then full solutions. Each find-and-fix
solution names the failing line before giving the correct work, and the key
prints a "common wrong answers" block for every planted number — for instance,
*if they got 2: cancelled the common factor to $x-1$ instead of $x+1$*. The
curriculum section with the standard (LIM-1, LIM-2) and difficulty range appears
on the key only; the student's pages carry no grade label.

**What was machine-verified.** SymPy recomputed all thirteen machine checks:
every two-sided limit, each one-sided limit as its own check (so problems 4, 5
and 6 are verified twice, once per side, including the two infinite limits with
opposite signs), the conjugate-simplified form evaluated at the point, and the
continuity equation solved for $k$. Three misconception traps were declared and
confirmed *distinguishable* — the wrong method has to land on a visibly
different number.

**Flagged for manual review.** Problem 8 is an open written response and is
labelled manual rather than claimed as verified. The key gives a model answer and
tells a reviewer what to look for: $0/0$ named as indeterminate rather than
undefined, an algebraic repair route named, and a sign analysis that treats each
side separately. One further note: on problems 4 and 6 the wrong claim is a
*sign*, not a number, so those are checked as paired one-sided limits rather than
as numeric traps — the trap mechanism only accepts a numeric wrong result.
