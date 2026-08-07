# Transformations, Compositions and Inverses: A Synthesis Review — three PDFs

A 12-problem precalculus review that mixes the three tools together, plus the
worked answer key and a two-page study guide.

| File | What it is |
|---|---|
| `ss_synthesis_curr405.pdf` | Study guide (2 pages) |
| `ws_synthesis_curr405.pdf` | Student worksheet, 12 problems (5 pages) |
| `ak_synthesis_curr405.pdf` | Step-by-step answer key (3 pages) |

**How the sheet is arranged.** Problems 1–3 are a short warm-up, one on each
tool and clearly labelled as such in the directions. From problem 4 on the tools
are shuffled, so the student has to work out *which* one is being asked for
before starting — that decision is the point of a synthesis review, and a
blocked sheet never asks for it. Difficulty runs 1 to 5.

Some highlights:

* **#7** composes `f(x)=√(x−1)` with `g(x)=x²+1` and the result simplifies to
  `|x|`, not `x` — so the equation has two solutions. This is the single most
  useful trap on the sheet.
* **#9** restricts a parabola and the restriction decides the sign of the square
  root; the wrong sign gives −1 instead of 7, and that wrong value is declared
  as a machine-checked trap and printed in the key under "Common wrong answers".
* **#11** nests an inverse inside a transformation.
* **#12** is the synthesis challenge: `(g∘f)⁻¹(9)` with a restricted `g`, and
  then the reason the inverse of a composition reverses the order.

**How much is machine-checked — honestly.** There are 15 responses across the 12
problems. **12 were recomputed with SymPy** and matched against the key before
the PDFs were built. **3 are instructor-judged** and marked `---` in the Quick
Answers bank: the written halves of #8 (describe the transformations in order),
#10 (what the simplification says about f and g) and #12 (why the order
reverses). The key's "What is verified" note names exactly those three.

Each of the three carries a grading note in the key. On #8, for instance, an
answer that names all three transformations but shifts up before stretching is
wrong, because the shift would be tripled.

All six study-guide items are fully machine-verified.
