# Polynomial Zeros and Turning-Point Constraints — Precalculus

Three PDFs are ready: the student worksheet, a full step-by-step answer key, and a
two-page study guide.

**Worksheet (6 pages, 12 problems).** The sheet works the two halves of the focus
together — where the zeros are, and what the degree then allows the graph to do:

- **Factor to locate zeros** (1, 2, 6, 9): a monic quadratic, GCF plus difference of
  squares, a cubic needing the Rational Root Theorem, and a quartic that is quadratic
  in $x^2$.
- **Multiplicity** (3, 7, 10): reading multiplicity off a factored form and deciding
  cross versus touch, including a quartic whose two zeros are both double (so it
  never crosses at all), and a sketch on a printed grid.
- **Turning-point constraints** (4, 8, 12): the bound read forwards (degree 5 allows
  4 turns), backwards (4 turns force degree at least 5), and finally the lower bound
  — why 5 distinct real zeros cannot coexist with 2 turning points.
- **End behaviour** (5, 11): two limits at infinity giving horizontal asymptotes,
  which is the rational-function half of the topic.

Work space runs 5–8 cm per problem, and problem 10 gets a full coordinate grid to
sketch on.

**What was verified, and what is not.** Sixteen independent SymPy checks cover the
twelve problems: 7 `zeros` checks, 2 `factor` checks (each factorisation proved
equivalent to the original polynomial), 2 `limit` checks at infinity, and 3
evaluations of the turning-point bounds. Problems 2, 4, 9 and 10 carry two checks
each because they have two parts.

**Two items are flagged for manual review, correctly:**

- **Problem 10(b)**, the sketch. Its zeros *are* machine-verified; the graph itself
  cannot be. The answer key gives a five-point checklist to grade it against
  (crossings at $-2$ and $3$, a touch at $1$, both ends rising, three turning points,
  and the correct sign on each interval).
- **Problem 12**, the justification. It is an explain-why question, so it is recorded
  as open reasoning rather than dressed up as a verified answer. The key contains a
  model answer and a grading note saying what full credit requires (the "must turn
  between consecutive zeros" idea; naming Rolle's theorem is not required).

The build reports this as "passed with manual-review items", which is the honest
outcome for a sheet that includes a sketch and a proof-style explanation.

**Answer key (4 pages).** Every solution shows the reasoning, not just the result —
why the turning-point bound is $n-1$, why an even multiplicity produces a touch, and
why dividing by the highest power exposes the horizontal asymptote. The quick-answer
bank sits at the top for fast grading, and the generated Curriculum section carries
the level and the standards codes.

**Study guide (2 pages).** Four sections — factor then read the zeros; multiplicity
(cross or touch); what the degree allows, stated in all three directions; and end
behaviour of a rational function — each with a rule box, a worked example, and a
try-it whose answer prints upside down inside the box. All eight study-guide answers
were verified by the same gate as the worksheet.
