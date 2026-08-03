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

## Fixed since the first 50 — do NOT work around these any more

The first wave of 50 hit ten real faults. All are fixed. If you find yourself
reaching for one of these workarounds, stop: the bug is gone, and the workaround
now degrades the artifact.

- **Traps work.** `\commonerror` used to overflow the answer key, so agents
  deleted their declared traps or wrapped the bank in `\raggedright` /
  `\emergencystretch`. Do neither. Declare traps freely — a misconception task
  without them is a worse worksheet.
- **Trap descriptions may contain any character.** `^`, `%`, `&`, `_` are
  escaped for you now. Write the description in plain English.
- **Stem length no longer breaks the page gate.** `check_log.py` reads a wrapped
  log. Name files for clarity, not brevity.
- **`workspace_cm` is a legal field** (0 < cm ≤ 24). If a problem genuinely
  needs more room than its type's default — displayed student work, a
  hand-built figure, a table to fill in — declare it and the page budget will
  charge for it. Do not compress a sheet to hit a ceiling; that is the trade
  this project explicitly rejects.
- **`\skillheading` is gated at 57 characters** before compile. Name the skill
  in plain words; leave the slug to the JSON, which is what the coverage gate
  actually reads.
- **`standards-map.md` gained 26 rows** (grades 6–8 geometry/ratio/statistics,
  grade-8 number system, HS congruence, similarity, complex numbers, vectors,
  matrices, statistics, sequences, binomial theorem, radicals). Check it again
  before concluding a code is missing. If it still is, say so in `response.md`
  and leave `standard` off rather than tagging an off-grade code — but a
  genuinely missing row is now rare.

## Traps that remain, and how to avoid them

Not bugs — real constraints the checkers enforce. Every one cost an earlier
agent a rebuild.

- **No `enumerate` anywhere in a study guide.** The answer-key segmenter prefers
  enumerate lists over boxes, so a numbered list inside a `formulabox` makes the
  guide segment as N "problems" and the binding gate fails with a confusing
  count mismatch. Use `itemize`.
- **`\ans{}` ends its paragraph.** A following `\\` is a fatal error. Put
  `\ans{}` last in a problem block, or start a new paragraph after it.
- **Put a `\par` before any `tabular` or `\ans` that follows prose**, or the
  table joins the text line and overfulls.
- **Directions blocks use `itemize`, never `enumerate`** — the layout checker
  treats an enumerate in a worksheet as a problem list and applies work-space
  rules to it.
- **A reference figure must sit before the first `\problem`.** Problem regions
  run from one `\problem` to the next, so a figure after the last one is scoped
  into that problem.
- **Variables `d f g j l p q` are now legal** alongside the originals, so a
  common difference can be `d` and a function value `f`. `e`, `i` and `o` stay
  reserved — they read as Euler's number, the imaginary unit, and zero.
- **A trap's `expr` now sees the problem's `at` bindings**, so lifting literals
  into named variables no longer makes the problem's traps illegal. A symbol the
  problem never binds is still refused.
- **`eval` needs a non-empty `at`.** Lift literals into named variables
  (`"expr": "a/b", "at": {"a": 45, "b": 99}`), which also exposes the givens to
  the prose checker.
- **`solve_interval` on an expanded trig quadratic returns MANUAL**, because the
  CAS is genuinely incomplete on that form and the verifier now says so instead
  of passing a short root list. State the expression factored.
- **Multiple verify entries may share one problem `id`** — the right encoding
  for a multi-part problem. Every entry for that id must repeat an identical
  `difficulty`.
- **Spacing around a minus does not matter.** `"t**4 - 3*t**2"` and
  `"t**4-3*t**2"` extract identically, and so does a spaced boxed answer.
  (An earlier version of this brief claimed otherwise, from an agent report
  nobody had tested. Both claims were checked directly before this line was
  rewritten.)
- **Fractions in boxed answers now normalize correctly** — `\frac`, `\dfrac`
  and `\tfrac` all work, with or without a leading `\,`, and a two-digit
  numerator is safe. (Earlier guidance here said the opposite and was wrong: the
  normalizer was matching a prefix and rewriting `\tfrac{11\pi}{6}` to `1/1`.
  Fixed. A fraction whose parts are not plain numbers is now left alone rather
  than mangled.)
- **A declared `subtitle` must contain no LaTeX markup.** `check_facet_coverage`
  matches it as a whitespace-normalised verbatim substring, so a `$i$` in the
  printed copy breaks a plain-text `i` in the JSON. Name symbols in words
  ("powers of the imaginary unit").
- **`\rule{\linewidth}` after prose needs a blank line**, not just a `\vspace`
  — `\vspace` does not end a paragraph, so the rule is typeset into the last
  prose line and overfulls by ~200pt. Same class as the `tabular`/`\ans` rule.
- **Prefer `\underline{\hspace{1.2cm}}` and `\\[0.9cm]`** over bare `\rule{}{}`
  in stems — raw dimensions leak into the prose checker as phantom numbers.
- **The 57-char `\skillheading` budget includes the `"Skill N --- "` prefix**,
  which eats about 12. Do not echo the JSON slug in the heading — six agents
  overflowed it that way, and the coverage gate reads the tag, not the title.
- **A trap `value` must be the verifier's own rounding of its `expr`**, compared
  at about six significant figures. On a large-magnitude answer that means
  sig-fig rounding, not two decimal places.
- **For `estimate` traps, check the two rounding places actually disagree**
  before declaring one. Rounding to the nearest hundred and the nearest thousand
  agree far more often than sin-for-cos does, and an indistinguishable trap is a
  hard failure.
- **A prose-filled `\dfrac` is a width hazard.** Put wide `\text{}` fractions in
  display math. If a rebuild returns the *identical* overfull measurement, your
  edit hit the wrong line — the log names the paragraph, not the fraction.
- **Declare stem furniture in `workspace_cm` BEFORE the first compile.** The
  budget charges a flat 0.6 cm of stem per problem, so a stem holding a table, a
  drawing, or displayed math costs 1.5–2 cm the model cannot see. Note the
  leverage: raising the printed `\problem[Ncm]` argument moves the budget and
  the real page count together and can never close the gap — only
  `workspace_cm` raises the ceiling without also raising the content.
- **Displayed math inside a `formulabox` costs about as much as a whole extra
  section.** Four sections whose formula boxes all carry displayed math will
  overflow the 2-page cap. Inline the formulas, or drop to three sections.
- **Budget four study-guide sections, not five,** when any section carries a
  figure or displayed math. Section cost is quantised: a section that will not
  fit in the page remainder moves entirely to the next page.

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
