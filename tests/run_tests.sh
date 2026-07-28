#!/usr/bin/env bash
# run_tests.sh — Regression tests for scripts/verify.py
#
# Each fixture encodes an expected exit code:
#   0 = all checks pass    1 = failures (wrong answers, bad schema, injection)
#   2 = manual review needed
#
# The injection fixture additionally asserts that no injected command output
# appears — i.e. disallowed expressions are rejected, not executed.
#
# Usage: bash tests/run_tests.sh
# Exit 0 = all tests pass.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VERIFY_PY="${SCRIPT_DIR}/../scripts/verify.py"
FIXTURES="${SCRIPT_DIR}/fixtures"

PYTHON="$(command -v python3 2>/dev/null || true)"
if [[ -z "$PYTHON" ]]; then
  echo "Error: python3 not found" >&2
  exit 1
fi
if ! "$PYTHON" -c "import sympy" 2>/dev/null; then
  echo "Error: sympy is not installed (pip3 install sympy)" >&2
  exit 1
fi

# fixture:expected_exit
CASES=(
  "pass_algebra.json:0"
  "pass_calculus.json:0"
  "pass_geometry.json:0"
  "fail_wrong_answers.json:1"
  "fail_geometry.json:1"
  "manual_only.json:2"
  "reject_injection.json:1"
  "reject_bad_schema.json:1"
  "reject_coverage_gap.json:1"
  "pass_coverage_types.json:0"
  "fail_coverage_types.json:1"
  "pass_stats_prob.json:0"
  "fail_stats_prob.json:1"
  "pass_data_calc.json:0"
  "fail_data_calc.json:1"
  "pass_reclaimed.json:0"
  "fail_reclaimed.json:1"
  "figs_demo.json:0"
  "fail_figure_schema.json:1"
)

failures=0

for case in "${CASES[@]}"; do
  fixture="${case%%:*}"
  want="${case##*:}"
  output=$("$PYTHON" "$VERIFY_PY" "$FIXTURES/$fixture" 2>&1)
  got=$?
  if [[ "$got" -ne "$want" ]]; then
    echo "❌ $fixture: expected exit $want, got $got"
    echo "$output" | sed 's/^/     /'
    failures=$((failures + 1))
  else
    echo "✅ $fixture: exit $got"
  fi
  # -x: the marker alone on a line means `echo` actually ran; the rejection
  # message quotes the expression inline, which must not count as a failure.
  if [[ "$fixture" == "reject_injection.json" ]] && echo "$output" | grep -qx "PWNED-MARKER"; then
    echo "❌ $fixture: injected command output detected — expression was EXECUTED"
    failures=$((failures + 1))
  fi
done

echo
if [[ "$failures" -gt 0 ]]; then
  echo "❌ $failures test(s) failed"
  exit 1
fi
echo "✅ All tests passed"

# Layout rules (figure scope + work space). Fixture-driven: a known-bad sheet
# must fail and a known-good one must pass, so the checker itself is tested.
if [ -f tests/fixtures/layout_bad.tex ]; then
  echo
  if python3 tests/check_layout.py tests/fixtures/layout_bad.tex >/dev/null 2>&1; then
    echo "❌ check_layout did NOT flag layout_bad.tex"; exit 1
  else
    echo "✅ check_layout flags layout_bad.tex"
  fi
  if python3 tests/check_layout.py tests/fixtures/layout_good.tex >/dev/null 2>&1; then
    echo "✅ check_layout passes layout_good.tex"
  else
    echo "❌ check_layout wrongly flagged layout_good.tex"; exit 1
  fi
fi

# Rendered figures (scripts/render_figures.py). Construction is the guarantee —
# the property suite parses the emitted TikZ (no LaTeX engine in CI) — and the
# checkers' \probfig sight-line is fixture-tested: a figs file rendered from
# OLD givens must be flagged against the edited JSON, a fresh one must pass,
# blind invocation (no --figs) must be loud, and a mixed \probfig/bare list
# must fail the all-or-nothing figure-scope rule even without the figs file.
if [ -f tests/fixtures/figs_demo.json ]; then
  echo
  output=$("$PYTHON" tests/test_render_figures.py 2>&1)
  if [ $? -ne 0 ]; then
    echo "❌ test_render_figures.py failed"
    echo "$output" | sed 's/^/     /'
    exit 1
  fi
  echo "✅ test_render_figures.py (renderer property suite)"

  FIGS_TMP="$(mktemp -d)/figs_demo.tex"
  if ! "$PYTHON" scripts/render_figures.py tests/fixtures/figs_demo.json "$FIGS_TMP" >/dev/null 2>&1; then
    echo "❌ render_figures.py failed on figs_demo.json"; exit 1
  fi
  echo "✅ render_figures.py renders figs_demo.json"

  output=$(python3 tests/check_prose_consistency.py tests/fixtures/ws_probfig_stale.tex \
           tests/fixtures/figs_demo_edited.json --figs "$FIGS_TMP" 2>&1)
  if echo "$output" | grep -q "figure shows"; then
    echo "✅ check_prose flags a STALE figs file (CASE-21 sighted through \\probfig)"
  else
    echo "❌ check_prose missed the stale figure label"
    echo "$output" | sed 's/^/     /'; exit 1
  fi

  output=$(python3 tests/check_prose_consistency.py tests/fixtures/ws_probfig.tex \
           tests/fixtures/figs_demo.json --figs "$FIGS_TMP" 2>&1)
  if echo "$output" | grep -q "Figure labels: all consistent"; then
    echo "✅ check_prose passes fresh figs"
  else
    echo "❌ check_prose wrongly flagged fresh figs"
    echo "$output" | sed 's/^/     /'; exit 1
  fi

  python3 tests/check_prose_consistency.py tests/fixtures/ws_probfig.tex \
    tests/fixtures/figs_demo.json >/dev/null 2>&1
  if [ $? -eq 2 ]; then
    echo "✅ check_prose is LOUD when \\probfig is unresolved (exit 2, not a silent pass)"
  else
    echo "❌ check_prose ran blind past unresolved \\probfig"; exit 1
  fi

  if python3 tests/check_layout.py tests/fixtures/ws_probfig_mixed.tex >/dev/null 2>&1; then
    echo "❌ check_layout did NOT flag the mixed \\probfig/bare list"; exit 1
  else
    echo "✅ check_layout flags a mixed \\probfig/bare list (\\probfig counts as valued)"
  fi
  if python3 tests/check_layout.py tests/fixtures/ws_probfig.tex --figs "$FIGS_TMP" >/dev/null 2>&1; then
    echo "✅ check_layout passes the all-\\probfig sheet (spliced)"
  else
    echo "❌ check_layout wrongly flagged the all-\\probfig sheet"; exit 1
  fi
fi
