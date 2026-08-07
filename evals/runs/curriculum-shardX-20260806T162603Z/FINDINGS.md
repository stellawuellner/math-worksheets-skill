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
