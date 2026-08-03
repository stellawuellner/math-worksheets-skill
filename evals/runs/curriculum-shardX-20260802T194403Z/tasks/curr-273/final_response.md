# Writing Recursive Arithmetic Sequence Formulas (Algebra 1)

Three PDFs are ready for an Algebra 1 student on arithmetic sequences as linear
functions, focused on writing recursive formulas. Every problem asks for both
lines of the rule — the first term and the step — and then a number the rule
produces, so the formula is the work and the number is what the gate can check.

- **Worksheet (7 pages, 10 problems).** The representations rotate: two listed
  sequences (a tiling pattern, and a descending drone altitude with a negative
  common difference); three applications with units and givens stated (a stack of
  chairs in centimeters, a draining tank in liters, a gym membership in dollars);
  two given recursive rules to run forward and backward (one solved as an
  equation in $n$, not by listing terms); a recursive-to-explicit conversion that
  names the slope and the intercept; a table with $a_3$ and $a_7$ known and $a_1$
  missing; and a synthesis on theater rows that ends in the sum of the first 15
  rows. Work space is 8–9.5 cm per problem, **declared as `workspace_cm` in the
  JSON** so the page budget charges for the two-line rule plus the computation
  each problem actually asks for. That is why the sheet is seven pages: the room
  is the content, not slack.
- **Answer key (3 pages).** Three labelled steps per problem — find $d$, write
  both lines, count the $n-1$ applications and compute — plus the generated
  quick-answer bank and a **"Common wrong answers"** block covering the six
  declared traps.
- **Study guide (2 pages).** Four skills matching the worksheet's four facets:
  the rule from a listed sequence, the rule from a situation, running a rule
  forward, and converting a recursive rule to an explicit linear function. Each
  has a rule box, a two-step worked example whose first step names the decision,
  and an upside-down try-it, plus a watch-out on writing the step line without
  its first line.

## Verification

All 10 worksheet problems are machine-checked with SymPy — 11 checks, because
the missing-first-term table problem carries two verified answers (the common
difference and $a_1$) under one problem id. The mix is 8 `eval` term
computations, 1 `solve` "which term" equation, and 1 `series` partial sum of 15
rows. All 8 study-guide boxes (4 worked examples + 4 try-its) are verified the
same way. **Nothing is flagged manual** and no tolerance was widened.

**Six misconception traps are declared and machine-checked**: adding a negative
common difference (104), multiplying by $n$ instead of $n-1$ in two different
contexts (190 and 97), starting the tank count an hour late (135), dropping the
joining fee from the explicit rule (840), and treating every theater row as row 1
(270). Verification proves each is a value the problem's own check rejects.

The two unit-carrying answers (181 cm, 120 L) are bound in both directions
(`answer_unit` ↔ `\answerline` ↔ the boxed key value). The facet plan is bound to
the printed subtitle and every facet has a study-guide worked example. Standards
are tagged `HSF-BF.A.2, HSF-LE.A.2` — the sequences row of
`references/standards-map.md`, verbatim; no code was invented. Full gate chain
green — exit 0, no manual items.
