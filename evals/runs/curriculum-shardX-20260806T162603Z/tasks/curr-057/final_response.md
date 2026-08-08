Here are three PDFs on adding three-digit numbers with regrouping — a
10-problem fluency worksheet, a full step-by-step answer key, and a two-page
study guide.

**Worksheet** (`ws_addregroup_curr057.pdf`, 5 pages). The set ramps from one
regroup to two, then to problems that ask for judgement, and no two problems
share the same shape:

- Problems 1 and 2: one regroup, out of the ones column only (347 + 128,
  256 + 137), set out in the vertical form with room for the carry digits.
- Problems 3 and 5: two regroups (486 + 275, 594 + 268) — the second carry only
  appears once the first has been added in, which is the step children skip.
- Problems 4 and 7: estimate by rounding each number to the nearest hundred,
  then add exactly, so the estimate is used as a check rather than as an answer.
- Problem 6: a word problem in pages (354 + 427), with the unit printed on the
  answer line.
- Problem 8: a find-and-fix. Dev added 476 + 258 and wrote 624. The student adds
  correctly and explains the error.
- Problem 9: three addends (268 + 145 + 87 books), where a carry can be worth
  two tens rather than one.
- Problem 10: estimate, add exactly, then explain how close the estimate came
  and why it landed above the exact sum.

**Answer key** (`ak_addregroup_curr057.pdf`, 3 pages). Every problem is worked
column by column, naming the carry each time. It also carries a **Common wrong
answers** block: I declared the classic slips as misconception traps — the
dropped ones carry, both carries thrown away, rounding to tens instead of
hundreds, rounding only one addend — and the system recomputed each wrong result
from the mistaken method. So 624 on problem 8, 751 on problem 3, 752 on problem
5, 920 on problem 7 and 856 on problem 10 each come with a one-line diagnosis of
what the student did.

**Study guide** (`ss_addregroup_curr057.pdf`, 2 pages). Four sections: adding
with one regroup, adding with two, estimating a sum and then adding, and finding
a lost carry. Each has a rule box, a worked example, and a try-it with the
answer printed upside down inside the box.

**How much of this is machine-checked.** The sheet asks for 14 responses; 12 are
machine-checked with SymPy. Every sum was recomputed and matched against the
printed key, every estimate was recomputed by rounding each addend and adding
(not by trusting my arithmetic), and every declared trap was proved to give a
*different* number from the correct answer, so the traps really do discriminate
the error they name. The remaining 2 responses are the written explanations in
problems 8 and 10. Those are genuinely open, so the Quick Answers strip prints
`---` for them, the "What is verified" note names problems 8 and 10, and the key
gives a rubric for each — what earns full credit, what earns half, and what
earns none. The numeric halves of both problems are machine-checked like the
rest.
