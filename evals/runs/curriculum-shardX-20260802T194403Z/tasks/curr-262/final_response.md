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

**Verification.** 10 of the 12 worksheet systems are fully machine-checked with
SymPy — each listed solution satisfies both equations *and* matches SymPy's
complete solution set. The two special cases are correctly **not** claimed as
verified: problem 9 (no solution) is declared `manual`, and problem 10 returns
MANUAL from the verifier because an infinite solution family cannot be counted —
its printed representative $(2, 2)$ was checked against both equations. In the
study guide, 6 of 8 results are machine-verified; the two special-case boxes
(example and its paired try-it) are `manual` by the same rule. The build passed
with exit 2, which is the correct outcome when genuine manual-review items exist.
