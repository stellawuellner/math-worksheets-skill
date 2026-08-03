# Approximating Irrational Roots on a Number Line — Grade 8 / Pre-Algebra

Three PDFs are ready:

- **`ws_roots_curr203.pdf`** — the student worksheet (5 pages, 10 problems)
- **`ss_roots_curr203.pdf`** — the study guide / skills summary (2 pages)
- **`ak_roots_curr203.pdf`** — the full step-by-step answer key (3 pages)

## What the worksheet covers

**Every problem carries its own number line**, drawn to the scale that problem
needs — whole numbers for the bracketing problems, tenths for the estimation
ones — so the student plots as well as computes. That is the focus of the sheet,
not a decoration on it.

1. **Trap the root between two whole numbers** (problems 1–2): $\sqrt{47}$ and
   $\sqrt{150}$, answered as inequalities and marked on an integer line.
2. **Squeeze it to the nearest tenth** (3, 5, 9, 10): $\sqrt{30}$, $\sqrt{83}$,
   and an applied one — a square patio of area $132$ square feet, whose side is
   asked to the nearest tenth of a foot.
3. **Plot on a tenths line** (6, 8): problem 6 reverses the task — a point $P$
   is already marked and the student decides which of $\sqrt{55}$, $\sqrt{58}$,
   $\sqrt{62}$ belongs there.
4. **Order roots with rational numbers** (4, 7): $\sqrt{20}$ against $4.5$, and
   a four-way ordering of $2.7$, $\sqrt{8}$, $3.1$, $\sqrt{10}$ — deliberately
   chosen so $3.1$ and $\sqrt{10}$ are close enough that eyeballing fails.

Problem 10 is the closing challenge and an error-analysis item: Nadia rounds the
*radicand* to the nearest perfect square and reports $7.0$ for $\sqrt{50}$. The
student finds $7.1$ and explains why her rule loses the size of the gap.

No calculators — every estimate is made by squaring candidate tenths, which is
the method the study guide teaches and the answer key shows in full.

## What was verified

All ten problems were recomputed independently by SymPy before anything
compiled — 13 checks in total, because the two bracketing problems are checked
twice (the lower whole number and the upper one) and problem 8 asks for two
roots. **All 13 passed; nothing is flagged for manual review.** The written
explanation in problem 10 is a bonus on top of a numeric answer that is checked,
so the problem is not left unverified.

Three misconception traps were declared and machine-checked as distinguishably
wrong: on problem 6, picking $\sqrt{55}$ ($7.4$) or $\sqrt{62}$ ($7.9$) instead
of the root that actually lands on $P$; and on problem 10, Nadia's $7.0$. Each
is printed in the key's common-wrong-answer block.

The study guide's four worked examples and four try-it items were verified the
same way (ten more checks, all passed).

## Using them

Give the study guide first. It lists the perfect squares worth memorising, then
states the one rule the whole topic rests on — squaring preserves order for
positive numbers — and gives a rule, a worked example and a try-it for each of
the four skills. The try-it answers are printed upside down inside their boxes.

The answer key shows the bracketing and the tenth-testing arithmetic for every
problem, plus a note on where the dot goes on that problem's line. It opens with
a quick-answer bank for grading and a curriculum section listing the standards
(8.NS.A, with 8.EE.A on the patio problem) and the difficulty range.
