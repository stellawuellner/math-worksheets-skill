#!/usr/bin/env python3
r"""check_answer_line.py — bind the worksheet's printed answer lines to the
verify JSON's answer_unit declarations (the sheet-side unit gate).

Usage: python3 tests/check_answer_line.py <ws_*.tex> <verify.json>

Why: verify.py proves the VALUE of every expected answer, and
check_answer_key.py binds the key's printed unit — this checker covers the
student-facing sheet, where the unit is part of the question:

  * a problem that declares "answer_unit" must carry an \answerline whose
    argument prints that unit (token-sequence match via tests/_units.py, so
    \answerline{cm$^2$} satisfies a declared "cm^2");
  * an \answerline with a non-empty unit argument on a problem that declares
    NO answer_unit is an unverified unit — declare it or drop it;
  * unit-less problems need no \answerline at all: \ansline (or the
    \problem-emitted line) is fine, and graph/proof problems opt out with
    \noansline. That stays SKILL.md guidance, not a gate — a universal
    \answerline requirement would false-fail good sheets.

Segmentation is the shared _tex_segments.segment_spans, so the enumerate,
\problem and examplebox shapes all parse. Exit 0 clean · 1 unit-binding
failure · 2 when zero problems parse (nothing was checked — NOT a pass,
mirroring the sibling checkers).
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _tex_segments import segment_spans, blank_comments  # noqa: E402
from _units import unit_in  # noqa: E402

ANSWERLINE_RE = re.compile(r"\\answerline\{([^{}]*)\}")


def main():
    if len(sys.argv) != 3:
        print("Usage: check_answer_line.py <ws.tex> <verify.json>",
              file=sys.stderr)
        return 2
    tex = blank_comments(open(sys.argv[1]).read())
    data = json.load(open(sys.argv[2]))
    spans = segment_spans(tex)
    if spans is None:
        print("\n  ⚠ PARSED ZERO PROBLEMS from this file.")
        print("    Nothing was checked, so this is NOT a pass. The worksheet")
        print("    must use \\problem{...} or an enumerate/\\item list.")
        return 2
    segments = [tex[a:b] for a, b in spans]

    declared = {}
    for e in data.get("problems", []):
        if isinstance(e, dict) and isinstance(e.get("answer_unit"), str):
            declared.setdefault(int(e.get("id", 0)), e["answer_unit"])

    print(f"Answer-line binding: {sys.argv[1]} "
          f"({len(segments)} problem segments, "
          f"{len(declared)} declared unit(s))")

    faults = []
    for pid, want in sorted(declared.items()):
        if pid > len(segments):
            faults.append(
                f"problem {pid} declares answer_unit '{want}' but the sheet "
                f"parses only {len(segments)} problem(s) — every declared "
                f"unit needs a problem (and its \\answerline) on the page")
    for i, seg in enumerate(segments, 1):
        args = ANSWERLINE_RE.findall(seg)
        want = declared.get(i)
        if want is not None:
            if not any(unit_in(arg, want) for arg in args):
                faults.append(
                    f"problem {i} declares answer_unit '{want}' but the sheet "
                    f"has no matching \\answerline — end the problem with "
                    f"\\answerline{{{want}}} so the student answers in the "
                    f"verified unit")
        else:
            for arg in args:
                if arg.strip():
                    faults.append(
                        f"problem {i} prints \\answerline{{{arg}}} but its "
                        f"JSON entry declares no answer_unit — the printed "
                        f"unit is unverified. Add \"answer_unit\" to problem "
                        f"{i} in the verify JSON, or drop the unit argument")

    if faults:
        for f in faults:
            print(f"  ❌ {f}.")
        print(f"\n❌ {len(faults)} unit-binding failure(s) — fix the sheet "
              "before delivering.")
        return 1
    print("✅ every declared answer_unit has a matching \\answerline and no "
          "undeclared unit is printed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
