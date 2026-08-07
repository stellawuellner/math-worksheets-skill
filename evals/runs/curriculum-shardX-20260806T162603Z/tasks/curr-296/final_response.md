# Evaluating Piecewise and Absolute-Value Functions — three PDFs

- **Study guide (`ss_piecewiseeval_curr296.pdf`, 2 pages)** — three sections. (1) Absolute
  value as a *distance*, with the order of operations spelled out, plus a watch-out box on the
  difference between $-3|x+2|$ and $|-3(x+2)|$. (2) Choosing the piecewise rule *before*
  computing, and why $<$ and $\le$ decide who owns a boundary value. (3) Working backwards
  from an output to the inputs, and why $|A| = k$ always splits into two equations. Each
  section has a rule box, a worked example with an explicit strategy step, and a try-it whose
  answer is printed upside down inside the box.
- **Worksheet (`ws_piecewiseeval_curr296.pdf`, 5 pages)** — 10 problems, each tied to a
  concrete model: a fill-in table, a thermostat whose "error" is an absolute value, a car
  park's two-rate price list, and two piecewise definitions in proper $\begin{cases}$
  notation so the notation and the model always appear together. It ends with a
  linear-quadratic comparison as the synthesis item.
- **Answer key (`ak_piecewiseeval_curr296.pdf`, 4 pages)** — Quick Answers bank, a "What is
  verified" note, a "Common wrong answers" line, a generated Curriculum section, and worked
  solutions that show the substitution and, on the piecewise problems, the condition check
  that came first.

## What is verified

The sheet asks for **21 responses** across 10 problems.

- **18 are machine-checked.** Every table value, every substitution, both absolute-value
  equations and the linear-quadratic system were recomputed with SymPy, and every printed
  boxed answer in the key was separately confirmed against the verified value. Seven of the
  ten problems (1, 2, 4, 5, 6, 7, 8) are fully machine-checked.
- **3 are instructor-judged: 3(b), 9(c) and 10(b)** — the written explanations. These are:
  why $x=2$ takes the second rule (the $\le$ argument, not "2 is bigger"); which of the values
  found in problem 9 actually solve $f(x)=13$ once each rule's condition is applied; and what
  the two intersection points mean. All three are marked `---` in the Quick Answers bank,
  listed by number in the key's "What is verified" note, and given a rubric in the key.

Nothing is marked `[unchecked]`.

## Notes for the adult

- Problem 9 is the important one. Solving both rules gives three candidate values and only one
  of them is a genuine solution; the discarded ones are discarded by *condition*, not by
  arithmetic. If your child can explain that, they understand piecewise functions.
- One misconception trap is declared and machine-checked: on problem 4, dropping the absolute
  value bars gives $x=8$ alone. The key prints that under "Common wrong answers".
- The grade level prints on the answer key only.
