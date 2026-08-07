# Finding Inverses with Domain Restrictions — three PDFs

A 10-problem precalculus set built around measured models, plus the worked
answer key and a two-page study guide.

| File | What it is |
|---|---|
| `ss_inverses_curr403.pdf` | Study guide (2 pages) |
| `ws_inverses_curr403.pdf` | Student worksheet, 10 problems (5 pages) |
| `ak_inverses_curr403.pdf` | Step-by-step answer key (3 pages) |

**Everything on the sheet is either a real measurement or a real algebraic
check** — no invented story detail. Every applied problem states its units in
the stem, and the answer line prints the unit the answer must be given in
(minutes, centimetres, kilograms, seconds, degrees Celsius). Three strands
alternate:

* **Inverting a measured model** (#1 phone bill → minutes, #4 spring length →
  load, #7 Fahrenheit → Celsius). Undo the rule, then answer in the *inverse's*
  unit, which is not the original's.
* **Restricting the domain, then inverting** (#3, #6, #8, #10). #3 and #8 ask
  for the domain of the inverse as an inequality before any value is computed;
  #8 is a parabola restricted at its vertex, where taking the wrong square root
  gives −2 instead of 8. #6 and #10 are falling-object models where the
  restriction is exactly what makes the rule one-to-one.
* **Checking that two rules undo each other** (#2, #5, #9) — a linear pair, then
  two rational pairs where the compound fraction has to be cleared.

**How much is machine-checked — honestly.** There are 17 responses across the 10
problems. **12 were recomputed with SymPy** and matched against the key before
the PDFs were built — every numeric answer, both domain inequalities, and all
three composition identities. **5 are instructor-judged** and marked `---` in
the Quick Answers bank: problems 2, 5, 6, 9 and 10.

Those five are the written halves. On #2, #5 and #9 the *answer* is machine-
checked but the "show that" work is not, and a bare "= x" proves nothing — so
the key prints what the shown work must contain. On #6 and #10 the question is
why the restriction is needed at all, which is prose; the key's grading note
distinguishes the mathematical reason (the rule squares the input, so two times
give the same height) from the physical remark ("negative time is impossible"),
which is worth only partial credit on its own.

One misconception trap is declared and machine-tested on #8: the verifier
confirmed that taking the minus square root yields −2, a value the problem's own
check rejects. That appears in the key under "Common wrong answers".

All six study-guide items are fully machine-verified.
