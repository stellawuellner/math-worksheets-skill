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
