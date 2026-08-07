# Inverse functions — worksheet, answer key and study guide

Three PDFs are ready for your Algebra 2 student, all on **finding and verifying inverse
functions**:

- **`ws_inverses_curr382.pdf`** — the student worksheet, 12 problems, 5 pages.
- **`ak_inverses_curr382.pdf`** — the full step-by-step answer key, 5 pages.
- **`ss_inverses_curr382.pdf`** — a 2-page study guide to keep beside the worksheet.

## What the worksheet covers

Every problem is an inverse-function problem, and the sheet ramps deliberately rather than
repeating one skeleton twelve times:

1. **Problems 1–2** are the plain pattern: a linear rule, inverted by writing $x = f(y)$ and
   solving for $y$.
2. **Problems 3–6** widen the idea — verifying a composition, inverting a rational rule,
   inverting a square-root rule, and reading a single value $m^{-1}(19)$ off the inverse.
3. **Problems 7–9** are the same four moves with harder algebra (a fraction with the
   variable in the numerator, a reciprocal plus a shift, a cube rule to test).
4. **Problems 10–12** are the challenges: find-then-verify in one problem, a quadratic that
   only has an inverse because its domain is restricted, and a rational rule whose inverse
   has an excluded input.

The four methods are interleaved after the warm-up (no method runs more than twice in a
row), so the student has to decide *which* technique a problem needs — that decision is the
thing that transfers to a test.

## What was verified, and what was not

The answer key's "What is verified" note is generated from the same data, so it says exactly
this: **13 of the 16 answers are machine-checked with SymPy; 3 are instructor-judged.**

- **Machine-checked (13):** every inverse rule was re-derived by the computer algebra
  system by solving $x = f(y)$ for $y$, every composition was independently simplified, and
  $m^{-1}(19) = 4$ was recomputed. If a printed answer disagreed with the algebra, the build
  would have refused to produce a PDF.
- **Instructor-judged (3):** the written explanations in **3(b)**, **11(b)** and **12(b)**.
  These are prose — "what does this tell you about $p$ and $q$", "why is the restriction
  necessary", "what goes wrong at the excluded input" — and no computer can grade them
  honestly. Each one is marked `---` in the Quick Answers bank rather than given a fake
  value, and the answer key prints a grading note for each saying what a correct response
  has to contain and what to reject.

I did not remove those written parts to get a fully-automated sheet. The reasoning is where
the understanding lives; the honest thing is to flag them, not to delete them.

## One planted misconception

Problem 6 is designed around the most common inverse error — undoing the operations in the
wrong order. A student who divides by 4 first and then subtracts 3 gets **1.75** instead of
**4**, and the answer key prints that wrong value in a "Common wrong answers" line so you can
diagnose it in one glance instead of reading the scratch work.

## Study guide

Four sections, each with a rule box, a worked example whose first step says *why* that method
applies, and a try-it problem with the answer printed upside down inside the box: inverting a
linear rule, inverting a rational rule, inverting roots and powers, and checking/using an
inverse. Every worked example and try-it answer in the guide is machine-verified too (9 of 9)
— the guide is the first thing the student learns from, so it is gated exactly like the key.
