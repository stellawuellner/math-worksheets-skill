# Finding Order and Scale Mistakes on Graphs — Grades 4–5

Three PDFs: the student worksheet, a full step-by-step answer key, and a two-page study
guide.

**Worksheet (8 problems).** Two displays sit at the top and every problem uses one of
them: a coordinate **Grid** with five labelled points, and a **Book Graph** whose
vertical axis is marked every 5 books. Both displays exist to set the two traps this
sheet is about.

- **Order errors** (problems 1 and 4). Ravi is told to plot (2, 5) and his mark lands on
  point B; the student has to read B's real pair off the grid and say what the mistake
  was. Problem 4 then makes the point measurable: C and D are a reversed pair, and the
  question asks how far apart they actually are.
- **Scale errors** (problems 2, 3, 6, 8). Leo reads 7 marks as 7 books; Sam reads 2
  marks as 2 books; the same data redrawn with a finer interval makes a student think
  more books were read; and the closing problem has a student count 30 marks up an axis
  whose marks are worth 5 each — landing at 150 instead of 30.
- **Scale errors inside a summary** (problems 5 and 7). Mia adds the mark counts and
  reports 21 books for the week; another student averages the mark counts and reports
  4.2 books a day. Both answers are wrong by exactly the interval — 21 × 5 = 105 and
  4.2 × 5 = 21 — and the key points that out, because that arithmetic relationship is
  the tell.

**Seven misconception traps are declared and machine-checked**, one for almost every
problem: the mark-count-as-value error (2, 3), the reversed-pair-is-the-same-place error
(4), the summed mark counts (5), the mean of mark counts (7), the stale interval (6),
and the cross-axis interval (8). Each was verified to be a value the problem's own check
rejects, and all seven are printed in the key's "Common wrong answers" block.

**Answer key.** Each solution reads the interval before reading the graph, shows the
multiplication, and states what a full-credit explanation must contain. Problem 8's
solution separates the two faults explicitly, because "the point is in the wrong place"
would hide the fact that there were two.

**Study guide (2 pages).** Three sections: the order inside an ordered pair, what one
mark on an axis is worth (with the "find the interval by subtracting two neighbouring
labels" habit), and totals and means when the axis is scaled. A watch-out box closes it:
a taller bar does not always mean a bigger number.

## What is verified, honestly

The sheet asks for 15 separate responses across the 8 problems.

- **11 are machine-checked** with SymPy: both of B's coordinates (read from the same
  data the Grid is drawn from), every mark-times-interval conversion, the week's true
  total of 105, the mean of 21 and the range of 25, and both parts of problem 8's
  arithmetic. The printed key was bound back to those verified values by the build.
- **4 are instructor-judged** and print as `---` in the Quick Answers bank: the
  diagnosis half of problems 1, 3, 6 and 8. The key states what each needs — naming the
  across-then-up order for 1, the size of one interval for 3, "the picture changed and
  the data did not" for 6, and *both* faults for 8.

Four of the eight problems are fully machine-checked end to end. The other four each
pair a checked number with a written diagnosis, which is the shape a misconception sheet
should have — the diagnosis is the assignment.
