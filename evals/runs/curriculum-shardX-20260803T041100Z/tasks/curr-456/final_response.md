# Interpreting the derivative as a limit and an instantaneous rate (AP Calculus AB/BC)

Three PDFs, all gated:

- **Worksheet** `ws_derivative_limit_curr456.pdf` — 8 guided concept-practice
  problems, 4 pages. The models are numerical rather than pictorial, which is
  the right model for this topic: **shrinking-window tables** of difference
  quotients and average velocities (problems 1 and 2) make the limit visible as
  a column closing on a value, and a **three-point data table** (problem 7)
  forces the estimate when no formula exists. Each problem gets 4.5–6 cm of
  work space; the rate problems carry unit-bearing answer lines.
- **Answer key** `ak_derivative_limit_curr456.pdf` — quick-answer bank plus a
  full solution that shows the difference quotient simplified *before* the
  limit is taken (resolving the $0/0$ rather than evaluating it), the filled
  table values, and what each number measures with its units.
- **Study guide** `ss_derivative_limit_curr456.pdf` — 2 pages, four skill
  sections (limit definition at a point · average rate to instantaneous ·
  reading a derivative as a rate · spotting a limit that *is* a derivative),
  each with a rule box, a strategy-first worked example, and a distinct try-it.

## Verification

- Worksheet JSON: **7 of 8 machine-verified, 1 manual.** Four `limit` checks
  (each on the literal difference quotient, so the CAS confirms the definition
  and not a shortcut), one `diff`, two `eval` — the task's `diff`/`limit`/`eval`
  targets.
- **Problem 8 is `manual` by design and the build exits 2 saying so.** It asks
  the student to prove from the definition that a linear function has one
  instantaneous rate everywhere, and to derive the units of $V'(t)$ from the
  difference quotient. That is open reasoning; no CAS can check it, so it is
  encoded as `{"type": "manual", ...}` rather than dressed up as verified. The
  key still prints a full model response plus a short "what to look for when
  grading" note.
- Study-guide JSON: **8 of 8 machine-verified** (4 examples + 4 try-its).
- **3 traps declared, all confirmed distinguishable**: reporting the average
  rate over $[2,3]$ (7) instead of the limiting velocity (6); evaluating $V$
  instead of $V'$ at $t = 5$ (20 gallons instead of 24 gallons per minute — the
  units are the tell); and subtracting the two distances without dividing by
  the 2-second window (12 instead of 6). All three are the standard
  average-vs-instantaneous confusions and print in the key's "common wrong
  answers" block.
- Three `answer_unit` declarations bound in both directions
  (`meters per second`, `gallons per minute`).
- Difficulty ramp `[1, 2, 2, 3, 3, 3, 4, 4]`; standard `FUN-3.A–FUN-3.C`
  verbatim from `references/standards-map.md`.

`BUILD PASSED` on the first attempt, with exit 2 for the one manual-review
item — the correct outcome for an explanation problem, not a defect. Residual
prose flags are worked intermediate values (35 m in the one-sided-window
comparison, the $12/2$ inside the study-guide example), the expected false-flag
class.
