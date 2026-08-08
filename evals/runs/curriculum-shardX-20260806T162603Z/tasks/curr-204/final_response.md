# Finding the Mistake in Sums of Radicals — Grade 8 / Pre-Algebra

Three PDFs are ready:

- **`ss_radsums_curr204.pdf` — Skills Summary (study guide, 2 pages).** Read this first.
  Three sections, each with a rule box, a worked example, and a "try it" whose answer is
  printed upside down inside the box: (1) testing whether two roots may be added at all
  (they usually may not — $\sqrt{a}+\sqrt{b} \neq \sqrt{a+b}$), (2) combining like radical
  terms by adding only the counts in front, (3) simplifying each radicand first so terms
  that looked different become like terms. A watch-out box names the two classic slips this
  sheet is built around.
- **`ws_radsums_curr204.pdf` — Worksheet (3 pages, 8 problems).** An error-analysis sheet.
  Two problems present a named student's wrong work and ask for the correction *and* the
  diagnosis (Priya in problem 2, Marco in problem 7). Two more get your child to disprove
  the shortcut themselves by computing both sides — once with perfect squares, once with
  roots that need decimals. The rest are clean practice, ending with a three-term challenge.
- **`ak_radsums_curr204.pdf` — Answer Key (3 pages).** Every problem re-printed with the
  reasoning, plus a Quick Answers strip, a Curriculum block (standard 8.NS.A), and a
  "Common wrong answers" block giving the exact wrong values the traps produce.

## What is verified, honestly

- **12 machine-checked responses in all.** Every value on the sheet — the sums, the
  combined radical terms, the decimal approximations and the two comparisons — was
  recomputed independently with SymPy before the PDFs were allowed to compile.
- **Three problems (2, 7 and 8) also carry an instructor-judged part.** Those are the
  diagnoses and the justification: "explain what Priya did wrong", "explain what Marco did
  wrong", "justify why the three terms could be combined". A written explanation cannot be
  machine-checked, so it prints as `---` in the Quick Answers strip and the answer key gives
  you the rubric for each — what a full-credit answer must name, and what does not count.
  That is why the key's note reads "5 of 8 problems fully machine-checked": the other three
  are half checked and half yours to read.
- **Both planted wrong answers are declared traps and were proved distinguishable.**
  Priya's 10 is exactly what "add the radicands, then take one root" produces, and Marco's
  $6\sqrt{6}$ is exactly what "add the counts *and* the radicands" produces. The build
  confirmed that neither wrong value could be mistaken for the correct one.
- The study guide's three worked examples and three try-it answers are verified the same
  way (8 checks, all machine-checked).
