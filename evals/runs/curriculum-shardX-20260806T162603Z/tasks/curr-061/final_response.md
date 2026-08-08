Here are three PDFs on subtracting two-digit numbers with place-value models —
an 8-problem worksheet, a full step-by-step answer key, and a two-page study
guide.

**Worksheet** (`ws_subtractmodel_curr061.pdf`, 5 pages). Every problem prints
the starting number as base-ten blocks — tall rods for tens, small squares for
ones — and the child works by crossing blocks out, then writes the number. The
model and the notation sit on the same line as each other throughout:

- Problems 1 and 2 (47 − 23, 68 − 35): enough ones to take from, so no rod has
  to be opened. This is the contrast case that makes regrouping meaningful.
- Problems 3 and 4 (52 − 27, 64 − 28): not enough ones, so one rod is opened
  into ten ones first. The instruction says so explicitly on problem 3 and
  leaves a little more to the child on problem 4.
- Problem 5 (71 − 38): round each number to the nearest ten and subtract, then
  use the blocks for the exact answer, so the estimate is used as a check.
- Problem 6 (82 − 45 marbles): a word problem, with the unit printed on the
  answer line.
- Problem 7: a find-and-fix. Sam worked out 63 − 27 and wrote 44. The child
  redoes it with the blocks and explains the error.
- Problem 8 (94 − 47): estimate, then work exactly, then explain why the
  estimate landed *below* the exact answer.

**Answer key** (`ak_subtractmodel_curr061.pdf`, 3 pages). Each problem is worked
in the language of the blocks — "open a rod, leaving five rods and thirteen
ones" — rather than as bare digit manipulation, so the explanation matches what
the child did on the page. It also carries a **Common wrong answers** block: I
declared the classic errors as misconception traps and the system recomputed
each wrong result from the mistaken method, so 44 on problem 7, 35 on problem 3,
44 on problem 4 and the two rounding slips on problems 5 and 8 each come with a
one-line diagnosis.

**Study guide** (`ss_subtractmodel_curr061.pdf`, 2 pages). Three sections:
subtracting without opening a rod, subtracting when you must open one, and
estimating a difference before subtracting. The first two rule boxes carry a
small block picture, including one showing a rod already opened into ten ones.
Each section has a worked example and a try-it with the answer upside down
inside the box.

**How much of this is machine-checked.** The sheet asks for 12 responses; 10 are
machine-checked with SymPy. Every difference was recomputed and matched against
the printed key, both estimates were recomputed by rounding each number and
subtracting, and every declared trap was proved to produce a *different* number
from the correct answer, so each trap really does discriminate the error it
names. The other 2 responses are the written explanations in problems 7 and 8.
Those are genuinely open, so the Quick Answers strip prints `---` for them, the
"What is verified" note names problems 7 and 8, and the key gives a rubric for
each covering full, half and no credit. The numeric halves of both problems are
machine-checked like the rest.
