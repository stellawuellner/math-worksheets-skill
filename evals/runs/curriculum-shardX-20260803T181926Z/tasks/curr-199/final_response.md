# Samples and chance — wrong denominators and loaded samples (Grades 6–7)

Three PDFs: the student worksheet, a step-by-step answer key, and a two-page
study guide.

**What the worksheet does.** Eight problems built around the two questions that
catch most errors in this unit: *"out of what?"* and *"who got asked?"* Six of
the eight are explicit find-and-fix items.

1. Warm-up: P(red) from a bag of 5 red, 3 blue and 4 green marbles.
2. Find and fix: Ines uses the *non-blue* marbles as the denominator.
3. Find and fix: a marble is removed and not replaced; Marco updates the
   numerator but not the total.
4. Find and fix: Max uses the walkers as the whole group when the student was
   drawn from the whole class — the same numerator, a different question.
5. Find and fix: Nora surveys at the bike rack. Scaling her sample up to the
   school gives 270 of 300 cyclists, and that absurd number is what exposes the
   bias.
6. Find and fix: a library survey concluding chess is the school's favourite
   club. Students total the survey and then say why the *place* invalidates it.
7. Two samples of reading hours — one from the book club, one drawn at random.
   Students compute both medians and choose which describes a typical student.
8. Open task: why the late-bus queue is a biased sample, what a fair plan would
   look like, and a probability plus an estimate from a properly random sample.

Difficulty runs 1 to 5.

**What was machine-verified.** Ten checks were recomputed with SymPy: every
probability as an exact fraction, both medians, and both scale-ups from a sample
to the school. Ten misconception traps are declared and each was proved to land
on a value the problem's own check rejects — so `3/9`, `4/12`, `6/10`, `45/105`,
9 and 5.5 are all genuinely distinguishable from the right answers. They print in
the answer key as a "Common wrong answers" list, which turns a wrong answer into
a diagnosis rather than a mark.

**What is flagged for manual review.** The explanation halves of problems 6 and
8. Both are genuinely open — they ask *why* a sample cannot be trusted and what
to do instead — so the answer key gives model wording and states what a
full-credit answer must contain, notably that the reason has to be about *who
could have been asked*, not about sample size.

**The study guide** covers the three skills the worksheet tests — choosing the
right denominator, deciding whether a sample is fair (with the scale-up formula),
and finding a median — each with a rule box, a worked example, and a try-it whose
answer is printed upside down inside the box.
