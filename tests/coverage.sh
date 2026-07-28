#!/usr/bin/env bash
# coverage.sh — run every test suite under coverage and enforce a floor.
# Used by CI and locally. Requires: pip install coverage
set -uo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"

FAIL_UNDER="${COVERAGE_FAIL_UNDER:-90}"

python3 -m coverage erase

# every fixture through the verifier
for f in tests/fixtures/*.json; do
  python3 -m coverage run --source=scripts -a scripts/verify.py "$f" >/dev/null 2>&1
done

# the python test suites (each exits nonzero on failure)
rc=0
for t in test_audit_fixes test_error_paths test_branches test_render_figures; do
  if ! python3 -m coverage run --source=scripts -a "tests/$t.py"; then
    echo "❌ tests/$t.py FAILED"
    rc=1
  fi
done

echo
python3 -m coverage report -m
python3 -m coverage report --fail-under="$FAIL_UNDER" >/dev/null || {
  echo "❌ coverage below ${FAIL_UNDER}%"
  rc=1
}

exit $rc
