# Math Model Rankings

Human-readable companion to `model-rankings.json`. Both files ship bundled with
the skill and are updated with each release — the skill makes no network
requests at runtime. Keep the two files in sync when updating.

Last updated: 2026-02-22

## Current Rankings (K-12 Math Generation)

### Tier 1 — Reasoning Models (FOUND_REASONING)
Step-by-step internal reasoning. Highest math accuracy. Use for problem generation + answer keys.

| Model ID pattern | Alias | Notes |
|---|---|---|
| `openai/o3` | o3 | Best overall math as of early 2026 |
| `openai/o1` | o1 | Strong reasoning, more accessible than o3 |
| `gemini-2.5-pro-deepthink` | deepthink | Google's reasoning model, excellent |
| `gemini-2.0-pro-deepthink` | deepthink | Previous generation, still solid |
| `deepseek-r1` | deepseek | Open source, competitive with o1 |
| `deepseek/deepseek-r1` | deepseek | Full model ID variant |

### Tier 2 — Strong Non-Reasoning (FOUND_STRONG)
No step-by-step reasoning, but high quality. Excellent LaTeX and pedagogical judgment.
Use when no Tier 1 is available. SymPy verification compensates for accuracy gap.

| Model ID pattern | Alias | Notes |
|---|---|---|
| `claude-opus-4` | opus | Excellent math + best LaTeX quality |
| `claude-opus-3-5` | opus | Previous generation Opus, still strong |

### Tier 3 — Standard Models (NONE → show recommendation)
Capable but not recommended for complex algebra. SymPy verification is essential.

| Model ID pattern | Notes |
|---|---|
| `claude-sonnet-4` | Good for basic problems, weaker on multi-step |
| `gemini-2.5-flash` | Fast, adequate for Pre-Algebra level |
| `openai/gpt-4o` | Decent, not specialized for math |

## How to Update

When new models ship that should be Tier 1 or Tier 2:

1. Update `model-rankings.json` (patterns + `last_updated`)
2. Update this file to match
3. Add matching patterns to `scripts/check_reasoning_model.sh`
4. Ship a skill release (ClawhHub for OpenClaw; tag the git repo for direct installs)

Key signals a model deserves Tier 1 promotion:
- Scores >80% on MATH benchmark or AIME
- Has documented chain-of-thought / reasoning architecture
- Consistently outperforms Sonnet-class on algebra in community testing

Resources for staying current:
- https://livebench.ai — live model benchmarks
- https://arxiv.org/list/cs.LG/recent — new model papers
- https://lmsys.org/blog — LMSYS Chatbot Arena (math category)
