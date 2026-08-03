# Circles and parabolas in standard form — Algebra 2 practice set

Three PDFs are ready:

- **Study guide** — `ss_conics_curr397.pdf` (2 pages)
- **Worksheet** — `ws_conics_curr397.pdf` (6 pages, 12 problems)
- **Answer key** — `ak_conics_curr397.pdf` (5 pages)

## What's on the worksheet

Twelve problems on completing the square, arranged so the same move keeps coming
back with something new around it rather than the same skeleton twelve times.

- **Problem 1** isolates the move itself: fill in the number that completes
  `x² − 10x + ___` and write the squared binomial.
- **Problems 2, 3** are circles in general form — one with straightforward signs,
  one where the signs and a negative constant both have to be handled.
- **Problems 4, 5** are quadratics into vertex form; problem 5 goes on to use the
  finished form to find the x-intercepts.
- **Problems 6, 7** add a coefficient in front of the squared terms, and the two
  problems handle it differently on purpose: a circle equation gets divided
  through by 2, a quadratic gets the 2 factored out of the x terms only. Telling
  those two apart is the point of the pair.
- **Problems 8, 9, 11** use the finished form: is a given point inside, on, or
  outside a circle; expand a standard form back to general form (the check on
  every other problem); and find where a line crosses a circle.
- **Problem 10** completes the square in y rather than x — a parabola on its side,
  where the vertex coordinates come out in the reverse order.
- **Problem 12** is the capstone: completing the square gives
  `(x−2)² + (y+3)² = −7`, and part (b) asks what that means for the graph.

Difficulty ramps 1 → 5, and the three skills are interleaved after the warm-up.

## What was verified

Twenty-two separate checks passed through the skill's SymPy verification gate.
Every rewrite is verified as an algebraic identity — the general form and the
completed form are proved to be the same expression, so a balance error cannot
slip past — and each radius, vertex coordinate, intercept, distance and
intersection point is checked on top of that. Problem 11's system is verified as
complete: SymPy confirms there are exactly two intersection points and that both
listed points satisfy both equations. The answer key's boxed answers are bound to
the verified values.

Three **misconception traps** were declared and proved distinguishable:

- reporting 25 as the radius when 25 is r² (problem 2);
- halving −12 instead of −6, i.e. completing the square before factoring the 2 out
  (problem 7);
- writing the sideways parabola's vertex as (2, 3) instead of (3, 2) (problem 10).

Each prints in the key as an "if they got N…" line with a diagnosis.

## What is flagged for manual review

**Problem 12, part (b)** is an open written explanation and is labelled `manual`
in the verification data — the build reports it as a manual-review item. The
computed part, 12(a), is machine-verified; only the reasoning about the empty
graph is not. The key gives a model answer, a marking guide (a bare "the radius is
√−7" does not earn full credit — the question is what happens to the graph), and a
follow-up problem for the borderline r² = 0 case.

Everything else on the sheet is machine-verified.
