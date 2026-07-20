#!/usr/bin/env python3
"""
check_prose_consistency.py — flag numbers in worksheet prose that don't appear
as givens in the verify JSON (the word-problem analog of the figure rule).

Usage: python3 tests/check_prose_consistency.py <worksheet.tex> <verify.json>

Matches worksheet \\problem{...} blocks to verify-JSON entries by order
(problem i ↔ i-th JSON id). Heuristic by design — a report for graders and
generators, not a hard gate. Exit 0 always unless files are unreadable.
"""

import json
import re
import sys

NUM_RE = re.compile(r"\d+(?:\.\d+)?|\.\d+")


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
    # drop TikZ (figure numbers are covered by the figure rule)
    block = re.sub(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", "", block,
                   flags=re.S)
    # drop spacing/format macro arguments like \hspace{4.5cm}, \vspace{5cm}
    block = re.sub(r"\\[a-zA-Z]+\{[\d.]+[a-z]{2}\}", "", block)
    return {float(n) for n in NUM_RE.findall(block)}


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
    tex_path, json_path = sys.argv[1], sys.argv[2]
    tex = open(tex_path).read()
    data = json.load(open(json_path))
    blocks = problem_blocks(tex)
    # group JSON entries by id — one worksheet problem may have several checks
    by_id = {}
    for e in data.get("problems", []):
        by_id.setdefault(int(e.get("id", 0)), []).append(e)

    total_nums = matched = 0
    report = []
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

    print(f"Prose-consistency report: {tex_path}")
    for pid, prose, missing in report:
        flag = f"  ⚠ missing from JSON: {missing}" if missing else "  ok"
        print(f"  problem {pid}: {len(prose)} prose numbers{flag}")
    rate = matched / total_nums if total_nums else 1.0
    print(f"\nMatch rate: {matched}/{total_nums} ({100*rate:.1f}%)")
    print("(heuristic — investigate misses; derived/rounded prose values and "
          "dates are expected false flags)")


if __name__ == "__main__":
    main()
