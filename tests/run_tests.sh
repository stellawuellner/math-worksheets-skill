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
  "reject_bigtol.json:1"
  "pass_bigtol_reason.json:2"
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
  layout_out=$(python3 tests/check_layout.py tests/fixtures/layout_bad.tex 2>&1)
  if [ $? -eq 0 ]; then
    echo "❌ check_layout did NOT flag layout_bad.tex"; exit 1
  else
    echo "✅ check_layout flags layout_bad.tex"
  fi
  # the optional-arg macro figure (\rtfig[scale=..]) must be SEEN: list 2 of
  # layout_bad is a fault only if the detector matches through the [..] arg —
  # exit code alone can't prove it (list 1 already fails the file)
  if echo "$layout_out" | grep -q "list 2:"; then
    echo "✅ check_layout sees \\rtfig[scale=..] as a valued figure (list 2 fault)"
  else
    echo "❌ check_layout missed the optional-arg macro figure — list 2 not flagged"
    exit 1
  fi
  if python3 tests/check_layout.py tests/fixtures/layout_good.tex >/dev/null 2>&1; then
    echo "✅ check_layout passes layout_good.tex"
  else
    echo "❌ check_layout wrongly flagged layout_good.tex"; exit 1
  fi
fi

# ── build.sh driver + template staging + python finder ───────────────────────
# The driver's contract is its exit-code map, so that is what gets fixture-
# tested: run_verify's 2 must CONTINUE (manual review) while a verify FAIL
# must stop BEFORE any compile. CI has no LaTeX engine — compiles run against
# a stub tectonic that records each invocation and emits the PDF compile.sh
# checks for, so these tests never need a real engine.
if [ -f tests/fixtures/trio/ws_build_demo.tex ]; then
  echo
  WORK="$(mktemp -d)"
  trap 'rm -rf "$WORK"' EXIT
  mkdir -p "$WORK/bin"
  cat > "$WORK/bin/tectonic" <<'EOS'
#!/usr/bin/env bash
# stub engine: record the call, emit the PDF compile.sh checks for
tex=""; out="."
while [ $# -gt 0 ]; do
  case "$1" in --outdir) out="$2"; shift 2 ;; -*) shift ;; *) tex="$1"; shift ;; esac
done
echo "$tex" >> "${TECTONIC_MARKER:?}"
touch "$out/$(basename "${tex%.tex}").pdf"
# compile.sh pipes engine output through grep -v under pipefail: emit at least
# one non-filtered line so the stub's silence is not mistaken for a failure
echo "stub tectonic: compiled $(basename "$tex")"
EOS
  chmod +x "$WORK/bin/tectonic"

  build_case() {  # name  expected-exit  json-to-use  [ak-override-file]
    local name="$1" want="$2" json="$3" ak="${4:-ak_build_demo.tex}"
    local dir="$WORK/$name" out got
    mkdir -p "$dir"
    cp tests/fixtures/trio/ws_build_demo.tex "$dir/ws_build_demo.tex"
    cp "tests/fixtures/trio/$ak" "$dir/ak_build_demo.tex"
    cp tests/fixtures/trio/ss_build_demo.tex "$dir/ss_build_demo.tex"
    cp "tests/fixtures/trio/$json" "$dir/verify_build_demo.json"
    cp tests/fixtures/trio/verify_ss_build_demo.json "$dir/verify_ss_build_demo.json"
    export TECTONIC_MARKER="$dir/compile_calls"
    out=$(PATH="$WORK/bin:$PATH" bash scripts/build.sh "$dir/verify_build_demo.json" \
          --outdir "$dir/out" 2>&1)
    got=$?
    if [ "$got" -ne "$want" ]; then
      echo "❌ build.sh $name: expected exit $want, got $got"
      echo "$out" | sed 's/^/     /'
      exit 1
    fi
    echo "✅ build.sh $name: exit $got"
  }

  build_case green 0 verify_build_demo.json
  if [ "$(wc -l < "$WORK/green/compile_calls")" -ne 3 ]; then
    echo "❌ build.sh green: expected 3 compile invocations"; exit 1
  fi
  echo "✅ build.sh green: compiled all three documents"

  # a failed verification must stop the run BEFORE any compile
  build_case broken-verify 1 verify_build_demo_broken.json
  if [ -f "$WORK/broken-verify/compile_calls" ]; then
    echo "❌ build.sh broken-verify: compiled despite a failed verify gate"; exit 1
  fi
  echo "✅ build.sh broken-verify: zero compile invocations (fail-fast held)"

  # run_verify's exit 2 (manual review) must continue, and the build ends 2
  build_case manual 2 verify_build_demo_manual.json

  # a wrong boxed answer fails the answer-key gate (after compiles — the gate
  # still fails the build)
  build_case broken-ak 1 verify_build_demo.json ak_build_demo_broken.tex

  # missing ss is a structural error, not a skip — unless --worksheet-only
  dir="$WORK/no-ss"; mkdir -p "$dir"
  cp tests/fixtures/trio/ws_build_demo.tex "$dir/ws_build_demo.tex"
  cp tests/fixtures/trio/ak_build_demo.tex "$dir/ak_build_demo.tex"
  cp tests/fixtures/trio/verify_build_demo.json "$dir/verify_build_demo.json"
  export TECTONIC_MARKER="$dir/compile_calls"
  if PATH="$WORK/bin:$PATH" bash scripts/build.sh "$dir/verify_build_demo.json" \
       --outdir "$dir/out" >/dev/null 2>&1; then
    echo "❌ build.sh no-ss: missing study guide passed"; exit 1
  fi
  echo "✅ build.sh no-ss: missing study guide is a hard failure"
  if PATH="$WORK/bin:$PATH" bash scripts/build.sh "$dir/verify_build_demo.json" \
       --outdir "$dir/out" --worksheet-only >/dev/null 2>&1; then
    echo "✅ build.sh no-ss --worksheet-only: worksheet alone builds"
  else
    echo "❌ build.sh no-ss --worksheet-only: should have passed"; exit 1
  fi

  # ambiguous discovery (two ws_ candidates) must be a named error
  dir="$WORK/ambig"; mkdir -p "$dir"
  cp tests/fixtures/trio/ws_build_demo.tex "$dir/ws_build_demo.tex"
  cp tests/fixtures/trio/ws_build_demo.tex "$dir/leo_ws_build_demo.tex"
  cp tests/fixtures/trio/ak_build_demo.tex "$dir/ak_build_demo.tex"
  cp tests/fixtures/trio/ss_build_demo.tex "$dir/ss_build_demo.tex"
  cp tests/fixtures/trio/verify_build_demo.json "$dir/verify_build_demo.json"
  cp tests/fixtures/trio/verify_ss_build_demo.json "$dir/verify_ss_build_demo.json"
  export TECTONIC_MARKER="$dir/compile_calls"
  out=$(PATH="$WORK/bin:$PATH" bash scripts/build.sh "$dir/verify_build_demo.json" \
        --outdir "$dir/out" 2>&1)
  if [ $? -eq 1 ] && echo "$out" | grep -q "ambiguous"; then
    echo "✅ build.sh ambig: two ws_ candidates rejected by name"
  else
    echo "❌ build.sh ambig: expected a named 'ambiguous' failure"
    echo "$out" | sed 's/^/     /'; exit 1
  fi

  # ── compile.sh template staging ────────────────────────────────────────────
  # A .tex that \inputs a shipped template gets the templates copied beside
  # it; one that doesn't must NOT trigger the copy (negative control).
  dir="$WORK/staging"; mkdir -p "$dir"
  printf '%s\n' '\documentclass{article}' '\input{worksheet-preamble}' \
    '\begin{document}x\end{document}' > "$dir/uses_template.tex"
  export TECTONIC_MARKER="$dir/compile_calls"
  if PATH="$WORK/bin:$PATH" bash scripts/compile.sh "$dir/uses_template.tex" "$dir" \
       >/dev/null 2>&1 && [ -f "$dir/worksheet-preamble.tex" ] \
       && [ -f "$dir/figure-macros.tex" ]; then
    echo "✅ compile.sh stages templates beside a .tex that \\inputs them"
  else
    echo "❌ compile.sh did not stage templates next to the target"; exit 1
  fi
  dir="$WORK/nostaging"; mkdir -p "$dir"
  printf '%s\n' '\documentclass{article}' '\begin{document}x\end{document}' \
    > "$dir/plain.tex"
  export TECTONIC_MARKER="$dir/compile_calls"
  PATH="$WORK/bin:$PATH" bash scripts/compile.sh "$dir/plain.tex" "$dir" >/dev/null 2>&1
  if [ -f "$dir/worksheet-preamble.tex" ]; then
    echo "❌ compile.sh staged templates into a document that never asked"; exit 1
  fi
  echo "✅ compile.sh leaves template-free documents alone"

  # ── run_verify.sh python finder ────────────────────────────────────────────
  # Must prefer a python that can import sympy over one that merely exists
  # (audit D1b), and when none qualifies, teach the interpreter-specific fix.
  cat > "$WORK/nosympy" <<'EOS'
#!/usr/bin/env bash
# fake python3 without sympy: fails the import probe, unusable otherwise
if [ "${1:-}" = "-c" ] && [ "${2:-}" = "import sympy" ]; then exit 1; fi
exit 97
EOS
  chmod +x "$WORK/nosympy"
  if MWS_PYTHON_CANDIDATES="$WORK/nosympy $PYTHON" \
       bash scripts/run_verify.sh tests/fixtures/pass_algebra.json >/dev/null 2>&1; then
    echo "✅ run_verify.sh skips a sympy-less python for the next candidate"
  else
    echo "❌ run_verify.sh gave up on the first (sympy-less) python"; exit 1
  fi
  out=$(MWS_PYTHON_CANDIDATES="$WORK/nosympy" \
        bash scripts/run_verify.sh tests/fixtures/pass_algebra.json 2>&1)
  if [ $? -ne 0 ] && echo "$out" | grep -q -- "-m pip install sympy"; then
    echo "✅ run_verify.sh with no sympy anywhere teaches the exact install command"
  else
    echo "❌ run_verify.sh no-sympy hint missing or wrong exit"
    echo "$out" | sed 's/^/     /'; exit 1
  fi

  echo
  echo "✅ driver, staging, and finder tests passed"
fi
