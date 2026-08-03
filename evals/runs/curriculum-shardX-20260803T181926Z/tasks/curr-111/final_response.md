# Whole-Number Division: Quotients and Remainders — three PDFs

- `ws_division_curr111.pdf` — student worksheet (6 pages, 10 problems)
- `ak_division_curr111.pdf` — full step-by-step answer key (2 pages)
- `ss_division_curr111.pdf` — 2-page study guide / skills summary

## What the worksheet asks

Ten problems, every one of them about reading a quotient and a remainder off a
model rather than just running an algorithm:

1. 27 counters drawn on the page — circle groups of 4 and report 6 R 3.
2. 38 tiles — rearrange into rows of 5 (an array model) and report 7 R 3.
3. Check with multiplication: $6 \times \square + 3 = 45$.
4. Estimate first: round 632 to a friendly hundred, then divide by 8.
5. 53 students, 8-seat vans — the leftover forces an extra van (answer in vans).
6. 74 marbles drawn on the page, shared among 9 friends.
7. Partial-quotients table: 145 stickers, 6 to a page.
8. Find the mistake: "87 ÷ 4 = 20 R 7" — the remainder rule alone shows it is
   wrong, before any redividing.
9. Estimate 1347 ÷ 5, then divide exactly and compare.
10. 96 cm of ribbon in 7 cm bows, plus a written explanation of why *this*
    leftover is dropped while the van leftover rounded up.

Difficulty runs 1 → 5, and the four methods (equal groups/arrays, checking by
multiplying back, estimating the quotient, interpreting the remainder) are
interleaved after the warm-up so the student has to choose the method rather
than repeat one. Each problem carries a CCSS tag (4.NBT.B.6, 4.OA.A.2) and
those tags generate the Curriculum section printed on the answer key; the grade
level appears there and nowhere on the student's pages.

## What was verified, and what is not

Every numeric answer on the sheet — 22 separate values across the ten problems,
including each quotient, each remainder, both estimates and the two rounded
compatible numbers — was recomputed by SymPy before anything compiled, and the
answer key's boxed answers were then bound back to those verified values
problem by problem.

**One item is flagged for manual review, correctly:** the written explanation in
problem 10 (why the ribbon leftover is dropped while the van leftover rounds up)
is open reasoning, so no machine can mark it. The answer key prints a full model
answer for you to compare against, and the build reports it as a manual-review
item rather than claiming it was verified.

Problem 8 also declares the misconception it targets — stopping a group early so
the remainder (7) exceeds the divisor (4). The verifier proved that wrong method
gives 20, visibly different from the correct 21, and the key prints that wrong
answer in its "common wrong answers" note.

## The study guide

Four sections, each with a rule box, a worked example whose first step says why
that method fits, and a try-it with the answer upside down inside the box:
equal groups and arrays; checking by multiplying back; estimating the quotient;
and reading what the remainder means (round up / drop it / it is the answer).
That last section is the one problem 10 asks the student to reason from.
