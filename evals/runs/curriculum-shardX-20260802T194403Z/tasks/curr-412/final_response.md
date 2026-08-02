Here are the three documents for procedural fluency in solving logarithmic
equations with domain checks (Precalculus / advanced algebra).

**Worksheet — 12 problems, ramped.** A boxed **worked pattern** at the top runs
the four-step routine end to end (domain → rewrite in exponential form → solve →
check), so the student sees the model before working independently. Each problem
then asks for the domain restriction first. The ramp: two straight conversions
(1–2), equal-base logs (3), building the product-rule tool (4), the first
combine-then-solve with an extraneous root (5), an explicit domain-check item
that evaluates the offending argument (6), an exact answer with e (7), a case
where the negative candidate is *valid* (8, arguments positive at x = −6),
rounded answers via e and via a non-integer exponent (9, 11), the quotient rule
with a fractional answer (10), and a synthesis needing the power rule then the
quotient rule (12). No two problems share a skeleton.

**Answer key — step by step.** Every solution prints the four steps under their
own labels, states the domain explicitly, and checks each candidate. Problem 5
shows the extraneous root and why it is extraneous; problem 8 shows the opposite
lesson — a negative candidate that survives because the *argument* is positive;
problems 9 and 11 warn against rounding before the last line.

**Study guide — 2 pages.** A domain-rule and properties box up front, then four
sections (one log = a number, log = log, two logs on one side, decimal answers),
each with a rule box, a worked example whose first step names why that method
applies, and a try-it with the answer upside down inside the box.

**Verification.** All 12 worksheet answers are machine-checked with SymPy: 9
`solve` checks (including the exact answer e² + 1 and the fraction 13/9 and the
two-root case {2, −6}), 1 `equiv` check for the log₂(8x) = 3 + log₂x rewriting,
1 `eval` for the domain-check evaluation, and 2 `approx` checks for the rounded
answers 10.54 and 20.99. All 8 study-guide results are checked the same way. One
part is *not* machine-verified and is labelled so on the page: the one-sentence
written explanation in problem 6 of why x = −2 is extraneous — the evaluated
argument (−4) that the explanation rests on is verified. The full gate chain is
green, including facet coverage and the per-problem binding of every boxed
answer to its verified value.
