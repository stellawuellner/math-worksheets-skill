# Composing Functions from Symbolic Rules — Algebra 2

Three PDFs are ready: the student worksheet, a full step-by-step answer key, and
a two-page study guide.

## What the worksheet covers

Ten problems on composing functions from symbolic rules, ramped from routine to
challenge (difficulty 1 → 4). They rotate through four distinct skills so your
student has to *choose* the method rather than repeat one:

1. **Running a composition at a number** (problems 1–2) — inside rule first. A
   value-free "composition machine" diagram in the directions shows the wiring,
   and problem 2 walks a small input/output table so the notation lands on
   something concrete before it goes symbolic.
2. **Building the composed rule** (3, 5, 6, 8, 10) — substitute the whole inner
   rule, in every slot, then expand. Includes a rational-function composition
   and one problem that composes first and then solves an equation.
3. **Order matters** (4, 7) — the same two rules composed both ways, side by
   side, so the non-commutativity is something the student *sees* rather than
   is told.
4. **Inverses by composition** (9) — both directions checked, which is what the
   definition actually asks for.

Problem 10 is a decomposition task ("write $h$ as $f \circ g$") with many
correct answers, so it is deliberately **flagged for manual review** — the
answer key gives a full model response plus a second valid split and says what
full credit requires.

## What was verified

Every machine-checkable answer was recomputed by SymPy before anything was
typeset: 13 checks across the 10 problems (three of them are the three rows of
the problem-2 table, two are the two orders in problem 7, and two are the two
directions of the inverse test in problem 9). Compositions are checked as
*equivalences* — the expanded answer really is the substituted expression — so
an expansion slip could not survive into the key. Problem 10 is the only
manual item.

The answer key was also machine-bound to the verified data problem by problem:
every boxed answer is the value the checker computed, in that problem's own
solution. The study guide's four worked examples and four try-it items are
verified the same way (10 more checks).

## The study guide

Two pages, four sections, each one a rule box, a worked example with the
strategy step written out, and a try-it whose answer is printed upside down so
your student attempts it before checking. There is a closing watch-out box on
the two mistakes this topic reliably produces: reading $f \circ g$ as
multiplication, and dropping the parentheses around a substituted rule.

## Notes

Grade level does not appear on the worksheet or the study guide by design — it
prints on the answer key, together with a generated curriculum section listing
the standards covered (HSF-BF.A.1c and HSF-BF.B.4) and the difficulty range.
