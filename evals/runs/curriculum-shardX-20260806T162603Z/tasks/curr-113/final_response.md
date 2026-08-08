# Interpreting Remainders in Real Situations — Grades 4–5

Three PDFs are ready: the student worksheet, a full step-by-step answer key, and a
two-page study guide.

**Worksheet (10 problems).** Every problem is a real situation that ends in a division
with a remainder, and the whole point is that the *same* division has three different
right answers depending on what the question asks. The sheet rotates deliberately
between four moves so your child has to decide which one applies rather than repeat a
procedure:

- **drop the remainder** — how many coolers/shelves fill up completely (problems 1, 5);
- **add one more group** — how many buses, vans, pallets must be ordered so nobody and
  nothing is left behind (3, 6, 10);
- **the remainder is the answer** — rolls left over, ribbon left on the roll, markers
  that cannot be shared evenly (2, 7, 9);
- **estimate first** — round to friendly tens, divide, and use that as a check on the
  exact answer (4, 8).

Difficulty ramps from single-step problems with small numbers (1–2) up to a two-step
problem (8 boxes of 144 markers shared among 25 classrooms) and a synthesis problem
that asks for the full pallets, the pallets that must be ordered, and why those two
numbers differ.

**Answer key.** Each solution shows the multiplication used to build the quotient, the
subtraction that produces the remainder, and then a sentence on *why* the remainder is
dropped, rounded up, or reported. There is a Quick Answers bank at the top for fast
grading, a curriculum block (4.NBT.B.6, difficulty 1–5), and a "Common wrong answers"
block for the two traps that were designed into the sheet: reporting 3 buses instead of
4, and 12 vans instead of 13. Both are the same misconception — reading the quotient
and never asking what happened to the remainder.

**Study guide (2 pages).** Four sections, each with a rule box, a worked example whose
first step names *which* interpretation the question calls for, and a try-it with the
answer printed upside down inside the box.

## What is verified, honestly

The sheet asks for 17 separate responses across the 10 problems.

- **15 are machine-checked** with SymPy: every quotient, every remainder, both estimates,
  and the two-step marker problem. The printed answer key was bound back to those same
  verified values by the build, so the key cannot drift from what was checked.
- **2 are instructor-judged** and marked `---` in the Quick Answers bank: problem 6(b)
  ("explain why the plain quotient will not do") and problem 10(c) ("explain why the
  answers to (a) and (b) differ"). These are written reasoning, and no computer algebra
  system can grade them. The answer key states exactly what a full-credit response must
  contain — for 6(b), that the 10 leftover riders are real people who need a 13th van;
  for 10(c), that the 128 leftover kits are what make 13 and 14 differ.

That split is why the build exits with a manual-review flag rather than a clean
"everything checked". Eight of the ten problems are fully machine-checked; the two
explain-items are the ones worth reading yourself.
