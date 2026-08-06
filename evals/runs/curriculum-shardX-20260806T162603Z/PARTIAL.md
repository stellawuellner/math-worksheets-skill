# PARTIAL RUN — 79 of 300 recorded

Generation stopped when the account's monthly spend limit was reached, not
because of any system fault. Every one of the 79 recorded tasks is complete
(result.json + gate_log.txt + all three PDFs); no task is half-written.

## How to resume

Task specs for all 300 are already scaffolded and are byte-identical to the
originals in the three 2026-08-02/03 runs — verified, and the property the
paired comparison depends on. Unrecorded tasks are simply the ones with no
`result.json`. Resume with the same brief:

    scratchpad/gen_prompt.md      the generation brief (forbids reading run 1)
    scratchpad/run2_batch_*       30 batches of 10; G00-G11 were dispatched

## Why the comparison is still valid on 79

Every number below is PAIRED — the same 79 specs, scored under the same gate
version — so the band skew of the recorded subset (early task ids run
elementary-heavy) cancels out. The subset is not a random sample of the 300,
so these figures should not be read as an estimate of the full-300 result.
