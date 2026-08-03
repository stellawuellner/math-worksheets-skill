# Writing Inequalities from Verbal Constraints — Grades 6–7

Three PDFs are ready: the student worksheet, a full step-by-step answer key,
and a two-page study guide.

## What the worksheet covers

Ten problems, and in every one the student writes the inequality before doing
any algebra — that translation is the skill being practised, not the solving.
Each problem has its own number line underneath so the solution gets graphed,
which is where "open circle or closed circle" becomes a real decision rather
than a rule to memorise.

1. **Phrase to symbol** (problems 1, 2, 8) — "at least", "no more than". The
   deciding question is always the same: *is the number in the sentence itself
   allowed?* Problem 8 is an error-analysis item: a classmate writes "no more
   than 12" as $n < 12$, and the student has to say what that loses.
2. **Story to inequality** (3, 4, 5, 9) — a one-time amount, a repeated
   amount, and a limit. Problem 4 is built so the joining fee and the monthly
   fee are easy to swap, which is the mistake worth catching; problem 5 turns
   the comparison around ("at least $500") so the direction cannot be
   copied from the problem before it. Problem 9 brings in a perimeter.
3. **Solve and read it back** (6, 7, 10) — problem 7 requires dividing by a
   negative, so the symbol flips; problem 6 ends with a whole-number answer
   ("at most 43 boxes") because the algebra alone does not answer the question
   asked. Problem 10 runs backwards: invent a situation that $25 + 8n \ge 65$
   could model and say what $n \ge 5$ means in it.

A phrase-to-symbol table sits in the directions, so the reference is on the
same page as the work.

## What was verified

Nine of the ten problems have machine-checkable answers, and all eleven
individual checks were recomputed by SymPy before anything was typeset — each
inequality's full solution set (not just the boundary number), plus the two
boundary values in problems 3 and 5 solved as equations. Checking solution
*sets* is what makes the strict-versus-inclusive distinction real: an answer of
$t \le 10$ where $t < 10$ is correct would have failed the gate.

The answer key was then bound to that verified data problem by problem, so no
printed answer can drift from the value that was checked.

Problem 10 is an open response with many correct answers, so it is **flagged
for manual review**. The key gives a complete model story, solves it, and lists
what a full-credit answer must contain — the one-time and repeating amounts
placed correctly, $n$ named as a count, and an interpretation that says "5 or
more" rather than restating the symbols.

## The study guide

Two pages, three sections — phrase to symbol, story to inequality, and
solve-flip-interpret — each with a rule box, a worked example whose first step
explains *why* that tool applies, and a try-it whose answer prints upside down
inside the box. The closing watch-out box covers the two errors this topic
reliably produces: applying the flip rule to a subtraction, and stopping at the
solved inequality instead of answering the question.

## Notes

The grade level does not print on the worksheet or the study guide by design —
it appears on the answer key, together with a generated curriculum section
listing the standard covered (7.EE.B.4) and the difficulty range.
