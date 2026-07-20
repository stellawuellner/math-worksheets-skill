# math-worksheets — Agent Skill

**v2.2.0** · [Changelog](#changelog)

Generate professional math practice worksheets, answer keys, and study guides for K-12 students. Three PDFs every time: worksheet → answer key → skills summary cheat sheet.

Works with any AI agent that can read files and run shell commands: **OpenClaw**, **Claude Code**, **Gemini**, **Codex**, and others. The skill follows the standard `SKILL.md` format (YAML frontmatter + instructions), and all platform-specific steps have portable fallbacks.

## Features

- **Three documents per request** — worksheet, step-by-step answer key, skills summary with formula boxes and mini examples
- **LaTeX quality** — coordinate planes, geometric figures, tables, multi-part problems via tectonic (no TeX installation required)
- **SymPy verification** — answers are verified with a computer algebra system before compiling; incorrect answers are caught before reaching students. Eleven check types cover algebra through calculus: `solve`, `zeros`, `factor`, `expand`, `eval`, `diff`, `integrate`, `limit`, `equiv` (trig identities), `solve_interval` (trig equations), and explicit `manual`
- **Hardened verification input** — every expression passes a strict token allowlist before parsing (numbers, whitelisted functions/variables, arithmetic only), and problem entries are schema-checked: unknown types or misspelled fields are hard failures, never silent skips
- **Auto reasoning-model detection** — inspects the host agent's config (OpenClaw, Claude Code, Gemini, Codex) and common `*_MODEL` environment variables to find the best available model (DeepThink, o1/o3, DeepSeek R1, Claude Opus) for math generation; shows setup guidance if none is configured. All detection is local — no network calls.
- **Platform-appropriate delivery** — chat-connected agents send the PDFs back on the originating channel (Telegram, iMessage, email); CLI/IDE agents report the output paths on disk
- **Elementary through AP Calculus BC** — Pre-Algebra, Algebra 1/2, Geometry, Pre-Calc, Calculus AB/BC including limits, derivatives, integrals, differential equations, and series (see `references/problem-library.md` for full topic menu)

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
pip3 install sympy
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
│   ├── check_reasoning_model.sh     ← auto-detects best available model (local only)
│   ├── compile.sh                   ← tectonic PDF compiler wrapper
│   ├── run_verify.sh                ← gates compilation on SymPy pass
│   └── verify.py                   ← SymPy verification template
├── references/
│   ├── latex-templates.md           ← LaTeX patterns (coordinate planes, figures, answer key)
│   ├── problem-library.md           ← problem type menu by course, Pre-Algebra → Calc BC
│   ├── model-rankings.md            ← human-readable model guidance
│   └── model-rankings.json          ← bundled model ranking reference
└── tests/
    ├── run_tests.sh                 ← regression suite for verify.py
    └── fixtures/                    ← pass/fail/manual/injection/schema fixtures
```

## Testing

```bash
bash tests/run_tests.sh
```

Fixtures pin the verifier's contract: correct algebra and calculus answer keys exit 0, wrong answers exit 1, manual-only sets exit 2, and — critically — injection attempts and schema violations (unknown types, misspelled fields) exit 1 without executing anything.

## Changelog

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
