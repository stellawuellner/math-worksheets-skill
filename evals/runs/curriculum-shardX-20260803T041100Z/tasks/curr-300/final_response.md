# Choosing Linear, Quadratic, or Piecewise Models (Algebra 1)

Three PDFs are ready.

- **Worksheet** (`ws_models_curr300.pdf`, 8 pages) — 12 problems in an
  interleaved-synthesis format. The directions box states the three pieces of
  evidence the sheet is built around: constant **first** differences (or a
  single fixed rate) means linear, constant **second** differences (or a product
  of two input-dependent quantities) means quadratic, and a stated boundary
  where the rule changes means piecewise. Four problems carry a difference
  table in the stem so the student has to read the evidence before writing a
  formula. Problems 1–4 are the blocked warm-up (linear table twice, then
  quadratic table twice); after that the families rotate with no same-family
  run longer than two — a piecewise parking charge, a linear pool-depth table
  with a written justification, the same parking rule solved backwards, a
  quadratic revenue model with two valid prices, two gym plans meeting at a
  point, a line meeting a parabola at two points, an error-analysis problem
  where a student extends a quadratic table with its first difference, and a
  three-part piecewise rideshare fare.
- **Answer key** (`ak_models_curr300.pdf`, 5 pages) — the generated
  quick-answer bank, then a full solution per problem that always *names the
  evidence first* and only then writes the model. Four problems carry a named
  common wrong answer (240 from charging the start-up fee six times, 168 ft
  from extrapolating a quadratic table linearly, 19 dollars from charging the
  hourly rate for the hours the flat fee already covered, and Rae's 29 from
  treating a first difference as a constant rate). Several solutions end with
  the check that matters for that family — verifying which piece of a piecewise
  model an answer lands in, and confirming both intersection points in the
  quadratic.
- **Study guide** (`ss_models_curr300.pdf`, 2 pages) — four sections matching
  the four worksheet skills (evidence for linear, evidence for quadratic,
  evidence for piecewise, comparing two models). Each rule box leads with the
  *evidence* rather than the formula, each worked example opens with a step
  naming why that family fits, and each try-it re-parameterizes its example.

## Verification

13 of the 15 checks are machine-verified with SymPy: 5 `eval` checks (each
model evaluated at a point outside its table, with the givens lifted into named
variables so the model's parameters are visible to the prose checker), 4 `solve`
checks (linear back-solve, projectile ground times, piecewise back-solve, and a
quadratic revenue equation with two roots), and 2 `system` checks — the
line-meets-line gym comparison and the line-meets-parabola case, whose expected
value is the full two-point solution set. Problems 6 and 12 carry more than one
verify entry under one problem id. One answer carries a verified unit (`ft`)
bound to the sheet's `\answerline` and the key's boxed answer in both
directions.

Two items are labelled for manual review and the key says so at the point of
use:

- problem 6(b) — "explain what in the table shows the relationship is linear
  rather than quadratic". The prediction in part (a) is machine-checked; the
  justification is prose.
- problem 12(c) — "explain why no single linear function fits, and describe the
  graph". Parts (a) and (b) are machine-checked; the explanation is prose.

Both are encoded as `{"type": "manual", ...}` rather than claimed as verified,
which is why the build exits 2. All 8 study-guide items (4 worked examples +
4 try-its) are fully machine-verified, and each of the four worksheet facets has
a matching worked example.

Four misconception traps are declared and machine-proved distinguishable from
the correct answers.

**Standards used:** `HSA-CED.A.1–A.4` for building a model from a context (row
"Creating equations & inequalities from context"), `HSF-IF.A–HSF-IF.C` for the
function-behaviour and piecewise-structure items (row "Function behaviour,
notation, graphs"), `HSA-REI.B.4` for solving the quadratics (row "Quadratics:
solve"), and `HSA-REI.C.6` for the two systems (row "Systems
(linear/quadratic)") — all taken verbatim from `references/standards-map.md`.

## Build

All 21 gates green on the third attempt (exit 2 for the two declared manual
items). Two failures, both real and both worth recording:

1. `compile-ws` failed the page budget at 8 pages against a 7-page ceiling. The
   cause was under-declared stem furniture: four problems carry a difference
   table and three are multi-part, which the budget charges at a flat 0.6 cm of
   stem each. Declaring an honest `workspace_cm` on all twelve problems raised
   the computed content from 99.1 cm to 119.1 cm and the ceiling with it; the
   sheet still prints 8 pages and no work space was taken from the student.
2. A layout defect I caught by rendering rather than from a gate:
   `\answerline{ft}` written inside the `\problem` stem prints **immediately
   after the stem**, because `\problem` typesets its argument before emitting
   the workspace, so the answer blank landed above 7.5 cm of blank paper. The
   fix is to drop the optional workspace argument and write the space into the
   stem instead — `\problem{stem \par\vspace*{7.5cm}\answerline{ft}}` — which
   `check_layout.py` credits identically. The same restructuring gives the
   multi-part problems 6 and 12 a work area between each part and its blank
   rather than all their space stacked at the end.

Page counts: worksheet 8 (budget 8), answer key 5 (budget 8), study guide 2
against its hard 2-page cap.
