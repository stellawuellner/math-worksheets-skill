#!/usr/bin/env bash
# check_reasoning_model.sh — Detect the best available reasoning model for math
#
# Agent-agnostic: inspects the config files of whichever agent harnesses are
# present (OpenClaw, Claude Code, Gemini, Codex) plus common *_MODEL
# environment variables, and checks whether a reasoning model or strong
# fallback is configured. All logic is local — no network requests are made.
#
# Outputs one line: "<STATUS> <alias> <full-model-id>"
#   FOUND_REASONING — a dedicated reasoning model is configured (o3, DeepThink, R1, etc.)
#   FOUND_STRONG    — a strong non-reasoning model is configured (Opus, etc.)
#   NONE            — only standard models found; recommend switching
#
# Exit 0 = usable model found
# Exit 1 = only standard models available

set -uo pipefail

# ── Reasoning model patterns (in priority order) ──────────────────────────────
# Format: "alias|pattern-to-match-in-model-id" (basic regex, matched per line).
# "/o3" catches provider-prefixed ids (openai/o3); "^o3" catches the bare ids
# used by Codex and the OpenAI API (o3, o3-pro, o3-mini).
REASONING_PATTERNS=(
  "o3|/o3"
  "o3|^o3"
  "o1|/o1"
  "o1|^o1"
  "deepthink|deepthink"
  "deepseek|deepseek-r1"
  "deepseek|deepseek/r1"
)

# ── Strong non-reasoning models (excellent for math, not pure reasoning) ──────
STRONG_PATTERNS=(
  "opus|claude-opus-4"
  "opus|claude-opus-3"
)

CONFIGURED_MODELS=""

add_models() {
  local new="$1"
  [[ -z "$new" ]] && return 0
  CONFIGURED_MODELS="${CONFIGURED_MODELS}
${new}"
}

# ── 1. Environment variables used by common agent harnesses ───────────────────
for var in OPENCLAW_MODEL ANTHROPIC_MODEL CLAUDE_MODEL OPENAI_MODEL \
           GEMINI_MODEL CODEX_MODEL MODEL; do
  val="${!var:-}"
  [[ -n "$val" ]] && add_models "$(echo "$val" | tr '[:upper:]' '[:lower:]')"
done

# ── 2. JSON config files (OpenClaw, Claude Code, Gemini) ──────────────────────
# A generic walk collects every string found under any key containing "model"
# (including dict keys, e.g. OpenClaw's agents.defaults.models map). This works
# across config schemas without hardcoding any one agent's structure.
JSON_CONFIG_PATHS=(
  "${HOME}/.openclaw/config.json"
  "${HOME}/.openclaw/openclaw.json"
  "${HOME}/.claude/settings.json"
  "${HOME}/.gemini/settings.json"
)

PYTHON="$(command -v python3 2>/dev/null || true)"

if [[ -n "$PYTHON" ]]; then
  for config_path in "${JSON_CONFIG_PATHS[@]}"; do
    [[ -f "$config_path" ]] || continue
    add_models "$("$PYTHON" - "$config_path" 2>/dev/null <<'PYEOF' || true
import json, sys

def strings(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield k
            yield from strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from strings(v)
    elif isinstance(obj, str):
        yield obj

def collect(obj):
    found = set()
    if isinstance(obj, dict):
        for k, v in obj.items():
            if "model" in k.lower():
                if isinstance(v, str):
                    found.add(v.lower())
                else:
                    found.update(s.lower() for s in strings(v))
            else:
                found |= collect(v)
    elif isinstance(obj, list):
        for v in obj:
            found |= collect(v)
    return found

try:
    with open(sys.argv[1]) as f:
        cfg = json.load(f)
    for m in sorted(collect(cfg)):
        print(m)
except Exception:
    pass
PYEOF
)"
  done
fi

# ── 3. TOML config files (Codex) ──────────────────────────────────────────────
# Parsed with grep/sed so no TOML library is required.
TOML_CONFIG_PATHS=(
  "${HOME}/.codex/config.toml"
)

for config_path in "${TOML_CONFIG_PATHS[@]}"; do
  [[ -f "$config_path" ]] || continue
  add_models "$(grep -E '^[[:space:]]*model[[:space:]]*=' "$config_path" 2>/dev/null \
    | sed -E 's/^[^=]*=[[:space:]]*"?([^"#]*)"?.*$/\1/' \
    | tr '[:upper:]' '[:lower:]' | tr -d ' ' || true)"
done

# ── Match against a pattern list ──────────────────────────────────────────────
check_patterns() {
  local -n patterns=$1
  for entry in "${patterns[@]}"; do
    local alias="${entry%%|*}"
    local substr="${entry##*|}"
    local match
    match=$(echo "$CONFIGURED_MODELS" | grep -i "$substr" | head -1 || true)
    if [[ -n "$match" ]]; then
      echo "$alias $match"
      return 0
    fi
  done
  return 1
}

# ── Check Tier 1: Reasoning models ───────────────────────────────────────────
if result=$(check_patterns REASONING_PATTERNS 2>/dev/null); then
  echo "FOUND_REASONING $result"
  exit 0
fi

# ── Check Tier 2: Strong non-reasoning ───────────────────────────────────────
if result=$(check_patterns STRONG_PATTERNS 2>/dev/null); then
  echo "FOUND_STRONG $result"
  exit 0
fi

# ── Nothing useful found ──────────────────────────────────────────────────────
echo "NONE"
exit 1
