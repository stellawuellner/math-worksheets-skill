# When a Number Rule Stops Working — Grades 4–5

Three PDFs: the student worksheet, a full step-by-step answer key, and a two-page study
guide.

**Worksheet (8 problems).** Every problem puts a named child in front of a few numbers,
lets them jump to a rule, and asks your child to find the case that breaks it. That is
the whole skill here — an "every / always" claim built from three friendly examples is
the most common way a fourth-grader goes wrong with factors, multiples and patterns.

The sheet works three related moves and mixes them so no two neighbouring problems use
the same one:

- **Repairing a pattern that drifted** (1, 5) — Ravi adds 8 once by mistake and carries
  the error forward; Toby sees the first step of 1, 4, 9, 16 is +3 and assumes it stays
  +3.
- **Testing a rule instead of trusting it** (3, 6, 7) — "every term in my pattern is
  prime", "a bigger starting number always wins", "the terms are all odd so the rule
  must be adding an even number".
- **Factor and prime facts** (2, 4, 8) — last digits do not decide primality; not every
  multiple of 3 is odd; and the closing problem asks why "divisible by 2 and 3 means
  divisible by 6" works while "divisible by 2 and 4 means divisible by 8" does not.

Two problems are explicit find-and-fix items (1 and 5), and both planted wrong answers
are declared as machine-checked misconception traps, along with two more on problems 1
and 3. The answer key prints them in a "Common wrong answers" block: 24 and 30 for
Ravi's drifted pattern, 19 for skipping past the counterexample, 13 for "add 3 every
time". Each trap was checked to be a value the problem's own verification rejects, so
none of them is accidentally also correct.

**Answer key.** Full reasoning per problem, not just answers: the term-by-term rebuild
for the pattern problems, the factor pair for each counterexample, and — for every
explain part — a written statement of what a full-credit response must contain.

**Study guide (2 pages).** Three sections (test the rule; last digits do not decide
primes; repairing a drifted pattern), each with a rule box, a worked example whose first
step says *why* that approach is chosen, and a try-it with the answer upside down inside
the box. A watch-out box closes it: a property the terms share is not the rule that made
them.

## What is verified, honestly

This sheet asks for 18 separate responses across 8 problems, and the split is unusually
lopsided because diagnosis is the point of the assignment:

- **11 responses are machine-checked** with SymPy — every corrected pattern term, every
  counterexample, both 10th terms and the `<` comparison in problem 6. The printed
  answer key was bound back to those verified values by the build.
- **7 responses are instructor-judged** and print as `---` in the Quick Answers bank:
  the explanation part of problems 1, 3, 4, 5, 6, 7 and 8. Only problem 2 is fully
  machine-checked end to end, which is why the key's own note reads "1 of 8 problems
  fully machine-checked" — the other seven each carry a written half that no computer
  algebra system can grade.

That is not a gap in the checking; it is what a misconception-analysis sheet is. The
answer key states, for each of those seven, the specific idea a correct explanation has
to contain — for problem 8, for instance, that 2 and 3 share no factor while 4 already
contains the 2. Read those seven; the rest grades itself.
