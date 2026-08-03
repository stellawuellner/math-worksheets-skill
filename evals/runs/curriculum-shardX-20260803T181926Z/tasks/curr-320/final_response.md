# Similar triangles: sides, perimeter, and area — three PDFs

Here is a 10-problem geometry set on similarity and the two scale
relationships students most often mix up: perimeter scales by $k$, area scales
by $k^2$.

**What is in each document**

- **Worksheet** (`ws_simscale_curr320.pdf`, 4 pages). Ten problems that rotate
  between three decisions: *find the scale factor or a missing side*, *scale a
  perimeter*, and *scale an area*. Problems 1–2 warm up on the scale factor
  itself; from problem 3 on, the three are interleaved, so the student has to
  decide whether the situation calls for $k$ or $k^2$ rather than reuse the
  last method. Two problems run the relationship backwards (given two areas,
  find a perimeter; given two perimeters, find an area), which is where the
  square root has to be taken. Problem 5 asks for the similarity criterion in
  words before the computation, problem 6 is the classic shadow measurement,
  and problem 10 is a challenge that chains perimeter ratio to area ratio and
  then asks *why*. Every answer has a unit blank printed with the unit the
  answer is checked in.
- **Answer key** (`ak_simscale_curr320.pdf`, 3 pages). Answers at a glance,
  then a numbered solution per problem — the pairing of corresponding parts,
  the proportion, the arithmetic, and the boxed answer with its unit — plus
  "listen for" notes naming the specific wrong answer each problem is designed
  to catch ($\frac{6}{15}$ instead of $\frac{15}{6}$; scaling an area by $k$;
  scaling a perimeter by the area ratio).
- **Study guide** (`ss_simscale_curr320.pdf`, 2 pages). Three sections — scale
  factor and missing sides, perimeter, area — each with the rule, a worked
  example that opens by saying which relationship the question needs, and a
  try-it whose answer is printed upside down inside the box. The watch-out box
  states the two errors the worksheet targets.

**What was verified**

All 11 machine-checkable answers were recomputed with SymPy before compiling:
each proportion, each perimeter scaling, and each area scaling including the
square-root direction in problem 8. The printed key was then bound
problem-by-problem to those values *and to the declared units*, so a
centimetre answer cannot be printed in feet. The two declared misconception
traps were machine-checked to be distinguishably wrong: scaling the tile area
by $\frac{3}{2}$ instead of $\frac{9}{4}$ gives 60 rather than 90, and scaling
the perimeter by the area ratio gives 26.67 rather than 20.

**Flagged for manual review (2 items)**

- Problem 5(a) — naming and justifying the AA criterion. The computed side
  ($DE = 8$ cm) is verified; the justification is a written answer, and a model
  argument is in the key.
- Problem 10(c) — explaining why doubling every side quadruples the area. Parts
  (a) and (b) are verified; part (c) is the reasoning, with a model answer in
  the key.

No figures are printed: every problem states its correspondence in words
($\triangle ABC \sim \triangle PQR$, with the sides named), which keeps each
problem's given values unambiguously its own.

Suggested order: study guide first, then the worksheet, then the answer key.
