# Teen Numbers — Fixing Swapped Tens and Ones (K–Grade 1)

Three PDFs are ready for a kindergarten/first-grade learner, all built around the
one error the topic is about: counting the tens and ones correctly and then
writing the two digits in the wrong order.

- **Worksheet** — `ws_teenplace_curr034.pdf`, **6 problems**. A ten-frame warm-up
  that names which digit counts the tens; three find-and-fix items (Mia writes 31
  for 1 ten and 3 ones; Ben writes 71 for seventeen; Ana writes 61 for one full
  ten-frame and 6 dots); and two compare-the-swapped-pair items (1 ten 2 ones vs.
  2 tens 1 one, and Jo's swapped number vs. the number she meant). Every problem
  gets 3–3.5 cm of building/drawing space plus its own answer location.
- **Answer key** — `ak_teenplace_curr034.pdf`. Three numbered reasoning steps per
  problem (name the tens, name the ones, write tens-first), the generated quick-
  answer bank, and the generated "Common wrong answers" block that tells a grader
  exactly what a 51 / 31 / 71 / 61 means.
- **Study guide** — `ss_teenplace_curr034.pdf`, 2 pages, three skill sections
  (read 1 ten and some ones · fix a swapped number · compare a swapped pair).
  Each has a rule box, a two-step worked example, and an upside-down try-it, and
  it closes with the watch-out that teen numbers are *said* ones-first but
  *written* tens-first.

## Verification

All 6 worksheet answers are machine-checked with SymPy — 4 `eval` place-value
computations and 2 `compare` relations. **Nothing is flagged manual.** All 6
study-guide boxes are verified too.

**Four misconception traps are declared** (51, 31, 71, 61), one on each `eval`
problem — every problem where the planted swap has a single comparable value.
The verifier proved each planted result is distinguishably wrong and that the
printed wrong number really is what the swapped method computes, and they print
in the key's "Common wrong answers" block. (`compare` problems 4 and 6 take no
traps: the trap field is only allowed on single-comparable-answer types.)

Standards: every problem is tagged `1.NBT` from `references/standards-map.md`.

## Gate chain

`build.sh` printed **BUILD PASSED — all gates green** (exit 0) on the first
attempt. The answer key `\input`s the generated quick-answer bank directly under
`\aktitleblock` with **no `\raggedright` and no `\emergencystretch`** anywhere —
the `\commonerror` block now closes its own paragraph, so the four trap lines set
and the key compiles clean at 2 pages with no overfull box.
