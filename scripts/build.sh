#!/usr/bin/env bash
# build.sh — the single gate-chain driver: verify JSON in, three gated PDFs out.
#
# Usage: build.sh <verify_<stem>.json> [--outdir DIR] [--worksheet-only]
#                 [--ws FILE] [--ak FILE] [--ss FILE] [--verify-ss FILE]
#
# WHY: the skill used to prescribe nine separate gate commands spread across
# four prose sections — an agent could skip any of them and nothing noticed
# (it happened twice in one audited session). This driver runs every gate in
# order, fail-fast, and ends with ONE machine-checkable verdict line, so
# "did the gates run" stops being a matter of prose discipline. A plain
# `a && b && c` chain cannot replace it: run_verify's exit 2 means "manual
# review, safe to compile" and must continue, while check_prose's exit 2
# means "parsed zero problems" and must stop — only a script can encode that.
#
# DOCUMENT DISCOVERY (in the verify JSON's directory):
#   verify_<stem>.json  →  ws_<stem>.tex, ak_<stem>.tex, ss_<stem>.tex,
#                          and verify_ss_<stem>.json for the study guide.
#   Also recognized per role: an optional student-name prefix
#   (leo_ws_<stem>.tex) and a tier letter inside the role token
#   (wsS_/wsC_/wsX_<stem>.tex — SKILL.md "Tiered worksheets"; give each tier
#   its own stem, e.g. verify_factoring_S_<date>.json, so tiers never share a
#   stem in one directory). More than one match for a role is an ERROR (name
#   them apart or pass --ws/--ak/--ss explicitly). Missing ak_/ss_ documents
#   are ERRORS, not skips — the skill mandates three documents — unless
#   --worksheet-only is given.
#
# GATE ORDER (fail-fast: the first FAIL stops the run and nothing after it
# executes; in particular nothing compiles after a failed verification):
#    1 template-*      tests/check_template_use.py on ws, ak, ss — the shell
#                      must \input{worksheet-preamble}, never hand-roll it
#                      (cheapest check first; nothing verifies or compiles a
#                      hand-rolled shell)
#    2 verify-ws       run_verify.sh on the worksheet JSON (2 = MANUAL, continue)
#    3 verify-ss       run_verify.sh on the study-guide JSON
#    4 coverage-ss     tests/check_ss_coverage.py — every "skill" the
#                      worksheet tags must have a tagged study-guide entry
#                      (zero/partial ws tagging is a FAIL, not a skip)
#    5 facet-coverage  tests/check_facet_coverage.py — worksheet facets must
#                      all have study-guide worked examples, and a declared
#                      "subtitle" must appear in the worksheet title block
#                      (no-op for sheets without a facet plan)
#    6 render-figures  scripts/render_figures.py, when shipped AND the JSON
#                      has triangle-type or "figure" problems (else skipped)
#    7 layout-ws       tests/check_layout.py (figure scope + work space)
#    8 compile-*       scripts/compile.sh for ws, ak, ss (ws first — it warms
#                      the tectonic package cache for the other two)
#    9 answer-key-*    tests/check_answer_key.py binds ak and ss to their JSONs
#   10 ss-structure    tests/check_study_guide.py — every worked example opens
#                      with a \step strategy line before any computation
#   11 prose-ws        tests/check_prose_consistency.py (exit 2 = parsed ZERO
#                      problems: a structural FAIL, not a manual-review pass)
#   12 prose-ss        the same checker on the study guide (examplebox prose
#                      givens bound to the ss JSON; same exit-2 semantics)
#
# EXIT CODES: 0 all gates green · 1 a gate failed (named in the verdict line)
#             · 2 green but manual review needed (run_verify's 2 propagates).

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TESTS_DIR="$SKILL_DIR/tests"

# --help prints this file's header block, so the docs above ARE the help text
# and cannot drift from it.
usage() { awk 'NR > 1 && !/^#/ {exit} NR > 1 {sub(/^# ?/, ""); print}' "${BASH_SOURCE[0]}"; }

# ── Arguments ─────────────────────────────────────────────────────────────────
JSON_FILE=""
OUT_DIR="$HOME/Documents/Worksheets"
WORKSHEET_ONLY=0
WS_OVERRIDE=""; AK_OVERRIDE=""; SS_OVERRIDE=""; VSS_OVERRIDE=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help) usage; exit 0 ;;
    --outdir) OUT_DIR="${2:?--outdir needs a directory}"; shift 2 ;;
    --worksheet-only) WORKSHEET_ONLY=1; shift ;;
    --ws) WS_OVERRIDE="${2:?--ws needs a file}"; shift 2 ;;
    --ak) AK_OVERRIDE="${2:?--ak needs a file}"; shift 2 ;;
    --ss) SS_OVERRIDE="${2:?--ss needs a file}"; shift 2 ;;
    --verify-ss) VSS_OVERRIDE="${2:?--verify-ss needs a file}"; shift 2 ;;
    -*) echo "Error: unknown option $1 (see --help)" >&2; exit 1 ;;
    *) JSON_FILE="$1"; shift ;;
  esac
done

if [[ -z "$JSON_FILE" ]]; then usage >&2; exit 1; fi
if [[ ! -f "$JSON_FILE" ]]; then
  echo "Error: verification file not found: $JSON_FILE" >&2; exit 1
fi

JSON_BASE="$(basename "$JSON_FILE")"
if [[ "$JSON_BASE" != verify_*.json ]]; then
  echo "Error: expected a file named verify_<stem>.json, got $JSON_BASE" >&2
  echo "(build.sh derives the ws_/ak_/ss_ document names from <stem>)" >&2
  exit 1
fi
STEM="${JSON_BASE#verify_}"; STEM="${STEM%.json}"
if [[ "$STEM" == ss_* ]]; then
  echo "Error: $JSON_BASE is the STUDY-GUIDE verification file. Pass the" >&2
  echo "worksheet's verify_<stem>.json — build.sh finds verify_ss_<stem>.json" >&2
  echo "on its own." >&2
  exit 1
fi
JSON_DIR="$(cd "$(dirname "$JSON_FILE")" && pwd)"
FIGS_TEX=""
WS_JSON="$JSON_DIR/$JSON_BASE"

PYTHON3="$(command -v python3 2>/dev/null || true)"
if [[ -z "$PYTHON3" ]]; then
  echo "Error: python3 not found — the layout/binding checkers need it." >&2
  exit 1
fi

# ── Result bookkeeping ────────────────────────────────────────────────────────
# One row per gate, appended in run order; finish() marks whatever never ran.
# Plain arrays only — macOS ships bash 3.2, no associative arrays.
GATES=(discover template-ws template-ak template-ss verify-ws verify-ss \
       coverage-ss facet-coverage render-figures layout-ws compile-ws \
       compile-ak compile-ss answer-key-ak answer-key-ss ss-structure \
       prose-ws prose-ss)
RESULTS=()
MANUALS=0
FAILED_GATE=""
PDFS=()
STEP=0

record() { RESULTS+=("$1|$2"); }

banner() { STEP=$((STEP + 1)); echo; echo "── step $STEP · $1"; }

finish() {
  local code="$1" row name seen g
  for g in "${GATES[@]}"; do
    seen=0
    for row in "${RESULTS[@]}"; do
      [[ "${row%%|*}" == "$g" ]] && seen=1
    done
    [[ "$seen" -eq 0 ]] && RESULTS+=("$g|SKIPPED(not reached)")
  done
  echo
  echo "── gate summary ──────────────────────────────"
  for row in "${RESULTS[@]}"; do
    printf '   %-16s %s\n' "${row%%|*}" "${row#*|}"
  done
  if [[ ${#PDFS[@]} -gt 0 ]]; then
    echo "── PDFs ──────────────────────────────────────"
    printf '   %s\n' "${PDFS[@]}"
  fi
  echo
  if [[ "$code" -eq 1 ]]; then
    echo "❌ BUILD FAILED — gate: $FAILED_GATE (fix it and re-run; later gates did not run)"
  elif [[ "$MANUALS" -gt 0 ]]; then
    code=2
    echo "✅ BUILD PASSED — $MANUALS verification run(s) flagged manual-review items (exit 2)"
  else
    echo "✅ BUILD PASSED — all gates green"
  fi
  exit "$code"
}

fail() { # gate-name [extra teaching line]
  FAILED_GATE="$1"
  record "$1" "FAIL"
  [[ $# -gt 1 ]] && echo "$2" >&2
  finish 1
}

# ── Gate 0: discovery ─────────────────────────────────────────────────────────
# Sets FOUND to the unique match for a role, or fails loudly. Tier letters sit
# INSIDE the role token (wsS_, not S_ws_ — SKILL.md's tier naming), the
# student-name prefix outside (leo_ws_).
find_role() {
  local role="$1" matches=() pat f
  for pat in "${role}" "${role}S" "${role}C" "${role}X"; do
    for f in "$JSON_DIR/${pat}_${STEM}.tex" "$JSON_DIR"/*"_${pat}_${STEM}.tex"; do
      [[ -f "$f" ]] && matches+=("$f")
    done
  done
  if [[ ${#matches[@]} -gt 1 ]]; then
    echo "Error: ambiguous ${role}_ document for stem '$STEM':" >&2
    printf '  %s\n' "${matches[@]}" >&2
    echo "Rename them apart (one worksheet set per stem per directory —" >&2
    echo "tiered sheets get tier-specific stems) or pass --${role} explicitly." >&2
    fail discover
  fi
  FOUND=""
  [[ ${#matches[@]} -eq 1 ]] && FOUND="${matches[0]}"
}

banner "discover documents for stem '$STEM' in $JSON_DIR"
if [[ -n "$WS_OVERRIDE" ]]; then WS_TEX="$WS_OVERRIDE"; else find_role ws; WS_TEX="$FOUND"; fi
if [[ -z "$WS_TEX" || ! -f "$WS_TEX" ]]; then
  fail discover "Error: worksheet ws_${STEM}.tex not found in $JSON_DIR (or --ws path missing)."
fi
AK_TEX=""; SS_TEX=""; SS_JSON=""
if [[ "$WORKSHEET_ONLY" -eq 0 ]]; then
  if [[ -n "$AK_OVERRIDE" ]]; then AK_TEX="$AK_OVERRIDE"; else find_role ak; AK_TEX="$FOUND"; fi
  if [[ -n "$SS_OVERRIDE" ]]; then SS_TEX="$SS_OVERRIDE"; else find_role ss; SS_TEX="$FOUND"; fi
  # The skill mandates three documents; a missing key or study guide is a
  # structural failure, not a skip — this is what makes the ss gate real.
  if [[ -z "$AK_TEX" || ! -f "$AK_TEX" ]]; then
    fail discover "Error: answer key ak_${STEM}.tex not found. The skill mandates ws+ak+ss; write it, or pass --worksheet-only to build the worksheet alone."
  fi
  if [[ -z "$SS_TEX" || ! -f "$SS_TEX" ]]; then
    fail discover "Error: study guide ss_${STEM}.tex not found. The skill mandates ws+ak+ss; write it, or pass --worksheet-only to build the worksheet alone."
  fi
  if [[ -n "$VSS_OVERRIDE" ]]; then SS_JSON="$VSS_OVERRIDE"; else SS_JSON="$JSON_DIR/verify_ss_${STEM}.json"; fi
  if [[ ! -f "$SS_JSON" ]]; then
    fail discover "Error: verify_ss_${STEM}.json not found. The study guide's worked examples must be verified too (SKILL.md step 3) — write the ss verification JSON next to the ws one."
  fi
fi
echo "   ws: $WS_TEX"
[[ -n "$AK_TEX" ]] && echo "   ak: $AK_TEX"
[[ -n "$SS_TEX" ]] && echo "   ss: $SS_TEX  (verify: $SS_JSON)"
record discover "PASS"

# Template shells first: the cheapest check, and it teaches the shell fix
# before any sympy verification runs — nothing downstream should ever see a
# hand-rolled preamble (the env names every later gate binds to live in the
# shipped template).
template_gate() { # gate-name tex-file
  local gate="$1" tex="$2"
  banner "template shell on $(basename "$tex")"
  if "$PYTHON3" "$TESTS_DIR/check_template_use.py" "$tex"; then
    record "$gate" "PASS"
  else
    fail "$gate"
  fi
}
template_gate template-ws "$WS_TEX"
if [[ "$WORKSHEET_ONLY" -eq 1 ]]; then
  record template-ak "SKIPPED(--worksheet-only)"
  record template-ss "SKIPPED(--worksheet-only)"
else
  template_gate template-ak "$AK_TEX"
  template_gate template-ss "$SS_TEX"
fi

# run_verify.sh exit semantics: 0 pass · 1 fail · 2 manual-review-but-safe.
run_verify_gate() { # gate-name json-file
  local gate="$1" json="$2" rc
  bash "$SCRIPT_DIR/run_verify.sh" "$json"
  rc=$?
  case "$rc" in
    0) record "$gate" "PASS" ;;
    2) record "$gate" "MANUAL"; MANUALS=$((MANUALS + 1)) ;;
    *) fail "$gate" ;;
  esac
}

banner "verify worksheet JSON ($JSON_BASE)"
run_verify_gate verify-ws "$WS_JSON"

if [[ "$WORKSHEET_ONLY" -eq 1 ]]; then
  record verify-ss "SKIPPED(--worksheet-only)"
else
  banner "verify study-guide JSON ($(basename "$SS_JSON"))"
  run_verify_gate verify-ss "$SS_JSON"
fi

# Skill coverage runs BEFORE anything renders or compiles: an uncovered skill
# means the study guide must gain a section, so later gates would be wasted.
if [[ "$WORKSHEET_ONLY" -eq 1 ]]; then
  record coverage-ss "SKIPPED(--worksheet-only)"
else
  banner "skill coverage: $JSON_BASE → $(basename "$SS_JSON")"
  if "$PYTHON3" "$TESTS_DIR/check_ss_coverage.py" "$WS_JSON" "$SS_JSON"; then
    record coverage-ss "PASS"
  else
    fail coverage-ss
  fi
fi

# Cross-file facet gates likewise run BEFORE any compile: they read only JSON
# + tex text, so a facet or subtitle drift is caught in milliseconds, not
# after three tectonic runs.
banner "facet coverage (ws facets ⊆ ss examples; subtitle binding)"
if [[ "$WORKSHEET_ONLY" -eq 1 ]]; then
  FACET_ARGS=("$WS_TEX" "$WS_JSON")
else
  FACET_ARGS=("$WS_TEX" "$WS_JSON" "$SS_JSON")
fi
if "$PYTHON3" "$TESTS_DIR/check_facet_coverage.py" "${FACET_ARGS[@]}"; then
  record facet-coverage "PASS"
else
  fail facet-coverage
fi

banner "render figures"
if [[ ! -f "$SCRIPT_DIR/render_figures.py" ]]; then
  # Defensive: the renderer ships separately; its absence is not a fault.
  echo "   render_figures.py not shipped — skipping."
  record render-figures "SKIPPED(renderer not shipped)"
elif ! grep -Eq '"type"[[:space:]]*:[[:space:]]*"triangle"|"figure"[[:space:]]*:' "$WS_JSON"; then
  echo "   no triangle-type or \"figure\" problems in the JSON — skipping."
  record render-figures "SKIPPED(no figure problems)"
else
  # render_figures imports verify.py, which needs sympy — same finder as
  # run_verify.sh so there is exactly one python-resolution path.
  source "$SCRIPT_DIR/find_python.sh"
  SYMPY_PY="$(find_sympy_python)" || fail render-figures
  if "$SYMPY_PY" "$SCRIPT_DIR/render_figures.py" "$WS_JSON"; then
    record render-figures "PASS"
    FIGS_TEX="$(dirname "$WS_JSON")/figs_${STEM}.tex"
    [[ -f "$FIGS_TEX" ]] || FIGS_TEX=""
  else
    fail render-figures
  fi
fi

banner "layout check (figure scope + work space) on $(basename "$WS_TEX")"
if "$PYTHON3" "$TESTS_DIR/check_layout.py" "$WS_TEX" ${FIGS_TEX:+--figs "$FIGS_TEX"}; then
  record layout-ws "PASS"
else
  fail layout-ws
fi

# Compile ws first: the first tectonic run downloads packages into the shared
# cache, so the ak/ss compiles that follow are fast.
compile_gate() { # gate-name tex-file
  local gate="$1" tex="$2"
  banner "compile $(basename "$tex") → $OUT_DIR"
  if bash "$SCRIPT_DIR/compile.sh" "$tex" "$OUT_DIR"; then
    record "$gate" "PASS"
    PDFS+=("$OUT_DIR/$(basename "${tex%.tex}").pdf")
  else
    fail "$gate"
  fi
}
compile_gate compile-ws "$WS_TEX"
if [[ "$WORKSHEET_ONLY" -eq 1 ]]; then
  record compile-ak "SKIPPED(--worksheet-only)"
  record compile-ss "SKIPPED(--worksheet-only)"
else
  compile_gate compile-ak "$AK_TEX"
  compile_gate compile-ss "$SS_TEX"
fi

if [[ "$WORKSHEET_ONLY" -eq 1 ]]; then
  record answer-key-ak "SKIPPED(--worksheet-only)"
  record answer-key-ss "SKIPPED(--worksheet-only)"
  record ss-structure "SKIPPED(--worksheet-only)"
else
  banner "answer-key binding: $(basename "$AK_TEX") ↔ $JSON_BASE"
  if "$PYTHON3" "$TESTS_DIR/check_answer_key.py" "$AK_TEX" "$WS_JSON"; then
    record answer-key-ak "PASS"
  else
    fail answer-key-ak
  fi
  banner "answer-key binding: $(basename "$SS_TEX") ↔ $(basename "$SS_JSON")"
  if "$PYTHON3" "$TESTS_DIR/check_answer_key.py" "$SS_TEX" "$SS_JSON"; then
    record answer-key-ss "PASS"
  else
    fail answer-key-ss
  fi
  banner "study-guide structure (strategy steps) on $(basename "$SS_TEX")"
  if "$PYTHON3" "$TESTS_DIR/check_study_guide.py" "$SS_TEX" "$SS_JSON"; then
    record ss-structure "PASS"
  else
    fail ss-structure
  fi
fi

banner "prose consistency on $(basename "$WS_TEX")"
"$PYTHON3" "$TESTS_DIR/check_prose_consistency.py" "$WS_TEX" "$WS_JSON" ${FIGS_TEX:+--figs "$FIGS_TEX"}
rc=$?
if [[ "$rc" -eq 0 ]]; then
  record prose-ws "PASS"
elif [[ "$rc" -eq 2 ]]; then
  # NOT a manual-review pass: exit 2 here means the checker parsed ZERO
  # problem blocks, i.e. nothing was checked at all.
  fail prose-ws "Error: check_prose_consistency parsed no problems — the worksheet must use \\problem{...} or an enumerate/\\item list. Nothing was checked, so this is a structural failure."
else
  fail prose-ws
fi

# Study-guide prose binding: the ss is the one document the student learns
# from FIRST and has no answer key to cross-check against — a drifted prose
# given beside a correct expr is invisible to every other gate. Runs after
# answer-key-ss (which hard-fails on box-count != problem_count), so the
# order-based example↔entry mapping is sound whenever this runs. No --figs:
# ss documents carry no \probfig, and if one ever appears the unresolved-
# probfig branch exits 2 loudly, which is correct.
if [[ "$WORKSHEET_ONLY" -eq 1 ]]; then
  record prose-ss "SKIPPED(--worksheet-only)"
else
  banner "prose consistency on $(basename "$SS_TEX")"
  "$PYTHON3" "$TESTS_DIR/check_prose_consistency.py" "$SS_TEX" "$SS_JSON"
  rc=$?
  if [[ "$rc" -eq 0 ]]; then
    record prose-ss "PASS"
  elif [[ "$rc" -eq 2 ]]; then
    fail prose-ss "Error: check_prose_consistency parsed no worked examples — the study guide must keep one worked example per examplebox (SKILL.md: box count = problem_count). Nothing was checked, so this is a structural failure."
  else
    fail prose-ss
  fi
fi

finish 0
