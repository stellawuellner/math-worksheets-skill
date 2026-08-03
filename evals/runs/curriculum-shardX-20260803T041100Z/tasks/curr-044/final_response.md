# Gaps and Overlaps When We Measure — Kindergarten/Grade 1

Three PDFs are ready:

- **Worksheet** (`ws_gaps_curr044.pdf`, 4 pages) — 6 problems, all about the same idea:
  what goes wrong when same-size cubes are laid down with **gaps** or with **overlaps**,
  and how to fix the count. Every problem shows the child a picture of exactly how that
  child laid the cubes down; the pictures print no numbers, so counting is real work.
  A value-free reference figure at the top (GOOD / GAPS / OVERLAPS) sits with the
  directions so it can never be mistaken for one problem's givens.
- **Answer key** (`ak_gaps_curr044.pdf`, 2 pages) — a generated quick-answer bank at the
  top (including a "common wrong answers" line for each declared trap), then a worked
  explanation for every problem written for the adult sitting with the child, with a
  "watch for" note naming the error that particular problem is designed to catch.
- **Study guide** (`ss_gaps_curr044.pdf`, 2 pages) — three skill sections, each with a
  rule box (with a picture), a worked example, and a distinct try-it whose answer is
  printed upside down inside the box: lay the cubes correctly, spot a gap/overlap
  mistake, fix the count.

## What was verified

5 of 6 problems are machine-checked with SymPy (`verify_gaps_curr044.json`):

| # | What is checked | Answer |
|---|---|---|
| 1 | count read from Ivy's correct lay-down | 8 cubes |
| 2 | compare 6 vs 8 (a gap count against the real length) | `<` |
| 3 | find-and-fix (overlaps): the ribbon's true length | 8 cubes |
| 4 | how many more cubes Rex counted than Ivy | 2 cubes |
| 5 | find-and-fix (gaps): how many cubes the gaps hid | 4 cubes |

**Problem 6 is flagged `manual`** and is the only unverified item: the child has to
decide whether Rex's bigger count means better measuring and *draw and explain why*.
No CAS can grade a drawing plus a reason, so the build reports it as a manual-review
item (exit 2) rather than pretending it was checked. The key states what a full-credit
answer contains and what does not earn credit.

**Three misconception traps are declared and machine-checked** to be distinguishable
from the correct answer, and they print in the key's "common wrong answers" block:

- problem 3 — reporting 10, the overlapped count (`8+2`);
- problem 4 — putting the counts together (18) instead of comparing them;
- problem 5 — adding to get 16 instead of finding what the gaps hid.

Two of the six problems (3 and 5) are explicit find-and-fix items, as requested.

## One honest gap: the standards code

`references/standards-map.md` has **no row for K–1 measurement**. Its nearest row,
"Measurement & data (length, mass, time) → 2.MD / 3.MD", is a grade 2–3 code, and the
map's own guidance says an off-grade tag is worse than an honest gap. So the `standard`
field is deliberately **left off** every problem in this sheet rather than tagged with a
code that does not describe a first-grade lesson. The content itself is standard 1.MD
material (measure a length by iterating a shorter unit end to end with no gaps or
overlaps); a `1.MD` row should be added to the map.

## Gate chain

`BUILD PASSED` (exit 2 — one manual-review item, which is the correct encoding for the
open drawing/explanation problem). All 21 gates green: templates, both verification
runs, skill and facet coverage, quick-answer bank, layout and answer-line binding, the
three compiles inside their page budgets, per-problem answer-key binding, study-guide
structure, and prose consistency (worksheet 7/9, study guide 12/12; the two worksheet
flags are the numbers 8 and 10 restated inside the open-response problem, which carries
no computed givens by definition).
