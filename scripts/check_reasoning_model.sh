#!/usr/bin/env bash
# check_reasoning_model.sh — Detect the best available reasoning model for math
#
# Model rankings are fetched from a hosted JSON (7-day cache) so recommendations
# stay current as new models ship. Falls back to bundled JSON, then hardcoded defaults.
#
# Outputs one line: "<STATUS> <alias> <full-model-id>"
#   STATUS = FOUND_REASONING | FOUND_STRONG | NONE
#
# Exit 0 = usable model found (FOUND_REASONING or FOUND_STRONG)
# Exit 1 = only standard models available (NONE)

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG="${HOME}/.openclaw/openclaw.json"

# ── Hardcoded defaults (last-resort fallback if JSON unavailable) ─────────────
HARDCODED_REASONING=(
  "o3|openai/o3"
  "o1|openai/o1"
  "deepthink|gemini-2.5-pro-deepthink"
  "deepthink|gemini-2.0-pro-deepthink"
  "deepseek|deepseek-r1"
)
HARDCODED_STRONG=(
  "opus|claude-opus-4"
  "opus|claude-opus-3-5"
)

# ── Read configured models from OpenClaw ─────────────────────────────────────
if [[ ! -f "$CONFIG" ]]; then
  echo "NONE (openclaw config not found)" >&2
  exit 1
fi

CONFIGURED_MODELS=$(python3 -c "
import json
with open('$CONFIG') as f:
    cfg = json.load(f)
models = set()
defaults = cfg.get('agents', {}).get('defaults', {})
for key in defaults.get('models', {}).keys():
    models.add(key.lower())
model_cfg = defaults.get('model', {})
for m in [model_cfg.get('primary', '')] + model_cfg.get('fallbacks', []):
    if m: models.add(m.lower())
for m in sorted(models): print(m)
" 2>/dev/null || true)

if [[ -z "$CONFIGURED_MODELS" ]]; then
  echo "NONE (could not parse openclaw config)" >&2
  exit 1
fi

# ── Try to load JSON rankings (fetched > bundled > hardcoded) ─────────────────
check_from_json() {
  local json_file="$1"
  local tier="$2"

  python3 -c "
import json, sys
with open('$json_file') as f:
    rankings = json.load(f)

configured = '''$CONFIGURED_MODELS'''.strip().split('\n')
tier_data = rankings.get('tiers', {}).get('$tier', {})
for entry in tier_data.get('patterns', []):
    alias = entry['alias']
    pattern = entry['match'].lower()
    for model in configured:
        if pattern in model:
            print(f'{alias} {model}')
            sys.exit(0)
sys.exit(1)
" 2>/dev/null
}

check_from_list() {
  local -n patterns=$1
  for entry in "${patterns[@]}"; do
    local alias="${entry%%|*}"
    local pattern="${entry##*|}"
    local match
    match=$(echo "$CONFIGURED_MODELS" | grep -i "$pattern" | head -1 || true)
    if [[ -n "$match" ]]; then
      echo "$alias $match"
      return 0
    fi
  done
  return 1
}

# ── Resolve model config file ─────────────────────────────────────────────────
CONFIG_JSON=$(bash "$SKILL_DIR/scripts/fetch_model_config.sh" 2>/dev/null || echo "NONE")

# ── Check Tier 1: Reasoning models ───────────────────────────────────────────
if [[ "$CONFIG_JSON" != "NONE" && -f "$CONFIG_JSON" ]]; then
  result=$(check_from_json "$CONFIG_JSON" "FOUND_REASONING" 2>/dev/null || true)
  if [[ -n "$result" ]]; then
    echo "FOUND_REASONING $result"
    exit 0
  fi
fi
# Hardcoded fallback for Tier 1
if result=$(check_from_list HARDCODED_REASONING 2>/dev/null); then
  echo "FOUND_REASONING $result"
  exit 0
fi

# ── Check Tier 2: Strong non-reasoning ───────────────────────────────────────
if [[ "$CONFIG_JSON" != "NONE" && -f "$CONFIG_JSON" ]]; then
  result=$(check_from_json "$CONFIG_JSON" "FOUND_STRONG" 2>/dev/null || true)
  if [[ -n "$result" ]]; then
    echo "FOUND_STRONG $result"
    exit 0
  fi
fi
# Hardcoded fallback for Tier 2
if result=$(check_from_list HARDCODED_STRONG 2>/dev/null); then
  echo "FOUND_STRONG $result"
  exit 0
fi

# ── Nothing useful ────────────────────────────────────────────────────────────
echo "NONE"
exit 1
