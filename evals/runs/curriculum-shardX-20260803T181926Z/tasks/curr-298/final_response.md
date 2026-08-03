# Piecewise Rules for Rates and Fees — Algebra 1

Three PDFs are ready: the student worksheet, a full step-by-step answer key, and
a two-page study guide.

**Worksheet (6 pages, 10 problems).** Every problem is a real price list — a
city garage, a shipper, an electric utility, a taxi, a community pool, a phone
plan, two competing garages, a print shop — and every one asks for the piecewise
rule in writing before any number is computed. The input variable and its unit
(hours, pounds, kilowatt-hours, miles, gigabytes, pages) are named in each stem,
and the output is always a cost in dollars. Difficulty ramps 1 → 5: the first
three problems are one-branch evaluations, the middle group works a cost back to
its input or recovers a missing rate, and the last two are a two-schedule
break-even system and a two-tier print job where the reduced rate has to be
found from a single job total.

The four skills the sheet exercises are: writing the rule from a schedule,
reading a cost back to its input, finding a missing rate inside a branch, and
comparing two schedules. Problem 3 is deliberately an error-analysis problem —
Priya's \$128.00 bill is exactly what the "charge everything at the top-tier
rate" mistake produces, and the student has to name the error before fixing it.

**What was machine-verified.** Nine of the ten answers were recomputed
independently with SymPy and the build was blocked until all nine agreed with
the answer key: the three evaluations (\$13.00, \$11.00, \$103.00, \$78.00), the
three solve-backwards problems (7 miles, \$3.50 per hour, 10 GB), the
break-even system (4 hours at \$10.00), and the print-shop rate (\$0.16 per
page). Three misconception traps were also checked for distinguishability — the
"bill every unit at the higher rate" error lands on \$19.00, \$128.00 and
\$138.00 respectively, all visibly different from the right answer, and each is
printed in the answer key's "common wrong answers" block so you can tell at a
glance which mistake a wrong answer came from.

**Flagged for manual review.** Problem 8 asks the student to explain, in
sentences, why the two branches of the phone-plan rule must agree at the
breakpoint and what a customer would see if they did not. That is open
reasoning, so it is not machine-checkable; the answer key carries a full model
answer plus a grading note saying what earns credit (evaluating both branches at
the breakpoint, and describing the downward jump in cost).

**Study guide (2 pages).** One section per skill, each with a rule box, a worked
example whose first line says *why* that method applies, and a try-it problem
with the answer printed upside down inside the box. The closing watch-out box
names the single most common error on this topic: applying the post-breakpoint
rate to all the units instead of only the ones past the breakpoint. The study
guide's four worked examples and four try-it answers were verified by the same
gate as the worksheet.
