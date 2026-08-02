# Subtracting Across a Zero — Grades 2–3

Three PDFs are ready: the student worksheet, a full step-by-step answer key, and
a two-page study guide.

**Worksheet (`ws_across_zero_curr062.pdf`, 4 pages, 10 problems).** Every
problem sits on the requested focus — subtraction that has to regroup across a
zero — and the sheet opens with a fully worked model of $305 - 168$ in the
directions so the student sees the trade before doing one alone. The ramp goes
one zero in the tens place (302, 605, 704) → the estimate that gives the answer
a sanity check → two zeros (500, 800) → checking a difference by adding it back
→ a find-and-fix item → the hardest classic, $1000 - 487$, where the trade
travels three places. No two problems repeat the same skeleton, and each one
gets 4.5–5 cm of vertical space, which is what a 2nd or 3rd grader actually
needs for the regrouping marks above the digits.

**Answer key (`ak_across_zero_curr062.pdf`).** Each solution names the trades in
place-value language ("2 hundreds, 9 tens, 12 ones"), not just the digits, and
every difference is checked by adding it back. Problem 9's entry explains the
mistake Rico made rather than only correcting it. A quick-answer bank sits at
the top for fast grading, and a "common wrong answers" line tells the grader
what a 555 on problem 9 means.

**Study guide (`ss_across_zero_curr062.pdf`, 2 pages).** Four sections, one per
skill the worksheet tests: trading across one zero, trading across two zeros,
estimating the difference first, and checking by adding. Each has a rule box in
plain language, a worked example that starts with *why* that method applies, and
a try-it whose answer is printed upside down inside the box so the student
attempts it before checking. The watch-out box names the single most common
error on this topic — subtracting the smaller digit from the larger one.

## Verification

All 10 worksheet problems are machine-verified with SymPy: 8 as exact
`eval` arithmetic and 2 as `estimate` (round each operand to the named place,
then subtract). Nothing on this sheet is left to manual review — the build
reported `BUILD PASSED — all gates green`, 10 passed / 0 failed / 0 manual.

All 8 study-guide boxes (4 worked examples + 4 try-its) are verified the same
way against `verify_ss_across_zero_curr062.json`.

The find-and-fix problem declares its planted wrong answer (555) as a
machine-checked misconception trap: the verifier recomputes the wrong method
$(9-4)\cdot100 + (5-0)\cdot10 + (8-3)$, confirms it really does produce 555, and
confirms 555 is distinguishable from the correct 445.

Standards tagged `3.NBT.A.2` throughout; difficulty ramps 1 → 4 with no drops.
