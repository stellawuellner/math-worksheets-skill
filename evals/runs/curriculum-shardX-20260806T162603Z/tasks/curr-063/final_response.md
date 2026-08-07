Here are three PDFs on estimating differences and checking reasonableness — a
10-problem workshop, a full step-by-step answer key, and a two-page study guide.

**Worksheet** (`ws_estdiff_curr063.pdf`, 4 pages). Every problem is a real
situation with its unit named and no story detail the student has to wade
through:

- Problems 1, 2, 7: round to the nearest **ten** and subtract — apples left in a
  shop, free seats on a bus, marbles left in a jar. The answer line prints the
  unit.
- Problems 3, 5, 9: round to the nearest **hundred** — library books on the
  shelves, unsold stadium seats, Sunday cinema tickets.
- Problems 4 and 6: estimate first, then work the difference exactly, so the
  estimate is used as a check rather than as a shortcut. Problem 4 adds a claim
  to judge: Mia says 437 eggs are left, and the estimate says about 300.
- Problem 8: a warehouse ships boxes and Ben writes 438. The student estimates,
  explains how the estimate rules 438 out, and then finds the exact answer.
- Problem 10: two students estimate 512 − 288, one to the nearest ten and one to
  the nearest hundred. The student works out both, finds the exact difference,
  and says which estimate landed closer and why.

**Answer key** (`ak_estdiff_curr063.pdf`, 3 pages). Every problem restated and
worked, always naming which digit decides the rounding ("for hundreds, look at
the tens digit") and, where a problem has an exact part, saying which way the
rounding pushed the estimate. A **Common wrong answers** block prints the
declared misconceptions with the number each produces — 437 on problem 4 and 438
on problem 8 are the "opened a hundred but never reduced the hundreds digit"
error, and the rounding slips on problems 1, 3 and 9 are each named — so a wrong
answer tells you what the student did.

**Study guide** (`ss_estdiff_curr063.pdf`, 2 pages). Four sections: estimating to
the nearest ten, estimating to the nearest hundred, checking an exact answer
against an estimate, and spotting an answer the estimate rules out. The last one
carries the rule worth remembering — rounding can move an answer by a few tens,
never by a whole hundred, so a gap that big means the exact working is wrong,
not that the estimate was poor. Each section has a worked example and a try-it
with the answer upside down inside the box.

**How much of this is machine-checked.** The sheet asks for 18 responses; 15 are
machine-checked with SymPy. Every estimate was recomputed by actually rounding
each number to the named place and subtracting — not by trusting my arithmetic —
and every exact difference was recomputed and matched against the printed key.
Each declared misconception was proved to produce a *different* number from the
correct answer, so the traps really do discriminate the errors they name. The
remaining 3 responses are the written judgements: whether Mia's claim is
reasonable (4c), why 438 cannot be right (8b), and which estimate landed closer
and why (10d). Those are genuinely open, so the Quick Answers strip prints `---`
for them, the "What is verified" note names problems 4, 8 and 10, and the key
gives a rubric for each — including what earns half credit. Every numeric answer
on the sheet is verified.
