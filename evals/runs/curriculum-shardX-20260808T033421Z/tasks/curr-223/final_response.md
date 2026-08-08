Here are the three PDFs for a Grade 8 / Pre-Algebra workshop set on **linear
representations, focused on converting between standard form $Ax + By = C$ and
slope-intercept form $y = mx + b$**.

**Skills Summary (study guide)** — `ss_formconv_curr223.pdf`, 2 pages.
An opening box says what each form is good for, then three sections: standard
to slope-intercept, slope-intercept back to standard, and reading both
intercepts straight off standard form. Each has a rule box, a two-step worked
example that names the strategy before computing, and a try-it with the answer
printed upside down inside the box. One watch-out box flags the single most
common slip: dividing only the $x$-term by the $y$-coefficient and leaving the
constant alone.

**Worksheet** — `ws_formconv_curr223.pdf`, 5 pages, 10 problems.
Every problem is a budget or mixture situation with the quantities and prices
stated ("$x$ notebooks at \$3 and $y$ pens at \$2 for \$36"), so standard form
arrives the way it actually arises. The two conversion directions alternate
with the intercept work rather than being blocked, so the student has to pick
the move each time; problem 8 pairs a table of whole-number combinations with
the same equation so the two representations can be checked against each other,
and problem 10 closes with an interpretation question. Work space is about 5 cm
per single-answer problem, with a separate blank for every part.

**Answer key** — `ak_formconv_curr223.pdf`, 2 pages.
Quick Answers bank labelled by response, then a worked solution per problem
that shows the division applied to *every* term, and — for the reverse
direction — the substitution that makes the $x$-terms cancel, which is why a
constant is left on the right. Curriculum block: 8.EE.B.6 and 8.F.B,
difficulty 1–4.

**What is verified, honestly.** Fifteen checks were declared across the ten
problems, and **fourteen are machine-checked with SymPy**. The conversions to
slope-intercept form are verified by actually solving the standard-form
equation for $y$ symbolically, so the printed answer is the CAS's own result;
the conversions to standard form are verified by substituting the
slope-intercept expression and confirming the $x$-terms cancel to exactly the
stated constant; intercepts, the slope from two intercept points, and the table
reading are all checked directly. Prose numbers on the worksheet match the
verification data 34 out of 34.

**One response is instructor-judged, not machine-checked**: problem 10(b),
which asks what the slope means for the gardener. The Quick Answers bank prints
`---` for it and the key's generated note reads "9 of 10 problems fully
machine-checked", naming problem 10. The worked solution states what a correct
interpretation must contain (the trade-off between the two plants, and the
meaning of the negative sign) and what does not earn credit.
