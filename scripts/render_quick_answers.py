#!/usr/bin/env python3
r"""render_quick_answers.py — construct the answer key's compact "Quick
Answers" bank FROM the verify JSON, so the at-a-glance grading column can
never disagree with the verified values.

Usage: render_quick_answers.py <verify_<stem>.json> <ak_<stem>.tex> [out.tex]
Default output: qa_<stem>.tex next to the JSON (verify_ prefix -> qa_,
mirroring figs_/meta_ naming). build.sh re-runs this EVERY build — the
render-figures pattern — so the gated path cannot go stale and no staleness
lint is needed (a value-comparison checker would just duplicate this
generator).

The bank is one multicols block of "N. value" entries, one per problem id
1..problem_count (verify.py guarantees full id coverage). Entries are PLAIN
TEXT, never \ans/\boxed: check_answer_key.py binds only boxed answers inside
problem segments and never resolves \input, so the bank cannot degrade the
strict per-problem gate (fixture-locked invariant).

Rendering rules (nothing raw is ever injected into LaTeX):
  * numeric expected — verbatim as written in the JSON (Decimal parse keeps
    a verified 6.30 printing as 6.30, not 6.3);
  * string expected — sympify -> sympy.latex; if sympify fails the entry
    falls back to "---" (TeX em-dash, "see solution");
  * lists comma-joined, dicts as var = value pairs;
  * manual-only ids print "---";
  * multi-entry ids join all expected values.
Column count adapts to the widest rendered entry (4 / 3 / 2) so factored and
interval answers don't wreck the layout.

PREFLIGHT: the ak_ source must \input{worksheet-preamble} (a hand-rolled
preamble is the transcription-drift class that produced the one-answer-per-
paragraph key this tool exists to fix, and the shipped preamble is what
guarantees multicol and the compact \ans) and must \input the bank file —
a generated bank the key never shows is the real silent failure. Both are
hard errors with teaching messages, fixture-tested.

Exit 0: bank written. Exit 1: preflight failure or invalid input.
"""

import json
import os
import re
import sys
from decimal import Decimal

import sympy


def _fmt(v):
    """One expected value -> bank text (never raw string injection)."""
    if isinstance(v, bool):
        return "---"
    if isinstance(v, (int, Decimal)):
        return str(v)
    if isinstance(v, float):
        return repr(v)
    if isinstance(v, str):
        try:
            return "$" + sympy.latex(sympy.sympify(v)) + "$"
        except (sympy.SympifyError, SyntaxError, TypeError, ValueError):
            return "---"
    if isinstance(v, list):
        return ", ".join(_fmt(x) for x in v)
    if isinstance(v, dict):
        return ", ".join(f"${k} = $ {_fmt(x)}" for k, x in sorted(v.items()))
    return "---"


def render_entry(entries):
    """All of one problem id's entries -> its single bank line text."""
    vals = [e["expected"] for e in entries
            if isinstance(e, dict) and "expected" in e]
    if not vals:  # manual-only: the worked solution is the answer
        return "---"
    text = ", ".join(_fmt(v) for v in vals)
    return text if text else "---"


def column_count(entries_text):
    """Deterministic adaptive columns: 4 for short entries, 3, then 2."""
    width = max((len(t) for t in entries_text), default=0)
    if width <= 12:
        return 4
    if width <= 20:
        return 3
    return 2


def render(data):
    by_id = {}
    for p in data.get("problems", []):
        if isinstance(p, dict) and isinstance(p.get("id"), int):
            by_id.setdefault(p["id"], []).append(p)
    pc = data.get("problem_count")
    n = pc if isinstance(pc, int) and pc > 0 else (max(by_id) if by_id else 0)
    if n == 0:
        raise ValueError("no problems in the verify JSON — nothing to bank")
    entries = [render_entry(by_id.get(i, [])) for i in range(1, n + 1)]
    cols = column_count(entries)
    lines = [
        "% GENERATED every build by scripts/render_quick_answers.py from the",
        "% verify JSON -- edit the JSON, not this file. Entries are plain",
        "% text, never \\ans/\\boxed, so check_answer_key.py's per-problem",
        "% binding stays STRICT (the checker never resolves \\input, and only",
        "% boxed answers inside problem segments count).",
        "\\medskip\\noindent{\\small\\textbf{Quick Answers}}\\par\\nopagebreak",
        "\\vspace{2pt}\\noindent\\rule{\\linewidth}{0.4pt}\\par\\nopagebreak",
        f"\\begin{{multicols}}{{{cols}}}\\small\\raggedcolumns\\noindent",
    ]
    for i, t in enumerate(entries, 1):
        sep = " \\\\" if i < len(entries) else ""
        lines.append(f"{i}.~{t}{sep}")
    lines += [
        "\\end{multicols}",
        "\\noindent\\rule{\\linewidth}{0.4pt}\\medskip",
        "",
    ]
    return "\n".join(lines)


def preflight(ak_tex, out_base):
    """Teaching-message errors for the two silent-failure classes."""
    faults = []
    if not re.search(r"\\input\{[^}]*worksheet-preamble(?:\.tex)?\}", ak_tex):
        faults.append(
            "the answer key does not \\input{worksheet-preamble} — hand-rolled "
            "preambles are the transcription-drift class that produced the "
            "one-answer-per-paragraph key, and the shipped preamble is what "
            "provides multicol and the compact \\ans. Start the key with the "
            "template preamble (see templates/worksheet-preamble.tex).")
    token = re.escape(out_base[:-len(".tex")] if out_base.endswith(".tex")
                      else out_base)
    if not re.search(r"\\input\{[^}]*" + token + r"(?:\.tex)?\}", ak_tex):
        faults.append(
            f"the quick-answer bank was generated but the key never shows it — "
            f"add \\input{{{token}}} directly under \\aktitleblock.")
    return faults


def main(argv):
    if len(argv) not in (3, 4):
        print("Usage: render_quick_answers.py <verify_TOPIC_DATE.json> "
              "<ak_TOPIC_DATE.tex> [out.tex]", file=sys.stderr)
        return 1
    json_path, ak_path = argv[1], argv[2]
    base = os.path.basename(json_path)
    stem = base[len("verify_"):] if base.startswith("verify_") else base
    stem = stem[:-len(".json")] if stem.endswith(".json") else stem
    out_path = argv[3] if len(argv) == 4 else \
        os.path.join(os.path.dirname(os.path.abspath(json_path)),
                     f"qa_{stem}.tex")
    try:
        # Decimal float parsing keeps the JSON's written precision: a verified
        # 6.30 must print 6.30 in the bank, not 6.3
        data = json.load(open(json_path), parse_float=Decimal)
        ak_tex = open(ak_path).read()
    except (OSError, json.JSONDecodeError) as e:
        print(f"Error reading input: {e}", file=sys.stderr)
        return 1
    faults = preflight(ak_tex, os.path.basename(out_path))
    if faults:
        for f in faults:
            print(f"render_quick_answers.py: {f}", file=sys.stderr)
        return 1
    try:
        text = render(data)
    except ValueError as e:
        print(f"render_quick_answers.py: {e}", file=sys.stderr)
        return 1
    with open(out_path, "w") as f:
        f.write(text)
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
