Here are the three PDFs for an 8-problem precalculus/statistics error-analysis set on
**diagnosing causation claims and biased study designs**.

**Worksheet — `ws_studydesign_curr449.pdf` (5 pages).** Every problem reports a claim in
which the arithmetic is right and the conclusion is wrong — that is the point of the sheet.
Part (a) has the student compute the figure the claim rests on, so they cannot dismiss it
before understanding it; the later part asks them to name the flaw. The eight items cover the
four ways this goes wrong: a percentage quoted without its base (problems 1 and 6), a sample
that selected itself (2 and 4), a group comparison where the subjects chose their own group
(5 and 7), and a correlation read as a cause (3 and 8). Difficulty ramps 1 → 5, closing with
a synthesis item where the student must also say what evidence *would* settle the question.

**Four of the planted wrong results are machine-checked misconception traps**, as asked:
quoting the 100% doubling as if it were the market share, dividing by the 3000 members
instead of the 240 respondents, reporting the 50% relative risk reduction as the absolute
change, and using all 400 plants as the denominator instead of the 200 treated. Each trap
value is computed from the wrong method's own expression and the build confirms the
problem's correct-answer check rejects it, so none of them is a hand-typed number.

**Answer key — `ak_studydesign_curr449.pdf` (3 pages).** Each problem restated, the
computation worked, and a full written diagnosis followed by a sentence saying what a
response must contain for full credit — for example, that problem 3 needs a *named* common
cause, not just the phrase "correlation is not causation". The key opens with a quick-answer
bank, a curriculum block, and the generated "common wrong answers" list.

**Study guide — `ss_studydesign_curr449.pdf` (2 pages).** Four sections — association versus
causation, who was actually asked, observational study versus experiment, and relative change
versus base rate — each with the rule that prevents the error, a worked example, and a try-it.

**What was verified, honestly.** The sheet asks for **18 separate responses**. **10 are
machine-checked** with SymPy: every proportion as an exact fraction, both group means, the
$r^2$ value, the absolute risk difference, and both readings from the admissions table. The
other **8 are instructor-judged** — one per problem, the diagnosis — and are marked `---` in
the quick-answer bank. On a sheet about study design that is unavoidable and correct: naming
a lurking variable or a sampling bias is an argument, not a number, and no computer algebra
system can grade it. The key prints a model diagnosis and an explicit full-credit criterion
for each of the eight. The eight study-guide examples and try-its are machine-checked.

No response is marked `[unchecked]`.
