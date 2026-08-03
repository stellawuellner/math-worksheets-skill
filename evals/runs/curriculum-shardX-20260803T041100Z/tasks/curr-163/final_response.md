# Percent Applications: Tax, Tip, Discount, and Markup — Grades 6–7

Three PDFs were generated and every gate in the build chain is green.

- **Worksheet** (`ws_percent_applications_curr163.pdf`) — 10 problems, all
  money contexts with the price and the percent stated explicitly and every
  answer asked for "in dollars". The sheet opens with a value-free percent-bar
  model showing the two situations (a percent added on vs. a percent taken off)
  so the student has a representation to name the base with. Coverage: three
  sales-tax problems, two tips, three discounts, two markups, interleaved so no
  method repeats twice in a row. The last two problems run the relationship
  backwards — given the sale price or the after-tax total, write and solve an
  equation for the original price, which is where the wrong-base error usually
  shows up.
- **Answer key** (`ak_percent_applications_curr163.pdf`) — names the base for
  every problem, shows the multiplier and the two-step alternative, and closes
  each solution with a check or a note on the specific wrong answer a grader
  will see. The generated quick-answer bank sits under the title block and
  prints the four declared traps.
- **Study guide** (`ss_percent_applications_curr163.pdf`) — 2 pages, one section
  per skill (sales tax · tip · discount · markup), each with a rule box that
  names the base, a worked example whose first step chooses the tool, and a
  distinct try-it with its answer upside down inside the box. A closing
  watch-out box covers the two-percents-two-bases error.

## Verification

All 10 problems are machine-checked by SymPy — **nothing is flagged manual**:

- Problems 1–4: `eval` with the price and the percent as named givens
  (`p*r/100`, `p*(100-r)/100`, `c*(1+r)/100`-style), so the numbers printed in
  the stems are the numbers the checker used.
- Problems 5–8: `approx` on the full multiplier chain, compared at cent
  precision.
- Problems 9–10: `solve` for the original price / pre-tax price.

The study guide's eight boxes (four examples, four try-its) are separately
verified as `approx`.

Four misconception traps are declared and were each proved distinguishable from
the correct answer:

- P5: reporting the tax alone as the total (1.78 instead of 26.28).
- P6: reporting the tip alone as the amount paid (10.51 instead of 68.91).
- P7: folding 25% off and 6% tax into one 19% change (58.32 instead of 57.24).
- P8: taking 45% of cost as the shelf price (8.37 instead of 26.97).

Standard `7.RP.A.3` (from `references/standards-map.md`, row "Percent problems")
is tagged on all 10 problems.

## Notes for the reviewer

Nothing is left for manual review. One gate failure occurred during authoring
and was fixed: the study guide's discount rule box overflowed the page width by
20pt because a `\dfrac` with prose inside it (`\frac{100 - \text{percent
off}}{100}`) was set inline; moving it into display math cleared it. The
remaining prose-checker flags are the decimal multipliers (1.08, 1.20, 0.7,
1.40) that the guide derives from the stated percents — expected false flags.
