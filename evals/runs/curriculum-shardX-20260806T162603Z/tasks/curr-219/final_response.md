Here are the three PDFs for a Grade 8 / Pre-Algebra error-analysis set on
**slope and rate of change, focused on inverted (upside-down) and sign-reversed
slope calculations**.

**Skills Summary (study guide)** — `ss_slopeerrors_curr219.pdf`, 2 pages.
An opening box names the two failure modes side by side ("upside down" gives
the reciprocal, "sign flipped" gives the right digits with the wrong sign),
then three sections: which difference goes on top, keeping the sign right, and
reading a rate of change from a table. Each has a rule box, a two-step worked
example, and a try-it with the answer printed upside down inside the box.

**Worksheet** — `ws_slopeerrors_curr219.pdf`, 4 pages, 8 problems.
Problem 1 is a plain slope computation to set the pattern. Problems 2–8 are all
diagnostic: six find-and-fix items (well past the two requested) where a named
student's wrong work is printed and the task is to compute the correct slope
and say what went wrong, plus two table problems where the wrong rate is
quoted as an un-simplified fraction so the inversion is visible. Four items
target inversion and four target sign reversal, so the student has to
distinguish the two rather than apply one label. Each part has its own answer
blank; multi-part items get about 2 cm of writing room per part.

**Answer key** — `ak_slopeerrors_curr219.pdf`, 3 pages.
Quick Answers bank, a "Common wrong answers" line for every declared trap
(generated from the verification data, so the grader sees "if they got 0.5:
inverted the ratio"), then a full worked solution per problem. The curriculum
block records 8.EE.B.5 / 8.EE.B.6 and difficulty 1–4.

**What is verified, honestly.** Eighteen checks were declared across the eight
problems. **Ten are machine-checked with SymPy**: every numerical slope and
every table difference on the sheet. Eight misconception **traps are also
machine-checked** — each planted wrong answer was recomputed from the wrong
method and proved to be a value the correct answer rejects, so no problem on
this sheet is blind to the error it is meant to catch.

**Seven responses are instructor-judged, not machine-checked**: the written
"name the error" or "explain who is right" part of problems 2–8. A written
diagnosis cannot be verified by a computer algebra system. The answer key does
not claim otherwise — the Quick Answers bank prints `---` for each of those
parts, and because every problem from 2 on carries one, the key's generated
note reads "1 of 8 problems fully machine-checked" and names problems 2–8 as
carrying an instructor-judged part. That is the correct reading: all the
numbers are checked, all the sentences are yours to grade, and each worked
solution states what a correct explanation must say and what should not earn
credit.
