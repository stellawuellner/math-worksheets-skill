# Interpreting Powers of i and the Complex Plane (Algebra 2)

Three PDFs are ready for an Algebra 2 student. Every problem pairs a picture or
a pattern with the notation that records it, which is what makes powers of $i$
stop feeling arbitrary.

- **Worksheet (5 pages, 10 problems).** Problem 1 is a table of $i^1$ through
  $i^5$ with three cells to fill, so the four-step cycle is discovered rather
  than announced; problem 2 uses it on $i^{27}$ via the remainder. Problems 3-5
  each come with their own blank Re/Im grid: adding two numbers tip-to-tail,
  seeing $i(3+4i)$ as a quarter turn, and getting the modulus out of a right
  triangle. Problem 8 asks why four quarter turns must return you to the start
  *before* any arithmetic is done. Problems 6, 9 and 10 connect the plane to
  non-real solutions — solutions on the imaginary axis, the four fourth-roots
  arranged a quarter turn apart, and a conjugate pair mirrored across the real
  axis.
- **Answer key (2 pages).** Each solution states the geometric reading next to
  the algebra ("the arrow to (3,4) becomes the arrow to (-4,3): same length,
  turned 90 degrees"), and problems 4, 8, 9 and 10 explicitly tie back to the
  cycle from problem 1. A generated quick-answer bank sits at the top for fast
  grading.
- **Study guide (2 pages).** Four sections: the cycle of powers with the
  divide-by-4-keep-the-remainder rule, the point/arrow dictionary for $a+bi$
  (with tip-to-tail addition and the modulus), multiplying by $i$ as a quarter
  turn — including why that *causes* $i^4 = 1$ — and non-real solutions as
  conjugate pairs. Each section has a rule box, a worked example whose first
  step names the decision, and a try-it with its answer printed upside down.

## Verification

All **10 of 10** worksheet problems and all **8** study-guide boxes (4 worked
examples + 4 try-its) were machine-checked with SymPy in the complex domain —
`"domain": "complex"` on the solve/zeros problems, so non-real roots are required
rather than silently dropped. Nothing on this sheet is open-ended, so nothing is
flagged `manual`. The full gate chain is green.

One note on tagging: `references/standards-map.md` has no complex-number code, so
the complex-plane problems carry the task's own `HSN-CN` reference, while the
three problems that are also quadratic-solving or polynomial-zero work carry the
map's `HSA-REI.B.4` and `HSA-APR.B.3` verbatim. No code was invented.
