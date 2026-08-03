# Systems of Two Linear Equations: Intersections as Solutions (Grade 8 / Pre-Algebra)

- **Worksheet** (`ws_systems_curr226.pdf`) — 10 problems, every one about what an
  intersection point *is*. The sheet opens with a small labelled graph of two lines
  crossing at (2, 3), captioned so it reads as a shared convention rather than any
  problem's data, and states the definition the whole sheet turns on: the crossing
  point is the one (x, y) that makes both equations true. Then: 3 test-the-point
  problems (including one where a claimed point satisfies only one equation),
  3 read-the-intersection-from-a-table problems, and 4 solve-and-interpret problems
  (equal expressions, a break-even story, a substitution system, and a build-your-own).
  5–7 cm of work space per problem, no problem outside the focus.
- **Answer key** (`ak_systems_curr226.pdf`) — full worked reasoning. Every algebraic
  solution ends by substituting back into *both* original equations, because that
  check is the concept being taught. Problems 8 and 10 carry model answers plus
  explicit grading notes (what to look for; how to grade a student's own system).
  A generated quick-answer bank sits under the title block.
- **Study guide** (`ss_systems_curr226.pdf`) — 2 pages, three sections matching the
  three worksheet skills: test a point · read an intersection from a graph or table ·
  solve for the intersection. Each has a rule box, a two-step worked example, and a
  distinct try-it with the answer upside down; a watch-out box covers the two
  standard errors (satisfying only one equation, and stopping at x).

## Verification

8 of 10 worksheet problems are machine-verified with SymPy's `system` check, which
confirms the printed point satisfies **both** equations *and* that it is the complete
solution set. All 6 study-guide answers are verified the same way.

**Two problems are flagged `manual`, correctly and deliberately:**

- Problem 8 asks the student to explain from a table of values and from the slopes
  why two parallel lines never meet. There is no value to compute — the answer is an
  argument, so it is encoded `{"type": "manual", ...}` and the key carries a model
  answer with a look-for list.
- Problem 10 asks the student to invent their own system with solution (4, −1).
  Infinitely many correct answers exist, so no single expected value can be checked;
  the key gives one valid system and tells the grader how to check the student's.

The build therefore ends at exit 2 (green with manual-review items), which is the
right outcome for open reasoning — not a gate failure. All other gates green on the
first attempt.

Standard `8.EE.C.8` is taken from `references/standards-map.md` (the row explicitly
covering systems, with graphical/algebraic/word-problem sub-codes). Facet plan
(`check-solution`, `intersection-from-graph`, `solve-and-interpret`) is declared, every
problem tagged, the subtitle bound to it, and each facet has its own study-guide
worked example. Difficulty ramps 1, 1, 2, 2, 2, 3, 3, 3, 4, 4.

Gate-log note: the worksheet prose report reads 64%. The flagged numbers are the
entries of the three tables of values printed inside problems 3, 4 and 8. Those are
outputs computed from the problems' own equations rather than givens, which is exactly
the derived-value false-flag class the report documents; each was recomputed by hand
against its line equation.
