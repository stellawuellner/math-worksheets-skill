# Teen numbers: reading and writing teen numerals and number words (K–1)

Three PDFs are ready for a kindergarten or first-grade learner working on teen
numbers and place value.

**Worksheet — 10 problems.** The sheet moves through four distinct kinds of task
so no skeleton repeats:

- *One ten and some ones* (problems 1, 2, 5, 8) — ten-frames and a story problem
  that force the "the 1 in 15 means ten" reading.
- *Number word to numeral* (3, 7) — write the numeral for **fourteen**, **sixteen**.
- *Numeral to number word* (4, 6) — read 18 and 12 aloud, write the word, then
  finish the place-value sentence "18 is one ten and ___ ones".
- *Comparing teen numbers* (9, 10) — write $<$ or $>$, once with numerals and once
  where the number words must be converted first.

Difficulty ramps 1, 1, 2, 2, 2, 2, 3, 3, 3, 4. Each problem gets 3–4 cm of
writing room and its own answer blank; the sheet prints on 3 pages (2 sheets
double-sided).

**Answer key.** Every solution is worked, not just stated: the count-on sequence
is spelled out, the ten is subtracted explicitly to expose the ones, and the
comparison problems explain that both numbers share one ten so only the ones
decide. Problem 8 carries a declared misconception trap — a student who reads the
1 in 15 as one *one* answers 14 — and the key's quick-answer bank prints that
wrong answer so the grader can name the error instead of just marking it wrong.

**Study guide (2 pages).** Three skill sections, each with a rule box, a worked
example, and a distinct upside-down try-it:

1. A teen number is one ten and some ones (ten-frame model).
2. Reading and writing teen number words (the "-teen" pattern, plus the irregular
   eleven / twelve / thirteen / fifteen).
3. Comparing two teen numbers by their ones digits.

A watch-out box flags the single biggest error: treating the leading 1 as one.

**Verification.** All 10 worksheet answers and all 6 study-guide results were
machine-checked with SymPy (`eval` and `compare` checks); nothing is flagged for
manual review. The full gate chain is green, including the per-problem binding
that ties every printed boxed answer back to its verified value, the facet-
coverage gate (every skill tested on the sheet has a worked example in the guide),
and the prose-consistency gate (100% of worksheet stem numbers trace back to the
verification data).

Standards tag: `1.NBT / 2.NBT.A`, taken verbatim from the skill's standards map.
