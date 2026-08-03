#!/usr/bin/env python3
r"""
check_log.py — gate the LaTeX log so a broken PDF cannot ship behind a green
checkmark.

Usage: python3 scripts/check_log.py <file.log> [--max-pages N]
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
  FAIL  page count above --max-pages N              — read from the log's
        "Output written on <file>.pdf (N pages" line (tectonic and pdflatex
        both print it, so the count is the engine's own, never estimated).
        build.sh passes the cap per role: SKILL.md hard-caps the study guide
        at 2 pages, and worksheets/answer keys get sanity ceilings. Without
        the flag the page gate is off — the cap is the caller's to declare.
  LOUD  --max-pages set but no "Output written" line — exit 2, never a pass:
        a budget the log cannot answer must fail loudly (same doctrine as an
        unreadable file), or the cap silently goes unenforced.

Exit 0 clean, 1 on any FAIL, 2 on usage/unreadable file/uncheckable budget.
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
# The engine's own final page count: "Output written on <file>.pdf (N pages,"
# (singular "1 page," for one). Both tectonic (--keep-logs) and pdflatex end
# their logs with this line, so the count is read, never estimated.
#
# TeX hard-wraps its log at 79 columns, ANYWHERE — including mid-path and
# between "pages" and the comma that used to be required here. That made this
# gate a function of how long the output path happened to be: a build in
# /tmp/evalbuild/curr-251/ with a 21-character stem wrapped right after
# "(5 pages", the match failed, and the build died claiming the log had no page
# count at all while the log plainly did. Found in an eval run, where the long
# per-task directories made it reproducible. So: unwrap first, and do not
# require the trailing delimiter.
OUTPUT_RE = re.compile(r"Output written on .*?\((\d+)\s*pages?")
WRAP = 79


def page_count(log_text):
    """Page count from the log's 'Output written' line, or None if absent.

    Matched against BOTH the raw log and an unwrapped copy, because the line may
    be split at the engine's column limit. Unwrapping only joins lines that are
    exactly at the wrap width, so genuinely separate lines stay separate.
    """
    m = OUTPUT_RE.search(log_text)
    if m:
        return int(m.group(1))
    joined, buf = [], ""
    for line in log_text.splitlines():
        buf += line
        if len(line) < WRAP:
            joined.append(buf)
            buf = ""
    if buf:
        joined.append(buf)
    m = OUTPUT_RE.search("\n".join(joined))
    return int(m.group(1)) if m else None


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
    args = list(argv[1:])
    max_pages = None
    if "--max-pages" in args:
        i = args.index("--max-pages")
        try:
            max_pages = int(args[i + 1])
        except (IndexError, ValueError):
            print("check_log: --max-pages needs a positive integer (a page "
                  "budget, e.g. --max-pages 2)", file=sys.stderr)
            return 2
        if max_pages < 1:
            print("check_log: --max-pages must be at least 1 — a zero/negative "
                  "budget can never pass and means the caller is misconfigured",
                  file=sys.stderr)
            return 2
        del args[i:i + 2]
    if len(args) != 1:
        print("Usage: check_log.py <file.log> [--max-pages N]   "
              "(OVERFULL_PT=<points> to tune)", file=sys.stderr)
        return 2
    try:
        # LaTeX logs are not reliably UTF-8 (raw bytes from fonts/engines)
        log_text = open(args[0], encoding="utf-8", errors="replace").read()
    except OSError as e:
        print(f"check_log: cannot read {args[0]}: {e}", file=sys.stderr)
        return 2

    try:
        overfull_pt = float(os.environ.get("OVERFULL_PT", "2"))
    except ValueError:
        print("check_log: OVERFULL_PT must be a number (points)", file=sys.stderr)
        return 2

    failures, warnings = scan(log_text, overfull_pt)

    pages = None
    if max_pages is not None:
        pages = page_count(log_text)
        if pages is None:
            # The cap must never be silently unenforced: a truncated log (or a
            # changed engine format) that hides the page count is exit 2, the
            # same loud-not-a-pass doctrine as an unreadable file.
            print("check_log: --max-pages is set but the log has no 'Output "
                  "written on <file>.pdf (N pages' line, so the page budget "
                  "CANNOT be checked. Recompile with a full log (tectonic "
                  "--keep-logs; pdflatex writes it by default) and re-run.",
                  file=sys.stderr)
            return 2
        if pages > max_pages:
            failures.append((
                f"Output written: {pages} pages (budget: {max_pages})",
                f"the document runs {pages} pages against its {max_pages}-page "
                "budget — SKILL.md hard-caps the study guide at 2 pages, and "
                "worksheets/answer keys get sanity ceilings (build.sh sets "
                "them). FIRST: if the overrun is real content the budget could "
                "not see — a displayed-math stem, a hand-built figure, a table "
                "in the stem — declare \"workspace_cm\" on those problems and "
                "the ceiling rises with them. The budget is computed from the "
                "JSON, so anything it cannot see must be declared. Only if the "
                "sheet is genuinely padded should you cut optional sections "
                "(watch-out box, vocabulary) or split it; shrinking work space "
                "to fit a ceiling is the trade this project rejects"))

    for line, advice in warnings:
        print(f"  ⚠ {line}\n    ({advice})")
    for line, advice in failures:
        print(f"  ❌ {line}\n    → {advice}")
    if failures:
        print(f"\n❌ {len(failures)} log fault(s): this PDF would ship with "
              "'??' references, missing glyphs, text running off the page, "
              "or too many pages. Fix the LaTeX and recompile.")
        return 1
    budget_note = ""
    if max_pages is not None:
        budget_note = f" {pages} page(s), within the {max_pages}-page budget."
    print("✅ log clean — no undefined references, missing characters, or "
          f"overfull lines above {overfull_pt}pt.{budget_note}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
