Three PDFs are ready for a fourth- or fifth-grade learner on **multistep volume,
conversion, and angle problems**, built as an interleaved review.

- **Worksheet (`ws_measurement_curr145.pdf`, 5 pages)** — 12 problems tagged
  across four facets: unit conversion (4), prism volume (3), angle measure (4)
  and multistep synthesis (2). Problems 1–2 warm up on single-step conversions;
  after that the facets rotate every problem or two, so the student has to decide
  each time whether the task is a conversion, a volume, or an angle relationship.
  The set closes with two syntheses: a tank in cm answered in litres, and a crate
  with mixed feet/inches edges answered in cubic feet. A value-free labelled box
  sits with the directions so no problem's figure can be misread as another's.
  Every problem carries 3.5–6 cm of work space with the answer blank *below* the
  work area, and nine problems print the required unit on that blank.
- **Answer key (`ak_measurement_curr145.pdf`, 2 pages)** — a quick-answer bank,
  then a numbered solution per problem that names the decision first (multiply or
  divide? which whole: 90 or 180? convert before or after?), then the arithmetic,
  then a check where one exists. It ends with a generated "Common wrong answers"
  block, so a grader seeing 146, 30000 or 36 knows exactly which misconception
  produced it.
- **Study guide (`ss_measurement_curr145.pdf`, 2 pages)** — four sections, one per
  facet, each with a rule/formula box, a worked example whose first step is the
  strategy sentence, and an upside-down try-it: conversion (with the
  multiply-vs-divide rule and a conversion table), prism volume (including the
  missing-edge case), angle measure (angles add; missing part = whole − part), and
  a four-step plan for multistep problems.

**Verification.** 12 of the 12 worksheet answers are machine-checked with SymPy
(11 `eval`, 1 `approx`), and all 8 study-guide results (4 worked examples + 4
try-its) as well. Problem 10 carries **two** entries: the numeric part (the
angle's true measure, 50°) is machine-verified, while the "explain what Rosa did
wrong" part is declared `manual` and is flagged for human review in the gate log —
it is not claimed as verified. Four misconception traps were declared and each was
machine-checked to be distinguishable from the correct answer. The full gate chain
passed (exit 2: manual-review item present, which is the correct outcome here).

**One note on standards tagging.** `references/standards-map.md` has no 4.MD/5.MD
row, and the skill forbids inventing codes, so every problem is tagged with the
map's verbatim measurement-and-data code `2.MD / 3.MD`. The content itself is
grade 4–5 (prism volume, multistep conversion, additive angle measure).
