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

source "$SCRIPT_DIR/../scripts/find_python.sh"
PYTHON="$(find_sympy_python)" || exit 1

# Eval manifests are product contract too: keep the quick skill-creator subset
# synchronized with the full capability suite, and pin coverage of every public
# verifier family before the slower fixture suite begins.
echo
if ! "$PYTHON" "$SCRIPT_DIR/test_eval_suite.py"; then
  echo "❌ test_eval_suite.py failed"
  exit 1
fi
eval_ran=1

echo
if ! "$PYTHON" "$SCRIPT_DIR/test_curriculum_eval_suite.py"; then
  echo "❌ test_curriculum_eval_suite.py failed"
  exit 1
fi
curriculum_eval_ran=1

echo
if ! "$PYTHON" "$SCRIPT_DIR/test_scoring_harness.py"; then
  echo "❌ test_scoring_harness.py failed"
  exit 1
fi
scoring_harness_ran=1

echo
if ! "$PYTHON" "$SCRIPT_DIR/test_author_review.py"; then
  echo "❌ test_author_review.py failed"
  exit 1
fi
author_review_ran=1

echo
if ! "$PYTHON" "$SCRIPT_DIR/test_page_budget.py"; then
  echo "❌ test_page_budget.py failed"
  exit 1
fi
page_budget_ran=1

# The visual harness needs TeX and so cannot run everywhere, but the guard that
# decides WHETHER its baselines apply to this machine is pure logic — it runs
# here, on every machine, TeX or not.
echo
if ! "$PYTHON" "$SCRIPT_DIR/test_visual_environment.py"; then
  echo "❌ test_visual_environment.py failed"
  exit 1
fi
visual_env_ran=1

echo
if ! "$PYTHON" "$SCRIPT_DIR/test_overprint.py"; then
  echo "❌ test_overprint.py failed"
  exit 1
fi
overprint_ran=1

# A recorded run is a snapshot; the code moves on. This asks whether the stored
# artifacts still look like what the skill produces TODAY — dead workarounds for
# fixed faults, printed defects no gate catches, content a reference file could
# now supply. Advisory: a stale artifact passed honestly when it was made, so
# this reports rather than fails the suite.
if [ -d "$SCRIPT_DIR/../evals/runs" ]; then
  echo
  if "$PYTHON" "$SCRIPT_DIR/check_artifact_health.py" --all >/dev/null 2>&1; then
    echo "✅ recorded eval artifacts match what the current code produces"
  else
    echo "⚠  recorded eval artifacts are stale against the current code —"
    echo "   run: python3 tests/check_artifact_health.py --all"
  fi
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
  "manual_cas_incomplete.json:2"   # CAS returns a confident, incomplete root set
  "pass_cas_factored.json:0"       # ...and the audit must not fire on a complete one
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
  "reject_figure_type.json:1"
  "reject_role_value.json:1"
  "pass_traps.json:0"
  "fail_trap_indistinct.json:1"
  "fail_trap_value_drift.json:1"
  "reject_trap_schema.json:1"
  "facets_good_ws.json:0"
  "facets_orphan.json:1"
  "facets_untagged.json:1"
  "facets_unknown.json:1"
  "interleave_blocked.json:2"
  "interleave_drill.json:0"
  "interleave_good.json:0"
  "interleave_single_facet.json:0"
  "reject_bad_format.json:1"
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

# oversized workspace: an unbreakable minipage taller than the page prints past
# the bottom margin, and check_log.py only WARNS on the resulting Overfull
# \vbox — so this fault is invisible unless check_layout catches it statically.
if "$PYTHON" "$SCRIPT_DIR/check_layout.py" "$FIXTURES/layout_oversized.tex" >/dev/null 2>&1; then
  echo "❌ check_layout did NOT flag layout_oversized.tex"; exit 1
else
  echo "✅ check_layout flags an over-page workspace (layout_oversized.tex)"
  layout_ran=$((layout_ran + 1))
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

# attribution greps: exit codes alone (LAYOUT_PAIRS below) cannot prove the
# fault names the RIGHT item — a fault naming the wrong one teaches the wrong
# fix. picquote: the pic-quote-only figure sits on item 1; nestfig: the valued
# figure sits on item 3 AFTER a nested part-list, exactly the item the naive
# parse used to drop.
require_fixture layout_bad_picquote.tex layout_bad_nestfig.tex
layout_out=$("$PYTHON" "$SCRIPT_DIR/check_layout.py" "$FIXTURES/layout_bad_picquote.tex" 2>&1)
if echo "$layout_out" | grep -q "items \[1\]"; then
  echo "✅ check_layout attributes the pic-quote figure to item 1"
else
  echo "❌ check_layout mis-attributed the pic-quote figure (no 'items [1]')"
  echo "$layout_out" | sed 's/^/     /'; exit 1
fi
layout_out=$("$PYTHON" "$SCRIPT_DIR/check_layout.py" "$FIXTURES/layout_bad_nestfig.tex" 2>&1)
if echo "$layout_out" | grep -q "items \[3\]"; then
  echo "✅ check_layout attributes the post-nested-list figure to item 3"
else
  echo "❌ check_layout mis-attributed the post-nested-list figure (no 'items [3]')"
  echo "$layout_out" | sed 's/^/     /'; exit 1
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

  # figure-type allowlist: a figure on a type with no bindable numbers (a
  # solve root list) must be rejected TEACHING the rewrite — the allowed
  # types and the "verify as approx/eval or drop the figure" path
  output=$("$PYTHON" "$VERIFY_PY" "$FIXTURES/reject_figure_type.json" 2>&1)
  if echo "$output" | grep -qF "['approx', 'eval']" \
     && echo "$output" | grep -q "or drop the figure"; then
    echo "✅ figure-on-solve rejection names the allowed types and the fix"
  else
    echo "❌ figure-on-solve rejection does not teach the rewrite"
    echo "$output" | sed 's/^/     /'; exit 1
  fi
fi

# ── Figure labelling convention (tests/test_figure_convention.py) ────────────
# The value-free \refrt reference figure teaches the labelling students apply
# to every renderer-built \probfig beside it, so the shipped macros, the doc
# examples, and render_figures.py's RIGHT_ANGLE_VERTEX must all put the right
# angle at the same vertex (the two once disagreed: \refrt at B, renderer at
# C — one sheet, two contradictory conventions). Pure text parse, CI-safe.
echo
output=$("$PYTHON" "$SCRIPT_DIR/test_figure_convention.py" 2>&1)
if [ $? -ne 0 ]; then
  echo "❌ test_figure_convention.py failed"
  echo "$output" | sed 's/^/     /'
  exit 1
fi
echo "✅ test_figure_convention.py (right-angle convention agreement)"

# ── Figure scope, both directions (tests/test_figure_scope.py) ───────────────
# has_valued_figure has been wrong in both directions eight minutes apart: it
# missed pgfplots tick labels (silent PASS, a graphed worksheet shipped), then
# flagged an EMPTY plotting grid a "plot a counterexample" problem needs
# (loud FAIL, and the only way to satisfy it is to delete the grid). Both are
# pinned, because fixing either one is what broke the other.
echo
output=$("$PYTHON" "$SCRIPT_DIR/test_figure_scope.py" 2>&1)
if [ $? -ne 0 ]; then
  echo "❌ test_figure_scope.py failed"
  echo "$output" | sed 's/^/     /'
  exit 1
fi
echo "✅ test_figure_scope.py (valued figure vs blank workspace)"

# ── SSA figure labels (tests/test_ssa_figure_labels.py) ─────────────────────
# The swing figure placed its fixed-side label at a flat 0.55, chosen against
# the reference drawing. Seven of twelve valid parameterisations printed the
# "?" arc on top of "b = N" — invisible to the LaTeX log, caught only by
# check_overprint, and the author's only lever was to change the givens.
echo
output=$("$PYTHON" "$SCRIPT_DIR/test_ssa_figure_labels.py" 2>&1)
if [ $? -ne 0 ]; then
  echo "❌ test_ssa_figure_labels.py failed"
  echo "$output" | sed 's/^/     /'
  exit 1
fi
echo "✅ test_ssa_figure_labels.py (every accepted triangle is readable)"

# ── Template verdicts are separate faults (check_template_use.py) ────────────
# A 60-character \skillheading was reported under the headline "hand-rolled
# shell" with twelve lines telling the author to start the document with the
# shipped shell — which it already did. Two authors in one run rebuilt against
# that misdirection. The rule was right; the verdict it was filed under was not.
tmpl_dir=$(mktemp -d)
cp "$SCRIPT_DIR/../templates/worksheet-preamble.tex" "$tmpl_dir/"
LONGHEAD="Skill 1 --- Naming a shape by counting how many straight sides it has"
write_ss() { # preamble-line heading
  cat > "$tmpl_dir/ss.tex" <<TEXEOF
\\documentclass[12pt]{article}
\\usepackage[margin=0.85in, top=0.7in, bottom=0.7in]{geometry}
$1
\\ssheader{Shapes}
\\begin{document}
\\sstitleblock{Shapes}
\\skillheading{$2}
\\end{document}
TEXEOF
}
write_ss '\\input{worksheet-preamble}' "$LONGHEAD"
out=$("$PYTHON" "$SCRIPT_DIR/check_template_use.py" "$tmpl_dir/ss.tex" \
        --template "$tmpl_dir/worksheet-preamble.tex" 2>&1)
if echo "$out" | grep -q "heading too long" && ! echo "$out" | grep -q "hand-rolled shell"; then
  echo "✅ a long heading on a correct shell is reported as a heading fault"
else
  echo "❌ a long heading is still filed under 'hand-rolled shell'"; exit 1
fi
if echo "$out" | grep -q "shell itself is fine"; then
  echo "✅ and the author is told the shell is not the problem"
else
  echo "❌ heading-only fault does not reassure about the shell"; exit 1
fi
write_ss '\\newcommand{\\problem}[1]{#1}' "Naming shapes by side count"
out=$("$PYTHON" "$SCRIPT_DIR/check_template_use.py" "$tmpl_dir/ss.tex" \
        --template "$tmpl_dir/worksheet-preamble.tex" 2>&1)
if echo "$out" | grep -q "hand-rolled shell" && echo "$out" | grep -q "Start ss.tex with"; then
  echo "✅ a genuinely hand-rolled shell still gets the shell verdict and remedy"
else
  echo "❌ shell fault lost its verdict or its remedy"; exit 1
fi
rm -rf "$tmpl_dir"

# ── Large-print page budget (tests/test_page_budget_type_size.py) ────────────
# The budget is calibrated at 12pt and SKILL.md offers 14pt/17pt accessible
# output, claiming it adapted automatically. It did not: a correct 17pt sheet
# failed compile-ws by a page, and the only fixes were cutting problems or
# shortening stems. The scale factors are measured, and this is the measurement.
echo
output=$("$PYTHON" "$SCRIPT_DIR/test_page_budget_type_size.py" 2>&1)
if [ $? -ne 0 ]; then
  echo "❌ test_page_budget_type_size.py failed"
  echo "$output" | sed 's/^/     /'
  exit 1
fi
echo "✅ test_page_budget_type_size.py (large print costs what it costs)"

# ── Facet plans, misconception traps, interleaving ───────────────────────────
# The unit suite pins the gate messages and the window/run math; the blocks
# below pin what only the CLI surfaces: report lines, the cross-file
# facet-coverage checker, and the prose binder's trap-number handling.
echo
facet_ran=0
output=$("$PYTHON" "$SCRIPT_DIR/test_facets.py" 2>&1)
if [ $? -ne 0 ]; then
  echo "❌ test_facets.py failed"
  echo "$output" | sed 's/^/     /'; exit 1
fi
echo "✅ test_facets.py (facet/trap/interleave unit suite)"

# The slot-coverage gate: 172 of 300 reviewed cases shipped a printed answer
# nothing verified, because the coverage rule counted problems and the promise
# was about answers.
output=$("$PYTHON" "$SCRIPT_DIR/test_answer_slots.py" 2>&1)
if [ $? -ne 0 ]; then
  echo "❌ test_answer_slots.py failed"
  echo "$output" | sed 's/^/     /'; exit 1
fi
echo "✅ test_answer_slots.py (every printed response slot has a check)"

# test_check_log.py existed but was never wired into this runner, so its
# assertions drifted from check_log.py's messages unnoticed and it had been
# failing silently. A test suite nothing runs is not a test suite.
output=$("$PYTHON" "$SCRIPT_DIR/test_check_log.py" 2>&1)
if [ $? -ne 0 ]; then
  echo "❌ test_check_log.py failed"
  echo "$output" | sed 's/^/     /'; exit 1
fi
echo "✅ test_check_log.py (page-budget and log-fault contract)"

# Six more suites were present in tests/ and invoked by nothing. They all pass
# today, which is exactly why this matters: test_check_log.py also passed once,
# then drifted from the message it asserts and stayed red without anyone
# noticing, because no runner called it. Any tests/test_*.py not named in this
# file is dead weight pretending to be coverage.
for suite in test_answer_key_binding test_audit_fixes test_branches \
             test_error_paths test_pipeline_fixes test_preamble_layout \
             test_verify; do
  output=$("$PYTHON" "$SCRIPT_DIR/$suite.py" 2>&1)
  if [ $? -ne 0 ]; then
    echo "❌ $suite.py failed"
    echo "$output" | sed 's/^/     /'; exit 1
  fi
  echo "✅ $suite.py"
done

# the 10+-problem nudge is exit-NEUTRAL but must be visible
output=$("$PYTHON" "$VERIFY_PY" "$FIXTURES/pass_calculus.json" 2>&1)
if echo "$output" | grep -q 'no "facets" declared'; then
  echo "✅ verify nudges a 10+-problem facetless sheet (exit stays 0)"
else
  echo "❌ nudge line missing for pass_calculus.json"; exit 1
fi
facet_ran=$((facet_ran + 1))

# a facet-tagged sheet prints the histogram beside the standards line
output=$("$PYTHON" "$VERIFY_PY" "$FIXTURES/facets_good_ws.json" 2>&1)
if echo "$output" | grep -q "facets: side-from-angle×2"; then
  echo "✅ verify prints the facet histogram"
else
  echo "❌ facet histogram missing for facets_good_ws.json"; exit 1
fi
facet_ran=$((facet_ran + 1))

# the interleave flag must teach the fix: run ids + a concrete swap
output=$("$PYTHON" "$VERIFY_PY" "$FIXTURES/interleave_blocked.json" 2>&1)
if echo "$output" | grep -q "swap id"; then
  echo "✅ interleave violation suggests a concrete swap"
else
  echo "❌ interleave violation did not suggest a swap"; exit 1
fi
facet_ran=$((facet_ran + 1))

# cross-file gates: ws facets ⊆ ss examples, subtitle bound to the title block
FACETCOV="$SCRIPT_DIR/check_facet_coverage.py"
require_fixture facets_good_ws.tex facets_good_ws.json facets_good_ss.json \
                facets_ss_gap.json facets_ss_untagged.json facets_subtitle_ws.tex
# fixture set:  tex:ws_json:ss_json(or -):expected_exit
FC_CASES=(
  "facets_good_ws.tex:facets_good_ws.json:facets_good_ss.json:0"
  "facets_good_ws.tex:facets_good_ws.json:facets_ss_gap.json:1"
  "facets_good_ws.tex:facets_good_ws.json:facets_ss_untagged.json:1"
  "facets_subtitle_ws.tex:facets_good_ws.json:facets_good_ss.json:1"
  "facets_good_ws.tex:facets_good_ws.json:-:0"
)
for case in "${FC_CASES[@]}"; do
  IFS=: read -r texf wsj ssj want <<<"$case"
  if [ "$ssj" = "-" ]; then
    output=$("$PYTHON" "$FACETCOV" "$FIXTURES/$texf" "$FIXTURES/$wsj" 2>&1)
  else
    output=$("$PYTHON" "$FACETCOV" "$FIXTURES/$texf" "$FIXTURES/$wsj" "$FIXTURES/$ssj" 2>&1)
  fi
  got=$?
  if [ "$got" -ne "$want" ]; then
    echo "❌ check_facet_coverage $texf/$wsj/$ssj: expected exit $want, got $got"
    echo "$output" | sed 's/^/     /'; exit 1
  fi
  echo "✅ check_facet_coverage $texf ($wsj vs $ssj): exit $got"
  facet_ran=$((facet_ran + 1))
done
# a failing subset gate must NAME the missing facet so the fix is findable
output=$("$PYTHON" "$FACETCOV" "$FIXTURES/facets_good_ws.tex" \
         "$FIXTURES/facets_good_ws.json" "$FIXTURES/facets_ss_gap.json" 2>&1)
if echo "$output" | grep -q "no worked example tagged 'pythagorean'"; then
  echo "✅ check_facet_coverage names the missing study-guide facet"
else
  echo "❌ check_facet_coverage did not name the missing facet"; exit 1
fi
# legacy sheets (no facet plan) must pass untouched
if "$PYTHON" "$FACETCOV" "$FIXTURES/trio/ws_build_demo.tex" \
     "$FIXTURES/pass_algebra.json" >/dev/null 2>&1; then
  echo "✅ check_facet_coverage passes a legacy no-plan sheet"
else
  echo "❌ check_facet_coverage failed a legacy no-plan sheet"; exit 1
fi
facet_ran=$((facet_ran + 1))

# prose binder: a planted wrong number counts as a given ONLY when declared
# as a trap (and trap desc numbers never count)
require_fixture ws_trap_prose.tex trap_prose.json trap_prose_undeclared.json
output=$("$PYTHON" "$SCRIPT_DIR/check_prose_consistency.py" \
         "$FIXTURES/ws_trap_prose.tex" "$FIXTURES/trap_prose.json" 2>&1)
if echo "$output" | grep -q "missing from JSON"; then
  echo "❌ check_prose flagged a DECLARED trap value as missing"
  echo "$output" | sed 's/^/     /'; exit 1
fi
echo "✅ check_prose accepts a declared trap value in error-analysis prose"
output=$("$PYTHON" "$SCRIPT_DIR/check_prose_consistency.py" \
         "$FIXTURES/ws_trap_prose.tex" "$FIXTURES/trap_prose_undeclared.json" 2>&1)
if echo "$output" | grep -q "missing from JSON: \[7.37\]"; then
  echo "✅ check_prose flags the same number when the trap is UNdeclared"
else
  echo "❌ check_prose missed the undeclared planted number"
  echo "$output" | sed 's/^/     /'; exit 1
fi
facet_ran=$((facet_ran + 1))

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
  "ss_bind_notryit.tex:ss_bind.json:1"
  "ss_tryit_good.tex:ss_tryit.json:0"
  "ss_tryit_missing.tex:ss_tryit.json:1"
  "ss_tryit_wrongans.tex:ss_tryit.json:1"
  "ss_tryit_good.tex:ss_tryit_roleswap.json:1"

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
#   picquote  — a figure whose ONLY values are pic-quote angle labels (the
#               taught circle template) passed a mixed list clean; the
#               value-free "$\theta$" twin must still PASS
#   includegraphics — an opaque image must be ASSUMED valued (all-or-nothing
#               scope), or a mixed list with an image passes clean
#   nest*     — the naive enumerate regex truncated at a nested part-list,
#               so items after it escaped BOTH rules (nestfig: dropped valued
#               figure; nestspace: dropped zero-workspace items — both exit 0
#               pre-fix); the multi-part template twin must still PASS
LAYOUT_PAIRS=(
  "layout_bad_probstyle.tex:fail"
  "layout_good_probstyle.tex:pass"
  "layout_bad_pagebreak.tex:fail"
  "layout_good_pagebreak.tex:pass"
  "layout_good_lineskip.tex:pass"
  "layout_bad_negspace.tex:fail"
  "layout_bad_picquote.tex:fail"
  "layout_bad_includegraphics.tex:fail"
  "layout_good_picquote_valuefree.tex:pass"
  "layout_bad_nestfig.tex:fail"
  "layout_bad_nestspace.tex:fail"
  "layout_good_nested.tex:pass"
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

# ── check_prose: \includegraphics hard gate ──────────────────────────────────
# An external image cannot be bound to the JSON — worse, its FILENAME digits
# (52/100 here, deliberately also JSON givens) leak into the prose scan and
# used to make the report read "all consistent" for an unverified figure. Like
# unresolved \probfig, that must be exit 2 with a message naming the checkable
# path (render_figures.py); the commented-out twin proves the gate runs on
# comment-blanked text (dead markup must not trip a hard gate).
require_fixture ws_includegraphics.tex ws_includegraphics.json ws_includegraphics_commented.tex
output=$("$PYTHON" "$SCRIPT_DIR/check_prose_consistency.py" "$FIXTURES/ws_includegraphics.tex" \
         "$FIXTURES/ws_includegraphics.json" 2>&1)
got=$?
if [ "$got" -eq 2 ] && echo "$output" | grep -q "render_figures"; then
  echo "✅ check_prose is LOUD on \\includegraphics (exit 2, names render_figures.py)"
else
  echo "❌ check_prose \\includegraphics gate: expected exit 2 naming render_figures.py, got exit $got"
  echo "$output" | sed 's/^/     /'; exit 1
fi
"$PYTHON" "$SCRIPT_DIR/check_prose_consistency.py" "$FIXTURES/ws_includegraphics_commented.tex" \
  "$FIXTURES/ws_includegraphics.json" >/dev/null 2>&1
got=$?
if [ "$got" -eq 0 ]; then
  echo "✅ check_prose ignores a commented-out \\includegraphics (exit 0)"
else
  echo "❌ check_prose fired on a commented-out \\includegraphics (exit $got)"; exit 1
fi

# ── check_prose: depth-aware item parse ──────────────────────────────────────
# Nested parts must stay inside their parent's block (3 top-level blocks, not
# 4) and the post-nested problem must be PARSED — its drifted 77 was invisible
# while the naive regex dropped everything after the part-list.
require_fixture ws_nested_prose.tex ws_nested_prose.json
output=$("$PYTHON" "$SCRIPT_DIR/check_prose_consistency.py" "$FIXTURES/ws_nested_prose.tex" \
         "$FIXTURES/ws_nested_prose.json" 2>&1)
got=$?
if [ "$got" -ne 0 ]; then
  echo "❌ check_prose ws_nested_prose.tex: expected exit 0 (report, not gate), got $got"
  echo "$output" | sed 's/^/     /'; exit 1
fi
if ! echo "$output" | grep -q "across 3 problem block(s)"; then
  echo "❌ check_prose counted nested parts as top-level problems (want 3 blocks)"
  echo "$output" | sed 's/^/     /'; exit 1
fi
if ! echo "$output" | grep -q "problem 3: .*missing from JSON: \[77.0\]"; then
  echo "❌ check_prose never parsed the post-nested problem (77 not flagged)"
  echo "$output" | sed 's/^/     /'; exit 1
fi
echo "✅ check_prose parses nested sheets per top-level problem (3 blocks, 77 flagged)"

# ── Template-use gate (tests/check_template_use.py) ──────────────────────────
# The 'never retype the preamble' rule finally has teeth: a hand-rolled shell
# (real e2e shape: local \input{preamble}, no template) and a post-template
# shadowing doc (\newenvironment/\renewcommand/\definecolor of shipped names)
# must FAIL; the SKILL.md shell with a rendered figs_* \input must PASS.
tpl_ran=0
TPL_CASES=(
  "tpl_bad_handrolled.tex:1"
  "tpl_bad_redefine.tex:1"
  "tpl_bad_longtitle.tex:1"
  "tpl_good.tex:0"
)
for case in "${TPL_CASES[@]}"; do
  fixture="${case%%:*}"
  want="${case##*:}"
  require_fixture "$fixture"
  output=$("$PYTHON" "$SCRIPT_DIR/check_template_use.py" "$FIXTURES/$fixture" 2>&1)
  got=$?
  if [ "$got" -ne "$want" ]; then
    echo "❌ check_template_use $fixture: expected exit $want, got $got"
    echo "$output" | sed 's/^/     /'; exit 1
  fi
  echo "✅ check_template_use: $fixture -> exit $got (as expected)"
  tpl_ran=$((tpl_ran + 1))
done
# the failure must teach the fix: the shipped shell and the staging fact
output=$("$PYTHON" "$SCRIPT_DIR/check_template_use.py" "$FIXTURES/tpl_bad_handrolled.tex" 2>&1)
if echo "$output" | grep -q 'input{worksheet-preamble}' && echo "$output" | grep -q "compile.sh stages"; then
  echo "✅ check_template_use failure teaches the shipped shell"
else
  echo "❌ check_template_use failure does not teach the fix"
  echo "$output" | sed 's/^/     /'; exit 1
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

# Page budget (check_log.py --max-pages, wired through compile.sh MAX_PAGES):
# SKILL.md hard-caps the study guide at 2 pages, but a 3-page guide shipped
# through every gate green — a documented rule with no check. The count comes
# from the log's own "Output written ... (N pages" line (both engines print
# it), so this stays CI-safe: log text only, no engine. A 3-page log must
# FAIL the cap teaching the fix, a 2-page log must PASS AT it, and a log with
# no "Output written" line must be LOUD (exit 2) — a cap that silently goes
# unchecked is the same false-green class.
require_fixture texlog_pages_over.log texlog_pages_at.log texlog_pages_missing.log
output=$("$PYTHON" "$SCRIPT_DIR/../scripts/check_log.py" "$FIXTURES/texlog_pages_over.log" --max-pages 2 2>&1)
# The message must name workspace_cm, and name it BEFORE the cut/split advice.
# Four eval agents overran a computed ceiling with honest content and were told
# to "tighten workspace" — the one trade this project rejects — while the field
# that actually raises the ceiling went unmentioned.
if [ $? -eq 1 ] \
   && echo "$output" | grep -q "workspace_cm" \
   && [ "$(echo "$output" | grep -o "workspace_cm\|split it" | head -1)" = "workspace_cm" ]; then
  echo "✅ check_log fails a 3-page log against --max-pages 2 (and names workspace_cm first)"
  log_ran=$((log_ran + 1))
else
  echo "❌ check_log let a 3-page log through --max-pages 2 (or the message doesn't teach)"
  echo "$output" | sed 's/^/     /'; exit 1
fi
if "$PYTHON" "$SCRIPT_DIR/../scripts/check_log.py" "$FIXTURES/texlog_pages_at.log" --max-pages 2 >/dev/null 2>&1; then
  echo "✅ check_log passes a 2-page log AT --max-pages 2 (the cap is inclusive)"
  log_ran=$((log_ran + 1))
else
  echo "❌ check_log wrongly failed a log exactly at the cap"; exit 1
fi
"$PYTHON" "$SCRIPT_DIR/../scripts/check_log.py" "$FIXTURES/texlog_pages_missing.log" --max-pages 2 >/dev/null 2>&1
if [ $? -eq 2 ]; then
  echo "✅ check_log is LOUD (exit 2) when --max-pages is set but the log hides the count"
  log_ran=$((log_ran + 1))
else
  echo "❌ check_log silently unenforced the page budget on a truncated log"; exit 1
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
# emit the kept log (--keep-logs) the page-budget gate reads: check_log takes
# the count from "Output written ... (N pages"; TECTONIC_PAGES (default 1)
# lets a test claim any page count without a real engine
printf 'Output written on %s.pdf (%s pages, 12345 bytes).\n' \
  "$(basename "${tex%.tex}")" "${TECTONIC_PAGES:-1}" > "$out/$(basename "${tex%.tex}").log"
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

  # a hand-rolled worksheet shell must fail at template-ws BEFORE anything
  # verifies or compiles (same fail-fast assertion style as broken-verify)
  dir="$WORK/handrolled"; mkdir -p "$dir"
  cp tests/fixtures/tpl_bad_handrolled.tex "$dir/ws_build_demo.tex"
  cp tests/fixtures/trio/ak_build_demo.tex "$dir/ak_build_demo.tex"
  cp tests/fixtures/trio/ss_build_demo.tex "$dir/ss_build_demo.tex"
  cp tests/fixtures/trio/verify_build_demo.json "$dir/verify_build_demo.json"
  cp tests/fixtures/trio/verify_ss_build_demo.json "$dir/verify_ss_build_demo.json"
  export TECTONIC_MARKER="$dir/compile_calls"
  out=$(PATH="$WORK/bin:$PATH" bash scripts/build.sh "$dir/verify_build_demo.json" \
        --outdir "$dir/out" 2>&1)
  got=$?
  if [ "$got" -ne 1 ] || ! echo "$out" | grep -q "gate: template-ws"; then
    echo "❌ build.sh handrolled: expected exit 1 at gate template-ws, got $got"
    echo "$out" | sed 's/^/     /'; exit 1
  fi
  if [ -f "$dir/compile_calls" ]; then
    echo "❌ build.sh handrolled: compiled despite a hand-rolled shell"; exit 1
  fi
  echo "✅ build.sh handrolled: exit 1 at template-ws, zero compile invocations"

  # ── page budget through the driver ─────────────────────────────────────────
  # The proven false green: a 3-page study guide shipped through all gates.
  # With the stub reporting 3 pages everywhere, ws (≤8) and ak (≤6) stay
  # within their sanity ceilings but the ss compile must fail its 2-page
  # SKILL.md cap — and the verdict must name the gate. (The green build_case
  # above already proves the budgets pass 1-page documents.)
  dir="$WORK/pagebudget"; mkdir -p "$dir"
  cp tests/fixtures/trio/ws_build_demo.tex "$dir/ws_build_demo.tex"
  cp tests/fixtures/trio/ak_build_demo.tex "$dir/ak_build_demo.tex"
  cp tests/fixtures/trio/ss_build_demo.tex "$dir/ss_build_demo.tex"
  cp tests/fixtures/trio/verify_build_demo.json "$dir/verify_build_demo.json"
  cp tests/fixtures/trio/verify_ss_build_demo.json "$dir/verify_ss_build_demo.json"
  export TECTONIC_MARKER="$dir/compile_calls"
  out=$(PATH="$WORK/bin:$PATH" TECTONIC_PAGES=3 bash scripts/build.sh \
        "$dir/verify_build_demo.json" --outdir "$dir/out" 2>&1)
  got=$?
  if [ "$got" -eq 1 ] && echo "$out" | grep -q "gate: compile-ss"; then
    echo "✅ build.sh page budget: a 3-page study guide fails at compile-ss (2-page cap enforced)"
  else
    echo "❌ build.sh page budget: 3-page study guide did not fail at compile-ss (exit $got)"
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
echo "✅ All tests passed — $verify_ran verify fixtures · $layout_ran layout fixtures · $log_ran log fixtures · $ak_ran answer-key fixtures · $tpl_ran template fixtures · $sg_ran study-guide fixtures · $cov_ran skill-coverage fixtures · $prose_ran ss-prose fixtures · $facet_ran facet/trap checks · $ansline_ran answer-line fixtures · $eval_ran capability-eval integrity check · $curriculum_eval_ran curriculum-eval integrity check · $scoring_harness_ran scoring-harness suite · $author_review_ran author-review suite · $page_budget_ran page-budget suite · $visual_env_ran visual-environment guard · $overprint_ran overprint detector"
