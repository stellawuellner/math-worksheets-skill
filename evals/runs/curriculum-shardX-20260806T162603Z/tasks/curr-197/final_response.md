Here are the three PDFs for the Grade 7 centre-and-spread fluency set.

- **Worksheet** (`ws_centre_spread_curr197.pdf`) — 12 problems that ramp from
  single-measure drill to real interpretation, with no two sharing a skeleton:
  mean, range, median of an even-length list, mode; then quartiles and the
  interquartile range of eight values; then the cases where the number and its
  meaning come apart — five bicycle prices where one 46-dollar bike pulls the
  mean past four of the five, a twelve-value set where the range is 22 but the
  IQR only 12, a **missing-value** problem (five numbers with mean 12, find the
  fifth), two bus routes with the *same median* and very different IQRs, a
  **mean absolute deviation**, a combined mean of two unequal groups (86, not
  85), and a closing nine-donation set where the student must pick which centre
  and which spread to print in a newsletter.
- **Answer key** (`ak_centre_spread_curr197.pdf`) — Quick Answers bank,
  generated Curriculum section (6.SP.A and 6.SP.B.5, difficulty 1–5), and
  solutions that show the ordered list, the halves and the subtraction, not just
  the number. The combined-mean solution states the trap explicitly: averaging
  80 and 90 gives 85 and over-weights the smaller group.
- **Study guide** (`ss_centre_spread_curr197.pdf`) — three sections: measures of
  centre, measures of spread, and how to pair them honestly (mean with range
  when values are even; median with IQR when one value sits far out). Each has a
  worked example and a try-it with the answer upside down inside the box; the
  watch-out is the unequal-group mean.

**What is verified.** The sheet asks for 23 responses. **20 are machine-checked**
with SymPy — every mean, median, mode, range, quartile and interquartile range
recomputed from the same data array printed in the problem's table; the missing
value solved from the mean equation rather than compared to a typed answer; the
mean absolute deviation recomputed term by term; and the combined mean
recomputed from the two group sizes. **3 are instructor-judged**: which measure
represents the bicycle prices (6c), which bus route is more predictable (9c),
and which centre-and-spread pair describes the donations honestly (12e). Each
carries a rubric in the key naming what a correct answer must contain, and the
bank marks them `---`. All nine study-guide checks are machine-verified.
