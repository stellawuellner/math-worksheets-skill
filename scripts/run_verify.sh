#!/usr/bin/env bash
# run_verify.sh — Run worksheet answer verification
# Usage: run_verify.sh <verify_TOPIC_DATE.json>
#
# Passes the JSON verification file to the bundled verify.py script.
# No code is generated or executed from user input — only structured
# data (the JSON file) is evaluated by the fixed verify.py.
#
# Requires: python3 with sympy installed
#   pip3 install sympy
#
# Exit codes:
#   0 — all automated checks passed — safe to compile
#   1 — one or more checks FAILED — fix answer key before compiling
#   2 — manual review needed — no automated failures, safe to compile

set -uo pipefail

JSON_FILE="${1:-}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VERIFY_PY="${SCRIPT_DIR}/verify.py"

if [[ -z "$JSON_FILE" ]]; then
  echo "Usage: run_verify.sh <verify_TOPIC_DATE.json>" >&2
  exit 1
fi

if [[ ! -f "$JSON_FILE" ]]; then
  echo "Error: verification file not found: $JSON_FILE" >&2
  exit 1
fi

# ── Find a Python 3 that has sympy ────────────────────────────────────────────
# Shared finder (scripts/find_python.sh): prefers the first candidate that can
# `import sympy` instead of the first that merely exists — the old loop picked
# a sympy-less python and gave up while a working one sat next in line.
source "${SCRIPT_DIR}/find_python.sh"
PYTHON="$(find_sympy_python)" || exit 1

# ── Run the fixed verification script ────────────────────────────────────────
"$PYTHON" "$VERIFY_PY" "$JSON_FILE"
EXIT_CODE=$?

exit $EXIT_CODE
