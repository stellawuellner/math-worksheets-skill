# Scatter Plots and Bivariate Association --- Does It Show Cause, or Only a Pattern? (Grade 8 / Pre-Algebra)

Three PDFs are ready: the student worksheet, a full step-by-step answer key, and
a two-page study guide.

## What is on the worksheet (8 problems)

The sheet opens with three data displays the whole set works from, so nothing
has to be re-read across pages:

- **Graph A** --- ice-cream cartons against sunscreen bottles for eight summer
  weeks in one town (the classic confounded pair);
- **Table B** --- test scores of ten students who *chose for themselves* whether
  to use a tutoring app;
- **Graph C** --- television hours against sleep hours for six students.

1. Read one point off Graph A: the 26-carton week sold **12** bottles.
2. **Find and fix** --- Dana reports the rise in sunscreen as 28. That is the
   change on the *horizontal* axis; the real rise in bottles is **14**.
3. Dana claims the plot proves ice cream causes sunscreen sales. Name a lurking
   variable and say why a scatter plot cannot show cause. *(Open --- manual review.)*
4. **Find and fix** --- Ravi averages all ten students and reports 78.5. Pooling
   the groups answers a different question; the app group's mean is **84**.
5. The non-user group's mean is **73**.
6. The advertisement claims the app "raises scores by eleven points". Explain why
   a self-selected study cannot support that, and what would.
   *(Open --- manual review.)*
7. **Find and fix** --- Sam reports the effect as 5, again by subtracting the
   horizontal axis. The change in sleep is **-2.5 hours**.
8. **Challenge** --- rewrite Sam's headline as a claim Graph C supports, then
   describe the randomized experiment that would test the cause claim.
   *(Open --- manual review.)*

Seven of the eight problems turn directly on the correlation-versus-causation
question; problem 1 is the warm-up read that puts the association on the table.
Problems 2, 4 and 7 are the find-and-fix items.

## What was machine-verified

Five problems were checked independently by the SymPy verifier before printing:
both scatter-plot readings, the two group means, and the signed change in sleep
hours. The chart values and the checks come from the same data in the
verification file, so the plotted points and the answer key cannot disagree.

Problems 3, 6 and 8 ask for explanations and a study design. Those are genuinely
open, so they are labelled **manual review** rather than dressed up as verified.
The answer key gives a model answer for each plus a short "look for" list, so a
parent or teacher can grade them consistently.

Three declared misconception traps were proved distinguishably wrong by the
verifier and print in the key's "Common wrong answers" block:

- reading the *horizontal* axis when the question is about the vertical one
  (28 instead of 14, and 5 instead of -2.5) --- the single most common scatter
  plot error, and the one that makes a causal story sound quantitative;
- averaging everyone together instead of the treatment group alone
  (78.5 instead of 84).

## The study guide

Two pages, three sections, each with a rule box, a worked example, and a
separate try-it whose answer is printed upside down inside the box:

1. reading a scatter plot --- direction, and which axis the question is about;
2. does the gap prove cause? --- compute each group's mean from that group's own
   data, then run the three checks (lurking variable, reverse cause, who chose
   the groups);
3. fixing a cause headline --- swap the causal verb, scope the claim to the data
   collected, and name the randomized experiment that would settle it.

## Notes

- The grade level prints on the answer key only, in the generated Curriculum
  section (8.SP.A.1 for the scatter-plot work, 6.SP.B.5 for the means, 7.SP.A for
  the sampling/inference question, difficulties 1--5).
- The worksheet runs 4 pages: one for the data displays and directions, three for
  the problems with real room to write the explanations this topic asks for.
