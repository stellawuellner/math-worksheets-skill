# Wrong Centre, Wrong Vector, Wrong Scale Factor — 6 error-analysis problems

Three PDFs are ready:

- **`ws_transerrors_curr349.pdf`** — the student worksheet (3 pages).
- **`ak_transerrors_curr349.pdf`** — the full step-by-step answer key with grading
  rubrics.
- **`ss_transerrors_curr349.pdf`** — a 2-page skills summary.

## What the worksheet covers

Every problem shows a student's work that is wrong in exactly one way, and asks
for the corrected value *and* a diagnosis. The three failure modes are kept
distinct on purpose, because they break differently:

1. **Wrong vector** — Ana subtracts image from original and reverses the
   direction of the translation.
2. **Wrong scale factor** — Ben adds 3 to each coordinate instead of multiplying,
   which is a slide, not an enlargement.
3. **Wrong scale factor** — Cara subtracts two sides (15 − 9) instead of dividing.
4. **Wrong centre** — a student dilates about the origin when the centre was
   given as C(1, 4): right size, wrong place.
5. **Wrong scale factor** — a student uses an *area* ratio (2.25) as the linear
   factor, missing the square root.
6. The challenge — dilating about the origin instead of about the endpoint M. The
   image length is right (12 either way) but the position is not, and the student
   has to say why one survived and the other did not.

## What is verified, and what is not

The sheet asks for **16 separate responses**.

- **10 are machine-checked** with SymPy — every corrected component, coordinate,
  scale factor and length.
- **6 are instructor-judged**, one per problem: the written diagnosis. That is the
  point of an error-analysis sheet, so none of them is dressed up as verified.
  Each is marked `---` in the Quick Answers bank, and the key gives a model
  response plus a full / half / no-credit rubric. The key's own "What is verified"
  note says 10 of 16.

There are no `[unchecked]` marks.

## Every planted wrong answer is machine-checked

All eight wrong results are declared as traps, and the verifier confirmed each is
distinguishably different from the correct answer — so no planted error can quietly
coincide with the right one. They print in the key under **Common wrong answers**:
−4, 1 and 8, 6, 10 and 12, 2.25, and 18.

## The study guide

Opens with the diagnostic frame — a wrong vector sends the figure the wrong way, a
wrong centre gives the right size in the wrong place, a wrong factor gives the
wrong size. Then three sections: the image-minus-original order for a vector, the
offset form for dilating about a centre that is not the origin, and the difference
between a length ratio and an area ratio. Each has a worked example whose first
step is the reasoning move and a try-it with the answer upside down inside the box.
