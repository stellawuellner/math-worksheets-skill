Here are three PDFs on correcting unequal shares that have been labelled halves
or fourths — a 6-problem find-and-fix worksheet, a full answer key, and a
two-page study guide.

**Worksheet** (`ws_equalshares_curr049.pdf`, 4 pages). Every problem shows a
strip or rectangle made of equal squares, already cut by someone who got it
wrong, and asks the child to catch it and fix it. Because the shapes are ruled
into squares, a five-year-old can settle the question by counting rather than
by eyeballing:

- Problem 1: Jonah cuts a strip of 8 squares into 5 and 3 and calls them halves.
- Problem 2: Mira cuts a strip of 8 into 3, 2, 2, 1 and calls them fourths —
  four pieces, but not four equal pieces, which is the commonest version of
  this error.
- Problem 3: a strip of 12 cut 8 and 4 and labelled halves.
- Problem 4: a strip of 12 cut 5, 3, 2, 2 and labelled fourths; here the child
  says which parts must change and how.
- Problem 5: a rectangle of 8 squares cut into two parts of *different shapes*
  (6 squares and 2). This separates "equal amount" from "same shape", which is
  where children usually go wrong next.
- Problem 6: Ella claims that cutting more pieces makes each piece bigger. The
  child works out a half and a fourth of the same 12-square strip and says
  whether she is right.

Each problem asks three things: compare the parts, say how big a *true* half or
fourth would be, and explain. Ruled lines are provided for the explanation.

**Answer key** (`ak_equalshares_curr049.pdf`, 3 pages). Every problem restated
and worked. It also carries a **Common wrong answers** block: for five of the
six problems I declared the classic misconception — sharing into four when the
task said halves, or into two when it said fourths — and the system recomputed
the number a child making that error would write. So if a child writes 2 where
4 belongs on problem 1, the key tells you what they did rather than just marking
it wrong.

**Study guide** (`ss_equalshares_curr049.pdf`, 2 pages). Three sections: fixing
two parts called halves, fixing four parts called fourths, and why a half of
something is always bigger than a fourth of it. Each has a rule box (with a
picture of a correctly halved strip), a worked example, and a try-it with the
answer upside down inside the box.

**How much of this is machine-checked.** The sheet asks for 17 responses in
all. 12 of them are machine-checked with SymPy — every comparison symbol and
every "how many squares in a true half/fourth" answer was recomputed and matched
against the printed key, and each declared misconception was proved to give a
*different* number from the correct one, so the traps genuinely discriminate.
The remaining 5 responses are the "explain" parts of problems 1, 2, 4, 5 and 6.
Those are genuinely open, so the Quick Answers strip prints `---` for them, the
"What is verified" note names those problems, and the key carries a rubric for
each saying what earns full, half and no credit. Only problem 3 has no written
part, so the key reports 1 of 6 problems *fully* machine-checked — that number
counts whole problems, not responses, and every numeric answer on the sheet is
verified.
