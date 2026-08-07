# Composing Piecewise and Nonlinear Functions — three PDFs

A 12-problem precalculus fluency set on composition, plus the worked answer key
and a two-page study guide.

| File | What it is |
|---|---|
| `ss_compose_curr402.pdf` | Study guide (2 pages) |
| `ws_compose_curr402.pdf` | Student worksheet, 12 problems (6 pages) |
| `ak_compose_curr402.pdf` | Step-by-step answer key (3 pages) |

**The ramp.** Problem 1 is a two-step numerical composition; problem 12 is a
radical composition with a quadratic inside and a domain argument. Nothing in
between repeats a skeleton — the polynomials become rational functions, then
radicals, and the piecewise rules get harder to route through. Three strands
alternate one after another all the way down the sheet:

* **Evaluating a composition** (#1, #4, #7, #10) — #4, #7 and #10 use piecewise
  rules. #7 asks for `(f∘g)(-5)` and `(g∘f)(-5)` side by side so the answers
  visibly differ; #10 sends a value through the *same* piecewise function twice
  and the two passes land in different branches.
* **Writing the composed rule** (#2, #5, #8, #11) — from a polynomial pair up to
  two compound rational fractions that simplify to a single clean fraction.
* **Solving a composition equation** (#3, #6, #9, #12) — including one that
  factors without expanding (#9) and one with a radical (#12).

**How much is machine-checked — honestly.** There are 16 answers across the 12
problems. **13 were recomputed with SymPy** and matched against the key before
the PDFs were built. **3 are instructor-judged** and marked `---` in the Quick
Answers bank: the written halves of #4 ("which rule for f did you use, and what
comparison told you?"), #10 ("why the two passes differ") and #12 ("why neither
answer is extraneous"). The key's "What is verified" note names those three
problems.

Those three prose parts are where the real teaching is, so they are not
decoration. Each carries a grading note in the key saying what a correct answer
must contain and what the standard wrong answer looks like — on #4, for example,
a student who tests the original input 4 against the boundary instead of the
inner value 11 gets the wrong branch and a plausible-looking wrong number.

All six study-guide items are fully machine-verified.
