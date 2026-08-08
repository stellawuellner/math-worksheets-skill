# Putting Patterns, Data and Points Together — Grades 4–5

Three PDFs: the student worksheet, a full step-by-step answer key, and a two-page study
guide.

**Worksheet (12 problems).** This is an interleaved review sheet, so the point is that
your child has to decide *which display and which method* each problem needs. Two
displays sit at the top: a **Two Rules table** (pattern S starts at 3 and adds 4;
pattern T starts at 1 and adds 6) and a **Book Plot** showing how many books each of 12
students read.

Problems 1–4 warm up on the pattern rules alone: the 8th term of each, the term where
the two patterns agree, and the gap between their 10th terms. From problem 5 on the four
kinds rotate:

- **reading the plot** (5, 8, 9) — how many read exactly 3; how many read *more than* 3
  (which excludes the stack sitting on 3); how many more read 3 than read 5;
- **coordinate pairs** (6, 10) — pairing matching terms of S and T, then plotting
  (term number, value) for four terms and seeing that a constant-step pattern always
  plots straight;
- **summarising data** (7, 11, 12) — the total books across the whole plot, the median
  and the mean, and finally a combined task: the club's weekly totals follow pattern S,
  so week 6 comes from the pattern rule and the six-week total comes from the data.

Problem 12(c) is the synthesis: use the *mean* to check the *total*, which is a real
check rather than adding the same six numbers again.

**Answer key.** Each solution names which display it reads and shows the terms generated
or the counts read. Two habits get pointed out explicitly: the count of crosses (12) and
the total of books (42) answer different questions about the same plot, and a bent line
on a plotted pattern means a term was generated wrongly, not a new shape.

**Study guide (2 pages).** Four sections, one per method: jumping to any term, counting
from a line plot, turning a pattern into ordered pairs, and totalling a whole plot
(including the mean-times-count check). Each has a rule box, a worked example whose
first step names the strategy, and a try-it with the answer upside down inside the box.

## What is verified, honestly

The sheet asks for 17 separate responses across the 12 problems.

- **15 are machine-checked** with SymPy: every generated term, the meeting term solved
  from 3 + 4(n−1) = 1 + 6(n−1), the gap of 16, both coordinate pairs, every count read
  off the Book Plot, the 42-book total, the median and mean of 3.5, and the six-week
  total of 78. The Book Plot's counts live in the verification data, so the drawn plot
  and the answers come from one source, and the key was bound back to the verified
  values by the build.
- **2 are instructor-judged** and print as `---` in the Quick Answers bank: the four
  plotted points in problem 10(b) — a drawing, which nothing can check automatically —
  and the written explanation in problem 12(c). The key gives the exact coordinates to
  check the drawing against, and states that 12(c) needs the mean-times-count idea
  rather than a repeat of the addition.

Ten of the twelve problems are fully machine-checked end to end.
