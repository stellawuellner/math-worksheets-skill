# Completing Short Algebraic and Segment Proofs — High School Geometry

Three PDFs are ready:

- `ws_segmentproofs_curr303.pdf` — the student worksheet, 8 problems, 5 pages
- `ak_segmentproofs_curr303.pdf` — the full step-by-step answer key, 4 pages
- `ss_segmentproofs_curr303.pdf` — a 2-page skills summary / study guide

## What the worksheet asks

All eight problems are short proofs, and the two-column table is the
representation the sheet works in: statements on the left, reasons on the right,
with blank cells the student fills. A value-free reference diagram at the top
fixes the labelling convention (four collinear points $A$, $B$, $C$, $D$; $AB$
means the length from $A$ to $B$), so no problem's figure can be misread as
another's data. Every length is stated in centimetres and each length answer has
a unit-labelled answer line.

- **Algebraic proofs** (problems 1, 3, 7) — supply the missing reasons for
  $3x + 7 = 25$, then the missing statements *and* reasons for
  $5(x-2) = 3x + 8$. Problem 7 is error analysis: Jordan's proof subtracts $2x$
  from one side only, reaching $x = 4$; the student names the first bad line,
  states what the Subtraction Property actually requires, and rewrites the proof
  to $x = 8$.
- **Segment proofs** (problems 2, 5, 8) — the Segment Addition Postulate with
  two parts, then with three parts ($AD = 37$ cm), then the synthesis proof that
  $\overline{AB} \cong \overline{CD}$ forces $\overline{AC} \cong \overline{BD}$
  for four collinear points, followed by a numerical instance.
- **Midpoint and congruent segments** (problems 4, 6) — the two-step move that
  students most often merge: midpoint gives *congruence*, congruence gives equal
  *lengths*, and only the second can be solved.

Difficulty ramps 1, 1, 2, 3, 3, 4, 4, 5.

## What was verified, and what is flagged

Twenty checks in total. **Fourteen are machine-verified by SymPy** — every value
of $x$ and every requested length ($AB = 17$ cm, $AM = 15$ cm, $BC = 8$ cm,
$AB = 28$ cm, $AB = 13$ cm, $AC = 19$ cm).

**Six items are explicitly flagged for manual review**, and that is the correct
outcome rather than a defect: a Reasons column, a named postulate and a written
two-column proof are prose that no CAS can check. They are listed in the
verification data as `manual` with a description of what a correct answer must
contain, and the answer key marks each one "Manual review". The build finished
green with exit 2 (manual-review items present).

The answer key gives a complete model proof for every problem — the full
statement/reason table, not just the value of $x$ — plus a numeric check
(e.g. $17 + 9 = 26$ cm) and grading notes on the reasons students most often get
wrong.

## The study guide

Three sections, each with a rule box, a worked example whose first step names
the strategy, and a try-it item with the answer upside down inside the box:
justifying the steps of an equation, segment proofs with the addition postulate,
and midpoints/congruent segments. A watch-out box flags the commonest wrong
reason ("combined like terms" for a move that is really the Subtraction
Property).

Standards: HSA-REI.A.1 for the algebraic proofs, HSG-CO.C for the segment
proofs, HSG-CO.A for the definition-driven midpoint and congruence work.
