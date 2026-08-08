# Off-by-One Errors in Sequence Indexing — Algebra 1

Three PDFs are ready:

- **Worksheet** (`ws_offbyone_curr274.pdf`) — 8 error-analysis problems, each showing work whose
  index is off by exactly one: adding the step $n$ times instead of $n-1$, dividing by the larger
  index instead of the index difference, reading a rule's first term at $n = 0$, subtracting
  indices to count a block of terms, and summing from $n = 0$. The student repairs the
  computation and, on five of them, names the miscount. Difficulty ramps 1 → 5, and the closing
  problem asks what the two remaining mistakes have in common.
- **Answer key** (`ak_offbyone_curr274.pdf`) — every correction worked out with the jump count
  written explicitly, a "Common wrong answers" block naming the five declared misconceptions and
  the exact number each produces (26, 6.25, 14, 54, 702), and a written rubric for each
  diagnosis. Quick Answers and a Curriculum block sit at the top.
- **Study guide** (`ss_offbyone_curr274.pdf`) — 2 pages built round the fence-post idea: jumps are
  one fewer than terms, where an explicit rule starts, and counting terms in a block. Each section
  has a rule box, a worked example, and a try-it with the answer upside down inside the box.

## What is verified, honestly

- **13 machine checks passed.** Every corrected value — the terms, the step, the term counts, the
  two summations (checked as symbolic sums, including the student's $n = 0$ version), and the two
  solve-for-the-term-number answers — was recomputed by SymPy and matched the key.
- **5 diagnoses are instructor-judged**: problems 1(b), 3(c), 4(b), 6(c) and 8(c). Those are
  written explanations, so they carry `manual` entries and printed rubrics. The key's "What is
  verified" note lists exactly those five as `---`.
- **5 misconception traps** were machine-tested for distinguishability, so each wrong method
  provably lands on a different number from the correct answer.
- All six study-guide examples and try-its were verified.

Nothing is marked `[unchecked]`.
