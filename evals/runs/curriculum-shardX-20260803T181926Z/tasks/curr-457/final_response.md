# Derivatives: Power, Product, and Quotient Rules — AP Calculus AB/BC

Three PDFs are ready: the student worksheet, a full step-by-step answer key, and a
two-page study guide.

**Worksheet (5 pages, 10 problems).** Nine of the ten problems are direct practice
with the power, product, and quotient rules; the tenth (problem 3) derives
$\frac{d}{dx}x^3$ from the limit definition and asks the student to confirm it
agrees with the power rule, which is where the rules come from. The ramp goes from
a term-by-term polynomial (1), through rewriting a radical and a reciprocal as
powers (2), to plain product and quotient applications (4–7), then two two-part
problems that ask for the derivative *and* its value at a point (8, 9), and ends
with a synthesis problem needing the quotient rule outside and the product rule
inside the numerator (10). Work space runs 5–9 cm per problem.

**What was verified.** Twelve independent SymPy checks cover all ten problems:
eight `diff` checks (each derivative re-derived by the CAS and compared to the
printed answer), one `limit` check on the difference quotient in problem 3, and two
`eval` checks for the point evaluations in 8(b) and 9(b). Problems 8 and 9 carry two
checks each because each has two parts — the derivative and the value — so neither
part rides on the other. Every boxed answer in the key was then machine-bound to its
own problem's verified value. **Nothing is flagged for manual review**; every answer
on this sheet is machine-checkable and passed.

**Answer key (3 pages).** Each solution names the rule first, labels $u$, $v$, $u'$,
$v'$, shows the substitution, and then simplifies — problem 4 also includes the
expand-first cross-check, and problem 5 points out why the $x$-terms cancel. The
quick-answer bank at the top is for fast grading; the generated Curriculum section
records the course, the AP unit code (FUN-3.A–FUN-3.C), and the difficulty range.
The course level prints only on this document.

**Study guide (2 pages).** Four sections — power rule (with the "rewrite first"
habit), product rule, quotient rule, and the limit definition — each with a rule
box, a worked example whose first step says *why* that rule applies, and a try-it
whose answer is printed upside down inside the box. All eight study-guide answers
were verified by the same gate as the worksheet.

**Note on scope.** Every problem stays inside differentiation rules a student has by
the end of AP Calculus AB Unit 2: no chain rule, no implicit differentiation, and
the only transcendental factors are $\sin x$ and $\cos x$, whose derivatives belong
to the same "core rules" topic.
