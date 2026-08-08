# Missing Roots and Sign Errors in Quadratic Solutions — three PDFs

- **Study guide (`ss_quaderrors_curr294.pdf`, 2 pages)** — three sections aimed straight at the
  two errors: taking *both* square roots, the zero-product property (and why you must never
  divide both sides by $x$), and the signs in the quadratic formula ($-b$ at the front, $2a$
  in the denominator). Each has a rule box, a worked example whose first step explains the
  choice of method, and a try-it with its answer printed upside down inside the box. A
  watch-out box explains the point students find genuinely confusing: $\sqrt{25}$ by itself
  means $5$; the $\pm$ comes from rooting *both sides of an equation*.
- **Worksheet (`ws_quaderrors_curr294.pdf`, 4 pages)** — 8 problems, ramped 1 to 5. Three are
  find-and-fix items (2, 4 and 8) where a named student's work is shown with exactly one
  mistake in it; the rest are straight solves chosen so the canonical error produces a
  visibly wrong answer. Work space runs 4.5–8 cm.
- **Answer key (`ak_quaderrors_curr294.pdf`, 3 pages)** — Quick Answers bank, a "What is
  verified" note, a **Common wrong answers** block (see below), a generated Curriculum
  section, and full worked solutions that show the substitution check as well as the algebra.

## What is verified

The sheet asks for **12 responses** across 8 problems.

- **8 are machine-checked.** Every solution set and the one rounded root were recomputed with
  SymPy, and the printed boxed answers in the key were separately confirmed to match the
  verified values. Five of the eight problems (1, 3, 5, 6, 7) are fully machine-checked.
- **4 are instructor-judged**, all of them the "name the error" and "explain" halves of the
  find-and-fix items: **2(a), 4(a), 8(a) and 8(c)**. These are written diagnoses, which no
  computer algebra system can grade. Each is marked `---` in the Quick Answers bank, the
  problems are named in the key's "What is verified" note, and the key states what full credit
  requires — for instance, 4(a) needs the student to name the *lost root* $x=0$, not merely
  say "you cannot divide by a variable".

No answer is marked `[unchecked]`.

## The misconception traps are machine-checked too

Every planted wrong answer on this sheet was declared in the verification data and proved
**distinguishably wrong** before the PDFs compiled — that is, the sheet's own check would
reject it. They are printed in the answer key as a "Common wrong answers" line under each
problem, so if your child hands back $x = 4$ on problem 2, the key tells you immediately that
they kept only the positive square root, and on problem 4 that $x=6$ alone means the root
$x=0$ was divided away.

## Notes for the adult

- The grade level prints on the answer key only.
- Problem 6 asks the student to write down $a$, $b$ *and* $-b$ before substituting. That one
  habit removes most quadratic-formula sign errors.
