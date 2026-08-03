# Transformations — diagnosing a wrong centre, vector or scale factor (Geometry)

Three PDFs: the student worksheet, a step-by-step answer key, and a two-page
study guide.

**What the worksheet does.** Six problems, all built on the same observation:
when a transformation comes out wrong, the arithmetic is usually fine and one of
three pieces of data is wrong — the translation vector, the scale factor, or the
centre of dilation. Four of the six are explicit find-and-fix items.

1. Warm-up: write the translation vector taking `A(-3,2)` to `A'(4,-1)`.
2. Find and fix: Lee subtracted pre-image minus image, so Lee's vector is the
   inverse translation. Students name the effect and correct it.
3. Find and fix: Kim applies a vector to two points but only shifts one of them
   vertically. Students compute both segment lengths and use the fact that a
   rigid motion preserves distance to prove an image point is wrong, then repair
   it.
4. Find and fix: Jo reads a scale factor off a *difference* of coordinates.
   Students compute both distances from the centre, take the ratio, and say why
   a difference can never be a scale factor.
5. Find and fix: Ravi doubles coordinates for a dilation whose centre is not the
   origin. Students identify which centre his method actually used, then apply
   `A' = C + k(A - C)` and check the result with a distance.
6. Open task: two dilations with the same scale factor and different centres,
   plus a method for recovering an unknown centre.

Difficulty runs 1 to 5.

**What was machine-verified.** Thirteen checks across problems 1-5 were
recomputed with SymPy — every vector component, every distance (exactly, or to
the two decimal places the sheet asks for), and every dilated coordinate. Ten
misconception traps are declared, and each was proved to land on a number
*different* from the correct answer, which is what makes each find-and-fix item
able to distinguish the error it targets. The traps print in the answer key as a
"Common wrong answers" list, so a wrong answer of 5, or 6, or 9.43 tells you
exactly which of the three data errors the student made.

**What is flagged for manual review.** Problem 6 only: it asks for a sketch and
two written explanations. The answer key supplies a model sketch description,
model wording for both parts, and a checklist of what a full-credit response
must contain.

**The study guide** teaches the three skills the worksheet tests — translation
vectors, scale factors as ratios, and dilating about a centre other than the
origin — each with a rule box, a worked example, and a try-it whose answer is
printed upside down inside the box. All six of its worked results are verified
by the same gate chain as the worksheet.
