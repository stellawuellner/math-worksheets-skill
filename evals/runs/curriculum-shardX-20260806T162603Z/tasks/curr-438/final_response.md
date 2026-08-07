Here are the three PDFs for a 10-problem precalculus/statistics set on **calculating
conditional and independent-event probabilities**.

**Worksheet — `ws_condprob_curr438.pdf` (4 pages).** The sheet opens with one survey table
(120 students, sport by instrument) that five of the problems read from, so the student
works with a single concrete representation rather than a new story per item. The rest are
real applications with the givens stated as numbers, not atmosphere: two cards drawn
without replacement, a production line with a stated defect rate, and a screening test
with a stated prevalence, sensitivity and false-positive rate. Difficulty ramps 1 → 5, and
the four methods (reading a table, conditioning, testing independence, the multiplication
rule) are interleaved so the student has to choose one.

The last table problem and the screening problem are the two that matter most: problem 3
deliberately reverses problem 2's condition so the student sees $P(A \mid B) \ne
P(B \mid A)$ on their own data, and problem 9 makes the same point with a 90%-sensitive
test whose positive result is only 37% likely to be real.

**Answer key — `ak_condprob_curr438.pdf` (3 pages).** Every problem restated and worked
line by line, with a quick-answer bank, a curriculum block, and a "common wrong answers"
list generated from five machine-checked misconception traps — dividing by the grand total
instead of the row total, treating a without-replacement draw as independent, adding
probabilities instead of multiplying, multiplying a defect rate by 5 instead of using the
complement, and reporting sensitivity when asked for the reverse conditional.

**Study guide — `ss_condprob_curr438.pdf` (2 pages).** Four sections, one per skill, each
with the rule, a worked example that starts by naming why that rule applies, and a try-it.
A watch-out box flags the $P(A\mid B)$ versus $P(B\mid A)$ confusion.

**What was verified, honestly.** The sheet asks for **16 separate responses**. **13 are
machine-checked** with SymPy — every probability computed as an exact fraction, the
algebraic expansion in problem 8, and the two rounded decimals in problems 7 and 9
recomputed exactly and compared at the printed precision. **3 are instructor-judged** and
marked `---` in the quick-answer bank: the independence conclusion in problem 4(c), the
interpretation of the expansion's terms in problem 8(b), and the independence argument in
problem 10(c). Those are written reasoning, which no computer algebra system can grade;
the key prints a model response and a full-credit criterion for each. The eight
study-guide examples and try-its are machine-checked.

No answer on the sheet is marked `[unchecked]` — every printed response either carries a
machine check or a written rubric.
