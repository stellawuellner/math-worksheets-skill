# Statistical questions and describing variability (Grades 6–7)

Three PDFs are ready:

- **`ws_stats_curr196.pdf`** — the student worksheet, 10 problems, 6 pages.
- **`ak_stats_curr196.pdf`** — the step-by-step answer key, 4 pages.
- **`ss_stats_curr196.pdf`** — a 2-page study guide.

## What the worksheet does

Two ideas, and the second is the one students skip.

**A question is statistical when its answers vary.** That is a property of the answers, not
of the topic — so "How tall is Priya?" is *not* statistical even though it is about height.
The sheet makes that test concrete rather than verbal: for each question the answers have
already been collected and drawn as a dot plot, and the student computes the range. A range
of zero is what "no variability" looks like as a number, and every dot in one stack is what
it looks like as a picture. Problems 1 and 2 are the same question with one word changed
("Priya" → "the students in our class"), which is the whole distinction in one edit.

**A distribution needs two numbers: a centre and a spread.** Problems 4–8 work with real
homework-time data from two classes, plotted on the same scale:

- Class A: $15, 20, 20, 25, 30, 30, 35, 40, 45, 60$ — mean 32, median 30, range 45, IQR 20.
- Class B: $28, 30, 30, 32, 32, 33, 34, 35, 36, 40$ — mean 33, range 12, IQR 5.

The two classes have essentially the same centre and wildly different spreads, which is
exactly the situation where quoting a mean alone misleads. Problem 9 draws one student at
random and asks for $P(\text{more than }30\text{ minutes}) = \tfrac{2}{5}$ — not one half,
because two students landed exactly on the median. Problem 10 asks the student to write to
the teacher and say why the mean alone would give a false picture.

Problem 6 carries a declared misconception trap: Sam takes the middle of the *unsorted*
list and reports a median of 35. The trap was machine-checked to be distinguishably wrong,
and the answer key names it for the grader.

## What was verified, and what was not

**Sixteen machine checks across problems 1–9**, all passing: every range, mean, median,
quartile, IQR, the difference of the two ranges, and the probability were recomputed
independently with SymPy from the same value lists that draw the dot plots, so the picture
and the answer key cannot disagree.

**Problem 10 is flagged for manual review** — it asks for a written explanation. The answer
key supplies the numbers to be used, a full model answer, and a marking guide: full credit
requires a spread measure quoted *with its number* and used to separate the two classes;
partial credit for saying they "differ in how spread out they are" without a range or IQR;
not sufficient to restate the two means.

## The study guide

Four short sections, each with a rule, a worked example whose first step explains why that
tool applies, and a distinct try-it with the answer printed upside down inside the box: is
it a statistical question, centre (mean and median), spread (range and IQR, with a dot
plot), and chance from a data set. All twelve study-guide values were verified by the same
checker as the worksheet.

Standards covered: 6.SP.A (statistical questions and variability), 6.SP.B.5 (centre and
spread of a distribution), and 7.SP.C.5, 7.SP.C.7 (simple probability). Difficulty ramps
1 → 5.
