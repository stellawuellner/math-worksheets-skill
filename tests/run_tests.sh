#!/usr/bin/env bash
# run_tests.sh — Regression tests for scripts/verify.py and the binding
# checkers (check_layout.py, check_answer_key.py).
#
# Each fixture encodes an expected exit code:
#   0 = all checks pass    1 = failures (wrong answers, bad schema, injection)
#   2 = manual review needed
#
# The injection fixture additionally asserts that no injected command output
# appears — i.e. disallowed expressions are rejected, not executed.
#
# Usage: bash tests/run_tests.sh   (from any cwd)
# Exit 0 = all tests pass. A missing fixture is a hard FAILURE, never a skip:
# the layout block once sat behind a cwd-relative [ -f ... ] guard and
# silently vanished when the suite ran from outside the repo root, printing
# a false "All tests passed" — the exact false-green class this suite exists
# to kill. The final summary counts what actually ran.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# anchor every path: relative references can never silently miss again
cd "$SCRIPT_DIR/.." || exit 1
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

require_fixture() {
  # a deleted/renamed fixture must fail the suite loudly, not shrink it
  for f in "$@"; do
    if [[ ! -f "$FIXTURES/$f" ]]; then
      echo "❌ missing fixture $FIXTURES/$f — its suite cannot run" >&2
      exit 1
    fi
  done
}

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
  "figs_demo.json:0"
  "fail_figure_schema.json:1"
  "reject_role_value.json:1"
)

failures=0
verify_ran=0

for case in "${CASES[@]}"; do
  fixture="${case%%:*}"
  want="${case##*:}"
  require_fixture "$fixture"
  output=$("$PYTHON" "$VERIFY_PY" "$FIXTURES/$fixture" 2>&1)
  got=$?
  if [[ "$got" -ne "$want" ]]; then
    echo "❌ $fixture: expected exit $want, got $got"
    echo "$output" | sed 's/^/     /'
    failures=$((failures + 1))
  else
    echo "✅ $fixture: exit $got"
  fi
  verify_ran=$((verify_ran + 1))
  # -x: the marker alone on a line means `echo` actually ran; the rejection
  # message quotes the expression inline, which must not count as a failure.
  if [[ "$fixture" == "reject_injection.json" ]] && echo "$output" | grep -qx "PWNED-MARKER"; then
    echo "❌ $fixture: injected command output detected — expression was EXECUTED"
    failures=$((failures + 1))
  fi
done

if [[ "$failures" -gt 0 ]]; then
  echo
  echo "❌ $failures test(s) failed"
  exit 1
fi

# Layout rules (figure scope + work space). Fixture-driven: a known-bad sheet
# must fail and a known-good one must pass, so the checker itself is tested.
echo
layout_ran=0
require_fixture layout_bad.tex layout_good.tex
if "$PYTHON" "$SCRIPT_DIR/check_layout.py" "$FIXTURES/layout_bad.tex" >/dev/null 2>&1; then
  echo "❌ check_layout did NOT flag layout_bad.tex"; exit 1
else
  echo "✅ check_layout flags layout_bad.tex"
fi
layout_ran=$((layout_ran + 1))
if "$PYTHON" "$SCRIPT_DIR/check_layout.py" "$FIXTURES/layout_good.tex" >/dev/null 2>&1; then
  echo "✅ check_layout passes layout_good.tex"
else
  echo "❌ check_layout wrongly flagged layout_good.tex"; exit 1
fi
layout_ran=$((layout_ran + 1))

# the optional-arg macro figure (\rtfig[scale=..]) must be SEEN: list 2 of
# layout_bad is a fault only if the detector matches through the [..] arg —
# exit code alone can't prove it (list 1 already fails the file)
layout_out=$("$PYTHON" "$SCRIPT_DIR/check_layout.py" "$FIXTURES/layout_bad.tex" 2>&1)
if echo "$layout_out" | grep -q "list 2:"; then
  echo "✅ check_layout sees \\rtfig[scale=..] as a valued figure (list 2 fault)"
else
  echo "❌ check_layout missed the optional-arg macro figure — list 2 not flagged"
  exit 1
fi


# Rendered figures (scripts/render_figures.py). Construction is the guarantee —
# the property suite parses the emitted TikZ (no LaTeX engine in CI) — and the
# checkers' \probfig sight-line is fixture-tested: a figs file rendered from
# OLD givens must be flagged against the edited JSON, a fresh one must pass,
# blind invocation (no --figs) must be loud, and a mixed \probfig/bare list
# must fail the all-or-nothing figure-scope rule even without the figs file.
if [ -f "$FIXTURES/figs_demo.json" ]; then
  echo
  output=$("$PYTHON" "$SCRIPT_DIR/test_render_figures.py" 2>&1)
  if [ $? -ne 0 ]; then
    echo "❌ test_render_figures.py failed"
    echo "$output" | sed 's/^/     /'
    exit 1
  fi
  echo "✅ test_render_figures.py (renderer property suite)"

  FIGS_TMP="$(mktemp -d)/figs_demo.tex"
  if ! "$PYTHON" "$SCRIPT_DIR/../scripts/render_figures.py" "$FIXTURES/figs_demo.json" "$FIGS_TMP" >/dev/null 2>&1; then
    echo "❌ render_figures.py failed on figs_demo.json"; exit 1
  fi
  echo "✅ render_figures.py renders figs_demo.json"

  output=$("$PYTHON" "$SCRIPT_DIR/check_prose_consistency.py" "$FIXTURES/ws_probfig_stale.tex" \
           "$FIXTURES/figs_demo_edited.json" --figs "$FIGS_TMP" 2>&1)
  if echo "$output" | grep -q "figure shows"; then
    echo "✅ check_prose flags a STALE figs file (CASE-21 sighted through \\probfig)"
  else
    echo "❌ check_prose missed the stale figure label"
    echo "$output" | sed 's/^/     /'; exit 1
  fi

  output=$("$PYTHON" "$SCRIPT_DIR/check_prose_consistency.py" "$FIXTURES/ws_probfig.tex" \
           "$FIXTURES/figs_demo.json" --figs "$FIGS_TMP" 2>&1)
  if echo "$output" | grep -q "Figure labels: all consistent"; then
    echo "✅ check_prose passes fresh figs"
  else
    echo "❌ check_prose wrongly flagged fresh figs"
    echo "$output" | sed 's/^/     /'; exit 1
  fi

  "$PYTHON" "$SCRIPT_DIR/check_prose_consistency.py" "$FIXTURES/ws_probfig.tex" \
    "$FIXTURES/figs_demo.json" >/dev/null 2>&1
  if [ $? -eq 2 ]; then
    echo "✅ check_prose is LOUD when \\probfig is unresolved (exit 2, not a silent pass)"
  else
    echo "❌ check_prose ran blind past unresolved \\probfig"; exit 1
  fi

  if "$PYTHON" "$SCRIPT_DIR/check_layout.py" "$FIXTURES/ws_probfig_mixed.tex" >/dev/null 2>&1; then
    echo "❌ check_layout did NOT flag the mixed \\probfig/bare list"; exit 1
  else
    echo "✅ check_layout flags a mixed \\probfig/bare list (\\probfig counts as valued)"
  fi
  if "$PYTHON" "$SCRIPT_DIR/check_layout.py" "$FIXTURES/ws_probfig.tex" --figs "$FIGS_TMP" >/dev/null 2>&1; then
    echo "✅ check_layout passes the all-\\probfig sheet (spliced)"
  else
    echo "❌ check_layout wrongly flagged the all-\\probfig sheet"; exit 1
  fi
fi

# Answer-key binding (per-problem \boxed gate — audit B1/B2/B3). Same fixture
# discipline: shuffled, masked, and precision-drift keys must FAIL; template
# shapes (enumerate, nested multi-part, \problem{}, examplebox study guide)
# must segment per problem and PASS.
echo
ak_ran=0
# tex_fixture:json_fixture:expected_exit
AK_CASES=(
  "ak_bind_good.tex:ak_bind.json:0"
  "ak_bind_shuffled.tex:ak_bind.json:1"
  "ak_bind_masked.tex:ak_bind.json:1"
  "ak_bind_precision.tex:ak_bind.json:1"
  "ak_bind_nested.tex:ak_bind_nested.json:0"
  "ak_bind_symbolic.tex:ak_bind_symbolic.json:0"
  "ss_bind_good.tex:ss_bind.json:0"
  "ak_bind_unstructured.tex:ak_bind.json:1"
  "ak_bind_shortkey.tex:ak_bind.json:1"
  "ak_bind_outside.tex:ak_bind.json:0"
  "ss_bind_notryit.tex:ss_bind.json:1"
  "ss_tryit_good.tex:ss_tryit.json:0"
  "ss_tryit_missing.tex:ss_tryit.json:1"
  "ss_tryit_wrongans.tex:ss_tryit.json:1"
  "ss_tryit_good.tex:ss_tryit_roleswap.json:1"
)
for case in "${AK_CASES[@]}"; do
  IFS=: read -r texf jsonf want <<<"$case"
  require_fixture "$texf" "$jsonf"
  output=$("$PYTHON" "$SCRIPT_DIR/check_answer_key.py" "$FIXTURES/$texf" "$FIXTURES/$jsonf" 2>&1)
  got=$?
  if [[ "$got" -ne "$want" ]]; then
    echo "❌ $texf: expected exit $want, got $got"
    echo "$output" | sed 's/^/     /'
    exit 1
  fi
  echo "✅ $texf: exit $got"
  ak_ran=$((ak_ran + 1))
done
# a failing key must NAME the problem so the fix is findable
output=$("$PYTHON" "$SCRIPT_DIR/check_answer_key.py" "$FIXTURES/ak_bind_masked.tex" "$FIXTURES/ak_bind.json" 2>&1)
if ! echo "$output" | grep -q "problem 2"; then
  echo "❌ ak_bind_masked.tex: failure did not name problem 2"; exit 1
fi
echo "✅ check_answer_key names the drifted problem"
# template-style keys must segment per problem — never the old '?' placeholder
output=$("$PYTHON" "$SCRIPT_DIR/check_answer_key.py" "$FIXTURES/ak_bind_good.tex" "$FIXTURES/ak_bind.json" 2>&1)
if ! echo "$output" | grep -q "3 problem segments"; then
  echo "❌ ak_bind_good.tex: expected '3 problem segments' in the report"; exit 1
fi
if echo "$output" | grep -qF "? problem segments"; then
  echo "❌ ak_bind_good.tex: report still prints the '?' segment placeholder"; exit 1
fi
echo "✅ check_answer_key reports real segment counts"
# the pairing and role failures must TEACH the fix, not just fail
output=$("$PYTHON" "$SCRIPT_DIR/check_answer_key.py" "$FIXTURES/ss_bind_notryit.tex" "$FIXTURES/ss_bind.json" 2>&1)
if ! echo "$output" | grep -q "add a tryitbox per examplebox"; then
  echo "❌ ss_bind_notryit.tex: pairing failure did not teach the tryitbox fix"; exit 1
fi
echo "✅ check_answer_key teaches the example→try-it pairing"
output=$("$PYTHON" "$SCRIPT_DIR/check_answer_key.py" "$FIXTURES/ss_tryit_good.tex" "$FIXTURES/ss_tryit_roleswap.json" 2>&1)
if ! echo "$output" | grep -q 'role.*tryit'; then
  echo "❌ ss_tryit_roleswap: role/position mismatch not named"; exit 1
fi
echo "✅ check_answer_key names the role/position disagreement"

# Study-guide structure (tests/check_study_guide.py): every worked example
# opens with a prose strategy \step before computing. Fixture-driven both
# ways — the one-liner answer chains of the pre-gate shape must FAIL, the
# lintwash variant (steps present, first step pure math) must FAIL, and the
# strategy-first guide (including a manual sketch box with no \ans) must PASS.
echo
sg_ran=0
require_fixture ss_steps_good.tex ss_steps_missing.tex ss_steps_mathfirst.tex ss_steps.json
output=$("$PYTHON" "$SCRIPT_DIR/check_study_guide.py" "$FIXTURES/ss_steps_good.tex" "$FIXTURES/ss_steps.json" 2>&1)
if [ $? -eq 0 ]; then
  echo "✅ check_study_guide passes the strategy-first guide"
else
  echo "❌ check_study_guide wrongly flagged ss_steps_good.tex"
  echo "$output" | sed 's/^/     /'; exit 1
fi
sg_ran=$((sg_ran + 1))
output=$("$PYTHON" "$SCRIPT_DIR/check_study_guide.py" "$FIXTURES/ss_steps_missing.tex" "$FIXTURES/ss_steps.json" 2>&1)
if [ $? -eq 1 ] && echo "$output" | grep -q "no strategy step"; then
  echo "✅ check_study_guide flags one-liner worked examples (no strategy step)"
else
  echo "❌ check_study_guide missed the stepless answer chains"
  echo "$output" | sed 's/^/     /'; exit 1
fi
sg_ran=$((sg_ran + 1))
output=$("$PYTHON" "$SCRIPT_DIR/check_study_guide.py" "$FIXTURES/ss_steps_mathfirst.tex" "$FIXTURES/ss_steps.json" 2>&1)
if [ $? -eq 1 ] && echo "$output" | grep -q "computation, not strategy"; then
  echo "✅ check_study_guide flags a math-only first step"
else
  echo "❌ check_study_guide accepted a computation as the strategy step"
  echo "$output" | sed 's/^/     /'; exit 1
fi
sg_ran=$((sg_ran + 1))

# Skill coverage (tests/check_ss_coverage.py): every worksheet skill needs a
# tagged study-guide entry, and tagging is all-or-nothing (audit-3b: an
# optional gate is a vacuous gate). JSON-only, so it runs anywhere.
echo
cov_ran=0
require_fixture sscov_ws_good.json sscov_ss_good.json sscov_ss_gap.json \
                sscov_ws_untagged.json sscov_ws_partial.json
output=$("$PYTHON" "$SCRIPT_DIR/check_ss_coverage.py" "$FIXTURES/sscov_ws_good.json" "$FIXTURES/sscov_ss_good.json" 2>&1)
if [ $? -eq 0 ]; then
  echo "✅ check_ss_coverage passes a covered pair (guide-only extras legal)"
else
  echo "❌ check_ss_coverage wrongly failed the covered pair"
  echo "$output" | sed 's/^/     /'; exit 1
fi
cov_ran=$((cov_ran + 1))
output=$("$PYTHON" "$SCRIPT_DIR/check_ss_coverage.py" "$FIXTURES/sscov_ws_good.json" "$FIXTURES/sscov_ss_gap.json" 2>&1)
if [ $? -eq 1 ] && echo "$output" | grep -q "quadratic-equations"; then
  echo "✅ check_ss_coverage names the uncovered skill"
else
  echo "❌ check_ss_coverage missed the coverage gap (or did not name it)"
  echo "$output" | sed 's/^/     /'; exit 1
fi
cov_ran=$((cov_ran + 1))
output=$("$PYTHON" "$SCRIPT_DIR/check_ss_coverage.py" "$FIXTURES/sscov_ws_untagged.json" "$FIXTURES/sscov_ss_good.json" 2>&1)
if [ $? -eq 1 ] && echo "$output" | grep -q "NO worksheet problem"; then
  echo "✅ check_ss_coverage fails an untagged worksheet (nothing checked ≠ pass)"
else
  echo "❌ check_ss_coverage let an untagged worksheet pass vacuously"
  echo "$output" | sed 's/^/     /'; exit 1
fi
cov_ran=$((cov_ran + 1))
output=$("$PYTHON" "$SCRIPT_DIR/check_ss_coverage.py" "$FIXTURES/sscov_ws_partial.json" "$FIXTURES/sscov_ss_good.json" 2>&1)
if [ $? -eq 1 ] && echo "$output" | grep -q "\[2, 3\]"; then
  echo "✅ check_ss_coverage names the untagged problem ids on partial tagging"
else
  echo "❌ check_ss_coverage partial-tagging failure missing or unnamed"
  echo "$output" | sed 's/^/     /'; exit 1
fi
cov_ran=$((cov_ran + 1))

# Study-guide prose binding (check_prose_consistency's examplebox path).
# The good fixture doubles as the known-bad test of the intermediate-value
# suppression itself: it prints 10(0.642788), which only stays un-flagged
# because 0.642788 equals a subexpression of the entry's expr at printed
# precision — disable suppression and the no-flags assertion fails.
echo
prose_ran=0
require_fixture ss_prose_good.tex ss_prose_drift.tex ss_prose.json
output=$("$PYTHON" "$SCRIPT_DIR/check_prose_consistency.py" "$FIXTURES/ss_prose_good.tex" "$FIXTURES/ss_prose.json" 2>&1)
rc=$?
if [ "$rc" -eq 0 ] && ! echo "$output" | grep -q "missing from JSON"; then
  echo "✅ check_prose parses exampleboxes and suppresses the printed intermediate"
else
  echo "❌ check_prose flagged the known-good study guide (suppression broken?)"
  echo "$output" | sed 's/^/     /'; exit 1
fi
prose_ran=$((prose_ran + 1))
output=$("$PYTHON" "$SCRIPT_DIR/check_prose_consistency.py" "$FIXTURES/ss_prose_drift.tex" "$FIXTURES/ss_prose.json" 2>&1)
if echo "$output" | grep -q "missing from JSON.*12"; then
  echo "✅ check_prose flags the drifted study-guide given (c=12)"
else
  echo "❌ check_prose missed the drifted prose given"
  echo "$output" | sed 's/^/     /'; exit 1
fi
prose_ran=$((prose_ran + 1))
# a study guide that drops the examplebox shape must fail LOUDLY (exit 2),
# mirroring the worksheet zero-parse guard
SS_ZERO="$(mktemp "${TMPDIR:-/tmp}/ss_zero.XXXXXX.tex")"
printf '\\documentclass{article}\\begin{document}No boxes here\\end{document}\n' > "$SS_ZERO"
"$PYTHON" "$SCRIPT_DIR/check_prose_consistency.py" "$SS_ZERO" "$FIXTURES/ss_prose.json" >/dev/null 2>&1
zero_got=$?
rm -f "$SS_ZERO"
if [ "$zero_got" -eq 2 ]; then
  echo "✅ check_prose exits 2 on a study guide with zero exampleboxes"
else
  echo "❌ check_prose ss zero-parse: expected exit 2, got $zero_got"; exit 1
fi
prose_ran=$((prose_ran + 1))

log_ran=0

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
  require_fixture "$fixture"
  if "$PYTHON" "$SCRIPT_DIR/check_layout.py" "$FIXTURES/$fixture" >/dev/null 2>&1; then
    got="pass"
  else
    got="fail"
  fi
  if [ "$got" = "$want" ]; then
    echo "✅ check_layout: $fixture -> $got (as expected)"
    layout_ran=$((layout_ran + 1))
  else
    echo "❌ check_layout: $fixture -> $got, expected $want"; exit 1
  fi
done

# Zero-parse guard: a sheet with no enumerate list and no \problem block was
# checked against NOTHING — that must be exit 2 specifically, never a pass.
ZERO_TEX="$(mktemp "${TMPDIR:-/tmp}/layout_zero.XXXXXX.tex")"
printf '\\documentclass{article}\\begin{document}Nothing here\\end{document}\n' > "$ZERO_TEX"
"$PYTHON" "$SCRIPT_DIR/check_layout.py" "$ZERO_TEX" >/dev/null 2>&1
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
if "$PYTHON" "$SCRIPT_DIR/../scripts/check_log.py" "$FIXTURES/texlog_bad.log" >/dev/null 2>&1; then
  echo "❌ check_log did NOT flag texlog_bad.log"; exit 1
else
  echo "✅ check_log flags texlog_bad.log"
  log_ran=$((log_ran + 1))
fi
if "$PYTHON" "$SCRIPT_DIR/../scripts/check_log.py" "$FIXTURES/texlog_ok.log" >/dev/null 2>&1; then
  echo "✅ check_log passes texlog_ok.log"
  log_ran=$((log_ran + 1))
else
  echo "❌ check_log wrongly flagged texlog_ok.log"; exit 1
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

  build_case() {  # name  expected-exit  json-to-use  [ak-override] [verify-ss-override]
    local name="$1" want="$2" json="$3" ak="${4:-ak_build_demo.tex}" vss="${5:-verify_ss_build_demo.json}"
    local dir="$WORK/$name" out got
    mkdir -p "$dir"
    cp tests/fixtures/trio/ws_build_demo.tex "$dir/ws_build_demo.tex"
    cp "tests/fixtures/trio/$ak" "$dir/ak_build_demo.tex"
    cp tests/fixtures/trio/ss_build_demo.tex "$dir/ss_build_demo.tex"
    cp "tests/fixtures/trio/$json" "$dir/verify_build_demo.json"
    cp "tests/fixtures/trio/$vss" "$dir/verify_ss_build_demo.json"
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
  # the skill-coverage gate must have RUN on the green build, not been skipped
  out=$(PATH="$WORK/bin:$PATH" TECTONIC_MARKER="$WORK/green/compile_calls" \
        bash scripts/build.sh "$WORK/green/verify_build_demo.json" \
        --outdir "$WORK/green/out" 2>&1)
  if echo "$out" | grep -q "coverage-ss.*PASS"; then
    echo "✅ build.sh green: coverage-ss gate ran and passed"
  else
    echo "❌ build.sh green: coverage-ss PASS missing from the gate summary"
    echo "$out" | sed 's/^/     /'; exit 1
  fi

  # a failed verification must stop the run BEFORE any compile
  build_case broken-verify 1 verify_build_demo_broken.json
  if [ -f "$WORK/broken-verify/compile_calls" ]; then
    echo "❌ build.sh broken-verify: compiled despite a failed verify gate"; exit 1
  fi
  echo "✅ build.sh broken-verify: zero compile invocations (fail-fast held)"

  # an uncovered worksheet skill fails coverage-ss BEFORE any render/compile
  build_case coverage-gap 1 verify_build_demo.json ak_build_demo.tex \
             verify_ss_build_demo_uncovered.json
  if [ -f "$WORK/coverage-gap/compile_calls" ]; then
    echo "❌ build.sh coverage-gap: compiled despite an uncovered skill"; exit 1
  fi
  echo "✅ build.sh coverage-gap: zero compile invocations (fail-fast held)"

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

echo
echo "✅ All tests passed — $verify_ran verify fixtures · $layout_ran layout fixtures · $log_ran log fixtures · $ak_ran answer-key fixtures · $sg_ran study-guide fixtures · $cov_ran skill-coverage fixtures · $prose_ran ss-prose fixtures"
