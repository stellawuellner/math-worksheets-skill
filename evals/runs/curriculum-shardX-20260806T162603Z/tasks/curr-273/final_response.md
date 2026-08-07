# Writing Recursive Rules for Arithmetic Sequences — Algebra 1

Three PDFs are ready:

- **Worksheet** (`ws_recursive_curr273.pdf`) — 10 problems, every one of them about building or
  running a recursive rule $a_1 = \ldots$, $a_n = a_{n-1} + d$. Deliberately, **no problem hands
  the student the first term**: two known terms are given (or two stages of a situation) and the
  student finds the step, walks back to $a_1$, states the rule, then uses it. Four are pure
  sequence problems, three are applications with units (theatre rows, weekly deposits, ladder
  rungs), and three run a given rule forward — listing terms, summing the first ten, and finding
  where two sequences meet. Difficulty ramps 1 → 5.
- **Answer key** (`ak_recursive_curr273.pdf`) — each step shown: how many *jumps* separate the two
  known terms, the division that gives $d$, the walk back to $a_1$, the stated rule, and the
  jump-count to the requested term. Quick Answers, a "Common wrong answers" block for the three
  declared misconceptions, and a Curriculum block sit at the top.
- **Study guide** (`ss_recursive_curr273.pdf`) — 2 pages: finding the step and the starting value,
  the same job from a situation, and extending/summing. Each has a rule box, a worked example
  whose first step says why that route was chosen, and a try-it with the answer upside down.

## What is verified, honestly

- **29 machine checks passed.** Every step $d$, every first term, every requested later term, the
  ten-term sum (checked as a symbolic summation), and the term number where the two sequences
  meet were recomputed by SymPy and matched the printed key.
- **1 response is instructor-judged**: problem 4(c), "explain why the step rule alone does not pin
  down the sequence". That is a written argument, so it carries a `manual` entry and a printed
  rubric. The key's "What is verified" note names problem 4 as the only `---`.
- **3 misconception traps** were machine-tested for distinguishability: subtracting the terms in
  the wrong order, counting one row too many when walking back, and multiplying the step by the
  term number instead of one less. Each provably lands on a different number from the right
  answer, and the key prints what a student who got it would have done.
- All six study-guide examples and try-its were verified.

Nothing is marked `[unchecked]`.
