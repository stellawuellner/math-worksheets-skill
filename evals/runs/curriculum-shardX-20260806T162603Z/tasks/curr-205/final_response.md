# Ordering Mixed Rational and Irrational Quantities — Grade 8 / Pre-Algebra

Three PDFs are ready:

- **`ss_ordering_curr205.pdf` — Skills Summary (study guide, 2 pages).** Read this first.
  Three sections, each with a rule box, a worked example, and a "try it" whose answer is
  printed upside down inside the box: (1) putting a fraction, a root and $\pi$ into decimal
  form, (2) comparing two quantities (including how negatives reverse), (3) ordering a
  mixed list and rewriting the answer in the original forms. A watch-out box tackles the
  habit this topic punishes hardest — judging size from how a number is printed.
- **`ws_ordering_curr205.pdf` — Worksheet (4 pages, 12 problems).** The three subskills are
  interleaved after a short warm-up, so your child has to decide each time whether the task
  is a conversion, a two-way comparison, or a full ordering. One comparison uses negatives,
  one needs a third decimal place to separate $\pi$ from $\sqrt{10}$, and the sheet ends
  with a synthesis challenge built on a student's wrong ordering.
- **`ak_ordering_curr205.pdf` — Answer Key (3 pages).** Every problem re-printed with the
  conversion actually shown — the squeezed squares, the division, the digit where two
  decimals first differ — plus a Quick Answers strip and a Curriculum block (standard
  8.NS.A, difficulty 1–5).

## What is verified, honestly

- **11 of the 12 problems are fully machine-checked.** Every decimal conversion, every
  rounded root, every comparison symbol and every ordering was recomputed independently with
  SymPy before the PDFs were allowed to compile. The orderings are checked as orderings —
  the checker sorts the quantities itself and compares the whole sequence, so a single
  swapped pair would have failed the build.
- **Problem 12 is split.** Part (a), the correct order, is machine-checked. Part (b) — the
  explanation of why Nadia's method fails — is **instructor-judged**, since it is written
  reasoning. It prints as `---` in the Quick Answers strip, and the answer key gives you the
  rubric: the answer must name the conversion step that was skipped.
- The study guide's three worked examples and three try-it answers are verified the same
  way (8 checks, all machine-checked).

One thing worth pointing out while marking: problem 11 is the sheet's trap by design. Its
largest quantity is a *root*, $\sqrt{36}$, and its smallest is a *fraction* — so a child who
has learned "roots are small, decimals are big" gets it wrong, which is exactly the habit
problem 12 then asks them to articulate.
