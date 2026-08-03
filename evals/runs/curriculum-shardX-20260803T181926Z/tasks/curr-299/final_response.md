# Absolute-Value, Piecewise, and Linear-Quadratic Models --- Boundaries and Open/Closed Endpoints (Algebra 1)

Three PDFs are ready: the student worksheet, a full step-by-step answer key, and
a two-page study guide.

## What is on the worksheet (8 problems)

Every problem lives at a **boundary** --- the input where one formula stops and
another starts --- because that single input is where almost all piecewise and
absolute-value errors happen. The directions state the rule the whole sheet turns
on: a closed inequality ($\le$, $\ge$) owns its boundary point, a strict one
($<$, $>$) does not, and exactly one rule may own each input.

1. **Warm-up** --- name which rule owns $x = 1$ for a piecewise $F$, then evaluate.
   $F(1) = 3$.
2. **Find and fix** --- Mia evaluates the same $F$ at the boundary and gets 7 by
   using the strict-inequality rule. The correct value is **5**. The key names the
   underlying idea: the top rule's values *approach* 7, but the value *at* 3 is 5.
3. **Find and fix** --- a second function reverses which side is closed, so Leo's
   habit of "always use the second rule at the boundary" gives 5 instead of **7**.
   There is no convention to memorise; you read the sign.
4. **Find and fix** --- a definition whose two conditions are *both* closed at
   $x = 1$, so it assigns two outputs and is not a function. Repair it with one
   character, then $H(1) = \mathbf{5}$.
5. The opposite fault: both conditions strict, so $x = 0$ has no output at all.
   Part (a) asks for the explanation and two one-character repairs --- **open
   response, flagged for manual review**. Part (b) repairs it and evaluates:
   $K(0) = \mathbf{0}$, which is machine-verified.
6. A tolerance model, $|2x - 5| \le 3$. Priya reports the passing range with open
   endpoints. Solving $|2x-5| = 3$ gives endpoints **$x = 1$ and $x = 4$**, and the
   $\le$ sign puts both *inside* the range --- her version would reject parts that
   meet the specification exactly.
7. A no-jump (boundary-matching) problem: find $k$ so the two pieces agree at
   $x = 2$. $k = \mathbf{-5}$. The key stresses that matching the values removes
   the jump but does not move the boundary.
8. **Challenge** --- a linear-quadratic model. Find every point where $y = x - 1$
   and $y = x^2 - 4x + 3$ meet: **$(1, 0)$ and $(4, 3)$** --- then say which
   $x$-value must carry the closed inequality if the line is used first.

Problems 2, 3 and 4 are the find-and-fix items; 5 adds a third. All eight
problems turn on the boundary or endpoint question.

## What was machine-verified

Eight of the nine checks were verified independently by the SymPy verifier
before anything printed --- all the piecewise evaluations, both absolute-value
endpoints, the value of $k$, and both intersection points of the
linear-quadratic system (checked as a full solution set, so a missing second
point would fail). The only item labelled **manual review** is problem 5(a), the
"explain why and give two repairs" part, which is genuinely open; its
machine-checkable half, $K(0)$, is verified alongside it rather than waved
through.

Three declared misconception traps were proved distinguishably wrong by the
verifier and print in the key's "Common wrong answers" block:

- using the strict-inequality rule at the boundary (7 instead of 5);
- assuming the *second* rule always owns the boundary (5 instead of 7);
- reading the boundary off the second rule of an overlapping definition
  (3 instead of 5) --- the ambiguity that makes it not a function.

## The study guide

Two pages, three sections, each with a rule box, a worked example, and a separate
try-it whose answer is printed upside down inside the box:

1. which rule owns the boundary --- test the conditions first, substitute second;
2. overlaps, gaps, and matching values --- both closed gives two outputs, both
   strict gives none, and "no jump" is a separate question answered by solving for
   the constant;
3. endpoints of an absolute-value range --- solve the equation to find them, read
   the sign to decide whether they belong.

## Notes

- The grade level prints on the answer key only, in the generated Curriculum
  section (HSF-IF.A--HSF-IF.C for the piecewise work, HSA-CED.A.1--A.4 for the
  tolerance and design models, difficulties 1--5).
- The answer key is written to be read by the student: each solution says which
  rule was chosen and why before it substitutes, which is the step the
  misconceptions skip.
