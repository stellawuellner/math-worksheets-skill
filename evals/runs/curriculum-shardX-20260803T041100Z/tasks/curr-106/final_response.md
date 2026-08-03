# Two-Digit Multiplication with Area Models (Grade 4–5)

Three PDFs: the student worksheet (10 problems, 5 pages), a step-by-step answer
key, and a two-page study guide.

## What the worksheet asks

The sheet is built around one model — a rectangle split by place value — and
every problem connects that picture to the multiplication sentence beside it.

- **Problems 1, 2, 3, 5, 7** — the model is pre-split (e.g. $20+3$ across,
  $10+4$ down). The student writes the four partial products in the regions and
  adds. Each grid has a full-height cell so the numbers actually fit.
- **Problems 4 and 8** — estimate first by rounding both factors to the nearest
  ten. Problem 8 plants the classic rounding error: $29$ must round *up*.
- **Problem 6** — a model with three regions printed ($1000$, $80$, $300$) and
  one empty. The student rebuilds the missing region from its own two labels
  ($4 \times 6 = 24$) and then totals $1404$.
- **Problem 9** — same model, blank labels: the student decomposes $45$ and $37$
  without help.
- **Problem 10** — error analysis. Maya kept only tens×tens and ones×ones and
  answered $624$; the student names the two missing cross regions and gives
  $864$.

Difficulty ramps 1, 2, 2, 2, 3, 3, 3, 3, 4, 4. Each model problem declares
`workspace_cm: 7.0`, so the page budget charges for the grid plus room to add —
the sheet runs 5 pages rather than being compressed onto 3.

## Verification

19 machine checks across the 10 problems — **19 verified, 0 manual**. Each
area-model problem carries two independent checks that must agree: the product
in standard notation ($23 \times 14 = 322$) and the sum of the four partial
products ($20 \cdot 10 + 20 \cdot 4 + 3 \cdot 10 + 3 \cdot 4 = 322$). If the
model and the notation ever disagreed, the build would fail.

**Four misconception traps are declared and machine-checked** (verify.py
confirms each wrong method lands on a number the problem's own check rejects,
and the answer key prints them for the grader):

- P4: rounding only one factor → 1680
- P6: totalling the three printed regions and never filling the empty one → 1380
- P8: rounding 29 down to 20 → 1200
- P10: tens×tens plus ones×ones only → 624 (the number printed in the stem, so
  the planted value is derived from the trap expression, not typed by hand)

`BUILD PASSED — all gates green`.

## Study guide (2 pages)

Three sections matching the three worksheet facets — building the model,
estimating the product, finding a missing partial product — each with a rule
box, a worked example that opens with a strategy line, and a distinct try-it
with the answer upside down inside the box. A watch-out box closes the guide on
the two-regions-instead-of-four error.

## Notes

- Standard `4.NBT.B.5` (multi-digit multiplication) from
  `references/standards-map.md`, used verbatim on every problem — it is the
  code the curriculum task names.
- The study guide's prose-consistency report shows a 58% number match. Every
  flagged value is a derived intermediate the guide prints on purpose (the
  partial products $200$, $60$, $800$, …) or a whole factor whose decomposition
  is what the JSON stores. The worksheet itself reports 100%.
