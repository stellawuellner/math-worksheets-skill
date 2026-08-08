Here are three PDFs on subtracting across a zero — a 10-problem fluency
worksheet, a full step-by-step answer key, and a two-page study guide.

**Worksheet** (`ws_subzero_curr062.pdf`, 6 pages). The set works through the two
shapes this topic actually splits into, then asks the student to use and check
the method:

- Problems 1–3 (305 − 142, 604 − 271, 703 − 258): a zero in the tens place.
  Problem 3 is the hard one — the ones need help *and* the tens have nothing to
  lend, so the borrowing has to start a column further left.
- Problems 4, 6, 9 (400 − 176, 600 − 248, 900 − 457): a number ending in two
  zeros, where it is easier to regroup once across the whole number before
  subtracting anything.
- Problems 5 and 10 (802 − 375, 806 − 349): estimate to the nearest hundred
  first, then subtract exactly. A lost regrouping usually throws the answer out
  by a whole hundred, which is precisely what an estimate catches.
- Problem 7: a word problem in seats (507 − 349), with the unit on the answer
  line.
- Problem 8: a find-and-fix. Rosa worked out 500 − 236 and wrote 364. The
  student subtracts correctly and explains the error.

Each computation problem is set out in the vertical form with room above the
digits for the crossed-out regrouping marks.

**Answer key** (`ak_subzero_curr062.pdf`, 3 pages). Every problem worked column
by column, saying what was opened and what it left ("open a hundred: seven
hundreds and ten tens, then nine tens and thirteen ones"). It also carries a
**Common wrong answers** block: the classic slips are declared as misconception
traps and the system recomputed each wrong result from the mistaken method — so
364 on problem 8, 555 on problem 3, 376 on problem 4, 448 on problem 6, and the
two rounding slips on problems 5 and 10 each come with a one-line diagnosis of
what the student did.

**Study guide** (`ss_subzero_curr062.pdf`, 2 pages). Four sections: borrowing
when the tens are zero, subtracting from a round hundreds number, estimating a
difference first, and finding a lost regrouping. Each has a rule box, a worked
example, and a try-it with the answer upside down inside the box.

**How much of this is machine-checked.** The sheet asks for 14 responses; 12 are
machine-checked with SymPy. Every difference was recomputed and matched against
the printed key, both estimates were recomputed by rounding each number and
subtracting, and each declared trap was proved to give a *different* number from
the correct answer, so the traps genuinely discriminate the errors they name.
The remaining 2 responses are the written explanations in problems 8 and 10.
Those are genuinely open, so the Quick Answers strip prints `---` for them, the
"What is verified" note names problems 8 and 10, and the key gives a rubric for
each — full, half and no credit. The numeric halves of both problems are
machine-checked like the rest.
