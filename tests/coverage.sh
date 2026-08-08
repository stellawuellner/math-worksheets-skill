#!/usr/bin/env bash
# coverage.sh — run every test suite under coverage and enforce a floor.
# Used by CI and locally. Requires: pip install coverage
set -uo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"

# 93, not the current 94.6: the floor is a ratchet against regression, not a
# target, and a point of margin keeps environment variance (a skipped TeX
# suite on a minimal machine) from flapping the gate. Raised from 90 after the
# 2026-08-08 coverage pass; raise it again only after the number has settled.
FAIL_UNDER="${COVERAGE_FAIL_UNDER:-93}"
source "$DIR/scripts/find_python.sh"
PYTHON="$(find_sympy_python)" || exit 1

"$PYTHON" -m coverage erase

# every fixture through the verifier
for f in tests/fixtures/*.json; do
  "$PYTHON" -m coverage run --source=scripts -a scripts/verify.py "$f" >/dev/null 2>&1
done

# The python test suites (each exits nonzero on failure).
#
# THIS LIST IS DERIVED, NOT MAINTAINED BY HAND. It was hand-maintained once and
# drifted: eleven wired suites — including every suite added for the slot gate,
# the figure house style and the calibration seeder — never ran under coverage,
# so the reported percentage described a shrinking fraction of the tests while
# reading like a whole-project number. Globbing means a new suite is measured
# the day it lands, and `tests/run_tests.sh` stays the place that decides what
# is wired.
rc=0
for t in tests/test_*.py tests/visual_regression.py; do
  if ! "$PYTHON" -m coverage run --source=scripts -a "$t"; then
    echo "❌ $t FAILED"
    rc=1
  fi
done

echo
"$PYTHON" -m coverage report -m
"$PYTHON" -m coverage report --fail-under="$FAIL_UNDER" >/dev/null || {
  echo "❌ coverage below ${FAIL_UNDER}%"
  rc=1
}

exit $rc
