# Measuring and Picture Graphs — Kindergarten / Grade 1

Three PDFs are ready:

- **Worksheet** — `ws_measure_curr045.pdf` (3 pages, 10 problems)
- **Answer key** — `ak_measure_curr045.pdf` (2 pages, full reasoning per problem)
- **Study guide** — `ss_measure_curr045.pdf` (2 pages, 3 skill sections)

## What the worksheet does

Every page carries the same two pieces of evidence — a **Sticker Chart** picture graph
(Mia 5, Leo 3, Ana 6, Sam 4; one star = one sticker) and a **Measuring Strip** table
(crayon 4, marker 6, pencil 7, straw 9 paper clips). The chart and strip are reprinted at
the top of each page so a child never has to flip back to find the data.

The ten questions interleave three subskills from the very first problem, so the child
must decide *which* picture holds the answer rather than repeating one procedure:

1. **read-picture-graph** (problems 1, 3, 6) — read one row, find the most, find the total
2. **measure-with-units** (2, 5, 8, 10) — compare two lengths, find how many units longer,
   order three objects, reason about unit size
3. **compare-from-data** (4, 7, 9) — how many more, who has the fewest, and a synthesis
   challenge where a claim ("Leo and Sam beat Ana and me") has to be tested against the
   two totals (7 vs 11 — the claim is false)

Difficulty ramps 1, 1, 2, 2, 2, 3, 3, 3, 4, 4. Problem 10 is the open synthesis item: the
same straw measures 9 paper clips but only 5 blocks, and the child must explain which unit
is longer.

## Verification

- **9 of 10 problems machine-verified** with SymPy through the build gate: picture-graph
  reads and differences (`read_data`), length differences (`eval`), and the ordering and
  greater-than/less-than comparisons (`compare`). Every printed boxed answer in the key is
  bound back to its own problem's verified value.
- **1 problem flagged manual** — problem 10 asks the child to justify why one block is
  longer than one paper clip. That is genuinely open reasoning, so it is declared
  `{"type": "manual"}` rather than claimed as verified. The key gives a model answer, a
  full-credit rubric line, and the specific wrong reasoning to listen for ("9 is bigger
  than 5, so paper clips are longer").
- The build reports this as `BUILD PASSED — 1 verification run flagged manual-review items
  (exit 2)`, which is the correct outcome for an explain-your-thinking item.

## Study guide

Three sections, one per worksheet subskill, each with a rule box, a worked mini-example
with a strategy step, and a try-it whose answer is printed upside down inside the box so
the child attempts it first. All six study-guide computations are machine-verified too.
The watch-out box flags the two errors this topic reliably produces: reading a bigger
*count* as a bigger *unit*, and answering "how many more" with the larger row instead of
the difference.
