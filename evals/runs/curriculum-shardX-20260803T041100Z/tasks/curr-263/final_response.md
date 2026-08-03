# Solving Systems by Elimination with Scaling — Algebra 1

Three PDFs were generated. The build is green; it exits 2 because one part of
one problem is an explanation, which is correctly encoded as manual review.

- **Worksheet** (`ws_elimination_scaling_curr263.pdf`) — 10 problems. The sheet
  opens with a value-free "elimination organizer" table (target · scale ·
  combine · back-substitute · check) that the student reuses on every problem.
  Five problems are realistic applications with the system already modelled from
  the situation (school store, theater tickets, bakery sales, a canoe in a
  current, a salt mixture), five are algebraic practice, and every one of the
  ten requires scaling before anything cancels — four scale a single equation,
  two scale both to an LCM, and four come from a context. Difficulty ramps 2 → 5.
- **Answer key** (`ak_elimination_scaling_curr263.pdf`) — each solution names the
  target variable and says *why* it is the cheaper one to eliminate, shows the
  multiplier applied to every term of the scaled equation, then back-substitutes
  and checks the pair in the *other* original equation. Application answers are
  translated back into the words and units of the story. The generated
  quick-answer bank sits under the title block.
- **Study guide** (`ss_elimination_scaling_curr263.pdf`) — 2 pages, three
  sections (scale one equation · scale both equations · build the system from a
  situation), each with a rule box, a worked example whose first step chooses the
  variable to eliminate, and a distinct try-it with the answer inverted inside
  the box, plus a watch-out box on the multiply-both-sides error.

## Verification

Ten `system` checks are machine-verified by SymPy: each listed solution is
substituted into every equation and the solution count is matched against
SymPy's full solution set, so a partial or extra solution would fail.

**One item is flagged manual and should stay that way:** problem 9(a) asks the
student to explain why multiplying only the left side of an equation breaks the
system while multiplying every term does not. That is a justification, not a
computation, so it is encoded as `{"type": "manual", ...}`. Problem 9(b) — the
corrected scaling and the resulting solution (6, 2) — is machine-verified, so
the error-analysis problem is half verified, half reviewed, which is the honest
split. The answer key prints a model answer and the credit criterion for the
explanation.

The study guide's six boxes (three examples, three try-its) are separately
verified as `system` checks.

Standard `HSA-REI.C.6` (from `references/standards-map.md`, row "Systems
(linear/quadratic)") is tagged on all entries. Every problem declares
`workspace_cm` (8–9 cm) because a scaled elimination plus a check needs more
room than the default.

## Notes for the reviewer

One gate failed on the first attempt and was fixed: the study guide's third
worked example overflowed the line by 9pt because a long `\step` ended with an
inline `\ans{}`; moving the boxed answer onto its own line cleared it. The
prose-checker flags on the study guide are intermediate arithmetic values
(scaled coefficients such as 62 and 46) that appear in the worked steps but not
as JSON givens — expected false flags.
