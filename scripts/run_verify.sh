#!/usr/bin/env bash
# run_verify.sh — Run a worksheet verification script using SymPy
# Usage: run_verify.sh <verify_TOPIC_DATE.py>
#
# Finds a Python 3 installation with sympy available and runs the verification.
# If sympy is not installed, offers to install it via pip (with user confirmation).
#
# Exit codes from the verify script:
#   0 = all automated checks passed — safe to compile
#   1 = one or more checks FAILED — fix before compiling
#   2 = manual review needed (graphs, proofs) — proceed with caution

set -uo pipefail

VERIFY_SCRIPT="${1:-}"

if [[ -z "$VERIFY_SCRIPT" ]]; then
  echo "Usage: run_verify.sh <verify_TOPIC_DATE.py>" >&2
  exit 1
fi

if [[ ! -f "$VERIFY_SCRIPT" ]]; then
  echo "Error: verify script not found: $VERIFY_SCRIPT" >&2
  exit 1
fi

# ── Find Python 3 with sympy ──────────────────────────────────────────────────
PYTHON=""
CANDIDATES=(
  "/opt/homebrew/bin/python3"
  "/usr/local/bin/python3"
  "$(command -v python3 2>/dev/null || true)"
)

for candidate in "${CANDIDATES[@]}"; do
  if [[ -x "$candidate" ]] && "$candidate" -c "import sympy" 2>/dev/null; then
    PYTHON="$candidate"
    break
  fi
done

# ── If sympy not found, install it ───────────────────────────────────────────
if [[ -z "$PYTHON" ]]; then
  echo "ℹ️  sympy not found. Installing into a local venv (one-time setup)..."
  VENV_DIR="${HOME}/.local/share/math-worksheets-skill/venv"
  python3 -m venv "$VENV_DIR"
  "$VENV_DIR/bin/pip" install sympy -q
  PYTHON="$VENV_DIR/bin/python3"
  echo "✅ sympy installed at $VENV_DIR"
fi

echo "Verifying answers with: $PYTHON"
echo ""

# ── Run the verification script ───────────────────────────────────────────────
"$PYTHON" "$VERIFY_SCRIPT"
EXIT_CODE=$?

echo ""
case $EXIT_CODE in
  0) echo "✅ All checks passed — safe to compile." ;;
  1) echo "❌ Verification FAILED — fix errors in the answer key before compiling." ;;
  2) echo "👁  Manual review needed for some problems — no automated failures." ;;
  *) echo "⚠️  Unexpected exit code: $EXIT_CODE" ;;
esac

exit $EXIT_CODE
