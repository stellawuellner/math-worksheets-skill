# Run 2 vs run 1 — machine-layer comparison

Run 2 (`curriculum-shardX-20260806T162603Z`) regenerates the SAME 300 task
specs as the three 2026-08-02/03 runs, verified byte-identical, under the
2026-08-06 system. 300/300 recorded; every task has all eleven artifacts and
`gate_chain_passed`.

**Every figure below is the SAME code applied to BOTH corpora**, so none of it
depends on when a gate was written.

|                                   | run 1 (old)      | run 2 (new) |
|-----------------------------------|------------------|-------------|
| slot-gate clean                   | 99 / 300         | **300 / 300** |
| open-ask gaps (unrubriced asks)   | 343 in 158 cases | **0** |
| stale rubrics                     | 1                | **0** |
| cases w/ BLOCKING bank defect     | 80               | **0** |
| verify entries                    | 3944             | 4923 |
| `manual` entries                  | 299 (8%)         | 998 (20%) |
| problems covered                  | 2928             | 2928 |

The `manual` jump is the point, not a side effect: explain/justify/sketch asks
now carry a rubric an instructor can grade from, where before they were
silently counted as machine-verified.

## What this does NOT show

Run 2 changed the system AND the generator model (claude-opus-5 →
claude-fable-5). The machine-layer figures above are attributable to the
system, because each is a deterministic checker run over finished artifacts.
**Rubric-score deltas from the external judge will not be cleanly attributable
to either**, and should not be reported as if they were.

Eleven advisory `bank_prints_given` notes remain in run 2. They are NOT
counted as defects: the signature is right about one time in seven, and the
run-2 instances that were inspected (curr-326) are genuine forward
computations whose answers happen to coincide with stem digits.

## Judge packaging

Both rubric versions ship: `evals/curriculum-judge-rubric.md` (v1, byte-frozen
for comparability with run 1) and `evals/curriculum-judge-rubric-v2.md`
(behavioural anchors). `evals/JUDGING-V2-ADDENDUM.md` instructs one pass
scoring both; the official verdict derives from v1 exactly as before, with a
shadow v2 verdict reported alongside. A verdict without `scores_v2` is
complete.

## Findings

`FINDINGS.md` records 20+ system defects the run surfaced, what was fixed
during it (presentation and measuring-instrument only) and what was
deliberately queued (anything that would move a pass/fail boundary mid-run).

## CORRECTION — the two runs are not judged under identical rubric text

I stated when packaging that run 2's rubric is "byte-identical to run 1's, so
scores stay comparable." That is wrong, and the error is worth stating exactly.

Run 2's `rubric.md` is byte-identical to the CURRENT canonical
`evals/curriculum-judge-rubric.md`. Run 1's `rubric.md` differs from it by 39
lines, because the canonical file was improved during this session — after run 1
had been judged.

The drift is entirely ADDITIVE, and the additions are this session's own fixes:

- a **"Quoting values"** section requiring every quoted number to be one the
  artifact actually prints — added precisely BECAUSE run 1's judge cited values
  that appear nowhere in the artifacts (curr-131's "4/5", curr-369's inverted
  hole, curr-005's "12<16");
- a definition of what **"surfaced"** means, after the surfacing check was found
  to test vocabulary rather than filenames;
- an instruction **not to copy a supplied total or ACCEPT label**, since the
  harness recomputes both.

The eight dimensions, the 0–4 scale, the hard-failure list and the ACCEPT rule
(no hard failures, all dimensions ≥ 3, total ≥ 27) are UNCHANGED.

**Decision: keep the improved text and disclose the confound.** Reverting to
run 1's wording to buy strict textual comparability would knowingly reinstate
the instructions whose absence produced fabricated citations — trading real
judging quality for a cleaner-looking comparison. That is the wrong trade.

**What this means for reading the results.** Dimension scores remain comparable
in scale. Differences in the QUALITY and honesty of findings between the runs
may partly reflect the better instructions rather than better artifacts. So the
run-to-run claim that carries weight is the machine layer — deterministic
checkers run over finished artifacts, identical code on both corpora — not the
rubric scores. That was already the stated position; this drift strengthens it.
