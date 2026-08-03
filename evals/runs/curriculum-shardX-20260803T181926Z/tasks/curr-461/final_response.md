# Implicit Differentiation — three documents

Here are the three PDFs on differentiating implicit relations (AP Calculus AB/BC,
FUN-3.D–FUN-3.E).

**Study guide** (`ss_implicit_curr461.pdf`, 2 pages) — three sections, each with a
rule box, a worked example whose first step is the reasoning, and a try-it whose
answer prints upside down inside the box:

1. *Differentiating a relation implicitly* — why the move is legal, and a
   term-by-term table ($x^3$, $y^3$, $xy$, $x^2y$, constants) showing exactly
   where the $dy/dx$ factor comes from.
2. *The slope at a point on the curve* — why an implicit derivative needs both
   coordinates, and why the point must be checked against the relation first.
3. *Tangent lines and special points* — point-slope tangents, horizontal tangents
   (numerator zero), vertical tangents (denominator zero).

**Worksheet** (`ws_implicit_curr461.pdf`) — 8 problems, all implicit
differentiation. The directions carry the same term-by-term table as the model.
Problem 1 differentiates the circle both ways and asks the student to show the
implicit and explicit answers agree; 2, 3, 4 and 5 build up through the product
rule ($xy$, the folium $x^3+y^3=9xy$, and $x^2y+y^3=10$); 6 asks for a tangent
line on an ellipse; 7 finds all points with a horizontal tangent; 8 is the second
implicit derivative of the circle, simplified using the relation itself, with a
concavity interpretation. Each problem gets 7.5–8.5 cm of work space. Difficulty
ramps 1 to 4.

**Answer key** (`ak_implicit_curr461.pdf`) — quick-answer bank, then a full
derivation per problem: differentiate, collect the $dy/dx$ terms, factor, divide,
and (where a point is involved) the on-curve check first. Grading notes are
included for problems 6 and 8. The curriculum section prints here only.

**What was machine-verified:** 14 checks behind the 8 problems.

- Problems 1 and 8 were verified *as derivatives*: SymPy differentiated
  $\sqrt{25-x^2}$ once and twice and confirmed the answers
  $-x/\sqrt{25-x^2}$ and $-25/(25-x^2)^{3/2}$ — which are exactly the implicit
  answers $-x/y$ and $-25/y^3$ rewritten on the upper arc. So the calculus itself,
  not just the arithmetic, is checked on those two.
- Problems 2–7 were verified in two parts each: the stated point really lies on
  the curve (the relation evaluates to exactly 0 there), and the slope formula
  evaluates to the printed value at that point. Problem 7's horizontal-tangent
  equation $3x^2 = 12$ was re-solved to $x = \pm 2$, and $(2,-4)$ was confirmed on
  the curve.

Nothing is flagged for manual review. One honest caveat worth stating: for
problems 2–7 the verifier confirms the arithmetic of the derivative formula and
the point, not that the formula was derived correctly — the full derivation is
written out in the key so you can follow it. Problems 1 and 8 do not have that
gap, which is why the circle appears at both ends of the sheet.
