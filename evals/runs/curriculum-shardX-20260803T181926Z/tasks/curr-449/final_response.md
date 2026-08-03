# Diagnosing Causal Claims and Biased Study Designs (Precalculus / Advanced Statistics)

Three PDFs are ready: the student worksheet, a full step-by-step answer key, and
a two-page study guide.

## What is on the worksheet (8 problems)

Every problem hands the student a number that is *arithmetically correct* and a
conclusion that is not. The work is to compute the statistic the claim rests on,
then say precisely what the design supports. Three cases run through the sheet:

**A club survey (problems 1--3).**
1. Of 400 members, 96 answered a survey link posted on the club website. The
   response rate is **6/25**.
2. Name the two biases at work when members choose whether to answer, and say who
   is over-represented. *(Open --- manual review.)*
3. **Find and fix** --- an officer calls 0.24 "the coverage". It is the response
   rate. Only 260 of the 400 members ever visit the website, so coverage is
   **13/20**, and the two are different faults with different remedies.

**A wellness program (problems 4--6).**
4. **Find and fix** --- seven people enrolled, two quit, and the advertisement
   reports a 6 kg mean computed from the finishers only. Over everyone who
   enrolled the mean is **4 kg**. That is attrition bias, and it always points the
   same direction.
5. The comparison group's mean is **2 kg**.
6. The company claims the program *makes* people lose twice as much. Explain why
   the data cannot support it --- naming how subjects entered the program group, a
   confounder, and the design that would. *(Open --- manual review.)*

**A poll (problems 7--8).**
7. **Find and fix** --- a weekday-morning farmers'-market sample is 55% retired
   against a town that is 20% retired, and the pollster reports the
   over-representation as 2.75 by dividing. Percentage points are a subtraction:
   **35**.
8. **Challenge** --- rewrite the headline for what the sample supports, then design
   the sampling plan (frame, probability selection, nonresponse follow-up) that
   would license it as written. *(Open --- manual review.)*

All eight problems bear directly on the focus: causal claims and biased study
designs. Problems 3, 4 and 7 are the find-and-fix items.

## What was machine-verified

Five problems were checked independently by the SymPy verifier before anything
printed: both exact probabilities, both group means, and the percentage-point
gap. Problems 2, 6 and 8 ask for explanations and a study design; those are
genuinely open, so they are labelled **manual review** rather than presented as
verified. The key gives a full model answer for each plus a "look for" list, so
the open items can be graded consistently --- including the answers that look
right but miss (naming "small sample size" instead of self-selection; proposing a
bigger sample at the same market).

Three declared misconception traps were proved distinguishably wrong by the
verifier and appear in the key's "Common wrong answers" block:

- reporting the response rate (0.24) as the coverage (0.65) --- two different
  faults, only one of which more data can fix;
- averaging the finishers instead of the enrollees (6 instead of 4);
- dividing two percentages and calling the ratio (2.75) a gap in percentage
  points (35).

## The study guide

Two pages, three sections, each with a rule box, a worked example, and a separate
try-it whose answer is printed upside down inside the box:

1. coverage vs. response rate --- two different fractions, two different faults,
   and why a larger sample fixes neither;
2. comparing two groups honestly --- attrition, who assigned the treatment,
   confounding, and random assignment as the remedy;
3. is the sample representative? --- percentage points are a subtraction, and a
   visible skew on a known variable warns about the unknown ones.

## Notes

- The watch-out box (a note that a regression slope on observational data is
  still association only) was cut to hold the guide to its two-page cap. It is
  the optional box; the try-its were kept.
- The grade level prints on the answer key only, in the generated Curriculum
  section (HSS-IC.A--HSS-IC.B for the design and inference problems,
  HSS-ID.A--HSS-ID.C for the summaries, difficulties 1--5).
