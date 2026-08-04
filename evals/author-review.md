# Post-eval author review

Independent judging answers **how well did this run perform?** Author review is
a separate, downstream phase that asks **what should change in the system?** It
must never edit, replace, or reinterpret the official score.

`scripts/review_eval_run.py` converts every scored task into a packet for the
system that generated the artifacts, validates one structured response per
case, and aggregates recurring `issue_key` values into an improvement backlog.
It is model-provider neutral: GitHub prepares and validates the packets, while
the author system may run in Claude Code, Codex, another agent harness, or a
human-supervised environment.

## Prepare a scored run

The run must contain `run.json`, its retained `tasks/`, and a complete
`verdicts/` directory. The official report should already have been generated
with `evals/score_eval.py`.

```bash
python3 scripts/review_eval_run.py prepare \
  --run-dir evals/runs/curriculum-shardX-20260803T041100Z \
  --output-dir /tmp/author-review/curriculum-shardX-20260803T041100Z
```

The output contains:

- `AUTHOR_REVIEW.md`: the author-system brief;
- `manifest.json`: expected cases and original author provenance;
- `tasks/<task-id>/packet.json`: prompt, contract, score, verdict, machine
  observation, and content-addressed paths to every retained artifact;
- `tasks/<task-id>/review.template.json`: the exact response shape.

Packets explicitly state that the independent result is immutable. The author
system must inspect the original PDFs and sources, check the judge's evidence,
record strengths to preserve, diagnose root causes, and propose actionable
changes with regression tests. A rejected case requires at least one root cause
and one improvement proposal. An accepted case may correctly report no defect.

## Response contract

Commit responses under the retained run:

```text
evals/runs/<run-id>/author-reviews/<task-id>.json
```

Each response records:

- author agent/model provenance;
- agreement, partial agreement, or disagreement with the judge, with evidence;
- strengths to preserve;
- root causes classified by the repository layer that owns the fix;
- proposed changes, affected files, regression tests, expected impact, and risk;
- a stable lowercase `issue_key` shared by every case that needs the same fix.

Do not use a different issue key merely because a defect appeared in a different
grade band. Conversely, do not collapse unrelated fixes just because the judge
used the same surface-level error category.

## Validate and aggregate

```bash
python3 scripts/review_eval_run.py aggregate \
  --packet-dir /tmp/author-review/curriculum-shardX-20260803T041100Z \
  --responses-dir evals/runs/curriculum-shardX-20260803T041100Z/author-reviews \
  --require-complete
```

Outputs are `summary.json`, `summary.md`, `case-reviews.csv`, `issues.jsonl`,
and `improvement-backlog.json`. The backlog groups cases by `issue_key`, keeps
all evidence-bearing variants, raises the group to its highest proposed
priority, and retains the full affected-task list. `merge` accepts repeated
`--backlog` arguments to create one cross-run backlog with both run and task
provenance. The GitHub workflow performs this merge automatically for every
completed review set.

GitHub issues should be created from the deduplicated backlog only after a human
or maintainer checks scope and priority. Never create one issue per eval case.

## GitHub intake

`.github/workflows/eval-results.yml` runs when verdicts, reports, or author
reviews change. It:

1. regenerates every official report and fails if the committed report is stale;
2. validates every scored run and generates all author packets;
3. validates committed author reviews when present and requires the set to be
   complete;
4. uploads the packets and any aggregated backlog as a GitHub Actions artifact.

The workflow can also be started manually for one `run_id`. It deliberately
does not call an LLM or require a provider API key. That separation keeps score
ingestion reproducible and lets the author system run with the same model and
environment that generated the artifacts.
