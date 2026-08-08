# When Does a Scale Factor Get Squared or Cubed? — 6 error-analysis problems

Three PDFs are ready:

- **`ws_scalefactor_curr344.pdf`** — the student worksheet (3 pages).
- **`ak_scalefactor_curr344.pdf`** — the full step-by-step answer key with grading
  rubrics.
- **`ss_scalefactor_curr344.pdf`** — a 2-page skills summary.

## What the worksheet covers

Every problem targets the same confusion: a single linear scale factor $k$ acts as
$k$ on lengths, $k^2$ on areas and $k^3$ on volumes, and students routinely use the
wrong power.

1. **Find and fix:** Dev multiplies an area of 24 cm² by 3 instead of by 9.
2. A cube of edge 5 cm scaled by 4 — the cube rule applied forwards.
3. **Find and fix:** Mia multiplies a cone's volume by 15/6 instead of by
   $(15/6)^3$.
4. Working backwards from a surface-area ratio to the linear factor (square root).
5. Working backwards from a volume ratio (cube root), then forwards to a surface
   area — with a note about not rounding early.
6. The challenge: a 1 : 20 scale model, where the same factor 20 produces 8000 for
   capacity and 400 for sheet metal, and the student has to say why.

## What is verified, and what is not

The sheet asks for **11 separate responses**.

- **8 are machine-checked** with SymPy — every scaled area, volume, capacity and
  every recovered scale factor. Declared units (cm², cm³, m², L) are bound in both
  directions, so the sheet's answer lines and the key's boxes must carry the same
  unit the JSON verified.
- **3 are instructor-judged**: the written diagnoses in 1(b), 3(b) and 6(c). Each
  is marked `---` in the Quick Answers bank, and the key supplies a model response
  plus a full / half / no-credit rubric. The key's own "What is verified" note
  says 8 of 11.

There are no `[unchecked]` marks.

## The planted errors are machine-checked

All four wrong methods are declared as traps, and the verifier confirmed each
produces a distinguishably wrong number. The key prints them under **Common wrong
answers**:

- 72 cm² — area multiplied by $k$ instead of $k^2$ (problem 1)
- 500 cm³ — volume multiplied by $k$ instead of $k^3$ (problem 2)
- 225 cm³ — volume multiplied by the height ratio, not its cube (problem 3)
- 6.25 — the surface-area ratio used as the linear factor (problem 4)

## The study guide

An opening box states all three rules together with the reason (count the
dimensions, that is the power). Then three sections — scaling an area, scaling a
volume, and working backwards from a ratio — each with a worked example whose
first step names the dimension count, and a try-it with the answer upside down in
the box.
