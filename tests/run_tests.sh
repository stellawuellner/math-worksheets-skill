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
# exit code alone can't prove it (list 1 already fails the file). The grep
# pins the FIGURE fault specifically: a bare "list 2:" would also match the
# answer-location fault and mask a broken detector.
layout_out=$("$PYTHON" "$SCRIPT_DIR/check_layout.py" "$FIXTURES/layout_bad.tex" 2>&1)
if echo "$layout_out" | grep -q "list 2: .*carry a figure"; then
  echo "✅ check_layout sees \\rtfig[scale=..] as a valued figure (list 2 fault)"
else
  echo "❌ check_layout missed the optional-arg macro figure — list 2 not flagged"
  exit 1
fi

# Answer-location rule (rule 4): a sheet with generous workspace but no
# designated answer blanks must FAIL naming the rule, and the known-good
# fixtures above already prove the acceptance branches (\ansline, \ansblank,
# \noansline in layout_good.tex — a \noansline-marked item passes).
require_fixture layout_bad_noans.tex
noans_out=$("$PYTHON" "$SCRIPT_DIR/check_layout.py" "$FIXTURES/layout_bad_noans.tex" 2>&1)
if [ $? -eq 1 ] && echo "$noans_out" | grep -q "answer location"; then
  echo "✅ check_layout flags a sheet with no designated answer location"
  layout_ran=$((layout_ran + 1))
else
  echo "❌ check_layout missed the missing answer blanks (rule 4)"
  echo "$noans_out" | sed 's/^/     /'; exit 1
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

# Effort markers (scripts/render_meta.py + check_prose_consistency --meta).
# Construction is the guarantee — the property suite tests the constructor —
# and the placement residue is fixture-tested: unresolved calls are loud,
# swapped/missing markers fail the index binding, hand-typed literals are
# banned even with no meta file in play.
echo
require_fixture meta_demo.json ws_probmeta.tex
output=$("$PYTHON" "$SCRIPT_DIR/test_render_meta.py" 2>&1)
if [ $? -ne 0 ]; then
  echo "❌ test_render_meta.py failed"
  echo "$output" | sed 's/^/     /'
  exit 1
fi
echo "✅ test_render_meta.py (marker constructor property suite)"

META_DIR="$(mktemp -d)"
META_TMP="$META_DIR/meta_demo.tex"
if ! "$PYTHON" "$SCRIPT_DIR/../scripts/render_meta.py" "$FIXTURES/meta_demo.json" "$META_TMP" >/dev/null 2>&1; then
  echo "❌ render_meta.py failed on meta_demo.json"; exit 1
fi
echo "✅ render_meta.py renders meta_demo.json"

if "$PYTHON" "$SCRIPT_DIR/check_prose_consistency.py" "$FIXTURES/ws_probmeta.tex" \
     "$FIXTURES/meta_demo.json" --meta "$META_TMP" >/dev/null 2>&1; then
  echo "✅ check_prose passes the fully-marked sheet (--meta resolved)"
else
  echo "❌ check_prose wrongly flagged the fully-marked sheet"; exit 1
fi

"$PYTHON" "$SCRIPT_DIR/check_prose_consistency.py" "$FIXTURES/ws_probmeta.tex" \
  "$FIXTURES/meta_demo.json" >/dev/null 2>&1
if [ $? -eq 2 ]; then
  echo "✅ check_prose is LOUD when \\probmeta is unresolved (exit 2, not a silent pass)"
else
  echo "❌ check_prose ran blind past unresolved \\probmeta"; exit 1
fi

# swapped markers: block 3 carrying \probmeta{4} (and vice versa) must fail
# the index binding NAMING the blocks
sed -e 's/\\probmeta{3}/\\probmeta{9}/; s/\\probmeta{4}/\\probmeta{3}/; s/\\probmeta{9}/\\probmeta{4}/' \
  "$FIXTURES/ws_probmeta.tex" > "$META_DIR/ws_swapped.tex"
output=$("$PYTHON" "$SCRIPT_DIR/check_prose_consistency.py" "$META_DIR/ws_swapped.tex" \
         "$FIXTURES/meta_demo.json" --meta "$META_TMP" 2>&1)
if [ $? -eq 2 ] && echo "$output" | grep -q "binding failed in block(s) \[3, 4\]"; then
  echo "✅ check_prose fails swapped \\probmeta{3}/\\probmeta{4} naming the blocks"
else
  echo "❌ check_prose missed the swapped markers"
  echo "$output" | sed 's/^/     /'; exit 1
fi

# one block missing its marker: all-or-nothing must fail
sed -e 's/\\probmeta{2} //' "$FIXTURES/ws_probmeta.tex" > "$META_DIR/ws_missing.tex"
"$PYTHON" "$SCRIPT_DIR/check_prose_consistency.py" "$META_DIR/ws_missing.tex" \
  "$FIXTURES/meta_demo.json" --meta "$META_TMP" >/dev/null 2>&1
if [ $? -eq 2 ]; then
  echo "✅ check_prose fails a sheet where one block lost its marker (all-or-nothing)"
else
  echo "❌ check_prose passed a partially-marked sheet"; exit 1
fi

# hand-typed literals are banned unconditionally (no --meta in play)
sed -e 's/\\probmeta{1}/(3 pts)/' "$FIXTURES/ws_probmeta.tex" \
  | sed -e 's/\\probmeta{[0-9]}//' > "$META_DIR/ws_literal.tex"
output=$("$PYTHON" "$SCRIPT_DIR/check_prose_consistency.py" "$META_DIR/ws_literal.tex" \
         "$FIXTURES/meta_demo.json" 2>&1)
if [ $? -eq 2 ] && echo "$output" | grep -q "hand-typed effort marker"; then
  echo "✅ check_prose bans a hand-typed \"(3 pts)\" literal"
else
  echo "❌ check_prose let a hand-typed point value through"
  echo "$output" | sed 's/^/     /'; exit 1
fi
sed -e 's/\\probmeta{1}/{\\footnotesize\\ensuremath{\\bigstar\\bigstar}}/' \
  "$FIXTURES/ws_probmeta.tex" | sed -e 's/\\probmeta{[0-9]}//' > "$META_DIR/ws_star.tex"
"$PYTHON" "$SCRIPT_DIR/check_prose_consistency.py" "$META_DIR/ws_star.tex" \
  "$FIXTURES/meta_demo.json" >/dev/null 2>&1
if [ $? -eq 2 ]; then
  echo "✅ check_prose bans a hand-typed \\bigstar"
else
  echo "❌ check_prose let a hand-typed \\bigstar through"; exit 1
fi

# the constructor itself gates garbage tags with a teaching message
output=$("$PYTHON" "$SCRIPT_DIR/../scripts/render_meta.py" /dev/stdin "$META_DIR/meta_bad.tex" \
         <<<'{"problem_count": 1, "problems": [{"id": 1, "type": "manual", "desc": "x", "difficulty": 7}]}' 2>&1)
if [ $? -eq 1 ] && echo "$output" | grep -q "\[1\]"; then
  echo "✅ render_meta.py rejects difficulty 7 naming the offending id"
else
  echo "❌ render_meta.py accepted an out-of-range difficulty"
  echo "$output" | sed 's/^/     /'; exit 1
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
  # unit binding (tests/_units.py): declared answer_unit must be printed in
  # the problem's own box; a printed lexicon unit the JSON never declared
  # (today's-real-artifact class) must hard-fail; the good key exercises
  # \text{ft}, split \text{cm}^2, "square units", and the ^\circ alias
  "ak_unit_good.tex:ak_unit.json:0"
  "ak_unit_wrong.tex:ak_unit.json:1"
  "ak_unit_missing.tex:ak_unit.json:1"
  "ak_unit_undeclared.tex:ak_bind.json:1"
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

# Sheet-side unit binding (check_answer_line.py): a declared answer_unit
# needs a matching \answerline on the worksheet, a printed unit needs a
# declaration — both directions fixture-tested, in both document shapes.
echo
ansline_ran=0
# tex_fixture:json_fixture:expected_exit
ANSLINE_CASES=(
  "ws_line_good.tex:ak_unit.json:0"
  "ws_line_good_prob.tex:ak_unit.json:0"
  "ws_line_missing.tex:ak_unit.json:1"
  "ws_line_mismatch.tex:ak_unit.json:1"
  "ws_line_undeclared.tex:ak_bind.json:1"
)
for case in "${ANSLINE_CASES[@]}"; do
  IFS=: read -r texf jsonf want <<<"$case"
  require_fixture "$texf" "$jsonf"
  output=$("$PYTHON" "$SCRIPT_DIR/check_answer_line.py" "$FIXTURES/$texf" "$FIXTURES/$jsonf" 2>&1)
  got=$?
  if [[ "$got" -ne "$want" ]]; then
    echo "❌ $texf: expected exit $want, got $got"
    echo "$output" | sed 's/^/     /'
    exit 1
  fi
  echo "✅ $texf: exit $got"
  ansline_ran=$((ansline_ran + 1))
done

# the shared matcher's edge semantics (token sequences, aliases, filters)
output=$("$PYTHON" "$SCRIPT_DIR/test_unit_binding.py" 2>&1)
if [ $? -ne 0 ]; then
  echo "❌ test_unit_binding.py failed"
  echo "$output" | sed 's/^/     /'
  exit 1
fi
echo "✅ test_unit_binding.py (unit matcher + answer_unit schema)"

# Quick-answer bank (scripts/render_quick_answers.py). Regenerated every
# build so staleness is impossible in the gated path; what needs fixtures is
# the preflight (a bank the key never shows, a hand-rolled preamble) and the
# strict-binding invariant: an \input'd bank must NOT degrade
# check_answer_key.py's per-problem gate.
echo
require_fixture qa_bank.json ak_qa_good.tex ak_qa_noinput.tex ak_qa_nopreamble.tex
output=$("$PYTHON" "$SCRIPT_DIR/test_render_quick_answers.py" 2>&1)
if [ $? -ne 0 ]; then
  echo "❌ test_render_quick_answers.py failed"
  echo "$output" | sed 's/^/     /'
  exit 1
fi
echo "✅ test_render_quick_answers.py (bank constructor property suite)"

QA_TMP="$(mktemp -d)/qa_demo.tex"
if "$PYTHON" "$SCRIPT_DIR/../scripts/render_quick_answers.py" \
     "$FIXTURES/qa_bank.json" "$FIXTURES/ak_qa_good.tex" "$QA_TMP" >/dev/null 2>&1 \
   && [ -f "$QA_TMP" ]; then
  echo "✅ render_quick_answers.py banks the mixed-type fixture"
else
  echo "❌ render_quick_answers.py failed on the known-good key"; exit 1
fi
"$PYTHON" "$SCRIPT_DIR/../scripts/render_quick_answers.py" \
  "$FIXTURES/qa_bank.json" "$FIXTURES/ak_qa_noinput.tex" "$QA_TMP" >/dev/null 2>&1
if [ $? -eq 1 ]; then
  echo "✅ render_quick_answers.py fails a key that never \\inputs its bank"
else
  echo "❌ render_quick_answers.py let a bank-less key through"; exit 1
fi
"$PYTHON" "$SCRIPT_DIR/../scripts/render_quick_answers.py" \
  "$FIXTURES/qa_bank.json" "$FIXTURES/ak_qa_nopreamble.tex" "$QA_TMP" >/dev/null 2>&1
if [ $? -eq 1 ]; then
  echo "✅ render_quick_answers.py fails a hand-rolled preamble"
else
  echo "❌ render_quick_answers.py accepted a hand-rolled preamble"; exit 1
fi
# strict-binding regression: with the \input{qa_demo} line present and the
# bank file on disk, the per-problem gate must stay STRICT (exit 0, no
# degraded-mode warning) — the verified invariant that makes plain-text
# banks safe at all
output=$("$PYTHON" "$SCRIPT_DIR/check_answer_key.py" "$FIXTURES/ak_qa_good.tex" \
         "$FIXTURES/qa_bank.json" 2>&1)
if [ $? -eq 0 ] && ! echo "$output" | grep -q "DEGRADED" \
   && echo "$output" | grep -q "7 problem segments"; then
  echo "✅ an \\input'd bank keeps check_answer_key in strict per-problem mode"
else
  echo "❌ the bank degraded (or broke) the per-problem binding gate"
  echo "$output" | sed 's/^/     /'; exit 1
fi

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

echo
echo "✅ All tests passed — $verify_ran verify fixtures · $layout_ran layout fixtures · $log_ran log fixtures · $ak_ran answer-key fixtures · $ansline_ran answer-line fixtures"
