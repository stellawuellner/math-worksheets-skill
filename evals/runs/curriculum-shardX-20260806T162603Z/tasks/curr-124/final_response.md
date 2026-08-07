# Comparing Fractions Without Being Fooled — Grades 4–5

Three PDFs: the student worksheet, a full step-by-step answer key, and a two-page study
guide.

**Worksheet (8 problems).** Every problem targets one specific way fourth- and
fifth-graders go wrong with fractions: comparing only the top numbers, or only the
bottom numbers, as if either were an ordinary whole number. The sheet is built so that
habit gives a visibly wrong answer every time.

- **Problem 2** (4/9 vs 4/7) and **problem 8** (6/7 vs 6/13, 5/12 vs 5/8) hold the
  numerator fixed, so only piece size can decide.
- **Problems 3, 5 and 6** are find-and-fix items with a named child and a written wrong
  claim: Dev says 3/8 > 3/5 "because 8 is greater than 5" (denominator-only); Sam says
  5/6 < 7/12 "because 5 is less than 7" (numerator-only); Lena says 6/10 and 3/5 must be
  different amounts "because none of their digits match". Each asks the student to
  rebuild the fractions over a common denominator, write the correct sign, and then say
  what went wrong.
- **Problems 4 and 7** work the benchmark route — one half decides 2/7 against 5/8
  instantly, and problem 7 is the case where the benchmark is *not* enough (three
  fractions all above a half) and a common denominator is needed.
- **Problem 1** is the equivalence warm-up, and the additive error (adding 8 to the top
  because 8 was added to the bottom) is declared as a trap.

Three misconception traps are declared and machine-checked: the additive equivalence
error on problem 1, and — on problems 3 and 6 — the "swap the denominator, leave the
numerator alone" move, which is the same denominator-only habit wearing a different
hat. All three appear in the key's "Common wrong answers" block, and each was verified
to be a value the problem's own check rejects.

**Answer key.** Each solution shows the scale factor, the rewritten fractions, and the
comparison of counts — never a bare sign. Every explain-part carries a written statement
of what a full-credit response must contain.

**Study guide (2 pages).** Three sections: building an equivalent fraction (multiply,
never add), comparing over a common denominator (with the same-numerator rule stated
correctly), and using one half as a benchmark. Each has a rule box, a worked example
whose first step names the strategy, and a try-it with the answer printed upside down.
A watch-out box names both errors side by side.

## What is verified, honestly

The sheet asks for 16 separate responses across the 8 problems.

- **12 are machine-checked** with SymPy: every equivalent numerator, every comparison
  sign, the lowest-terms form of 6/10, and the three-fraction ordering in problem 7. The
  printed answer key was bound back to those verified values by the build.
- **4 are instructor-judged** and print as `---` in the Quick Answers bank: the
  diagnosis half of problems 3, 5 and 6, and the "state the true rule and say why" part
  of problem 8. These are written reasoning and cannot be machine-graded.

That is why the key reports 4 of 8 problems as *fully* machine-checked: the other four
each have a numeric half that was checked and a written half that was not. The diagnosis
is the point of a misconception sheet, so those four are the ones worth reading. For
each, the key states the specific idea a correct answer must contain — piece size for
problems 3 and 6, the shared factor of 2 for problem 5, and both the corrected rule and
its reason for problem 8.
