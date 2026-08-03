# Interpreting Correlation and Least-Squares Regression — Precalculus / Advanced Statistics

Three PDFs are ready: the student worksheet, a full step-by-step answer key, and
a two-page study guide.

**Worksheet (5 pages, 10 problems).** One data set carries the whole sheet:
eight students' weekly practice hours against their scores on a 120-point exam,
shown as both a table and a scatter plot with the fitted line drawn on it. The
regression output is given the way software gives it — $\hat{y} = 52 + 6x$ with
$r = 0.977$ — because the standard being exercised is interpretation, not
hand-computation of the coefficients.

Worth knowing: the data was constructed so that $\hat{y} = 52 + 6x$ is the exact
least-squares line for those eight points, not an approximation. The residuals
are $+3, -3, -3, +3, +3, -3, -3, +3$; they sum to zero and are uncorrelated with
$x$, which is what makes the line least-squares. That is why problem 6 (half the
points lie above the line) and problem 7 (the line passes through
$(\bar{x}, \bar{y}) = (4.5, 79)$) both come out exactly, and it means anyone who
recomputes the regression from the table will get the printed equation back.

Difficulty ramps 1 → 5: prediction, then reading an observed value, then the
residual and its sign, then $r^2$ and its complement, then two structural
properties of least squares, and finally extrapolation and causation.

**What was machine-verified.** Nine of the ten answers were recomputed
independently and the build was blocked until each agreed with the answer key:
both predictions (82 and 100 points), the observed score read from the table
(85), the residual (+3), $r^2 = 0.955$, the unexplained share (4.5 percent),
the fraction of points above the line (1/2), the mean score (79), and the
extrapolated value (172). Three misconception traps were checked for
distinguishability and are printed in the answer key's "common wrong answers"
block: reversing the residual to predicted minus observed (gives $-3$), taking
$\sqrt{r}$ instead of $r^2$ (gives 0.988, which is impossibly larger than $r$),
and reporting the explained rather than the unexplained percent (95.5).

**Flagged for manual review.** Problem 10 asks for a written paragraph on why
the model must not be extrapolated past the observed 1-to-8-hour range, and why
$r = 0.977$ still does not establish causation — with one confounding variable
named and one study design that would settle it. That is open reasoning and is
labelled manual. The answer key gives a full model answer and a grading note
listing the three things part (b) must contain, plus the specific wrong answer to
correct: a student who proposes collecting *more* observational data has not
removed the confounder.

**Study guide (2 pages).** Four sections — predicting from the line, residuals
and what their sign means, reading $r$ and $r^2$, and the two limits no
correlation can overcome — each with a rule box, a worked example that opens by
saying why that tool applies, and a try-it with the answer printed upside down
inside the box. The try-it in section 3 uses a negative correlation on purpose,
so the student sees that $r^2$ discards the direction. The watch-out box carries
the sentence-level habit that matters most here: write "accounted for by," never
"caused by."
