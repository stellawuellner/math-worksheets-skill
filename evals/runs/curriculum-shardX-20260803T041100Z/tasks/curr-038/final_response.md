# Missing Addends Within 20 — three PDFs

**Worksheet** (`ws_missingaddend_curr038.pdf`, 8 problems, ~3 pages).
Every problem is a missing-addend equation within 20 (8 of 8 on the requested
focus), and every one is anchored to a representation or a real situation:

1–2. counters on a ten-frame / two ten-frames (`6 + ? = 10`, `8 + ? = 13`)
3. a number bond with the whole 15 apples and one part 9
4. a full crayon box: write the subtraction sentence, then solve `7 + ? = 16`
5. a cube-train tape diagram, `? + 5 = 12`
6. an application: a 20-cube tower with 12 cubes stacked, answered in cubes
7. error analysis — Mia adds 5 and 13 to get 18; the student names the mistake and fixes it
8. challenge — two equations with the same whole (`? + 6 = 14`, `9 + ? = 14`), then compare the two missing numbers

Difficulty ramps 1, 1, 2, 2, 2, 3, 3, 4. Every problem has 3–4.5 cm of work
space plus an answer line; problem 6 carries a unit-tagged answer line
(`Answer: ____ cubes`), bound to its `answer_unit` in the JSON.

**Answer key** (`ak_missingaddend_curr038.pdf`). Full reasoning, not answers:
each solution names the whole and the known part, shows the count-on *and* the
subtraction, and checks by adding back. The generated quick-answer bank sits at
the top for fast grading, and it prints the two declared misconception traps
("if they got 32 / 18: added the two numbers instead of finding the missing
part"), so the grader sees the error, not just the mark.

**Study guide** (`ss_missingaddend_curr038.pdf`, 2 pages). Three sections, one
per worksheet skill — count on with a ten-frame, subtract to find the part,
missing addends in a story — each with a rule/model box, a two-step worked
example, and an upside-down-answer try-it. A watch-out box flags the exact
misconception the worksheet traps: the two visible numbers are not both parts.

## Verification

All 10 verification entries for the 8 worksheet problems (problem 8 is
multi-part: two equations plus the comparison) were machine-checked with SymPy,
as were all 6 study-guide results — **16 verified, 0 manual**. The two declared
traps were proved distinguishably wrong by the verifier. The full gate chain is
green (`BUILD PASSED`), including per-problem binding of every printed boxed
answer back to its verified value and the unit binding on problem 6.

Standard: `1.OA.C.6` from `references/standards-map.md`, matching the task's
`standard_refs`. The prose-consistency reports flag only TeX box dimensions
(0.8, 0.9, 4.2 …) and the intermediate counting numbers inside a worked
example — no story number is unaccounted for.
