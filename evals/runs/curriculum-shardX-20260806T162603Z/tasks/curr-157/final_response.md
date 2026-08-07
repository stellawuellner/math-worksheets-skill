# Unit Rates from Fractions and Mixed Numbers — Grades 6–7

Three PDFs: the student worksheet, a full step-by-step answer key, and a two-page study
guide.

**Worksheet (12 problems).** A fluency sheet on the one thing that makes 6.RP unit rates
hard: when both quantities are fractions, "per one" is a division by a fraction. The
ramp is deliberate and no two problems share a skeleton.

- **1–3** are the clean shape — 3/4 mile in 1/2 hour, 5/8 km in 1/4 hour, 7/8 metre in
  1/4 second — with the answer in mph, km/h and m/s.
- **4, 5, 11** add the mixed number that has to be converted before dividing
  (2½ feet in ¾ second; 3⅓ pages in ⅖ minute; 1½ cups for ⅔ of a batch).
- **6, 9** are comparisons: two runners, and two shops selling cashews. Each asks for
  both unit rates *and* the comparison sign, because the whole point is that a smaller
  total price or a shorter time settles nothing on its own. The cashew problem is the
  good one — the shop with the lower price *and* the smaller bag turns out to be the
  cheaper one per kilogram.
- **7, 8, 10** turn the rate the other way up: how long for the whole tank, miles per
  gallon, and how long to move a whole pool given 7/8 of it in 1¾ hours.
- **12** is the synthesis: two legs of a bike ride at 7 mph and 5 mph, whole-ride speed
  of 6.2 mph, and then the question of why that is *not* the average of 7 and 5.

Answers stay exact — no rounding — and every measurement unit (mph, km/h, m/s, ft/s,
hours) is declared in the verification data and printed on both the worksheet's answer
line and inside the key's boxed answer.

**Answer key.** Every solution shows the reciprocal step written out, the unreduced
product, and the reduction, plus a direction check where one is available ("filling more
than was done must take longer than the time already spent", "2¼ cups is more than 1½,
as it must be").

**Study guide (2 pages).** Four sections: a rate when both quantities are fractions,
rates that start with a mixed number (convert first — dividing part by part is wrong),
comparing two rates fairly, and turning the rate the other way up. Each has a rule box,
a worked example whose first step names the strategy, and a try-it with the answer
upside down inside the box.

## What is verified, honestly

The sheet asks for 19 separate responses across the 12 problems.

- **18 are machine-checked** with SymPy as exact rational arithmetic — every unit rate,
  both comparison signs, the whole-pool time solved from the rate equation, and all
  three speeds in problem 12. The printed key was bound back to those verified values by
  the build, so a boxed answer cannot drift from what was checked.
- **1 is instructor-judged** and prints as `---` in the Quick Answers bank: problem
  12(d), the explanation of why the whole-ride speed is not the average of the two leg
  speeds. The key states what full credit requires — total distance over total time, and
  the observation that the two legs last different amounts of time, so the faster leg
  carries more weight. Averaging would only be right if the two times were equal.

Eleven of the twelve problems are fully machine-checked end to end; problem 12 has three
checked numbers and one written half.
