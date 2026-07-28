#!/usr/bin/env python3
"""
check_prose_consistency.py — flag numbers in worksheet prose that don't appear
as givens in the verify JSON (the word-problem analog of the figure rule).

Usage: python3 tests/check_prose_consistency.py <worksheet.tex> <verify.json>
                [--figs <figs.tex>]

Matches worksheet \\problem{...} blocks to verify-JSON entries by order
(problem i ↔ i-th JSON id). Heuristic by design — a report for graders and
generators, not a hard gate. Exit 0 always unless files are unreadable, the
parse comes up empty, or \\probfig{N} figures cannot be resolved (pass the
figs file scripts/render_figures.py emitted via --figs, or the figure check
runs blind).
"""

import json
import re
import sys

from _probfig import CALL_RE, expand_probfigs, probfig_bodies

NUM_RE = re.compile(r"\d+(?:\.\d+)?|\.\d+")


def item_blocks(tex):
    """Extract each \\item body inside an enumerate.

    The shipped worksheet templates use enumerate/\\item rather than the
    \\problem{...} macro, so a generator that follows the templates produced
    ZERO parsed blocks here and the report still said "all consistent".
    Parsing both shapes is what makes this checker apply to real worksheets.
    """
    blocks = []
    for env in re.finditer(r"\\begin\{enumerate\}(.*?)\\end\{enumerate\}", tex, re.S):
        body = env.group(1)
        parts = re.split(r"\\item\b", body)[1:]
        blocks.extend(p.strip() for p in parts if p.strip())
    return blocks


def problem_blocks(tex):
    """Extract the argument of each \\problem{...} handling nested braces."""
    blocks = []
    for m in re.finditer(r"\\problem\{", tex):
        i, depth, buf = m.end(), 1, []
        while i < len(tex) and depth:
            c = tex[i]
            depth += (c == "{") - (c == "}")
            if depth:
                buf.append(c)
            i += 1
        blocks.append("".join(buf))
    return blocks


def prose_numbers(block):
    # drop TikZ coordinates (not human-visible), but keep figure LABELS —
    # see figure_label_numbers, which is checked separately (CASE-21)
    block = re.sub(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", "", block,
                   flags=re.S)
    # drop \probfig{N} calls — the braced arg is a problem INDEX, not a prose
    # value, and would otherwise be flagged as "missing from JSON" noise
    block = re.sub(r"\\probfig\{\d+\}", "", block)
    # drop spacing/format macro arguments like \hspace{4.5cm}, \vspace{5cm}
    block = re.sub(r"\\[a-zA-Z]+\{[\d.]+[a-z]{2}\}", "", block)
    return {float(n) for n in NUM_RE.findall(block)}


def figure_label_numbers(block):
    """Numbers printed in figure LABELS — \\node[...]{...} text and pic "..."
    quotes. These are the human-visible figure values that must come from the
    JSON (audit 3d: previously the whole tikzpicture was stripped, so a figure
    labeled with a wrong side length was never checked). Excludes coordinates."""
    nums = set()
    for m in re.finditer(r"\\node\b[^{]*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}", block):
        label = m.group(1)
        label = re.sub(r"\\[dt]?frac\s*\{?(-?\d+)\}?\s*\{?(-?\d+)\}?", r"\1/\2", label)
        # subscript indices are point NAMES, not printed quantities — the SSA
        # swing figure labels its two apexes $B_1$/$B_2$
        label = re.sub(r"_\{?\d+\}?", "", label)
        nums |= {float(n) for n in NUM_RE.findall(label)}
    for m in re.finditer(r'"\s*\$?([^"$]*)\$?\s*"', block):  # pic "$34^\circ$"
        nums |= {float(n) for n in NUM_RE.findall(m.group(1))}
    return nums


def json_numbers(entry):
    found = set()

    def walk(v):
        if isinstance(v, bool):
            return
        if isinstance(v, (int, float)):
            found.add(float(v))
        elif isinstance(v, str):
            for n in NUM_RE.findall(v):
                found.add(float(n))
        elif isinstance(v, list):
            for x in v:
                walk(x)
        elif isinstance(v, dict):
            for x in v.values():
                walk(x)

    walk({k: v for k, v in entry.items() if k not in ("id", "note", "desc")})
    return found


def main():
    argv = sys.argv[1:]
    figs_path = None
    if "--figs" in argv:
        i = argv.index("--figs")
        figs_path = argv[i + 1] if i + 1 < len(argv) else ""
        del argv[i:i + 2]
    if len(argv) != 2 or figs_path == "":
        print("Usage: check_prose_consistency.py <worksheet.tex> <verify.json> "
              "[--figs <figs.tex>]", file=sys.stderr)
        sys.exit(2)
    tex_path, json_path = argv
    tex = open(tex_path).read()
    data = json.load(open(json_path))
    # Expand \probfig{N} into the rendered figure bodies BEFORE parsing, so
    # the figure-label check (CASE-21) sees the labels the student sees. An
    # unresolved call means an UNCHECKED figure — like the zero-parse guard
    # below, that must never read as a pass.
    if figs_path:
        tex, unresolved = expand_probfigs(tex, probfig_bodies(open(figs_path).read()))
    else:
        unresolved = sorted({int(n) for n in CALL_RE.findall(tex)})
    if unresolved:
        print(f"  ⚠ UNRESOLVED \\probfig for problem(s) {unresolved}.")
        print("    Those figures' labels live in the generated figs file, so this")
        print("    check cannot see them. Re-run with the file render_figures.py")
        print("    emitted:  --figs /tmp/figs_TOPIC_DATE.tex")
        print("    (and re-run scripts/render_figures.py if the JSON changed).")
        sys.exit(2)
    blocks = problem_blocks(tex) or item_blocks(tex)
    # group JSON entries by id — one worksheet problem may have several checks
    by_id = {}
    for e in data.get("problems", []):
        by_id.setdefault(int(e.get("id", 0)), []).append(e)

    total_nums = matched = 0
    report = []
    fig_flags = []
    for i, block in enumerate(blocks):
        prose = prose_numbers(block)
        given = set()
        for entry in by_id.get(i + 1, []):
            given |= json_numbers(entry)
        # 100·x style: a prose "20%" is 20 in prose but 0.2 or 20/100 in JSON
        given |= {g * 100 for g in given} | {g / 100 for g in given if g}
        missing = sorted(p for p in prose if p not in given)
        total_nums += len(prose)
        matched += len(prose) - len(missing)
        report.append((i + 1, sorted(prose), missing))
        # figure-label consistency (CASE-21): visible figure numbers must be givens
        fig = figure_label_numbers(block)
        fig_missing = sorted(f for f in fig if f not in given and f not in prose)
        if fig_missing:
            fig_flags.append((i + 1, fig_missing))

    print(f"Prose-consistency report: {tex_path}")
    if not blocks:
        print("\n  ⚠ PARSED ZERO PROBLEMS from this file.")
        print("    Nothing was checked, so this is NOT a pass. The worksheet")
        print("    must use \\problem{...} or an enumerate/\\item list.")
        sys.exit(2)
    for pid, prose, missing in report:
        flag = f"  ⚠ missing from JSON: {missing}" if missing else "  ok"
        print(f"  problem {pid}: {len(prose)} prose numbers{flag}")
    rate = matched / total_nums if total_nums else 1.0
    scope = f"{len(blocks)} problem block(s)"
    print(f"\nMatch rate: {matched}/{total_nums} ({100*rate:.1f}%) across {scope}")
    if total_nums == 0:
        print("  ⚠ no numbers found in any problem — check the parse before trusting this")
    if fig_flags:
        print("Figure-label numbers not found in JSON givens (audit 3d):")
        for pid, miss in fig_flags:
            print(f"  ⚠ problem {pid}: figure shows {miss}")
    else:
        print("Figure labels: all consistent with JSON givens.")
    print("(heuristic — investigate misses; derived/rounded prose values and "
          "dates are expected false flags)")


if __name__ == "__main__":
    main()
