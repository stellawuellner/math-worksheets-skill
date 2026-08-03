# Linear Contexts, Tables, Equations, and Graphs — Grade 8 / Pre-Algebra

Three PDFs, all gated green:

- **Worksheet** (`ws_linearreps_curr225.pdf`, 5 pages) — 12 problems. All four
  representations appear: stories, tables, equations, and three labelled
  reference graphs drawn once at the top of the sheet (so the figure belongs to
  no single problem and cannot be misapplied to its neighbour). Every problem
  moves between two representations, and the directions make the decision
  explicit: which form do you have, which do you need.
- **Answer key** (`ak_linearreps_curr225.pdf`, 3 pages) — numbered steps, with
  step 1 naming the *reason* the method fits (a change asks for a subtraction,
  a known $y$ means solving rather than substituting, a falling line means a
  negative rate). Problem 7's key shows the full matching argument, including
  why Graphs A and C are ruled out.
- **Study guide** (`ss_linearreps_curr225.pdf`, 2 pages) — three sections
  (reading a table/graph, rate of change from two points, building and using
  the equation), each with a rule box, a worked example, and a distinct try-it
  with the answer upside down. Watch-out box covers the two errors this topic
  generates most: reading a change in $y$ as the rate when the table steps by
  more than one, and losing the negative sign on a falling line.

## What the sheet actually exercises

| Facet | Problems |
|---|---|
| `read-the-representation` (read a value and a change from a table) | 1, 6, 10 |
| `rate-of-change` (slope from two points, a graph, or a story) | 2, 4, 8, 11 |
| `equation-and-prediction` (build $y = mx + b$, use it both ways) | 3, 5, 7, 9, 12 |

Interleaved throughout — max same-facet run of 2, and that only across the two
parts of a single multi-part problem. Difficulty ramps `1 → 5` across the 16
verification entries. Problems 1, 6, 10 and 12 are two-part (read, then rate),
so the sheet keeps the reading skill and the computing skill distinct.

## Verification

- **16 verification entries covering all 12 problems, all machine-verified —
  0 manual.** Four `slope` from stories or graphs, four more `slope` paired
  with three `read_data` table reads, three `eval` predictions, and two `solve`
  problems used backwards. All four verification targets named by the task
  (`slope`, `solve`, `eval`, `read_data`) are exercised.
- **6 of 6 study-guide boxes machine-verified** (3 worked examples + 3 try-its).
- The three reference graphs are the source for problems 2, 4, 5, 7 and 11, and
  every point the key reads off them ((0,3), (4,11), (0,12), (5,2), (0,0),
  (3,12)) is a verified JSON given, so the drawing and the answers cannot drift.
- Problem 9 declares `answer_unit: "cm"`; the sheet prints `\answerline{cm}` and
  the key boxes `39 cm`, so the unit is gated in both directions.
- Standards, verbatim from `references/standards-map.md`: `8.F.A.1–8.F.B.5` for
  the function/representation problems and `8.EE.B.5, 8.EE.B.6` for the
  slope problems.

Nothing here is open-ended, so nothing is flagged for manual review. The prose
checker reports 40/44 (90.9%); the four flags are the table x-column entries
that no single check consumes (2, 1, 2) and the workspace dimension on problem
9 — all in the "expected false flag" class the checker documents.

`BUILD PASSED` on the first run: all 21 gates green.
