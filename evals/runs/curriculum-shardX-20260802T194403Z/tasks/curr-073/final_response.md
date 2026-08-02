# Unknown Factors and Related Division Facts — Grade 2–3

Three PDFs are ready.

**Worksheet (`ws_ufactor_curr073.pdf`, 5 pages, 10 problems).** Every problem hides one
factor and asks the student to recover it. The sheet runs through four related
representations: dot arrays (problems 1, 2, 7), bare unknown-factor equations with the blank
in either position (3, 6), equal-group stories with the total and the number of groups stated
in units (4, 8), and related division facts read straight off a multiplication fact (5, 9).
It ends with a two-step packing problem (10: rolls into bags, bags into boxes) that requires
two unknown-factor steps in a row. Difficulty ramps 1 → 4 and the methods interleave after
the two-problem warm-up, so the student has to decide which model fits rather than repeat one.

**Answer key (`ak_ufactor_curr073.pdf`, 2 pages).** A quick-answer bank for grading at the top,
then a worked solution for each problem that names the unknown-factor equation first, shows
the skip-count or times-table fact that resolves it, and confirms with the related division
fact. Problem 9's solution flags the trap of answering with the mystery number (6) instead of
the requested product (48).

**Study guide (`ss_ufactor_curr073.pdf`, 2 pages).** One section per skill on the sheet:
array model, unknown-factor equation, equal-group story, fact family. Each has a rule box,
a two-step worked example, and a different try-it with the answer printed upside down inside
the box for self-checking. A closing watch-out box addresses the two errors this topic
produces most: writing the total in the blank, and stopping after step one of a two-step story.

## Verification

All 10 worksheet answers are machine-checked with SymPy: 8 as `solve` on the unknown-factor
equation (e.g. `4*n - 24 = 0`), 2 as `eval` of the related-fact computation. **Nothing is
flagged manual** — no problem on this sheet is open-ended. All 8 study-guide boxes (4 worked
examples + 4 try-its) are verified the same way, so the numbers a student learns from are
checked too. The full gate chain passed green: verification, skill and facet coverage,
layout and work-space, answer-line binding, page budgets, per-problem answer-key binding,
worked-example structure, and prose–JSON number consistency.
