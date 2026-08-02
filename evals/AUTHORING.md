# Authoring brief for eval-run generation

You are producing one eval artifact set per task: a worksheet, a step-by-step
answer key, and a study guide, all three gated and recorded. This is the brief
every generating agent works from, so runs stay comparable across agents.

Read `SKILL.md` first — it is the authoring contract. This file only adds the
things that have actually gone wrong, plus the exact commands for logging.

## Per task

```bash
TASK=curr-123                      # your assigned id
STEM=<short_topic>_${TASK//-/}     # e.g. limits_curr451
D=/tmp/evalbuild/$TASK && mkdir -p $D
python3 evals/run_eval.py next --run "$RUN"   # or read the prompt from task.json
```

Write four files in `$D`:

| File | Contents |
| --- | --- |
| `verify_$STEM.json` | one entry per worksheet problem, `problem_count` = the task's expected count |
| `ws_$STEM.tex` | the worksheet |
| `ak_$STEM.tex` | the answer key |
| `ss_$STEM.tex` | the study guide |
| `verify_ss_$STEM.json` | one entry per study-guide box, in document order |

Then:

```bash
bash scripts/build.sh $D/verify_$STEM.json --outdir $D 2>&1 | tee $D/gate_log.txt
```

Fix whatever it names and re-run until it prints `BUILD PASSED`. Keep the LAST
run's `gate_log.txt` — the judge is entitled to see the chain that passed.

Write a short `$D/response.md` (what you would tell a parent: what the three
documents contain, what was verified, what is flagged manual). Then record:

```bash
python3 evals/run_eval.py record $TASK --run "$RUN" --from $D \
  --response-file $D/response.md \
  --generator-model <your exact model id> --latency-seconds <elapsed>
```

`--generator-model` must be your real model identifier, not the agent name. The
run is designed so acceptance can later be broken down by the model that drove
the skill; a wrong or missing label silently pools two models into one number.

## What has actually failed here

These are real gate failures from earlier tasks in this suite, not hypotheticals.

- **The answer key must `\input{qa_$STEM}`** directly under `\aktitleblock`.
  `build.sh` generates the quick-answer bank and then fails if the key never
  shows it.
- **`\wsheader` has a 36-character budget** (`\akheader` and `\ssheader` get 60).
  Use a short running title — `\wsheader{Algebraic Limits}` — and put the full
  topic in the title block, which has its own space.
- **Standards codes come from `references/standards-map.md` only.** Never invent
  one. Use the code string exactly as that file writes it.
- **Skill tags are all-or-nothing and gating.** Every worksheet problem carries a
  `"skill"`, and the study guide needs a `\skillheading` section for each
  distinct one. Three or four skills is the working range; five is the ceiling.
- **The study guide is capped at 2 pages, mechanically.** Three sections of
  formula box + example + try-it fits. If you overflow, cut the watch-out box
  first, never the try-it.
- **Each `examplebox` needs at least two `\step` lines and a boxed answer**, and
  each `tryitbox` needs its result in `\ans{}`. `verify_ss` entries are bound
  positionally, so they must be listed example, try-it, example, try-it, …, with
  every try-it tagged `"role": "tryit"`.
- **Never claim verification you do not have.** A proof, sketch, or "explain
  why" is `{"type": "manual", "desc": ...}`. The build exits 2 and says so; that
  is the correct outcome, not a failure to fix.
- **Difficulty must ramp**: start at 1–2, majority 2–3, finish with one or two
  4–5. `verify.py` reports the ramp and flags drops.

## Quality bar

These artifacts are going to an independent judge that recomputes every answer
and inspects every page. It rejects a task outright for a wrong or ambiguous
problem, a missing artifact, a problem count that differs from the task, a
severe layout defect, or a focus that appears in under 70% of the problems.

So: match the requested problem count exactly, keep every problem inside the
named focus, give real work space (the page budget is computed from content —
do not compress to save a page), and make the study guide something a student
could actually learn the skill from rather than a formula dump.

## Do not

- Do not commit to git. Artifacts are committed centrally after each wave.
- Do not edit anything outside `/tmp/evalbuild/$TASK` and the run folder.
- Do not hand-roll the LaTeX preamble; `\input{worksheet-preamble}` always.
- Do not re-record a task another agent already recorded.
