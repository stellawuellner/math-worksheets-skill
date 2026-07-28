#!/usr/bin/env python3
r"""
check_log.py — gate the LaTeX log so a broken PDF cannot ship behind a green
checkmark.

Usage: python3 scripts/check_log.py <file.log>
       OVERFULL_PT=<points> to tune the overfull threshold (default 2)

An engine can exit 0 and produce *a* PDF while the output is unusable: an
undefined \ref prints literally as "??", a Missing character silently drops a
glyph from the page, and an Overfull \hbox runs text off the printed sheet.
All three live ONLY in the .log — tectonic even deletes it unless --keep-logs
— so no source-side checker can see them, and compile.sh used to print
"PDF ready" over all of them. compile.sh now runs this scan on the kept log
after every compile (both engines write the same log format) and propagates
the exit code.

Rules:
  FAIL  "LaTeX Warning: Reference ... undefined"  — the PDF prints "??"
  FAIL  "There were undefined references"          — ditto, the summary line
  FAIL  "Missing character"                        — a glyph is absent from
        the PDF (usually a Unicode symbol pdflatex cannot typeset; see the
        ASCII-only rule in references/latex-templates.md)
  FAIL  Overfull \hbox above OVERFULL_PT points    — text physically runs off
        the page edge. Default 2pt: sub-point overhangs are invisible on
        paper and blocking them would teach agents to bypass the gate.
  WARN  Overfull \vbox                             — reported, never fails:
        \vbox warnings are noisy on fixed-height layouts (every nearly-full
        page emits one), so blocking on them would produce false alarms.
        Revisit if a sheet ever ships with visibly clipped columns.

Exit 0 clean, 1 on any FAIL, 2 on usage/unreadable file.
"""
import os
import re
import sys

# (pattern, why it means the PDF is broken, how to fix it)
HARD_RULES = [
    (re.compile(r"LaTeX Warning: Reference .*"),
     "an undefined \\ref prints literally as '??' in the PDF",
     "fix or remove the \\ref, or add the missing \\label"),
    (re.compile(r"There were undefined references"),
     "at least one \\ref printed as '??'",
     "match every \\ref{...} to an existing \\label{...}"),
    (re.compile(r"^Missing character: .*", re.M),
     "the engine dropped a glyph — it is simply absent from the printed page",
     "replace the character with a LaTeX macro or ASCII marker "
     "(see the ASCII-only rule in references/latex-templates.md)"),
]
HBOX_RE = re.compile(r"Overfull \\hbox \((\d+(?:\.\d+)?)pt too wide.*")
VBOX_RE = re.compile(r"Overfull \\vbox \((\d+(?:\.\d+)?)pt too.*")


def scan(log_text, overfull_pt):
    """Return (failures, warnings) — each a list of (offending line, advice)."""
    failures, warnings = [], []
    for pattern, why, fix in HARD_RULES:
        for m in pattern.finditer(log_text):
            failures.append((m.group(0).strip(), f"{why} — {fix}"))
    for m in HBOX_RE.finditer(log_text):
        pts = float(m.group(1))
        advice = ("text physically overflows the printed page — shorten the "
                  "line, allow a break point, or scale the figure")
        if pts > overfull_pt:
            failures.append((m.group(0).strip(), advice))
        else:
            warnings.append((m.group(0).strip(),
                             f"under the {overfull_pt}pt threshold — invisible on paper"))
    for m in VBOX_RE.finditer(log_text):
        warnings.append((m.group(0).strip(),
                         "vertical overfull — check the page for clipped content "
                         "(reported only; \\vbox warnings are noisy on full pages)"))
    return failures, warnings


def main(argv):
    if len(argv) != 2:
        print("Usage: check_log.py <file.log>   (OVERFULL_PT=<points> to tune)",
              file=sys.stderr)
        return 2
    try:
        # LaTeX logs are not reliably UTF-8 (raw bytes from fonts/engines)
        log_text = open(argv[1], encoding="utf-8", errors="replace").read()
    except OSError as e:
        print(f"check_log: cannot read {argv[1]}: {e}", file=sys.stderr)
        return 2

    try:
        overfull_pt = float(os.environ.get("OVERFULL_PT", "2"))
    except ValueError:
        print("check_log: OVERFULL_PT must be a number (points)", file=sys.stderr)
        return 2

    failures, warnings = scan(log_text, overfull_pt)
    for line, advice in warnings:
        print(f"  ⚠ {line}\n    ({advice})")
    for line, advice in failures:
        print(f"  ❌ {line}\n    → {advice}")
    if failures:
        print(f"\n❌ {len(failures)} log fault(s): this PDF would ship with "
              "'??' references, missing glyphs, or text running off the page. "
              "Fix the LaTeX and recompile.")
        return 1
    print("✅ log clean — no undefined references, missing characters, or "
          f"overfull lines above {overfull_pt}pt.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
