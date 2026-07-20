#!/usr/bin/env bash
# compile.sh — Compile a LaTeX file to PDF using tectonic
# Usage: compile.sh <input.tex> [output-dir]
#
# Requirements: tectonic (brew install tectonic)
# Tectonic auto-downloads any missing LaTeX packages on first use.

set -euo pipefail

TEX_FILE="${1:-}"
OUT_DIR="${2:-$(dirname "$TEX_FILE")}"

if [[ -z "$TEX_FILE" ]]; then
  echo "Usage: compile.sh <input.tex> [output-dir]" >&2
  exit 1
fi

if [[ ! -f "$TEX_FILE" ]]; then
  echo "Error: File not found: $TEX_FILE" >&2
  exit 1
fi

# Locate a LaTeX engine: tectonic preferred (auto-downloads packages);
# pdflatex fallback for systems with a classic TeX install (packages must
# already be present — needs texlive-latex-base + texlive-pictures or similar).
TECTONIC=""
for candidate in "$(command -v tectonic 2>/dev/null || true)" \
                 "/opt/homebrew/bin/tectonic" \
                 "/usr/local/bin/tectonic" \
                 "${HOME}/.cargo/bin/tectonic" \
                 "/home/linuxbrew/.linuxbrew/bin/tectonic"; do
  if [[ -n "$candidate" && -x "$candidate" ]]; then
    TECTONIC="$candidate"
    break
  fi
done
PDFLATEX="$(command -v pdflatex 2>/dev/null || true)"

if [[ -z "$TECTONIC" && -z "$PDFLATEX" ]]; then
  echo "Error: no LaTeX engine found. Install tectonic (brew/cargo install tectonic)" >&2
  echo "or a TeX distribution providing pdflatex." >&2
  exit 1
fi

mkdir -p "$OUT_DIR"

echo "Compiling: $(basename "$TEX_FILE") → $OUT_DIR/"
if [[ -n "$TECTONIC" ]]; then
  "$TECTONIC" "$TEX_FILE" --outdir "$OUT_DIR" 2>&1 | grep -v "^note: downloading"
else
  LOG="$(mktemp)"
  if ! "$PDFLATEX" -interaction=nonstopmode -halt-on-error \
       -output-directory "$OUT_DIR" "$TEX_FILE" > "$LOG" 2>&1; then
    echo "pdflatex failed — last lines of log:" >&2
    tail -25 "$LOG" >&2
    if grep -q "\.sty' not found" "$LOG"; then
      echo "Hint: pdflatex doesn't auto-download packages — install texlive-latex-extra" >&2
      echo "(plus texlive-pictures for TikZ/pgfplots) or use tectonic instead." >&2
    fi
    rm -f "$LOG"
    exit 1
  fi
  rm -f "$LOG"
  # pdflatex (unlike tectonic) drops .aux/.log next to the PDF — the output
  # directory is a deliverable, keep only the PDF
  JOB="$(basename "${TEX_FILE%.tex}")"
  rm -f "${OUT_DIR}/${JOB}.aux" "${OUT_DIR}/${JOB}.log" "${OUT_DIR}/${JOB}.out"
fi

PDF="${OUT_DIR}/$(basename "${TEX_FILE%.tex}").pdf"
if [[ -f "$PDF" ]]; then
  echo "✅ PDF ready: $PDF"
  echo "$PDF"
else
  echo "❌ Compilation failed — check LaTeX errors above" >&2
  exit 1
fi
