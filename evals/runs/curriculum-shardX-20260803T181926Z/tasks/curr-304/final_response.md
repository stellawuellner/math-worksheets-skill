# Proof logic — circular reasoning and unsupported statements (Geometry)

Three PDFs are ready:

- **Worksheet** (`ws_prooflogic_curr304.pdf`, 5 pages) — 6 problems, all on
  diagnosing a bad justification: (1) find the circular step in a student proof of the
  Vertical Angles Theorem, (2) choose which of three offered reasons actually supports
  a statement (one is circular, one assumes a missing given), (3)–(5) three
  find-the-mistake items where a wrong reason produces a wrong number, and (6) explain
  the loop in an isosceles-triangle argument and rewrite it correctly.
- **Answer key** (`ak_prooflogic_curr304.pdf`, 3 pages) — every solution names the
  faulty reason, says *why* it is unavailable, and then works the algebra with a
  check against the givens. It includes a model two-column repair for problem 6, a
  quick-answer bank, a generated Curriculum section (HSG-CO.A–HSG-CO.D,
  difficulty 2–5), and a "common wrong answers" line for each declared trap.
- **Study guide** (`ss_prooflogic_curr304.pdf`, 2 pages) — three sections: how to
  test a reason for circularity, what each given actually entitles you to write
  (linear pair vs. vertical vs. corresponding angles), and segment addition vs. the
  stronger midpoint given. Each has a rule box, a worked example that opens by naming
  the strategy, and a separate try-it.

**Find-and-fix items (3, more than the two requested).** Problems 3, 4 and 5 each
print the student's planted wrong result — 70°, AM = 13, and 38° — and each of those
numbers is declared as a machine-checked misconception trap. SymPy confirmed that
each is exactly what the unsupported reason computes and that the problem's own check
rejects it, so the sheet demonstrably distinguishes the error it targets.

**What was verified, and what is flagged.** All 6 numeric checks (x and the requested
measure in problems 3, 4 and 5) were recomputed by SymPy and passed. Problems 1, 2
and 6 are labelled **manual review**: naming a circular step, choosing among reasons,
and writing a corrected proof are arguments, not calculations, and no CAS can grade
them. The answer key gives a full model answer for each plus a bracketed note on
what earns credit. Two of the study guide's six boxes are manual for the same reason
(the circular-reasoning example and its try-it). Layout, work space, answer blanks
with units, page budget, and the binding of every boxed answer to its verified value
all passed the build gates.
