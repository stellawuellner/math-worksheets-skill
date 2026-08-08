# Standard form: circles and parabolas

Three PDFs for your Algebra 2 student, all on **rewriting circle and parabola equations in
standard form**:

- **`ws_stdform_curr397.pdf`** — the student worksheet, 12 problems, 5 pages.
- **`ak_stdform_curr397.pdf`** — the full step-by-step answer key, 4 pages.
- **`ss_stdform_curr397.pdf`** — a 2-page study guide.

## The ramp

This is a fluency sheet, so it repeats the *skill* twelve times without repeating the
*skeleton* once. Each problem changes exactly one thing about the last one:

1. **Problems 1–4** are the plain pattern: one square to complete on a parabola, then a
   circle needing only the $x$ square, then a parabola with larger numbers, then a circle
   needing both squares.
2. **Problems 5–8** add a second demand: complete the square *and* report the radius;
   complete it with fractions (half of 5 is not a whole number); factor a leading 2 out
   before completing; divide a whole equation by 2 first.
3. **Problems 9–11** run the process backwards — build the equation from a centre and radius
   and expand it, find the missing coefficient $a$ from a point on a parabola, and complete a
   square with a leading 3.
4. **Problem 12** is the finish: standard form, radius, and then a question about the
   original equation.

No two problems share a skeleton, and the four sub-skills alternate rather than sitting in
blocks, so the student has to notice *which* variation is in front of them.

## What was verified, and what was not

The key's generated note says it exactly: **17 of the 18 answers are machine-checked with
SymPy; 1 is instructor-judged.**

- **Machine-checked (17):** every completed square was checked as an *identity* — the
  computer algebra system confirmed that the rewritten form is equal to the original
  expression for every value of the variables, not merely that some numbers matched. That is
  the right check for this topic: it catches an unbalanced completing constant, which is the
  error this skill actually produces. Both radii, both vertex coordinates and the missing
  coefficient $a$ were recomputed too.
- **Instructor-judged (1):** part **12(c)**, "explain how the original equation already rules
  out a parabola". It is a reasoning answer, so it is marked `---` in the Quick Answers bank
  rather than given a value, and the key says what full credit needs — a reference to *both*
  squared terms being present and matching. Answering "because it looks round" does not use
  the standard-form reasoning the question asks for.

## Study guide

Four sections, each with a rule box, a worked example whose first step explains why the move
is needed, and a try-it with the answer upside down inside the box: completing the square on
a parabola, completing two squares on a circle, handling a leading coefficient other than 1
(and reading the feature off afterwards), and building an equation from a centre and radius.
The sign trap — a centre of $-3$ giving $(x+3)$ — is called out explicitly. All 10 of its
worked answers are machine-verified.
