# math-worksheets — Agent Skill

[![tests](https://github.com/stellawuellner/math-worksheets-skill/actions/workflows/tests.yml/badge.svg)](https://github.com/stellawuellner/math-worksheets-skill/actions/workflows/tests.yml)
[![coverage](https://img.shields.io/badge/coverage-92%25-brightgreen)](tests/coverage.sh)
[![verifier](https://img.shields.io/badge/false%20accepts-0%2F6993%20corpus-brightgreen)](tests/eval_gsm8k.py)
![python](https://img.shields.io/badge/python-3.11%2B-blue)
![license](https://img.shields.io/badge/license-MIT-blue)

**v3.5.0** · [Changelog](#changelog) · elementary → AP Calculus BC · agent-agnostic · every answer machine-verified

> Ask in plain language — **"make Leo a law-of-sines worksheet"** — and get three print-ready PDFs whose every answer has been checked by a computer algebra system before it reaches a student.

| Worksheet | Answer key | Skills summary |
|:---:|:---:|:---:|
| [<img src="docs/samples/worksheet_geometry-1.png" width="250">](docs/samples/worksheet_geometry-1.png) | [<img src="docs/samples/answerkey_geometry-1.png" width="250">](docs/samples/answerkey_geometry-1.png) | [<img src="docs/samples/skills_summary-1.png" width="250">](docs/samples/skills_summary-1.png) |
| To-scale figures, work space, ramped difficulty | Step-by-step solutions, boxed answers | Formula boxes + worked mini-examples |

*Real, unretouched output. The `read_data` type even renders data charts from the same numbers it verifies:* [data-handling worksheet →](docs/samples/worksheet_data-1.png)

Works with any AI agent that can read files and run shell commands — **Claude Code**, **Gemini**, **Codex**, **OpenClaw** — via the standard `SKILL.md` format, with portable fallbacks for every platform-specific step.

## Why it's different: nothing ships unverified

Most worksheet generators ask a language model for the answers and trust them. This one doesn't. The model proposes problems as **structured data**; a fixed, audited SymPy script decides what's correct; and the printed PDFs are then bound back to those verified values — so a transcription slip in the answer key can't slip through.

```mermaid
flowchart LR
    A[Natural-language<br/>request] --> B[Model designs<br/>problems as JSON]
    B --> C{{"verify.py — SymPy<br/>26 check types"}}
    C -->|any wrong answer| B
    C -->|all pass| D[Compile LaTeX → 3 PDFs]
    D --> E{{"check_answer_key.py<br/>check_prose_consistency.py"}}
    E -->|PDF ≠ verified value| D
    E -->|bound| F[Deliver:<br/>worksheet · key · guide]
    style C fill:#e8f5e9,stroke:#2e7d32
    style E fill:#e8f5e9,stroke:#2e7d32
```

The guarantee is enforced, not aspirational: a **mandatory coverage gate** means no problem can be skipped, the verifier's expression parser is a strict **allowlist** (no code execution), and the whole thing is validated against the **GSM8K** and **MATH** datasets with **0 false accepts on 6,993 checks**. Where a task genuinely can't be machine-checked (proofs, "explain why"), it's honestly marked `manual` rather than faked. See the [Trust model](#trust-model) for the exact boundary.

## Trust model

**Guaranteed** — every problem with a machine-checkable answer is CAS-verified; the mandatory coverage gate (`problem_count`) means no worksheet problem is silently skipped; a fully hand-checked sheet fails unless explicitly acknowledged; and `check_answer_key.py` / `check_prose_consistency.py` bind the printed worksheet, figures, and answer key back to the verified values — the key **per problem**: every verified answer must appear in its own problem's `\boxed{}`/`\ans{}` at the printed precision, so a swapped or mis-boxed key fails even when every number appears somewhere in the document. Validated on GSM8K and MATH — **0 false accepts on 6,993 checks**.

**Human review still required** — `manual`-typed problems (proofs, constructions, "explain why", matrices/vectors), the soft alignment warnings from the binding checkers, and any problem whose *statement* is ambiguous. An optional [LLM-judge review aid](references/manual-review-aid.md) flags likely errors in that content first, but does not gate it. Verification proves the math and its transcription — it does not prove pedagogical intent.

## Features

- **Three documents per request** — worksheet, step-by-step answer key, and a skills-summary study guide (all three verified). The guide can also be built **alone** (`--study-guide-only`) with its full gate chain, for "just make me a reference sheet" requests.
- **Study guides built on the learning-science results, not just formatted** — worked examples with a mandatory strategy step, retrieval-practice try-its with upside-down answers, optional `\why{}` self-explanation asides, optional `\fadestep{}` completion problems (backwards fading), and a dual-coding rule pairing spatial skills with value-free diagrams. Two pages by default; a declared `"pages"` (1–6) buys room for diagrams or a user-requested longer guide, and `verify.py` validates the declaration.
- **26 verification types, elementary → AP Calc BC** — arithmetic, fractions, `solve`/`factor`/`expand`, `system`, `inequality`, `stats`, `probability`, `read_data` charts, coordinate geometry, `triangle` (law of sines/cosines, SSA-aware), `diff`/`integrate`/`definite_integral`/`limit`/`series`, `estimate`, `compare`, complex numbers, and explicit `manual`. [Full menu →](references/problem-library.md)
- **Provenance binding** — `check_answer_key.py` and `check_prose_consistency.py` confirm the printed worksheet, figures, and answer key match the verified JSON, problem by problem.
- **Standards, difficulty & Bloom** — every problem tags a CCSS/AP code (K–4 through AP CED), a 1–5 difficulty (ramp-checked), and a cognitive level; tiered support/core/challenge worksheets on request. [Standards map →](references/standards-map.md)
- **A figure house style, not a snippet pile** — the preamble ships graph styles (`wsgrid` and friends: 7mm pencil-sized unit squares, a gridline at every integer, tick labels white-backed so a curve can never strike a number) and chart styles (`wsbar`, a true `wshist`, `wsboxplot pair`, `\wsdotplot`, stem-and-leaf, scaled pictograms); `figure-macros.tex` ships to-scale triangles, congruence/parallel marks, a CCSS-8 transformation grid, fixed-size solids with nets, and the K-4 model set — ten frames, arrays, proportional base-ten blocks, clock faces, fractions on a number line, tape models, coins. Compile-tested via `tectonic`, with a `pdflatex` fallback. [House style →](references/latex-templates.md)
- **Figures that survive the photocopier** — black ink with meaning carried by dash pattern, fill pattern, weight and label, never by hue; a measured line-weight hierarchy (minor grid < major grid < axis < data). Figures are space-generous by policy: budget the page for the figure's natural size rather than shrinking it until a student cannot plot on it.
- **Accessible output** — large-print and dyslexia-friendly modes (`extarticle` at 14/17pt plus `\accessiblemode`): roomier leading, bigger answer blanks, sans-serif prose *and* math, emphasis set bold rather than italic. A student whose IEP entitles them to large print can use the same generator everyone else does. [How →](references/latex-templates.md#accessibility)
- **Paper and locale** — US Letter, A4, and Legal; `\mwslocale{eu}` prints decimal commas and `\times`. The verify JSON stays canonical, so only the *printed* form is localised and every gate keeps one number format.
- **Page budget computed from content** — 50 graphing problems that each need a coordinate plane are allowed the ~24 pages they need; a flat cap could only be met by shrinking the work space. `build.sh` prints the ideal page count and the double-sided sheet count, so paper cost is visible before printing. [Details →](references/latex-templates.md#page-budget-measured-not-guessed)
- **Grading help in the key** — declared misconception `traps` print as a "Common wrong answers" block ("If they got 7.37: used cos instead of tan"), turning grading into teaching.
- **Visual regression testing** — every document is rendered and compared against an approved baseline, so a layout fault nobody wrote a rule for still cannot ship silently.
- **Portable delivery** — chat agents send PDFs back on the originating channel; CLI/IDE agents report the paths.

## Examples

> **You:** *"Leo's studying the law of sines and cosines — make him an 8-problem worksheet with a figure on each, plus an answer key."*

The skill designs 8 ramped problems, writes a `verify.json`, runs it through SymPy (all 8 pass), compiles three PDFs, and confirms every boxed answer in the key matches the verified value — producing exactly the documents shown above, ready to print.

**More you can ask for** — one skill, from counting to Calc BC:

- *"Make Lucy, my 3rd grader, a times-tables worksheet — 12 problems with a study guide."*
- *"Factoring trinomials for an 8th grader, 15 problems, mixed difficulty."*
- *"A data-handling sheet: read values off a bar chart, then mean / median / mode / range — 8 problems."*
- *"AP Calc chain-rule practice, 10 problems, full worked answer key."*
- *"Systems of equations aligned to 8.EE.C.8, with a scaffolded support tier and a challenge tier."*
- *"Leo needs graphing-polynomials practice — use his homework photo as the style guide."*

The skill handles the rest: problem design, SymPy verification, answer-key and figure binding, compile, and delivery on whatever channel the request came from.

## Install

### OpenClaw

```bash
openclaw skills install math-worksheets
```

Or download `math-worksheets.skill` from [ClawhHub](https://clawhub.com) and install locally.

### Claude Code

Clone into your skills directory (personal or per-project):

```bash
git clone https://github.com/stellawuellner/math-worksheets-skill ~/.claude/skills/math-worksheets
# or, for a single project:
git clone https://github.com/stellawuellner/math-worksheets-skill .claude/skills/math-worksheets
```

Claude Code picks up the skill from `SKILL.md` automatically.

### Gemini, Codex, and other agents

Clone the repo anywhere and point the agent at it — e.g. reference the skill from your `GEMINI.md` / `AGENTS.md` context file, or just say:

> *"Follow the instructions in ~/skills/math-worksheets/SKILL.md to make a worksheet on factoring trinomials."*

Everything in the skill is plain markdown, bash, and Python — no agent-specific runtime is required.

### Prerequisites (all platforms)

**tectonic** — the LaTeX compiler (auto-downloads packages on first use):

```bash
brew install tectonic       # macOS or Linux with Homebrew
cargo install tectonic      # any platform with Rust
sudo apt install tectonic   # Debian/Ubuntu (recent releases)
# or a release binary: https://github.com/tectonic-typesetting/tectonic/releases
```

**Python 3** with **sympy** for answer verification:

```bash
pip3 install "sympy>=1.12"   # bundles mpmath, used for numerical checks
```

For a repo-local development setup that does not modify Homebrew or system
Python, create `.venv`; the build and test scripts discover it automatically:

```bash
python3 -m venv .venv
.venv/bin/python3 -m pip install "sympy==1.14.0" "coverage>=7"
```

**On versions, because "0 false accepts" is a claim about a CAS, not about a script.** `verify.py` enforces a floor of **sympy 1.12** and refuses to run below it. The floor is the weaker of the two controls and it is worth saying why: this verifier's sympy surface is small and old, so an out-of-range CAS does not raise `AttributeError` and stop — it computes, and answers differently. A floor catches the loud failure; the dangerous one is silent. The control that carries weight is the stamp. The corpus baselines (GSM8K, MATH) were established on **1.14.0**, and every run prints the version it actually used — and says so explicitly when that is not 1.14.0, rather than letting the run inherit a guarantee nobody measured it under. There is deliberately **no upper bound**: refusing to run on a newer sympy would age this skill into uselessness, and an author who cannot run the gate at all ships unverified answers instead.

No tectonic? `compile.sh` falls back to `pdflatex` — install the package set up front since pdflatex can't auto-download: `texlive-latex-base texlive-pictures texlive-latex-recommended texlive-latex-extra`. That path has a real version floor too: the figure house styles need **pgfplots ≥ 1.18**, and older distributions ship less (Ubuntu 20.04 has 1.16). The preamble checks and stops with an actionable message, because pgfplots' own refusal — *"Please use at most `compat=1.16`"* — points the wrong way: lowering the compat level silently changes axis scaling under every shipped style. tectonic always fetches a current pgfplots, so this only bites the fallback path.

## Skill Contents

```
math-worksheets/
├── SKILL.md                          ← workflow and instructions
├── LICENSE                           ← MIT
├── scripts/
│   ├── build.sh                      ← ONE command: full gate chain + three compiles, fail-fast
│   ├── compile.sh                    ← tectonic/pdflatex wrapper (stages templates/)
│   ├── verify.py                     ← the fixed, audited verifier (26 check types; --schema)
│   ├── page_budget.py                ← page budget computed from the problem set (paper-aware)
│   ├── render_figures.py             ← builds TikZ figures FROM the verify JSON, so a figure
│   │                                   cannot disagree with the answer it illustrates
│   ├── render_quick_answers.py       ← generates the answer key's Quick Answers bank
│   ├── render_meta.py                ← difficulty/effort markers from the JSON tags
│   ├── check_log.py                  ← reads the LaTeX log for real layout faults
│   ├── find_python.sh                ← shared finder: first python3 that can import sympy
│   ├── run_verify.sh                 ← gates compilation on SymPy pass
│   ├── review_eval_run.py            ← author diagnosis packets and improvement backlog
│   └── score_eval_run.py             ← PDF evidence, judge packets, and run scoring
├── templates/
│   ├── worksheet-preamble.tex        ← the \input-able preamble: headers, boxes, \problem,
│   │                                   and the figure HOUSE STYLES (wsgrid/wsbar/wshist/
│   │                                   wsboxplot/\wsdotplot/wsstemleaf …)
│   └── figure-macros.tex             ← triangles, congruence marks, transformation grid,
│                                       fixed-size solids + nets, and the K-4 model set
│                                       (\tenframefig \arrayfig \basetenfig \clockfig
│                                       \fraclinefig \tapefig \coinrowfig …)
├── references/
│   ├── latex-templates.md            ← figure house style, planes, figures, charts, answer key
│   ├── problem-library.md            ← problem menu + verification recipes, K → Calc BC
│   ├── standards-map.md              ← CCSS (K–4, 5–8, HS) + AP CED codes; difficulty ladders
│   └── manual-review-aid.md          ← optional LLM-judge pass for open reasoning
├── evals/
│   ├── evals.json                    ← quick 3-prompt skill-on/off smoke subset
│   ├── capability-suite.json         ← 28-task E2E suite, graders, profiles, coverage map
│   ├── curriculum-suite-500.json     ← 500 unique counting-through-calculus prompts
│   ├── curriculum-judge-rubric.md    ← v1 acceptance procedure (frozen)
│   ├── curriculum-judge-rubric-v2.md ← v2 behavioural anchors (shadow-scored)
│   ├── JUDGING-V2-ADDENDUM.md        ← what v2 changes, handed to the judge with the packet
│   ├── run_eval.py                   ← start / next / record / status / package a run
│   ├── score_eval.py                 ← aggregates a judge's verdicts into the run report;
│   │                                   refuses self-judging, recomputes ACCEPT from the
│   │                                   scores, and reports contradictions with the record
│   ├── repair_artifacts.py           ← deterministic re-gate of stored artifacts
│   ├── seed_defects.py               ← seeded-defect CALIBRATION runs: plants known defects
│   │                                   in known-clean sheets, keeps controls, seals the
│   │                                   manifest outside the run so judging stays blind
│   ├── generate_curriculum_suite.py  ← deterministic curriculum manifest generator
│   ├── AUTHORING.md                  ← authoring brief + known-open traps
│   ├── author-review.md              ← scored-run feedback loop for the author system
│   ├── scoring-harness.md            ← retained-run layout and two-stage grading workflow
│   ├── runs/                         ← recorded runs: artifacts, observations, verdicts
│   └── analysis/                     ← findings and verdict reviews, OUTSIDE the judge packet
├── tests/
│   ├── run_tests.sh                  ← the regression suite (107 fixtures/checks + 7 suites)
│   ├── coverage.sh                   ← every suite under coverage, floor 90%
│   ├── check_answer_key.py           ← binds printed answer key to verified JSON
│   ├── check_answer_slots.py         ← every PRINTED response needs its own verify entry,
│   │                                   and a slot label must not promise a form the value
│   │                                   is not in
│   ├── check_prose_consistency.py    ← binds worksheet prose + figure labels to JSON
│   ├── check_layout.py               ← figure scope, work space, answer location
│   ├── check_overprint.py            ← reads rendered word boxes for collisions
│   ├── check_answer_line.py          ← answer_unit ↔ \answerline pairing
│   ├── check_ss_coverage.py / check_facet_coverage.py / check_study_guide.py
│   ├── check_template_use.py         ← the shell must \input the preamble, never hand-roll it
│   ├── check_artifact_health.py      ← recorded-run artifact integrity
│   ├── visual_regression.py          ← renders each document, diffs against approved baselines
│   ├── test_*.py                     ← 29 suites; coverage.sh globs and runs them all
│   ├── test_dependency_versions.py   ← the sympy floor + measured baseline + the
│   │                                   pgfplots compat floor, checked against every
│   │                                   file that states a version
│   ├── test_suite_wiring.py          ← asserts every suite runs somewhere it can assert
│   │                                   something — in particular that the render-and-
│   │                                   read-back suites run in the CI job that has TeX
│   ├── baseline/                     ← approved ink-density signatures, one file per page
│   │   └── ENVIRONMENT.txt           ← the TeX/poppler stack they were recorded in
│   ├── eval_gsm8k.py / eval_math_dataset.py  ← corpus evals
│   └── fixtures/                     ← 62 verify fixtures + LaTeX probes
└── .github/workflows/
    ├── tests.yml                     ← regression and pinned visual gates
    └── eval-results.yml              ← scored-run intake and author-review packets
```

## Testing

```bash
bash tests/run_tests.sh                    # contract suite (107 fixtures/checks)
bash tests/coverage.sh                     # every suite under coverage, floor 90%
python3 tests/visual_regression.py         # rendered pages vs approved baselines
python3 tests/visual_regression.py --approve   # re-record after an intended design change
python3 scripts/score_eval_run.py doctor       # eval-grading PDF prerequisites
python3 scripts/review_eval_run.py --help      # post-eval author feedback loop
```

`run_tests.sh` pins the runtime contract across **107 fixtures and checks** — 38 verify, 19 answer-key, 16 layout, 10 facet/trap, 5 log, 5 answer-line, 4 template, 4 skill-coverage, 3 study-guide, 3 prose — plus integrity suites for the capability and curriculum evals, the scoring harness, author review, the page budget, the visual-environment guard and the overprint detector, and the fixture half of **29 Python suites**. `run_tests.sh` runs 20 of those 29 directly; `coverage.sh` globs and runs all 29, and CI runs both, so every suite executes on every push — `tests/test_suite_wiring.py` asserts exactly that rather than leaving it to this sentence. The eval checks keep the 3-task smoke subset synchronized with the 28-task capability suite, require coverage of every public verifier type, prove the 500 curriculum prompts remain unique and evenly distributed, prevent judge-supplied totals or ACCEPT labels from bypassing the rubric, and keep post-eval diagnoses from changing official scores. Correct keys exit 0, wrong answers exit 1, manual-only exit 2, and injection or schema violations exit 1 without executing anything.

`coverage.sh` runs the fixtures and **every** `tests/test_*.py` under `coverage` and fails below **90%** (currently **90%**). The suite list is globbed, not hand-maintained: it was hand-maintained once and drifted until eleven wired suites never ran under coverage, so the reported percentage described a shrinking fraction of the tests while reading like a whole-project number. Among them: `test_audit_fixes.py` (soundness pins from two adversarial audits), `test_error_paths.py` (input validation for every type), `test_verify.py` (scale-aware numeric comparison, symbolic traps, the equation form, and the defensive branches that keep a malformed key producing a verdict rather than a traceback), `test_answer_slots.py` (per-response coverage and the slot-form contract), `test_tikz_libraries.py` (which compiles every figure snippet the docs print, plus a 7-page probe exercising the whole house style), `test_seed_defects.py` (the calibration seeder's transforms), and `test_preamble_layout.py`, which compiles a document and reads the resulting PDF back to pin printed behaviour a source-only checker cannot see.

**Visual regression.** Every layout fault this project has fixed was originally found by a human looking at a PDF, so `visual_regression.py` renders each document to grayscale, reduces it to a 48×48 ink-density grid, and compares against a committed baseline (~7KB per page, diffable in git). Comparison is band-aware: a single page-wide threshold missed a header collision entirely, because the running head is a thin strip. A diff is not automatically a bug — read the reported region, then either fix it or re-approve and commit the new baseline alongside the design change.

**Baselines belong to one machine, and the harness knows which.** An ink signature is a property of a font and rasteriser stack, not only of a design: a different TeX Live or poppler moves cells with nothing in the design touched. So the environment is compared before any page is — by recorded tool versions, and by two canary documents that exercise both font stacks the cases use. On a machine that does not match, the page comparison is printed but **not enforced**, and `--approve` refuses to run; adopting a new reference rendering takes the explicit `--approve --rebase-environment`. That keeps a contributor's first run from being red through no fault of theirs, and keeps an unrelated environment's rendering from quietly replacing the approved one.

The canonical environment is CI, not a laptop — the `visual` job pins `ubuntu-24.04` and sets `MWS_VISUAL_STRICT=1`, which turns environment drift from an advisory into a failure so the gate cannot silently stop testing. When the runner image does move, re-record on it: run the `tests` workflow manually with **Re-record visual baselines** checked, download the `visual-baselines` artifact, and commit it on its own.

CI runs everything on every push. For deeper validation, the corpus evals check the verifier against GSM8K and the MATH dataset — **0 false accepts on 6,993 checks**.

> The coverage and false-accept badges reflect the enforced CI floor and the last corpus run; connect the repo to Codecov if you want a live coverage badge.

## Changelog

### v3.5.0 — 2026-08-08
- **Study guides overhauled around the worked-example literature.** New optional macros: `\why{...}` prints a one-line self-explanation aside under a step (the reason the move is legal — a printed model of the habit the research prompts train), and `\fadestep{...}` turns a try-it into a completion problem ("Started for you: … / Finish it:"), implementing backwards fading for multi-step skills. Boxes gained printed title tabs (RULE / EXAMPLE / TRY IT / WATCH OUT) — the signaling principle applied to a reference card, and the tab text keeps the meaning after a grayscale photocopy — plus rounded corners and a unified border weight. SKILL.md now states which learning effect each structural element rides on, and adds a dual-coding rule: spatial skills get a value-free diagram beside the rule.
- **`--study-guide-only`.** A guide with no worksheet builds via `build.sh <verify_ss_…json> --study-guide-only`: all six guide-integrity gates run for real (template, verify, compile with page cap, answer binding, structure, prose) plus overprint; sheet-relative gates skip by name. Mutually exclusive with `--worksheet-only`; refuses a worksheet JSON with the correct invocation in the error.
- **Study-guide length is declared, not hard-coded.** Top-level `"pages"` (integer 1–6, default 2) in the verify_ss JSON sets the compile-ss page cap; `verify.py` validates it so a typo fails at verify time with the policy in the message. The 2-page default stays the design — the declaration exists for guides whose skills genuinely need diagram room and for users who ask for a longer guide.
- Visual baselines re-recorded for the redesign (the documented `--approve` path); the driver suite gained five `--study-guide-only` cases and the preamble suite pins all four tabs and both macros on the rendered page.

### v3.4.0 — 2026-08-08
- **The curr-482 class is now flagged: a stem that asks for a formula nothing verifies.** The slot gate counts the responses the answer bank PRINTS; this reads what the STEM ASKS FOR, which is the only place the shortfall is visible. `verify.json` covered an antiderivative and an evaluated value while the stem said "Write the particular solution y = f(x), then evaluate y(1)" — so the count balanced and the bank simply never printed the formula. **Advisory, not a hard fail, and the measurement is the reason**: 20 fires over 6,096 corpus problems, all 20 reading as real on adjudication — good for a flag, short of the 100%-on-corpus bar every hard-fail lint here had to clear. The load-bearing distinction is that an antiderivative *is* the general solution and *cannot be* the particular one (its constant is fixed by an initial condition no `integrate` check sees), so the same entry covers one ask and not the other; both directions are pinned. Two shapes were measured and deliberately excluded rather than tolerated: a general solution keyed by `integrate` (genuinely covered), and ordinary set-up-and-solve word problems — a wider noun list including a bare "equation" fired 24 times with over half defensible, and is not shipped.

### v3.3.2 — 2026-08-08
- **The version contract is now stated once and enforced.** Four places stated a sympy version, using three different numbers, and nothing checked any of them: CI installed `sympy>=1.12`, the dev setup said `==1.14.0`, the prose said "baselines were established on 1.14", and a changelog line claimed SymPy was "pinned" when no code read a version at all. `verify.py` now refuses to run below **1.12** and prints the version every run — saying explicitly when it is not the **1.14.0** the GSM8K/MATH corpora were measured on, so a run cannot quietly inherit a guarantee nobody measured it under. **The floor is the weaker control and the README says so**: this verifier's sympy surface is small and old, so an out-of-range CAS does not raise `AttributeError` and stop — it computes, and answers differently. No upper bound, deliberately: an author who cannot run the gate ships unverified answers instead.
- **pgfplots ≥ 1.18 is now checked, not assumed.** `compat=1.18` is a hard requirement of the figure house styles, and Ubuntu 20.04 ships 1.16. Unguarded, pgfplots refuses with *"Please use at most `compat=1.16`"* — advice that fixes the error and silently changes axis scaling under every shipped style. The preamble stops first with a message naming the actual fix (tectonic, or a newer texlive). Only reachable on the pdflatex fallback; tectonic always fetches a current pgfplots.
- `tests/test_dependency_versions.py` pins all of it, including that CI's lower bound can never drop below the verifier's floor. It caught its own first bug: `_version_tuple` stripped non-digits rather than stopping at them, reading `1.14.0rc1` as `(1, 14, 1)` and sorting a release candidate above the release it precedes.

### v3.3.1 — 2026-08-08
- **`\ans` was math-only in study guides, and an end-to-end build found it.** `\akheader` replaces `\ans` with a text-safe compact box; `\ssheader` does not, so an `ss_` document got the base definition — a bare `\boldsymbol`, which is illegal outside math mode. Every shipped exemplar happens to write `$\ans{...}$`, so the text-mode path had never been exercised; a study guide written from SKILL.md's prose ("print each result with `\ans{...}`") instead failed the `compile-ss` gate with `! Missing $ inserted`, the last gate in the chain, the error naming a line two away from the cause. `\ensuremath` fixes it with no change to math-mode output at all — visual regression moved 0 of 2304 cells on the study-guide case — and `tests/test_preamble_layout.py` now pins both authoring forms, mutation-tested against the old macro.
- **Four test suites were reporting green without running.** `test_ssa_figure_labels.py`, `test_tikz_libraries.py`, `test_overprint.py` and `test_page_budget_type_size.py` render a real document and read the PDF back, so they open by probing for a LaTeX engine and skip cleanly when there is none. CI's `verify` job installs poppler but not TeX, and those four were invoked only there — so on every push they printed "skipped" and exited 0, including the figure label-collision measurement and the probe that compiles every figure snippet the docs print. They now run in the `visual` job, which is the one that installs texlive, and `tests/test_suite_wiring.py` fails the build if an engine-dependent suite is ever again wired only where no engine exists. A clean skip is right on a laptop and worthless in CI; nothing distinguished the two.
- **Doc corrections found by auditing claims against the code, not by a red build.** SKILL.md stated the worksheet and answer-key page caps as a fixed 8 and 6; `build.sh` computes them per sheet from `page_budget.py` and uses 8/6 only as the fallback when that fails — a 50-problem graphing set is allowed 26 pages, so an author reading the old text would have cut content the gate never asked them to cut. The README claimed all suites were wired into `run_tests.sh` (9 of 28 are not; they run under `coverage.sh`), quoted a stale fixture count in one of two places, and omitted `evals/score_eval.py` from the file tree. The suite-wiring guard now pins the suite count too.
- **The calibration controls are adjudicated**, and one of the three judge findings is the judge's own error: a hard failure claiming three number lines label their first interior tick as 1, where all three label the right endpoint, in the TikZ source and in the rendered PDF. So the honest control reading is 1 real defect / 1 false hard failure / 1 judgement call, and the 10% false-hard-failure rate now travels beside the 20% detection rate.

### v3.3.0 — 2026-08-08
- **Figure house style.** Four parallel reviews rendered real corpus pages and judged them against printed practice books. They found figures that defeat their own pedagogy: a blank grid with gridlines only every 2 units (no line at any odd integer, on the figure whose job is plotting integer points), a bar chart printing each bar's value on the bar — answering the `read_data` question for the student — a two-panel comparison whose panels auto-scaled independently, 3D solids overprinting their own labels, base-ten blocks drawn from three inconsistent units, and a grade-3 fraction comparison distinguishing its two points by red vs blue, which photocopies into two identical dots. Below grade 5 there were essentially no templates at all, so every K-4 sheet hand-rolled its models and the generator visibly avoided whole strands — zero clock faces, zero coins, zero multiplication arrays in the entire corpus. Ships ~20 preamble styles and ~30 macros, each compiled and rendered before merging, plus a 7-page probe pinned as a fixture test.
- **The verifier stopped failing correct answers it could not express.** Decimal keys are compared scale-aware (five separate authors had rewritten correct mathematics — `4.9t²` became `5t²` — to satisfy exact float comparison); `equiv`/`expand`/`factor` can carry misconception traps, making error analysis reachable on factoring and rewrite sheets; `equiv` accepts the equation the student actually writes (`"expected": "(x-3)**2 + (y+5)**2 = 25"`), with `lhs - rhs` compared as before; divergence, identities and contradictions became answers rather than MANUAL fallthroughs. Re-measured over 1200 verify JSONs and 13,297 entries: **0 verdict changes** — this widened what can be stated, it did not reclassify what was already decided.
- **The answer bank tells the truth about what is unchecked.** Multiple `manual` responses on one problem used to collapse into a single `---` with their slot labels dropped, so a grader could not see how many judgements were owed; and the marker was appended at the end, reordering parts against the printed page (measured: of 1041 ids with two or more lettered slots, all 1041 declare in ascending order). A new hard gate catches a slot label promising a FORM its value is not in — `the equation` keyed to a slope, `colon form` keyed to a fraction.
- **Seeded-defect calibration** (`evals/seed_defects.py`). A judge that scores every sheet 4/5 is indistinguishable from a judge that reads nothing, and a 300-case run cannot tell them apart because nobody knows its true defect count. The seeder plants catalogued defects in known-clean sheets, keeps controls for the false-positive denominator, admits a case only if every gate stays **green** (a defect a gate catches says nothing about the territory the judge covers), and seals the manifest outside the run directory. **The first run's numbers are in the repo and they are not flattering to the judge: 3 of 15 planted defects detected, 1 of 10 clean controls failed on a fabricated citation, and two passes over identical artifacts agreed on only 68% of verdicts.** So no single-pass ACCEPT rate is quoted anywhere in this README — the [calibration write-up](evals/analysis/curriculum-shardX-20260808T033421Z/CALIBRATION.md) explains why one would not mean anything. The CAS gate above is a different instrument with a different guarantee; only the judge-based scores carry this caveat.
- **Coverage measures the whole test suite again.** `coverage.sh` globs `tests/test_*.py` instead of carrying a hand-maintained list that had drifted until eleven wired suites — every suite added for the slot gate, the figure styles and the seeder — never ran under it.

### v3.2.1 — 2026-08-02
- **Eval suites** — a 28-task capability suite with hard-gate profiles and a map covering all 26 verifier types, and a 500-prompt curriculum acceptance suite spanning kindergarten counting to AP Calculus BC, generated deterministically so the checked-in manifest cannot drift from its source. Three new integrity suites keep them honest.
- **`\ans` works inside math mode.** `$m=\ans{3}$` used to fail with "Missing $ inserted"; it now boxes in place, and keeps the flush-right end-of-proof layout in prose.
- **Visual baselines now know which machine they belong to.** An ink signature is a property of a font and rasteriser stack; a foreign TeX Live or poppler moves cells with the design untouched, and re-recorded baselines from another machine would make every later contributor's first run red. The harness compares the environment before it compares a page — recorded tool versions plus two canary documents — and on a mismatch reports diffs without enforcing them and refuses `--approve`. `MWS_VISUAL_STRICT=1` makes drift a hard failure instead, so the gate cannot quietly retire; CI sets it on a pinned `ubuntu-24.04` runner, which is now the canonical rendering environment, with a manual re-record path when the image moves.

### v3.2.0 — 2026-07-31
- **Printed-page fixes, each reproduced before fixing.** The multi-part answer line is suppressed automatically (`\ansline`/`\ansblank` clear the auto-emit flag, and `\problem` tests it after typesetting the stem). The running head can no longer collide: a 68-character title used to overprint the Name/Date blanks by **181pt** on every page, and both head boxes are now shrink-to-fit inside a reserved width. Name/Date print on page 1 only. The answer key dropped its redundant right-hand label, taking its title budget from ~28 characters to ~68. Study-guide page geometry is recomputed by `geometry` rather than patched afterwards, and no box can split mid-text.
- **Grayscale-safe study guide.** Measured, the four box background fills span **5 of 255** luminance in grayscale, so on the black-and-white printer most people use, formula/example/try-it/watch-out were indistinguishable. They keep their colours and now also differ in frame shape.
- **Visual regression harness** (`tests/visual_regression.py`) — documents are rendered and compared against committed ink-density baselines, so a layout fault nobody wrote a rule for cannot ship silently. Band-aware, because a page-wide threshold missed the header collision.
- **Page budget computed from the problem set** (`scripts/page_budget.py`) — replaces the flat 8/6-page caps, which were wrong in both directions at once. Paper-aware (Letter/A4/Legal), reports double-sided sheet count, 100-problem ceiling.
- **Accessibility** — large-print and dyslexia-friendly modes via `extarticle` + `\accessiblemode`; sans-serif prose and math, roomier leading, bigger answer blanks. The header-title budget scales with type size.
- **Locale** — `\mwslocale{eu}` prints decimal commas and `\times`; the verify JSON stays canonical so every gate keeps one number format.
- **Common wrong answers in the key** — declared `traps` render as "If they got 7.37: used cos instead of tan", emitted through `\commonerror` so the correct-answer binding stays strict.
- **New gates:** workspace larger than the page (the engine only warns), and header titles too long for their slot (shrink-to-fit degradation caught before compile).
- **Reusable sheets:** the title-block date is optional and empty by default; `\schoolname` prints a school or teacher name in the footer.

### v3.1.0 — 2026-07-23
- **Removed the model-selection subsystem.** The skill no longer detects, switches, or recommends an AI model. `scripts/check_reasoning_model.sh` and `references/model-rankings.{md,json}` are deleted, and the SKILL.md "Model Selection" section is replaced with a short accuracy note: generate problems with whatever model your agent runs, and the SymPy gate catches wrong answers regardless. Model choice is the agent's job, not the skill's.
- **De-coupled from OpenClaw primitives.** Removed OpenClaw-specific runtime assumptions from the workflow: no `sessions_spawn` delegation, no `image`-tool photo path, and no `~/.openclaw/media` / `imsg` / `gog` delivery specifics. Photo input and delivery are now written generically for any agent's capabilities. OpenClaw remains a supported harness, on equal footing with the others.
- **Reusable, undated worksheets + branding** (from the prior change): title-block date is optional, and a `\schoolname` hook prints a school or teacher name in the footer.

### v3.0.0 — 2026-07-20
- **Trust audit + hardening (breaking-adjacent):** an independent adversarial audit found and fixed soundness gaps confirmed by execution — `solve`/`zeros` no longer silently drop complex roots (declare `"domain"`), `integrate` rejects domain-invalid antiderivatives (`ln(x)` for `1/x`), the numeric-equality fallback no longer accepts a crafted vanishing-polynomial, `approx`/`triangle` use scale-aware tolerance, and `solve_interval` confirms completeness via mpmath instead of a blanket manual downgrade. Pinned by `tests/test_audit_fixes.py`.
- **Mandatory coverage gate + provenance binding:** `problem_count` is now required and an all-manual sheet fails unless acknowledged; `tests/check_answer_key.py` binds the printed answer key to the verified JSON, and `check_prose_consistency.py` now also checks figure-label numbers. The skills summary is verified through its own `verify_ss` JSON.
- **New verify types:** `system`, `series`, `inequality`, complex via `I`, `stats` (mean/median/mode/range/variance/stdev/quartiles), `probability`, `read_data` (charts/tables), `definite_integral` (mpmath quadrature), `estimate`, and `compare` — plus task-reframing recipes that turn many "understanding" topics into checkable tasks. 24 types total.
- **Standards, difficulty, Bloom:** per-problem `standard` (K–4 through HS + AP CED, in `references/standards-map.md`), `difficulty` (1–5 ladders, ramp-checked), and `bloom` tags; tiered-differentiation workflow.
- **Coverage:** elementary → AP Calculus BC; validated against the Marble OS-taxonomy (503 topics) — ~61% machine-verifiable, with an honest `manual` boundary for open reasoning (optional LLM-judge review aid in `references/manual-review-aid.md`).
- **Portability & release:** agent-agnostic (OpenClaw/Claude Code/Gemini/Codex); pdflatex fallback; SymPy version-stamped into every report (a floor was added later, in v3.3.2 — "pinned" overstated what this release shipped); MIT `LICENSE`; CI runs the test suites on every push.
- **Testing:** regression suite (18 fixtures incl. injection/schema/coverage) + audit-fix suite (21 assertions); verifier validated on GSM8K calculator annotations (4282/4282, test split) and MATH boxed answers (2711/2711) with 0 false accepts, 6,993 checks in total.

### v2.3.0 — 2026-07-20
- **Geometry & trig verification:** Six new check types — `approx` (tolerance-based comparison for rounded answers, the workhorse for measurement problems), `distance`, `midpoint`, `slope` (with `"undefined"` for vertical lines), `polygon_area` (shoelace over raw vertices), and `triangle` (full SSS/SAS/ASA/AAS/SSA solver via law of sines/cosines in fixed code, accepting either triangle in the ambiguous SSA case). Geometry types take raw givens — points, sides, angles — so the model transcribes data and the audited script does the formulas
- **Degree mode:** `solve_interval` and `triangle` accept `"unit": "deg"` so Geometry/Pre-Calc answer keys verify in the units students actually use
- **Figure library:** `latex-templates.md` grows from one figure to a full set — to-scale SAS triangle, parallel lines with transversal, central/inscribed angles, shaded sector, unit circle, radian/degree trig graphs, cylinder/cone/prism/sphere, and a two-column proof template. All templates compile-tested; conventions section requires figures drawn to scale from the problem's actual values
- **Verification recipes:** problem-library.md maps every problem kind to its verify type, so choosing the check is mechanical, not judgment
- Tests: geometry pass/fail fixtures added to the regression suite (31 new cases)

### v2.2.0 — 2026-07-20
- **Scope:** Expanded coverage through AP Calculus AB/BC — limits, derivatives, integrals, differential equations, parametric/polar calculus, and series added to the problem library; skill description updated so calculus requests trigger it
- **Verification:** Five new SymPy check types — `diff` (with optional order), `integrate` (verified by differentiating the expected antiderivative), `limit` (with one-sided support), `equiv` (symbolic equivalence with `trigsimp` and a deterministic numeric fallback for trig identities), and `solve_interval` (trig equations on `[a, b)`); existing types gain an optional `var` field
- **Security:** Closed an arbitrary-code-execution hole — `sympify` evaluates raw strings via `eval`, so a crafted expression in the verify JSON could execute code despite the v2.0.0 static-data design. Every expression now passes a strict token allowlist (numbers, whitelisted function/variable names, arithmetic operators only) before parsing; disallowed input is a verification failure, never executed
- **Robustness:** Strict per-type schema validation — unknown problem types, misspelled fields, and missing required fields are hard failures (exit 1) instead of silently downgrading to manual review
- **Testing:** Added `tests/` regression suite with fixtures for passing algebra/calculus keys, wrong answers, manual review, injection attempts, and schema violations

### v2.1.0 — 2026-07-20
- **Portability:** Skill is now agent-agnostic — works in OpenClaw, Claude Code, Gemini, Codex, and any agent that can read files and run shell commands
- `check_reasoning_model.sh` now inspects OpenClaw, Claude Code (`~/.claude/settings.json`), Gemini (`~/.gemini/settings.json`), and Codex (`~/.codex/config.toml`) configs plus common `*_MODEL` environment variables; recognizes bare OpenAI reasoning-model ids (`o3`, `o3-pro`, `o1`) used by Codex
- SKILL.md delegation and delivery steps rewritten per-platform with portable fallbacks (generate inline / report file paths when no subagent or channel tooling exists)
- `compile.sh` finds tectonic in cargo and Linuxbrew locations; docs cover non-Homebrew installs
- Removed stale hosted-JSON ranking text from SKILL.md (rankings are bundled-only since v2.0.0)

### v2.0.0 — 2026-02-23
- **Security:** Eliminated RCE surface — verification no longer generates or executes AI-written Python code. The AI now writes a structured JSON data file (`verify_TOPIC_DATE.json`); the fixed, auditable `scripts/verify.py` evaluates it using SymPy. No user input is ever executed as code.
- **Security:** Removed `fetch_model_config.sh` — skill no longer makes any network requests at runtime
- **Security:** Removed auto-`pip install` from `run_verify.sh`; sympy must be installed as a prerequisite (`pip3 install sympy`)
- **Security:** `check_reasoning_model.sh` is now fully local; reads OpenClaw config optionally with graceful fallback to bundled defaults
- `references/model-rankings.json` remains bundled as a static reference

### v1.0.0 — 2026-02-22
- Initial release
- Three documents per request: worksheet, answer key, skills summary
- SymPy verification gate (exit 0/1/2)
- Auto reasoning-model detection
- LaTeX compilation via tectonic
- Channel-matched delivery (Telegram, iMessage)

## License

MIT
