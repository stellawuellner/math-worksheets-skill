Three PDFs are ready for an Algebra 1 student on **solving linear systems by
substitution**, built as a procedural-fluency ramp.

- **Worksheet (`ws_substitution_curr262.pdf`, 5 pages)** — 12 systems, no two
  built on the same skeleton. The directions carry a fully worked pattern
  ($y = x + 1$, $2x + y = 7$), then the ramp runs: three systems with a variable
  already isolated (1, 2, 4), three that must be isolated first (3, 5, 8), a
  fraction-valued solution (7), the two special cases — no solution (9) and
  infinitely many (10) — and three word models (6 tickets, 11 rectangle
  perimeter, 12 acid mixture). Difficulty tags run 1 → 5 and the facets rotate
  after the warm-up, so the student has to decide *which* variable to isolate
  rather than repeat one move. Each problem gets 5–7 cm of work space and an
  answer blank.
- **Answer key (`ak_substitution_curr262.pdf`, 3 pages)** — quick-answer bank
  first, then a three-step solution per system: which equation to substitute into
  and why, the one-variable solve, the back-substitution, and a check in the
  equation that was *not* substituted into. Problems 9 and 10 show the collapse
  ($-6 = 1$ false → parallel lines; $8 = 8$ true → same line) and say exactly what
  to accept as a correct student answer.
- **Study guide (`ss_substitution_curr262.pdf`, 2 pages)** — four sections, each
  with a rule box, a worked example whose first step is the strategy sentence, and
  an upside-down try-it: substituting a given isolated variable, isolating first
  (choose the coefficient-1 variable; parenthesise before subtracting), reading
  the special cases, and building a system from a story (count equation + value
  equation).

**Verification.** 11 of the 12 worksheet systems are fully machine-checked with
SymPy. Ten of them match SymPy's complete solution set exactly; problem 9, the
no-solution case, is checked as an **inconsistent system** — SymPy is asked for
the full solution set of $y = 2x + 3$ with $4x - 2y = 1$, finds it empty, and
confirms the key's "no solution" claim rather than leaving it to a reader. The
same check covers the study guide's worked special-case example. Only the
*dependent* systems are left for review, and only for the half a machine cannot
settle: worksheet problem 10 and its study-guide try-it return MANUAL because an
infinite solution family cannot be counted, while the representative pair each
one prints, $(2, 2)$, **is** machine-checked against both equations. So the build
exits 2 with exactly two flagged items — the honest count — and every other
answer on all three documents, 11 on the worksheet and 7 in the study guide, is
verified.
