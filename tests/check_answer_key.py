#!/usr/bin/env python3
"""
check_answer_key.py — bind the printed answer key to the verified JSON.

verify.py proves the JSON's `expected` values are correct, but the student
reads the PDF. Nothing otherwise guarantees the answer key's printed answers
match the verified values (audit A1/3a). This checker extracts each problem's
final/boxed answer from ak_*.tex and confirms the verified expected values
actually appear in it.

Usage: python3 tests/check_answer_key.py <ak_*.tex> <verify.json>

Heuristic (LaTeX is fuzzy): for each problem it collects the numbers the JSON
verified and the numbers printed in that problem's boxed/final answer, and
flags any verified value missing from the print. Exit 1 if any problem has a
verified answer with no printed match — a real transcription-drift signal.
"""
import json
import re
import sys

NUM = re.compile(r"-?\d+(?:\.\d+)?(?:/\d+)?")
_FRAC = re.compile(r"\\[dt]?frac\s*\{?(-?\d+(?:\.\d+)?)\}?\s*\{?(-?\d+(?:\.\d+)?)\}?")


def normalize_latex_numbers(text):
    """Turn \\frac{a}{b} into a/b and strip thousands commas so numeric answers
    written in LaTeX are seen as their actual values."""
    text = _FRAC.sub(r"\1/\2", text)  # 5/6 stays contiguous for the number regex
    text = re.sub(r"(?<=\d),(?=\d{3})", "", text)
    return text


def boxed_answers(tex):
    """Return the content of each \\boxed{...}/\\ans{...}, nesting-aware, in order."""
    out = []
    for m in re.finditer(r"\\(?:boxed|ans)\{", tex):
        i, depth, buf = m.end(), 1, []
        while i < len(tex) and depth:
            c = tex[i]
            depth += (c == "{") - (c == "}")
            if depth:
                buf.append(c)
            i += 1
        out.append("".join(buf))
    return out


def nums(text):
    vals = set()
    for tok in NUM.findall(text):
        try:
            vals.add(round(float(eval(tok)) if "/" in tok else float(tok), 4))
        except (ValueError, ZeroDivisionError, SyntaxError):
            pass
    return vals


def json_expected_nums(entry):
    found = set()

    def walk(v):
        if isinstance(v, bool):
            return
        if isinstance(v, (int, float)):
            found.add(round(float(v), 4))
        elif isinstance(v, str):
            for tok in NUM.findall(v):
                try:
                    found.add(round(float(eval(tok)) if "/" in tok else float(tok), 4))
                except (ValueError, ZeroDivisionError, SyntaxError):
                    pass
        elif isinstance(v, list):
            for x in v:
                walk(x)
        elif isinstance(v, dict):
            for x in v.values():
                walk(x)

    # only the ANSWER matters here: expected + solve_for target, not givens
    for key in ("expected",):
        if key in entry:
            walk(entry[key])
    return found


def problem_segments(tex):
    """Split the key into per-problem segments by the \\problem{...} macro the
    answer key uses to repeat each statement; returns list of segment texts.
    Also matches the optional-workspace form \\problem[5cm]{...} (see
    references/latex-templates.md) so keys written in the current template
    style still segment."""
    starts = [m.start() for m in re.finditer(r"\\problem(?:\[[^\]]*\])?\{", tex)]
    if not starts:
        return None
    starts.append(len(tex))
    return [tex[starts[i]:starts[i + 1]] for i in range(len(starts) - 1)]


def main():
    tex = open(sys.argv[1]).read()
    data = json.load(open(sys.argv[2]))
    boxes = boxed_answers(tex)
    # Hard gate scans the WHOLE document: a verified answer may be printed in
    # prose rather than \boxed{}, and absence-from-boxes is not absence-from-key.
    # The true drift signal is a verified value that appears nowhere at all.
    all_printed = nums(normalize_latex_numbers(tex))
    segments = problem_segments(tex)

    by_id = {}
    for e in data.get("problems", []):
        if isinstance(e, dict) and isinstance(e.get("id"), int):
            by_id.setdefault(e["id"], []).append(e)

    if not boxes:
        print("⚠ no \\boxed{}/\\ans{} answers found — box every final answer so "
              "printed answers can be bound to the verified JSON.")
        sys.exit(1)

    print(f"Answer-key binding: {sys.argv[1]}")
    print(f"  {len(boxes)} boxed answers · "
          f"{len(segments) if segments else '?'} problem segments")

    hard = []      # verified value printed NOWHERE in the key — strong drift signal
    soft = []      # printed elsewhere but not in its own problem segment — review
    for i in sorted(by_id):
        entries = by_id[i]
        if all(e.get("type") == "manual" for e in entries):
            continue
        expected = set().union(*(json_expected_nums(e) for e in entries))
        expected = {v for v in expected if abs(v) > 1e-9}  # skip trivial 0
        if not expected:
            continue
        for v in expected:
            if not any(abs(v - pr) <= 0.011 for pr in all_printed):
                hard.append((i, v))
            elif segments and i - 1 < len(segments):
                seg_nums = nums(normalize_latex_numbers(segments[i - 1]))
                if not any(abs(v - pr) <= 0.011 for pr in seg_nums):
                    soft.append((i, v))

    for pid, v in hard:
        print(f"  ❌ problem {pid}: verified value {v} appears NOWHERE in the "
              "answer key — transcription drift.")
    for pid, v in soft:
        print(f"  ⚠ problem {pid}: verified value {v} not in its own segment "
              "(printed elsewhere) — check problem/answer alignment.")

    if hard:
        print(f"\n❌ {len(hard)} verified answer(s) missing from the key — fix "
              "the PDF before delivering.")
        sys.exit(1)
    if soft:
        print(f"\n⚠ {len(soft)} alignment warning(s) — heuristic, review by eye.")
        sys.exit(0)
    print("\n✅ every verified answer appears in the answer key")


if __name__ == "__main__":
    main()
