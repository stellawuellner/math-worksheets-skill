# Signed rational numbers: choosing the right move — three PDFs

Here is a 12-problem set on signed rational-number work, built so that the
student has to *decide* which rule an expression needs rather than repeat one
procedure down a column.

**What is in each document**

- **Worksheet** (`ws_signedrat_curr170.pdf`, 4 pages). Twelve problems that
  rotate between four moves: *adding and subtracting signed numbers* (including
  subtracting a negative), *multiplying and dividing them*, *ordering rationals
  written as integers, fractions and decimals*, and *evaluating mixed
  expressions in the correct order*. The first three are a short warm-up; after
  that the four kinds are interleaved deliberately, and the directions box asks
  the student to read each problem before reaching for a rule. Problem 10 shows
  a wrong answer (Priya evaluated $-24 \div (-6) \cdot (-2)$ as $-2$) and asks
  what went wrong; problem 12 is a challenge ordering four negative numbers
  that sit close together in mixed forms. Every problem has room to show the
  work, which is where sign errors get caught.
- **Answer key** (`ak_signedrat_curr170.pdf`, 3 pages). Answers at a glance,
  then a step-by-step solution for every problem with the final answer boxed,
  and a "listen for" line naming the specific wrong answer that problem
  usually produces ($-11$ for $-8+3$; $-17$ for $-6-(-11)$; $-0.6 < -0.75$ when
  the negatives are ordered as if they were positive).
- **Study guide** (`ss_signedrat_curr170.pdf`, 2 pages). Four short sections —
  add/subtract, multiply/divide, comparing, mixed expressions — each with the
  rule stated plainly, a worked example that opens by saying *why* that move
  comes first, and a try-it whose answer is printed upside down inside the box
  for self-checking.

**What was verified**

All 12 answers were recomputed with SymPy before anything was compiled — every
evaluation, both orderings, and the fraction-versus-decimal comparison — and
the printed key was then bound problem-by-problem to those verified values, so
a boxed answer cannot drift from the checked one. The misconception planted in
problem 10 was machine-checked to be distinguishably wrong: multiplying before
dividing gives $-2$, while working left to right gives $-8$.

**Nothing is flagged for manual review** — every problem here has a
machine-checkable answer. Three problems additionally ask the student to *say*
how they decided (problems 5, 8 and 12); those sentences are not machine-checked,
and the key shows what a good answer sounds like.

Suggested order: study guide first, then the worksheet, then the answer key.
