# Testing & Evaluation

Three layers, from fastest to most thorough.

## 1. Regression suite (seconds, run on every change)

```bash
bash tests/run_tests.sh
```

Fixture-pinned contract for `scripts/verify.py`: correct algebra/calculus/geometry
answer keys exit 0, wrong answers exit 1, manual-only sets exit 2, injection
attempts and schema violations exit 1 without executing anything.

## 1b. Visual regression (needs TeX; skips cleanly without it)

```bash
python3 tests/visual_regression.py            # check
python3 tests/visual_regression.py --approve  # re-record an intended design change
```

Each case is rendered, reduced to a 48×48 ink-density grid, and compared against
a committed baseline. It catches the class of fault no rule anticipated, because
it looks at the printed page rather than the source.

**Read this before you re-approve anything.** A baseline is specific to the font
and rasteriser stack that produced it. A different TeX Live or poppler moves
cells with the design untouched, and that has already happened here once: a
branch arrived with seven re-recorded baselines that failed the harness at 6.6%
while its own code rendered identically to the previous baselines. So the
harness checks the environment first — recorded tool versions in
`tests/baseline/ENVIRONMENT.txt`, plus two canary documents covering both font
stacks — and behaves accordingly:

| Situation | What happens |
| --- | --- |
| Environment matches | Full gate. A page diff is a design change; fix it or `--approve` it. |
| Environment differs | Diffs are printed, **nothing is enforced**, and `--approve` is refused. |
| Environment differs, `MWS_VISUAL_STRICT=1` | Hard failure. CI sets this so drift can't silently retire the gate. |
| You mean to move the reference here | `--approve --rebase-environment`, committed on its own. |

If your machine reports drift, that is expected and not your problem to fix:
the authoritative run is the `visual` CI job, which pins `ubuntu-24.04`. When
the runner image itself moves, re-record on it — run the `tests` workflow
manually with **Re-record visual baselines** checked, download the
`visual-baselines` artifact, and commit it as a standalone change.

`tests/test_visual_environment.py` pins this guard's behaviour with rendering
stubbed, so it runs on machines with no TeX at all and is part of
`tests/run_tests.sh`.

## 2. Corpus evals (minutes, run when the verifier changes)

Ground-truth math datasets exercised against the verifier. Three metrics each:
**parse coverage** (does the allowlist accept real-world expressions),
**accept-correct** (ground-truth answers must PASS), and **reject-perturbed**
(shifted answers must FAIL — any pass here is a false-accept bug).

**GSM8K** (grade-school arithmetic; ~4,300 calculator annotations):
```bash
curl -sSL -o /tmp/gsm8k_test.jsonl \
  https://raw.githubusercontent.com/openai/grade-school-math/master/grade_school_math/data/test.jsonl
python3 tests/eval_gsm8k.py /tmp/gsm8k_test.jsonl --report /tmp/gsm8k_report.json
```
Baseline result (2026-07-20): 4,282/4,282 parse coverage, 100% accept-correct,
0 false accepts. This eval caught a real tokenizer gap (leading-decimal
numbers like `.5`) on its first run.

**MATH dataset** (Hendrycks et al.; Prealgebra/Algebra/Geometry/Precalculus with
symbolic boxed answers — the closest match to this skill's scope). Needs the
dataset downloaded locally (Hugging Face is blocked in some sandboxes):
```bash
python3 tests/eval_math_dataset.py MATH/test \
  --subjects prealgebra algebra geometry precalculus
```

## 3. End-to-end skill evals (the real question: does the skill help?)

**Quick skill-creator loop** — the 3-prompt `evals/evals.json` smoke subset is
for fast skill-on versus skill-off comparison. It covers factoring facets,
triangle rendering/ambiguous SSA, and AP Calculus chain/product rules. Grade
the outcome artifacts: readable PDFs, complete verification JSON, exact problem
count, requested behavior, and zero independently detected wrong answers.

**Full capability suite** — `evals/capability-suite.json` contains 28 tasks:
single-turn, multi-turn, asset-backed, stress, adversarial bypass, manual-review,
worksheet-only, multi-set, accessibility/locale/paper, and negative-routing
cases. It defines hard-gate profiles, execution conditions, task-specific
assertions, and an explicit map covering all 26 public verifier types. Run the
same model/harness in isolated skill-on and skill-off trials; use three trials
per normal task and one for expensive stress tasks. Report hard-gate pass rate,
quality among passes, pass@1, pass^3, and the paired skill delta. Never average
away a wrong answer, uncovered printed problem, missing requested artifact, or
false machine-verification claim.

`tests/test_eval_suite.py` validates the manifests and keeps the quick subset
synchronized with the full suite. It runs as part of `tests/run_tests.sh`.

**500-prompt curriculum acceptance suite** —
`evals/curriculum-suite-500.json` spans ten equally weighted bands from
kindergarten counting through AP Calculus BC: 100 topic families with five
distinct instructional focuses apiece. Every prompt requests a worksheet,
step-by-step answer key, and 1–2 page study guide. Run generation in clean
workspaces, preferably in shards of 25, then have a trained person or an
independent second agent apply `evals/curriculum-judge-rubric.md`. Acceptance
requires no hard failure, at least 3/4 on every quality dimension, and at least
27/32 overall. `tests/test_curriculum_eval_suite.py` pins exact regeneration,
500 distinct focus strings and normalized-unique prompts, the 50-per-band
distribution, artifact contract, all 26 verifier targets, and the judge threshold.

**SkillsBench** — the community benchmark for agent skills
(https://github.com/benchflow-ai/skillsbench, paper: arXiv:2602.12670), built
on the BenchFlow harness with uniform skill injection and sandboxed trials.
To evaluate this skill in its framework, package a task family
("generate a verified math worksheet on <topic>") as BenchFlow `task.md`
packages with the graders from `evals/evals.json` as checks, and run
skill-on vs skill-off trials. Requires network access to clone the harness.
