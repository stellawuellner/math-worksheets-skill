Here are three PDFs on composing larger shapes from smaller two-dimensional
shapes — a 10-problem interleaved review, a full answer key, and a two-page
study guide.

**Worksheet** (`ws_composeshapes_curr050.pdf`, 5 pages). Every figure is drawn
on small squares, so a five- or six-year-old settles each question by touching
and counting rather than by guessing from the outline. The sheet blocks a short
warm-up and then interleaves four different jobs, so the child has to decide
what the question is asking rather than repeat one move:

- Problems 1–3 (warm-up): count the small squares in a built shape — two
  squares side by side, a corner piece, then a rectangle where counting a whole
  row at a time is faster.
- Problem 4: two matching triangles joined along their long edges. Name the new
  shape, then say how much it covers.
- Problem 5: two builds side by side — which uses more squares?
- Problem 6: a part-built rectangle. How many more squares are needed?
- Problem 7: back to counting, now on a plus-shaped figure.
- Problem 8: two corner pieces interlocking into a rectangle — name it and
  count it.
- Problem 9: two shapes that look nothing alike and use the same eight squares.
  The child compares them and explains how that is possible.
- Problem 10 (synthesis): finish a rectangle, and explain the method used
  instead of placing squares one at a time.

**Answer key** (`ak_composeshapes_curr050.pdf`, 3 pages). Each problem restated
and worked, with the counting strategy named each time (count a row at a time;
ignore the join line; take the placed squares from the finished total). Quick
Answers and a Curriculum block (1.G) sit at the top.

**Study guide** (`ss_composeshapes_curr050.pdf`, 2 pages). Four sections, one
per job: counting the small squares, naming the shape the pieces make,
comparing two builds, and finishing a build. Each has a rule box, a worked
example — two of them with a small picture — and a try-it with the answer
printed upside down inside the box.

**How much of this is machine-checked.** The sheet asks for 14 responses. 10 of
them are machine-checked with SymPy: every "how many small squares" answer was
recomputed from the figure's own corner coordinates (so the picture and the
answer cannot disagree), both comparison symbols were recomputed, and both
"how many more are needed" answers were recomputed as a subtraction. The other
4 responses are open: naming the built shape in problems 4 and 8, and the
explanations in problems 9 and 10. A shape's name is a word rather than a
computed value, so those are flagged rather than claimed — the Quick Answers
strip prints `---`, the "What is verified" note names problems 4, 8, 9 and 10,
and the key gives a rubric for each, including which near-misses earn half
credit (for instance "rectangle" for the square in problem 4). The count half of
problems 4 and 8 is machine-checked like the rest.
