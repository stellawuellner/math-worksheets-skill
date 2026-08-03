# Scatter Plots and Bivariate Association — Grade 8 / Pre-Algebra

Three documents, all compiled and gated: a 12-problem student worksheet, a full
step-by-step answer key, and a 2-page study guide.

## What is on the worksheet

Twelve problems on **using bivariate evidence to make and qualify predictions**. All
twelve sit inside that focus, and the sheet is built so that the *qualification* is graded
as heavily as the arithmetic:

- **read-the-trend** (4 problems) — read a point off Scatter Plot A, find the point that
  does not fit, compare two students' scores, and summarise the whole plot with a mean;
- **predict-from-the-line** (5 problems, one of them two-part) — evaluate the trend line
  $y = 0.8x + 45$, compute a residual, and find where two classes' trend lines agree;
- **qualify-the-prediction** (4 problems) — association versus causation, interpolation
  versus extrapolation, and how far one outlier moves a summary.

Scatter Plot A (ten students, study minutes against quiz score, with the trend line drawn
over the observed range only) sits in a boxed panel with the directions, before problem 1,
because it is shared by seven problems — a value-bearing display placed beside one problem
gets applied by a student working the next one.

Two-problem warm-up, then interleaved; the longest same-subskill run after the warm-up is
2. Difficulty ramps 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 5 with no drops. The sheet is designed
so problems 3 and 7 do identical arithmetic and problem 8 asks why only one of them is
defensible. Problem 12 is the synthesis challenge: a newspaper headline whose number the
trend line really does produce, at a study time far outside the data, giving a quiz score
above the maximum possible.

## What was verified, and what is flagged manual

- **10 of 12 problems (13 checks) machine-verified** by SymPy: 3 `read_data` reads off the
  plot (85, the outlier's study time 22, a score gap of 36), 5 `eval` predictions and
  residuals (69, 65, 3, 93), 2 `stats` means (72.7 with the outlier, 70.78 without), and 1
  `solve` for where two trend lines cross (36 minutes). Problem 4 carries two verify
  entries under one id — the prediction and its residual — with identical difficulty.
- **3 flagged manual** (problems 5, 8, 12): why association is not causation, the
  interpolation/extrapolation argument, and the synthesis paragraph. These are
  justification answers with no single recomputable value, so they are declared
  `{"type": "manual"}` and the build exits 2 listing them. The key supplies a full credit
  rubric for each rather than a bare answer.
- **3 misconception traps declared and machine-checked as distinguishable**: adding the
  slope instead of multiplying by it (problem 3 → 75.8), subtracting study times instead
  of scores (problem 9 → 40), and dropping the outlier from the total but still dividing
  by ten (problem 11 → 63.7). All three print in the key's "Common wrong answers" block.

The study guide has one section per subskill (rule box → worked example → try-it), 6
boxes, all 6 machine-verified. Its skill-3 rule box is the four-question checklist —
range, possibility, outlier, causation — that the worksheet's explanation problems are
graded against.

## Standards

Every problem is tagged `8.SP.A.1`, the "Bivariate data, scatter plots" row of
`references/standards-map.md`, copied verbatim. No gap here.

## Gate result

`BUILD PASSED` on the first run, exit 2 with the three manual-review items. Worksheet 7
pages (budget 7), answer key 5 (budget 7), study guide 2 (cap 2). The one prose-consistency
flag is problem 12's headline numbers (75 and 105), which are the newspaper's claim being
criticised rather than givens the computation uses — the documented false-flag case for a
manual problem.
