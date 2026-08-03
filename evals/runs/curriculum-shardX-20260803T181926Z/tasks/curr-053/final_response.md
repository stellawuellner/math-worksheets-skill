# Comparing Three-Digit Numbers — Grades 2–3

Three PDFs are ready:

- `ws_comparing_curr053.pdf` — the student worksheet, 10 problems, 5 pages
- `ak_comparing_curr053.pdf` — the full step-by-step answer key, 3 pages
- `ss_comparing_curr053.pdf` — a 2-page skills summary / study guide

## What the worksheet asks

All ten problems compare three-digit numbers by place value, and every one of
them is anchored to a representation rather than to bare digits:

- **Place-value charts** (problems 1, 3, 7, 10) — the number goes into a
  hundreds/tens/ones chart first, and the child compares from the left. Problem
  3 is the zero-as-placeholder case ($508$ against $580$) and problem 7 is the
  case where hundreds and tens tie and the ones place decides.
- **Base-ten blocks** (problems 2 and 6) — flats, rods and cubes. Problem 6 is
  built around the classic error: Nina has more rods ($9$ tens) but Sam has more
  hundreds, so Sam's $209$ still beats Nina's $198$.
- **Ordering three numbers** (problems 5 and 9) — least-to-greatest and
  greatest-to-least, each with a hundreds tie that has to be broken on tens.
- **Real counts** (problems 4 and 8) — cans collected by two schools, and steps
  on two step counters. Problem 8 states a wrong claim ("my tens digit is
  bigger") and asks the child to test it.

Problem 10 is the challenge: a number is $5$ hundreds, ? tens, $7$ ones, and
must sit between $547$ and $587$. The child finds the smallest one that works.

Difficulty ramps 1, 1, 2, 2, 3, 3, 3, 4, 4, 5. No problem needs anything beyond
place value to 1,000 — no addition or subtraction is required to answer any of
them.

## What was verified

Sixteen SymPy checks cover all ten problems (several problems carry more than
one: the block problems verify each number *and* the comparison). **Nothing is
flagged for manual review** — the build finished with every gate green.

One misconception trap is declared and machine-proved distinguishable: writing
Sam's blocks as $29$ by skipping the empty tens place. It prints in the answer
key as a "common wrong answer" note so the grader can name the error rather
than just mark it wrong.

The answer key repeats every problem and shows the comparison one place at a
time — which place tied, which place decided, and why the remaining digits did
not matter. Each final comparison is boxed as a full statement
(e.g. $462 > 429$) so it matches the way the child writes it.

## The study guide

Four sections, each with a rule box, a worked example whose first step says why
that step comes first, and a try-it item with the answer printed upside down
inside the box:

1. comparing on a place-value chart,
2. reading and comparing base-ten blocks (with a drawing of a flat, a rod and a
   cube),
3. putting three numbers in order,
4. answering a comparison question asked in a story.

All problems are tagged to standard 2.NBT.A.
