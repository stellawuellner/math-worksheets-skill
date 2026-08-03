# Ten-Frames: How Many Do You See? — Kindergarten / Grade 1

Three PDFs are ready: the student worksheet, a full step-by-step answer key written
for the adult sitting beside the child, and a two-page study guide.

**Worksheet (4 pages, 10 problems).** Every problem shows a real ten-frame — two
rows of five boxes, drawn to size, with the counters filled in. All ten problems are
about structured quantities to 10 on those frames:

- **Say how many** (1, 2, 3, 5, 8): starts with a full top row so the child can say
  "five" and count on, then breaks the pattern with 4-above-4 (a doubles picture)
  and, at problem 8, a frame whose top row is *not* full — the one arrangement that
  catches a child who has learned "top row means five" as a rule instead of a
  observation.
- **How many more make ten** (4, 7): the empty boxes are the missing amount.
- **Compare two frames** (6, 9, 10): less-than, then two different arrangements of
  the same amount (the answer is `=`), and finally a comparison of the *empty*
  boxes, where the frame with more dots needs fewer.

Each problem has 3–4 cm of blank space and its own answer line.

**What was verified.** All 10 answers were recomputed independently with SymPy
before anything was typeset: 7 count/quantity checks and 3 comparison checks
(`<`, `=`, `>`). The answer key's boxed answers were then bound problem by problem
to those verified values, so the key cannot drift from the pictures. **Nothing is
flagged for manual review.**

I also declared three *misconception traps*, which the verifier confirmed are
distinguishably wrong and which are printed in the answer key as "common wrong
answers": counting the empty boxes as if they held counters (problem 1), counting
only the top row (problem 5), and assuming the top row is full when it holds three
(problem 8). If your child gives one of those numbers, the key tells you exactly
which habit produced it.

**Answer key (3 pages).** Every problem is re-shown with numbered steps in plain
language, plus a "listen for" or teaching note where a specific wrong answer is
likely. The quick-answer bank at the top is for fast checking. The grade level
appears on this document only — never on the pages the child works from.

**Study guide (2 pages).** Three sections — say how many, how many more make ten,
and which frame shows more — each with a rule box, a worked example with its own
ten-frame picture, and a try-it whose answer is printed upside down inside the box
so the child can check it without being shown the work. All six study-guide answers
were verified by the same gate as the worksheet.

**Note on standards.** All problems are tagged `K.CC.A.1–K.CC.C.7`, which is how the
skill's standards map writes the counting-and-cardinality band; the narrower
K.CC.B.4–B.5 sub-codes this task cites are inside that range but do not appear as
their own row in the map, so I used the map's string rather than inventing one.
