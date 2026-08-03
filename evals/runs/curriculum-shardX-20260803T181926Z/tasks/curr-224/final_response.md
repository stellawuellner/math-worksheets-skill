Three PDFs are ready for a Grade 8 / pre-algebra student on linear
representations and equations, focused on diagnosing confusion between slope and
$y$-intercept.

- **Worksheet** (8 problems, `ws_slopeint_curr224.pdf`, 4 pages) — seven of the
  eight problems are find-and-fix items, and every one of them turns on the same
  confusion seen from a different representation. Equation: Lin reads
  $y = 3x + 5$ as slope 5 / intercept 3 and gets 23 instead of 17; Rae assumes
  the *first* number in $y = 12 - 2x$ is the slope and gets 58 instead of 2.
  Two points: Dev computes $\Delta x / \Delta y$ and gets $\frac{1}{2}$ instead of
  2 — and the key points out that an inverted slope is always the reciprocal of
  the right one, which is a one-line self-check. Table: Sofia calls 13 the rate
  of change when the real step is 4, then calls the same 13 the $y$-intercept
  when the table starts at $x = 1$ and the intercept (9) is one step off the left
  edge. Equation from a point: Owen writes $y = 4x + 20$ from the point $(3, 20)$,
  and testing his own equation at $x = 3$ gives 32, not 20 — the correct
  intercept is 8. The synthesis problem is a draining pool measured at 2 min /
  46 gal and 8 min / 22 gal, where a student reports both an inverted rate
  ($-0.25$ instead of $-4$ gal/min) and a reading-as-starting-value (46 instead
  of 54); the key names these as the same mistake made twice. Problem 8 is an open
  explanation. Work space runs 5–7.5 cm per problem.
- **Answer key** (`ak_slopeint_curr224.pdf`, 4 pages) — three to five numbered
  steps per problem: name the slip in words, redo the work, box the answer, then
  run an *independent* check — the $x = 0$ test, a direction check (a falling line
  cannot exceed its own starting value), walking the line four steps to confirm a
  slope, rebuilding $y = 4x + 9$ and testing it against both ends of the table,
  and substituting the second pool reading into the recovered equation. It
  carries the generated quick-answer bank and the generated "Common wrong
  answers" block (23, 58, 0.5, 13, 13, 20, $-0.25$, 46), plus a model answer and
  a full-credit checklist for the open item.
- **Study guide** (2 pages, `ss_slopeint_curr224.pdf`) — three skills matching
  the worksheet tags: read the roles rather than the order (with the $x = 0$
  test), slope from two points with $y$ on top (and the reciprocal check for an
  inverted slope), and the intercept a table does not show (step back from the
  first row by the step size). Each has a rule box, a two-step worked example and
  an upside-down try-it, plus a watch-out box on the diagnostic that an equation
  failing its own point means a coordinate was used as an intercept.

**Verification.** 7 of the 8 worksheet problems are machine-checked with SymPy:
four `eval` checks (evaluating $mx + b$ both ways round, backing a table up to
$x = 0$, and recovering $b = y - mx$), two `slope` checks from coordinate pairs,
a `read_data` `difference` query that reads the step size straight out of the
same table printed on the worksheet, and a `solve` of $4(3) + b = 20$. Problems 6
and 7 each carry two entries under one id, so both halves of those two-part items
are bound. All 6 study-guide results are machine-checked. Problem 8 is a
genuinely open explanation and is declared `{"type": "manual"}`; the build exits 2
with one manual-review item, and it is nowhere described as machine-verified.

Eight planted wrong results are declared misconception traps (23, 58, 0.5, 13,
13, 20, $-0.25$, 46). The verifier proved each one distinguishably wrong and
derived from the stated wrong method rather than typed by hand.

**Standards.** Equation and slope problems are tagged `8.EE.B.5, 8.EE.B.6`
("Linear equations & slope") and the table/function-interpretation problems
`8.F.A / 8.F.B` ("Functions (gr 8)"), both copied verbatim from
`references/standards-map.md`. Together they cover the task's `8.EE.B.6 / 8.F.B.4`
reference; no code was invented.

**Gate-log note.** Worksheet prose matched 30 of 32 numbers; the two flags are
the "1" naming the fraction $\frac{1}{2}$ in Dev's wrong line and the "0" in
"$0$ minutes" in the pool problem — both are prose about the setup rather than
computation givens. Study-guide flags are intermediate values inside worked
examples (18, 12) and references to $x = 0$ and $x = 1$. The table printed on the
worksheet is the same `data` object the `read_data` check reads, so the figure
and the check cannot disagree. The grade level appears only on the answer key.
