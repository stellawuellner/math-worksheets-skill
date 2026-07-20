# Testing & Evaluation

Three layers, from fastest to most thorough.

## 1. Regression suite (seconds, run on every change)

```bash
bash tests/run_tests.sh
```

Fixture-pinned contract for `scripts/verify.py`: correct algebra/calculus/geometry
answer keys exit 0, wrong answers exit 1, manual-only sets exit 2, injection
attempts and schema violations exit 1 without executing anything.

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

**skill-creator loop** — realistic worksheet prompts run by an agent *with* the
skill and *without* it (baseline), graded against the assertions in
`evals/evals.json`: three PDFs produced, verification JSON present and passing,
requested problem count, figures present, spot-checked answer correctness.
The with/without delta is the skill's measured value. Test prompts live in
`evals/evals.json`; run via the skill-creator tooling or by spawning the two
runs per prompt manually.

**SkillsBench** — the community benchmark for agent skills
(https://github.com/benchflow-ai/skillsbench, paper: arXiv:2602.12670), built
on the BenchFlow harness with uniform skill injection and sandboxed trials.
To evaluate this skill in its framework, package a task family
("generate a verified math worksheet on <topic>") as BenchFlow `task.md`
packages with the graders from `evals/evals.json` as checks, and run
skill-on vs skill-off trials. Requires network access to clone the harness.
