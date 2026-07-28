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

# Layout fixture pairs beyond the original enumerate pair, same contract
# (bad exits nonzero, good exits 0):
#   probstyle — \problem-macro sheets; the checker used to see only enumerate
#               lists, so a zero-workspace \problem sheet passed VACUOUSLY
#   pagebreak — workspace \vspace outside a minipage is discarded at page
#               breaks (the good twin wraps it in the unbreakable minipage)
#   lineskip  — \\[5cm] is real writing room; rejecting it taught generators
#               to route around the gate (false positive, must PASS)
#   negspace  — itemsep=3cm minus \vspace{-2.9cm} leaves 0.1cm; an unsigned
#               regex credited the full 3cm (false negative, must FAIL)
LAYOUT_PAIRS=(
  "layout_bad_probstyle.tex:fail"
  "layout_good_probstyle.tex:pass"
  "layout_bad_pagebreak.tex:fail"
  "layout_good_pagebreak.tex:pass"
  "layout_good_lineskip.tex:pass"
  "layout_bad_negspace.tex:fail"
)
for pair in "${LAYOUT_PAIRS[@]}"; do
  fixture="${pair%%:*}"
  want="${pair##*:}"
  [ -f "$FIXTURES/$fixture" ] || { echo "❌ missing fixture $fixture"; exit 1; }
  if python3 "$SCRIPT_DIR/check_layout.py" "$FIXTURES/$fixture" >/dev/null 2>&1; then
    got="pass"
  else
    got="fail"
  fi
  if [ "$got" = "$want" ]; then
    echo "✅ check_layout: $fixture -> $got (as expected)"
  else
    echo "❌ check_layout: $fixture -> $got, expected $want"; exit 1
  fi
done

# Zero-parse guard: a sheet with no enumerate list and no \problem block was
# checked against NOTHING — that must be exit 2 specifically, never a pass.
ZERO_TEX="$(mktemp "${TMPDIR:-/tmp}/layout_zero.XXXXXX.tex")"
printf '\\documentclass{article}\\begin{document}Nothing here\\end{document}\n' > "$ZERO_TEX"
python3 "$SCRIPT_DIR/check_layout.py" "$ZERO_TEX" >/dev/null 2>&1
zero_got=$?
rm -f "$ZERO_TEX"
if [ "$zero_got" -eq 2 ]; then
  echo "✅ check_layout exits 2 on a sheet where zero problems parse"
else
  echo "❌ check_layout zero-parse: expected exit 2, got $zero_got"; exit 1
fi

# Log hygiene (scripts/check_log.py, the gate compile.sh runs on the kept
# TeX log). CI has no LaTeX engine, so the gate is fixture-tested on saved
# log snippets: undefined refs / missing chars / big overfulls must FAIL,
# a clean log with only sub-threshold overfulls must PASS.
if python3 "$SCRIPT_DIR/../scripts/check_log.py" "$FIXTURES/texlog_bad.log" >/dev/null 2>&1; then
  echo "❌ check_log did NOT flag texlog_bad.log"; exit 1
else
  echo "✅ check_log flags texlog_bad.log"
fi
if python3 "$SCRIPT_DIR/../scripts/check_log.py" "$FIXTURES/texlog_ok.log" >/dev/null 2>&1; then
  echo "✅ check_log passes texlog_ok.log"
else
  echo "❌ check_log wrongly flagged texlog_ok.log"; exit 1
fi
