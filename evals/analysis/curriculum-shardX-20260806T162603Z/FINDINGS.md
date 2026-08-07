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

## Later batches (R00–R11 complete)

Fixed mid-run (advisory only, cannot change any pass/fail):
- **enumitem option lengths leaked into the prose scan.** Reported by THREE
  batches independently. `\begin{itemize}[leftmargin=1.1cm, itemsep=2pt]` inside
  a stem put 1.1 and 2.0 into the "missing from JSON" list; on one sheet this
  alone moved the reported match rate 73.5%→90.0%, on another 56.4%→100%.
  check_prose_consistency exits 2 only on structural faults, never on a number
  mismatch, so stripping key=length option pairs changes no verdict — it only
  stops the checker crying wolf on standard list formatting. Bare bracket
  labels (`\item[3]`) still count, because the student reads that 3.

Queued — each WOULD change what passes, so untouched mid-run:
- **`eval` compares exactly, so ordinary decimal models fail intermittently.**
  Reported independently by R07 and R08. `9.4 - 0.4*x` at x=20 evaluates to
  1.4000000000000004 against an `expected: 1.4` parsed as exactly 7/5;
  `200*1.2**t` at t=3 likewise. Passes or fails depending on which value lands
  on a representable binary float — the worst possible shape to debug — and the
  message ("expected 7/5") points at the JSON rather than the arithmetic.
  `eval` accepts no `tol` and has no rounds-to fallback, while `approx` has
  both. CONSEQUENCE ALREADY VISIBLE IN THIS RUN: one agent re-chose a trend
  line from 9.4−0.4x to 9.5−0.5x purely because halves are exact in binary.
  That is problem design bent by a tool defect. Highest-priority queued item.
- `system` cannot express "infinitely many solutions": the MANUAL path makes
  check_answer_key demand a listed value in the box while the correct printed
  answer is "infinitely many", so two gates want different things (R07).
- Shared display panels above problem 1 are invisible to the page budget, and
  `workspace_cm` REPLACES the type default rather than adding to it, so
  charging a shared panel means recomputing every problem by hand (R07).
- `check_layout` reports `\vspace` inside a `\problem` stem as "outside any
  minipage" — `minipage_depth_fn` counts literal `\begin{minipage}` and
  `\problem`'s is in the preamble. Wrong diagnosis on the sheet shape SKILL.md
  teaches first; the offered fix (star the glue) does work (R06).
- `\skillheading`'s 57-char failure does not name WHICH heading overflowed
  (R06).
- Solution-set trap `value` must be a list, and SKILL.md's traps section shows
  only the scalar form (R06, R10).

## R05 — a gate that hard-fails correct work on JSON shape alone

**`check_answer_key.py:459` misses symbolic answers wrapped in a list.**
CONFIRMED at source by me, not just reported:

    symbolic = any(isinstance(e.get("expected"), str) and ... for e in entries)

    bare string   "18 - 3*x/2"    -> symbolic True
    1-elem list  ["18 - 3*x/2"]   -> symbolic False   <- same mathematics

`verify.py` accepts both forms identically, and `--schema` shows the LIST form
for `solve`. When `symbolic` stays False the magnitude-matching branch never
runs, so a key boxing `y = -3/2 x + 18` tokenises to {-1.5, 18} against JSON
numbers {18, 3, 2} — eight binding failures across four problems on curr-223,
every one reported as "the boxed value is wrong", pointing the author at a
correct answer key. Unwrapping the list fixed all eight with ZERO change to the
key. Fix: walk the `expected` structure the way `json_expected_nums` already
does.

Queued, not fixed: it changes gate results, which is a measured dimension of
the comparison. Note the class though — this is a FALSE FAILURE, and its cost
is the same as the `eval` exactness bug: an author changed the artifact to
satisfy a tool defect rather than a mathematical need.

**Shared figure banks above problem 1 are verified by nobody.** Four sheets
printed a fully labelled coordinate grid with plotted data while the layout
gate said "none of the N problems carries a valued figure" — `problem_regions`
starts at the first `\problem`, and `figure_label_numbers` never sees the bank.
A drifted tick or mis-plotted point on a shared graph is invisible to the whole
chain, and the rule mildly rewards hoisting figures out of problems to quiet
the scope check. This is the same undocumented pattern R02/R04/R06/R07 each
arrived at independently — it is now the standard answer to mixed-representation
sheets, and nothing checks it.

## R12 — the `equiv` cluster (three findings, one root)

An `equiv` answer is a whole EXPRESSION written as `lhs - rhs`, and three
separate parts of the system present it as if it were a value:

- **check_answer_key's message.** `expected: "(x-4)**2 + (y+1)**2 - 25"` boxed
  as `\ans{25}` produced three faults reading "verified value 1 … 2 … 4 is in
  the worked steps but NOT in the box — the boxed value is wrong". The boxed
  value was not wrong; the rule is that an `equiv` answer is the entire
  rewritten form, so every literal must appear in one box. The author hunts a
  numeric error that does not exist. Naming the type ("this entry's answer is
  an expression — box the whole rewritten form") would end it in one read.
- **The Quick Answers bank** then prints that same entry as
  `(x − 3)² + (y + 5)² − 16` on a sheet that asked for centre-radius form, so a
  grader scanning the bank sees a subtraction where the student wrote an
  equation. Faithful to the JSON, consistent with form preservation, and still
  misleading at a glance. An `equiv` row could render `lhs = rhs`.
- **And `equiv` cannot carry traps at all** (R04), so error analysis on any
  symbolic answer is unreachable.

Together these make `equiv` the least well-served type in the system despite
being the correct choice for every "rewrite in this form" task. Queued as one
piece of work rather than three.

## R12 — other

- Solution-set trap `value` must be a list; `--schema` says only "that set as
  printed", which reads as a scalar. Third independent report (R06, R10, R12).
- NEAR MISS, cause not confirmed: a `tangent` label ~0.4 cm from a `$Q$` vertex
  label extracted as `Qtangent` while check_overprint passed. The agent moved
  the label rather than confirm whether it was a real collision, and said so.
  Same class as the KNOWN-OPEN SSA note.
- INFERRED (not observed): `check_layout`'s work-space floor counts glue only,
  so a problem whose height comes from an 8 cm tikzpicture needs an artificial
  `\problem[Ncm]` that adds blank space the problem does not need.

## R16 — `eval` exactness, THIRD independent report

`{"type":"eval","expr":"sqrt(d/4.9)","at":{"d":78.4},"expected":4}` — 78.4/4.9
is EXACTLY 16 and the answer is exactly 4 — reported as
`→ 1.26491106406735*sqrt(10) (expected 4)`. The agent rewrote the free-fall
model from 4.9t² to 5t² to get a green build.

That is three independent reports (R07, R08, R16) and three separate occasions
where an author changed correct mathematics to satisfy a float-comparison
defect. Together with the trend line (9.4−0.4x → 9.5−0.5x) and the JSON-shape
workaround in R05, this run has produced FIVE documented instances of an
artifact bent to fit a tool. That is the single strongest finding of the run and
the first item for the post-run iteration.

Fixed mid-run (render level only, cannot change any verdict):
- A literal `(-1)` coefficient could survive `evaluate=False` nested inside a
  product: `-x**2/2` printed `\frac{\left(-1\right) x^{2}}{2}`. Normalised at
  the RENDER level rather than in the tree — a deeper tree pass reorders or
  distributes, which would break the form preservation the function exists for.
  Now `\frac{- x^{2}}{2}`; 9/12 still unreduced, factored products still
  factored.

Queued from R16:
- The study-guide unit rule is met for the first time as an answer-key BINDING
  failure two gates later, because `check_answer_line.py` (whose message
  teaches the answer_unit contract) runs only on the worksheet.
- `--schema` says solution-set traps take "the roots the wrong method yields",
  which reads as numeric; `[5, -2]` is rejected, `["5", "-2"]` accepted. Fourth
  independent report of the trap-shape doc gap.

## R14 — a SILENT-PASS hole in the slot gate itself (fixed immediately)

`SUBPART_RE`'s character class omitted `[`, so the marker in `\item[(a)]` — the
form **AUTHORING.md itself prescribes** — did not match. `subparts_in` returned
0 for `\item[(a)] … \item[(b)]` and 2 for the same problem written
`\textbf{(a)} … \textbf{(b)}`. A sheet following the brief's own guidance
silently lost the lettered-sub-part half of the gate, and the failure direction
is a PASS.

Exposure measured before deciding: **133 of 300** run-2 worksheets use
`\item[(a)]`. The gate was blind on 44% of the corpus it was being used to
score.

FIXED MID-RUN, and the reasoning differs from every other entry above. This is
a defect in the MEASURING INSTRUMENT, not in the generator. Scoring happens
after generation, so a corrected gate applies uniformly to all 300 tasks in both
runs and cannot advantage early tasks over late ones. Leaving it would have made
the run's headline number partly unearned.

RE-MEASURED, same corrected gate, both runs:
    run 2 (new system): 291 clean / 0 flagged
    run 1 (old system):  99 clean / 201 flagged

Run 2 is clean even under the corrected gate, which is a STRONGER result than
the original number: those 133 sheets were built while the gate was blind to
their sub-parts, so the per-response entries were declared because the CONTRACT
asked for them, not because a gate forced them. The written guidance did the
work on its own.

Also from R14, queued: `solve` compares float-coefficient roots exactly
(`sqrt(9.8*d) - 70` → 499.999999999999 rejected against 500) with no `tol`
available — the same class as the `eval` defect and a fourth forced content
change; and the trap-shape doc gap, now a fifth independent report.

## SYNTHESIS — symbolic and complex answers are second-class throughout

Six batches reported what look like six unrelated defects. They are one theme:
every mechanism the system added for TEACHING quality works on scalars and
degrades or vanishes on symbolic, list-valued or complex answers.

- **Traps are unreachable** on `equiv`, `expand`, `factor` (R04, R13) — so
  polynomial arithmetic, long division and factoring sheets ship with NO
  "Common wrong answers" block, though their classic errors (undistributed
  subtraction, dropped placeholder, candidate list without fractions) are as
  mechanical as the trigonometry ones that do get traps.
- **Trap `value` cannot be complex** (R13): four of seven planted results on a
  complex-arithmetic error-analysis sheet could not be declared, so the printed
  wrong number is hand-typed — the exact drift the field exists to prevent.
- **Trap `value` must be a list on solution-set types**, undocumented in
  `--schema` (five independent reports: R06, R10, R12, R14, R16).
- **`check_answer_key` treats a list-valued `expected` as non-symbolic**
  (R05, R13), so magnitude matching never runs and a correct key fails with
  "the boxed value is wrong". R13 adds that `\pm 7i` is unreadable to the
  binder while `7i \text{ or } -7i` passes — the JSON side loses the sign and
  the printed side must carry it.
- **`equiv` is misreported by three separate components** (R12).
- **Float-coefficient answers fail exact comparison** on `eval` (R07, R08, R16)
  and `solve` (R14), with no `tol` escape on either.

CONSEQUENCE, stated plainly: the system is most trustworthy on elementary
arithmetic and least trustworthy exactly where the mathematics gets symbolic —
Algebra 2 upward. That is the inverse of where a parent needs the most help,
and it is invisible in any per-case review because each instance looks like a
small local annoyance.

This is the run's most valuable output. No single case could have shown it; it
took 300 sheets across ten bands, and the pattern is the argument for
prioritising the queued numeric/symbolic work as ONE project rather than eight
tickets.

## Lint false positives in MY OWN new gates (narrowed, measured)

Three batches hit false positives in the two lints shipped this week, and in
every case the author fixed correct work to clear the gate — the exact harm the
lints exist to prevent.

- **Eponym false positive** (R15, R21 ×2). "Pascal's triangle", "the
  Pythagorean form", "the Lagrange bound" read as leftover NAMES. The original
  exemption checked whether a neighbouring token was capitalised, so
  "Fundamental Theorem" passed and "the Lagrange form" did not — the exemption
  was decided by typography. One author rewrote a correct rubric into worse
  prose; another added a sentence to a stem purely to satisfy it (that one was
  an improvement, but it was not the author's choice to make).
  NARROWED: a capitalised word followed by a mathematical noun is vocabulary.
- **Open-ask false positive** (R19). "the two methods **describe** the same
  tangent line" is a declarative statement ABOUT the mathematics; nothing is
  asked, so a manual entry would have been a rubric for a non-question. The
  verb now has to sit in IMPERATIVE POSITION — segment start, after sentence
  punctuation, after `\item`, `}`, `and`, `then` or a comma.

Measured across BOTH runs (600 sheets) after narrowing:
    stale-desc lint: 1 fire  (the real Priya defect in run 1, still caught)
    open-ask lint:   run 1 — 343 gaps in 158 cases
                     run 2 — 0

## PAIRED RESULT (all figures under identical, current gate versions)

                              run 1 (old)      run 2 (new)
    slot-gate clean            99 / 300         291 / 291
    open-ask gaps             343 in 158 cases  0
    stale rubrics               1                0

## Post-run fix wave — queued items surfaced by the fixes themselves

**Page budget (FIXED, committed).** See the commit for the measurement. Three
things the fix surfaced that are NOT fixed:

1. **The two-column inference is guessing a layout the JSON cannot see.** After
   the fix the halving fires on 0 of 600 corpus sheets, and not one worksheet in
   the corpus uses `multicols` at all. It is correctly gated now, but a future
   all-`compare` sheet with no declarations would still be halved with no
   `multicols` anywhere. The real fix keys it on a `multicols` signal read from
   the .tex, which needs a `budget()` signature change and a build.sh edit.

2. **The residual −1 under-measurement (293 sheets) is the stem-picture gap**,
   not these bugs: `\problem[3.5cm]` blocks whose stems hold an `itemize` plus a
   tikzpicture number line, all charged the flat 0.6cm stem rate. The old
   first-entry bug was ACCIDENTALLY COMPENSATING for it (an `inequality`
   default of 8.0cm), so removing the bug makes the real gap visible. The
   `unpriced` advisory already names this class but stays silent whenever
   `workspace_cm` is declared at all — so it never fires on exactly these sheets.

3. **NEW, and a data-integrity class nobody had found:** curr-300's worksheet
   uses bare `\problem{...}` with no bracket, and `\problem`'s optional argument
   defaults to `0pt` — so its JSON `workspace_cm` declarations describe space
   the document never reserves. Nothing cross-checks the JSON's declared
   workspace against the .tex's actual `\problem[...]` argument. That is the
   same shape as every other drift this project has chased: two files asserting
   different things with no gate between them.
