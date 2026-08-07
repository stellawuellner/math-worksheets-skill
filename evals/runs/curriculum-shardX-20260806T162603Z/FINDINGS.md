# System findings reported by run-2 generation agents

DELIBERATELY NOT FIXED DURING THE RUN. Changing verify.py, SKILL.md or a gate
mid-run would mean tasks built before and after the change faced different
systems, which contaminates the paired comparison this run exists to produce.
These are queued for the iteration after the run is scored.

## R04 (curr-200..212)

1. **`read_data` query `difference` needs `key` as a 2-element list; nothing
   says so.** TESTED. `{"query":"difference","key":"Wed"}` yields
   `too many values to unpack (expected 2)` — a Python message naming neither
   the field nor the requirement, attributed to the problem rather than the
   field. Confirmed at `scripts/verify.py:1768` (`a, b = p["key"]`), and
   confirmed passing with `"key": ["Fri","Thu"]`.
   FIX: state the pair form in SKILL.md's `read_data` row; raise
   VerifyInputError naming `key` when it is not a 2-list. Every other misuse
   path in the schema teaches its fix; this one does not.

2. **`equiv` cannot carry `traps`, which blocks machine-checked error analysis
   on any symbolic answer.** TESTED. curr-206 problem 10 is a find-the-error
   item on `x^4 · x^3 = x^12`; the correct answer is symbolic so `equiv` is the
   only faithful type, and traps are refused there. Knock-on: the planted wrong
   result is then not a JSON given either, so check_prose_consistency flags the
   printed `12` as "missing from JSON" on an otherwise correct sheet.
   FIX: give `equiv` the list-shaped trap form solution-set types already have
   (`"exprs": ["x**12"]`, distinguishable when not equivalent to `expected`).
   The agent did NOT work around it — the item kept its ask and declared no
   trap, which is the correct behaviour under the brief.

3. **Shared data displays have no documented home.** A bar chart inside a
   problem is a valued figure beside figureless problems, which check_layout
   fails; the rule's own remedy (a value-free reference figure) cannot apply,
   because a data display IS its values. What works: place it before the first
   `\problem` so it belongs to no region, captioned with the problem numbers
   that use it. Pedagogically good, but named nowhere — an author who does not
   know it will delete the chart or fight the gate.
   FIX: document the pattern in SKILL.md / latex-templates.md.

4. **Minor: `\begin{itemize}[leftmargin=1.1cm]` leaks its bracketed dimensions
   into the prose scan** (curr-202 reported phantom 1.1 and 2.0).
   `_prose_stripped` strips braced dimensions but not list options in `[...]`.
   Same class as the `\rule`/`minipage` leaks already fixed there. Advisory
   checker, low severity.

## Fixed DURING the run (presentation only — see the note below)

Four defects reported by R01/R02/R03/R08/R09/R11 were fixed mid-run rather than
queued, because each was actively degrading artifacts or blocking correct work,
and none changes what verification passes or fails. The measured dimensions
(slot coverage, bank correctness, manual fraction) are unaffected; only how the
key reads and whether LaTeX can set it. Tasks recorded before the fixes differ
from later ones in these presentational respects, and that is stated here rather
than smoothed over.

1. **Unit fractions printed as `1 · 1/n`.** Reported independently by three
   batches. `parse_expr(evaluate=False)` builds `Mul(1, Pow(4,-1))` for "1/4"
   and latex printed the redundant factor; every numerator-1 fraction was
   affected and nothing else. This SHIPPED into delivered banks (curr-081 had 6
   of 8 rows malformed, curr-327 two slope rows). Agents correctly refused to
   dodge it by rewriting the mathematics. Fixed by dropping unit factors after
   parsing; form preservation re-verified (9/12 unreduced, mixed numbers mixed,
   factored products factored).
2. **"What is verified" counted problems, not answers.** A find-and-fix sheet —
   correction plus diagnosis on every item — has zero fully-machine-checked
   PROBLEMS, so curr-269 printed "0 of 8" with eleven passing SymPy checks
   behind it. That is the original defect inverted: it understates verification
   and a parent reads it as "nothing was checked". Now "11 of 19 answers
   machine-checked, across 8 problems".
3. **Quick Answers bank could overfull and fail compile-ak.** A `\\`-terminated
   row in multicols has no break point, so a long symbolic answer beside a
   descriptive `slot` label overflowed. Both author levers were bad — shorten
   the label (against the guidance) or change the mathematics — and one agent
   shortened "(a) fully factored form" to "(a)" for a green build. Rows now wrap
   (`\raggedright\sloppy`).
4. **Stale-rubric lint false-fired on the word "Rubric".** `_DESC_STOP` lacked
   the single most natural word to open a rubric with — and the word SKILL.md
   itself uses for what a desc IS. It hard-failed a correct sheet. Stop list
   extended with grading vocabulary; the real Priya defect still fires.
5. **`values_pinned` credited `system` with 1 slot.** Its `expected` is a dict,
   so the list-length test never fired and its membership in the multi-slot set
   was dead code; a two-variable system printing two blanks was flagged.

## Still queued (would change what passes — deliberately NOT touched mid-run)

- `page_budget.py` reads `workspace_cm` only off the FIRST entry of a
  multi-entry id, while the advisory pass in the same file merges across
  entries — the two halves disagree, and the gate tells you to declare a field
  you already declared. TESTED with a controlled probe (R03).
- `page_budget.py`'s two-column halving keys off the TYPE DEFAULT workspace,
  not the effective per-problem value, so sheets of `compare`/`estimate`
  problems get halved even when every problem declares a large `workspace_cm`.
  TESTED by flipping one type field (R00).
- `equiv` cannot carry traps, blocking machine-checked error analysis on any
  symbolic answer (R04).
- `read_data` `difference` needs a 2-list `key`; the error is a Python
  unpack message (R04).
- `eval` with a float base vs a decimal `expected` fails on Float/Rational
  exactness (R08).
- Solution-set trap field shapes (`exprs` strings, list `value`) are absent
  from `--schema` (R10).
- The bank collapses several `manual` entries of one id into ONE trailing
  `---` and drops their `slot` labels, so a grader cannot see which parts are
  unscored (R11).
- `run_eval.py record` degrades quietly on a stem collision: writes a
  `result.json` with no artifacts and still prints a success line. Three agents
  hit it from stale `/tmp/evalbuild2` dirs and self-corrected. Audited: all
  recorded tasks have complete artifacts.
- Traps on fraction-valued answers can never reach the "Common wrong answers"
  block (`value` must be numeric), so a whole error-analysis sheet emitted none
  (R03).
- `right_triangle` figures at extreme aspect ratios cluster their labels;
  check_overprint misses it (R11).
