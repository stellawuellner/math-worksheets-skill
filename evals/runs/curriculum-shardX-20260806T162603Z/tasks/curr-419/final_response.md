# Find and fix: degree–radian and quadrant–sign errors (Precalculus)

Three PDFs are ready.

**Study guide (`ss_trigerrors_curr419.pdf`, 2 pages)** — three sections, each with
a rule box, a worked example that starts by naming the decision being made, and a
try-it with the answer printed upside down inside the box: choosing the right
conversion factor (and the "did the $\pi$ cancel?" self-check), attaching the sign
from the quadrant with ASTC, and reading the *correct ratio* off the reference
angle. A watch-out box covers the range each inverse-trig key actually returns.

**Worksheet (`ws_trigerrors_curr419.pdf`, 5 pages)** — 8 find-and-fix problems.
Each one shows work a student handed in, and asks for two things: the correct
answer, then a written diagnosis of what went wrong. Four target degree–radian
confusion (an inverted conversion factor, a calculator left in radian mode, one
left in degree mode, and answers given in degrees for a radian interval); three
target quadrant signs (keeping the reference angle's positive value, trusting
$\tan^{-1}$'s single output, and picking a quadrant from one sign while ignoring
a second given); one targets reading cosine's value where sine's was needed.
Difficulty ramps 1 → 5.

**Answer key (`ak_trigerrors_curr419.pdf`, 4 pages)** — full worked solutions with
the reasoning spelled out, a Quick Answers bank, and a Curriculum section listing
HSF-TF.A.2 and HSF-TF.B.5 against the problems that use them.

## What is verified, honestly

The sheet asks for **16 responses across the 8 problems**, and the split is even:

- **8 are machine-checked** by SymPy — one per problem: every corrected value,
  every solution set, checked before anything compiled. Solution sets are checked
  for *completeness* on their interval, not just for containing the right roots,
  which is what makes problem 4 ("the student found only one solution") a real
  check rather than a claim.
- **8 are instructor-judged** and printed as `---` in the Quick Answers bank —
  one per problem, the written diagnosis. Naming an error is prose, and no
  computer algebra system can grade prose. The answer key prints a grading rubric
  for each: problems 4 and 8 require **two** distinct faults to be named for full
  credit, and problem 2 requires the fault to be located in the sign step rather
  than in the reference angle.

The key's own "What is verified" note reports the same 8-and-8 split. Nothing is
marked `[unchecked]`.

**Every planted wrong answer on this sheet is a declared, machine-checked
misconception trap** — eight of them. Each was recomputed by the verifier and
confirmed to produce a value the problem's own check rejects, so each really does
distinguish the error it names. That includes the two solution-set traps, where
the wrong method drops a root (problem 4) or returns the right angles in the
wrong unit (problems 3 and 8).
