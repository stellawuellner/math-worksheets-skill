#!/usr/bin/env bash
# run_verify.sh — Run a worksheet verification script
# Usage: run_verify.sh <verify_TOPIC_DATE.py>
#
# Finds a Python with sympy available, runs the verification, and
# gates on exit code (0=pass, 1=fail, 2=manual review needed).

set -euo pipefail

VERIFY_SCRIPT="${1:-}"

if [[ -z "$VERIFY_SCRIPT" ]]; then
  echo "Usage: run_verify.sh <verify_TOPIC_DATE.py>" >&2
  exit 1
fi

if [[ ! -f "$VERIFY_SCRIPT" ]]; then
  echo "Error: verify script not found: $VERIFY_SCRIPT" >&2
  exit 1
fi

# ── Find Python with sympy ────────────────────────────────────────────────────
PYTHON=""
CANDIDATES=(
  "/tmp/skill-venv/bin/python3"
  "/tmp/mlx-audio-venv/bin/python3"
  "$(command -v python3 2>/dev/null || true)"
  "/opt/homebrew/bin/python3"
)

for candidate in "${CANDIDATES[@]}"; do
  if [[ -x "$candidate" ]] && "$candidate" -c "import sympy" 2>/dev/null; then
    PYTHON="$candidate"
    break
  fi
done

if [[ -z "$PYTHON" ]]; then
  echo "⚠️  sympy not found. Installing in a temp venv..."
  python3 -m venv /tmp/worksheet-verify-venv
  /tmp/worksheet-verify-venv/bin/pip install sympy -q
  PYTHON="/tmp/worksheet-verify-venv/bin/python3"
fi

echo "Verifying with: $PYTHON"
echo ""

# ── Run verification ──────────────────────────────────────────────────────────
"$PYTHON" "$VERIFY_SCRIPT"
EXIT_CODE=$?

case $EXIT_CODE in
  0) echo "✅ Verification passed — proceed to compile." ;;
  1) echo "❌ Verification FAILED — fix errors before compiling." ;;
  2) echo "👁  Manual review needed — no automated failures." ;;
esac

exit $EXIT_CODE
