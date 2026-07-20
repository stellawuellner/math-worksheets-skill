# Manual-Review Aid (optional LLM-judge pass)

Some problems can never be CAS-verified: proofs, explanations, "why does…",
strategy choices, open-ended reasoning, and the model *answers* the key prints
for them. These are correctly typed `manual`. This aid does NOT change that —
it adds an **independent second-pass reviewer** that catches likely errors
before a human sees them, reducing (not replacing) human review.

**Trust boundary — read this first.** An LLM judge is *not deterministic* and
does **not** earn the SymPy-grade guarantee. A `manual` problem stays `manual`.
The judge's verdict is advice for the human reviewer, never a gate that lets an
answer ship unreviewed. Never mark a problem `PASS`/verified on the strength of
a judge verdict.

## When to use it

Run it over the `manual`-typed problems and over any worked explanation in the
answer key or skills summary — i.e. exactly the content the CAS checkers can't
reach. Skip it for machine-verified problems (they already have a real gate).

## How to run it

Spawn a *separate* model instance (a different context from the generator) as an
adversarial checker, one call per manual item. Give it only the problem
statement and the printed model answer, and ask it to find errors — not to
agree.

Prompt template:

```
You are an exacting math teacher reviewing an answer key for errors. You are
NOT the author and your job is to find mistakes, not to approve.

Problem: <problem statement>
Printed model answer: <the answer-key text for this problem>

Check, step by step:
1. Is every mathematical claim correct?
2. Does the reasoning actually establish the conclusion (no gaps, no circularity)?
3. For a proof: is each step justified by a stated reason?
4. Is anything stated that is false or misleading for the target grade level?

Respond as JSON:
{"verdict": "ok" | "suspect", "issues": ["..."], "confidence": 0.0-1.0}
Default to "suspect" if you are unsure.
```

Treat any `suspect` verdict — or low confidence — as "human must review this
one closely." An `ok` verdict lowers, but does not remove, the need for a human
pass.

## What it does and doesn't close

- **Reduces human load** on explanations/proofs by surfacing the obviously-wrong
  ones first.
- **Does not** make reasoning content verified. Pedagogical fit ("is this the
  right problem for this student?"), ambiguity, and genuinely open responses
  remain human judgment — and should. Simulating a guarantee here would lower
  trust, not raise it.
