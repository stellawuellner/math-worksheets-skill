Here are the three PDFs for the right-triangle error-analysis set:

- **Worksheet** — `ws_trigerrors_curr324.pdf` (4 pages)
- **Answer key** — `ak_trigerrors_curr324.pdf` (3 pages)
- **Study guide** — `ss_trigerrors_curr324.pdf` (2 pages)

**What the worksheet covers.** Six problems, each showing a calculation that
produced a wrong answer, evenly split across the three error families named in
the topic:

- **wrong ratio** — cosine used where sine was needed (1), tangent used to find a
  hypotenuse it cannot reach (6);
- **wrong inverse** — inverse tangent applied to an opposite/hypotenuse pair (3),
  and a ratio reported as if it were the angle (4);
- **degree mode** — a calculator left in radians returning a *negative* side
  length (2) and a rise less than half its true value (5).

Every problem asks two things: redo it correctly, and name the error. Four of the
six also ask what about the printed answer should have given it away, which is
the habit the sheet is really training. Each problem carries its own diagram,
generated from the same givens the answer is checked against, with a value-free
reference triangle at the top fixing the labelling convention.

**What is verified, honestly.** The verification file holds 12 entries — one per
response, because a find-and-fix item is two answers.

- **6 entries are machine-checked** with SymPy: 11.18 cm, 9.23 in, 32.58°,
  54.62°, 14.78 m, 29.73 ft.
- **6 entries are instructor-judged**: the "name the error" half of every
  problem. Written diagnosis cannot be machine-checked, so the key prints a
  grading rubric for each.

Because every problem pairs a computed value with a written diagnosis, **no
problem is fully machine-checked end to end** — the key's "What is verified" note
says exactly that, and the Quick Answers bank shows `---` in the (b) slot of all
six. No answer is marked `[unchecked]`.

All six wrong answers are declared as misconception traps and independently
recomputed, so the key's "Common wrong answers" block confirms that 16.58 cm,
−2.44 in, 28.30°, 0.58°, 7.11 m and 14.41 ft really are what each named error
produces — the planted numbers are derived, not typed.

**Study guide.** Three sections matching the three error families: name the two
sides before choosing the ratio; match the inverse to the pair of sides you have
(and remember that dividing gives the ratio, not the angle); and check
DEG mode plus estimate the size before accepting a result. Each has a rule
box, a worked example opening with the reasoning, and a try-it with its answer
printed upside down.
