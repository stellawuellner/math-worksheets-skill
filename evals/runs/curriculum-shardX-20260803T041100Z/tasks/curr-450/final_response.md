# Distributions, Regression, and Inference — Precalculus / Advanced Statistics

Three documents, all compiled and gated: a 12-problem student worksheet, a full
step-by-step answer key, and a 2-page study guide.

## What is on the worksheet

Twelve problems on **comparing models and making qualified data-based inferences**, built
around one data set (six hours of bacterial colony counts) and two competing models fitted
to it — a linear one and an exponential one. The whole sheet is a single argument carried
out in three moves:

- **summarise-the-distribution** (4 problems) — median 17.5, mean 21.33, IQR 22, total 128,
  with the mean-above-median ordering read as right skew and the IQR contrasted with the
  range;
- **compare-two-models** (4 problems) — residuals of both models at the same hour, the
  linear model's residual at the far end, and a read of the exponential model's residual
  table;
- **qualify-the-inference** (4 problems) — why one residual cannot choose a model, a
  probability drawn from the residual signs, what the model can and cannot support about a
  time beyond the data, and the closing lab-report paragraph.

Data Set A and both model equations sit in a boxed panel with the directions, before
problem 1, since most of the sheet reads from them; a display carrying numbers next to one
problem gets applied by a student working the next. Problem 10's residual table lives
inside its own stem, where its values bind to that problem's verified data.

Two-problem warm-up, then interleaved; the longest same-facet run after the warm-up is 2.
Difficulty ramps 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 5 with no drops.

The sheet is deliberately designed so the better model still fails a test: every one of
Model E's residuals is zero or positive and the misses grow with the hour, so the
"winning" model is systematically biased low. Problems 10, 11 and 12 are built on that
fact, which is what turns "which model fits" into "what may I claim".

## What was verified, and what is flagged manual

- **9 of 12 machine-verified** by SymPy: 3 `stats` summaries (median 17.5, mean 21.33, IQR
  22), 3 `eval` residuals (−4, 0.5, 5), 2 `read_data` reads (total 128, and hour 6 as the
  largest residual), and 1 `probability` (2/3).
- **3 flagged manual** (problems 5, 11, 12): why a single residual cannot choose a model,
  what the model supports about a time outside the observed range, and the conclusion
  paragraph. These are justification answers with no recomputable value, so they are
  declared `{"type": "manual"}` and the build exits 2 listing them. The key gives each a
  component-by-component credit rubric rather than a single "answer".
- **4 misconception traps declared and machine-checked as distinguishable**: quoting the
  median as the mean on a skewed distribution (problem 2 → 17.5), computing predicted
  minus observed so the residual's sign reverses (problem 3 → 4), reporting the range
  instead of the IQR (problem 6 → 41), and counting the two zero residuals as positive
  (problem 8 → 1). All four print in the key's "Common wrong answers" block.

The study guide has one section per facet (rule box → worked example → try-it), 6 boxes,
all 6 machine-verified. Its skill-3 rule box is the four-question checklist — range,
plausibility, bias, sample — that the worksheet's explanation problems are graded against.

## Standards

Distribution, residual and model-comparison problems are tagged `HSS-ID.A–HSS-ID.C`
("Statistics: data displays, spread, regression"); the inference and probability problems
are tagged `HSS-IC.A–HSS-IC.B` ("Inference & experimental design"). Both strings are copied
verbatim from `references/standards-map.md`, en-dashes included. No gap here.

## Gate result

`BUILD PASSED` on the first run, exit 2 with the three manual-review items. Worksheet 7
pages (budget 7), answer key 5 (budget 7), study guide 2 (cap 2). Prose consistency 100% on
both the worksheet and the study guide.
