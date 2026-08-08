# Analyzing Transformations with Multiple Parameters — three PDFs

A 10-problem precalculus set on reading and using the parameters in
`g(x) = a·f(b(x − h)) + k`, plus a worked answer key and a two-page study guide.

| File | What it is |
|---|---|
| `ss_transformparams_curr401.pdf` | Study guide (2 pages) |
| `ws_transformparams_curr401.pdf` | Student worksheet, 10 problems (5 pages) |
| `ak_transformparams_curr401.pdf` | Step-by-step answer key (3 pages) |

**What the sheet does.** Three strands rotate through it so no parameter is
practised in isolation:

* **Reading the parameters** (#2, #5, #8) — each of these asks for a value
  *and* for the transformations in order. #8 is the one to watch: `f(6 − x)`
  cannot be read at all until the input is rewritten as `−(x − 6)`, and
  students who skip that step reliably answer "shift 6 left".
* **Evaluating a transformed function** (#1, #4, #7) — with a table of the
  parent function as the concrete model. #4 deliberately asks for one value
  the table covers and one it does not, so the table is a picture and the rule
  is the tool.
* **Expanding the transformed rule** (#3, #6, #9, #10) — substitute, expand,
  and see the parameters survive. #9 factors `2x − 8` into `2(x − 4)` (the step
  that makes the shift readable), and #10 completes the square and then asks
  why the stretch has to happen before the vertical shift.

**How much is machine-checked — honestly.** There are 16 answers on 10
problems. **12 were recomputed with SymPy** and matched against the key before
the PDFs were built. **4 are instructor-judged**: the "describe the
transformations in order" halves of problems 2, 5, 8 and 10. No software can
grade prose, so those are marked `---` in the answer key's Quick Answers bank,
and the key's "What is verified" note names exactly which problems they are.

For each of the four, the answer key prints a grading note saying what a
correct response must contain and what the standard wrong answer looks like —
for instance, on #10 an answer that lists all three parameters but shifts up 5
before stretching by 4 is wrong, because the stretch would multiply that 5.

All six study-guide items (three worked examples, three try-its) are fully
machine-verified.
