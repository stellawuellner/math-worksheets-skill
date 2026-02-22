# math-worksheets — OpenClaw Skill

Generate professional math practice worksheets, answer keys, and study guides for K-12 students. Three PDFs every time: worksheet → answer key → skills summary cheat sheet.

## Features

- **Three documents per request** — worksheet, step-by-step answer key, skills summary with formula boxes and mini examples
- **LaTeX quality** — coordinate planes, geometric figures, tables, multi-part problems via tectonic (no TeX installation required)
- **SymPy verification** — answers are verified with a computer algebra system before compiling; incorrect answers are caught before reaching students
- **Auto reasoning-model detection** — automatically uses the best available model (DeepThink, o1/o3, DeepSeek R1, Claude Opus) for math generation; shows setup guidance if none configured
- **Live model rankings** — fetched from this repo with a 7-day cache so recommendations stay current as models evolve
- **Channel mirroring** — sends back via the same channel the request came from (Telegram, iMessage, email)
- **K-12 coverage** — Pre-Algebra through Pre-Calculus (see `references/problem-library.md` for full topic menu)

## Install

```bash
openclaw skills install math-worksheets
```

Or download `math-worksheets.skill` from [ClawhHub](https://clawhub.com) and install locally.

**Prerequisites:**
```bash
brew install tectonic   # LaTeX compiler — auto-downloads packages
```

## Usage

Just ask naturally:

> *"Make Lucy a 20-problem worksheet on exponents and roots"*
> *"Leo needs practice on graphing polynomials — use his homework photo as a guide"*
> *"Factoring trinomials worksheet for an 8th grader, 15 problems"*

The skill handles everything: model selection, problem generation, SymPy verification, compile, and delivery.

## Skill Contents

```
math-worksheets/
├── SKILL.md                          ← workflow and instructions
├── scripts/
│   ├── check_reasoning_model.sh     ← auto-detects best available model
│   ├── fetch_model_config.sh        ← fetches live model rankings (7-day cache)
│   ├── compile.sh                   ← tectonic PDF compiler wrapper
│   ├── run_verify.sh                ← gates compilation on SymPy pass
│   └── verify.py                   ← SymPy verification template
└── references/
    ├── latex-templates.md           ← LaTeX patterns (coordinate planes, figures, answer key)
    ├── problem-library.md           ← K-12 problem type menu by course
    ├── model-rankings.md            ← human-readable model guidance
    └── model-rankings.json          ← machine-readable rankings (fetched by skill)
```

## Keeping Model Rankings Fresh

The skill fetches `references/model-rankings.json` from this repo with a 7-day local cache. To update rankings when new models ship:

1. Edit `references/model-rankings.json` — add new entries to `FOUND_REASONING` or `FOUND_STRONG`
2. Bump `last_updated`
3. Commit and push — all installed instances pick it up within 7 days

PRs welcome for new model additions.

## License

MIT
