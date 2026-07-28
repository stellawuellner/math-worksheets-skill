#!/usr/bin/env python3
"""
check_answer_key.py — bind the printed answer key to the verified JSON,
problem by problem.

verify.py proves the JSON's `expected` values are correct, but the student
reads the PDF. Nothing otherwise guarantees the answer key's printed answers
match the verified values (audit A1/3a). This checker splits the key into
per-problem segments and requires each problem's verified values to appear in
THAT problem's \\boxed{}/\\ans{} answer.

Usage: python3 tests/check_answer_key.py <ak_*.tex or ss_*.tex> <verify.json>

Why per problem, per box (audit B1/B2/B3): a whole-document number match let
a key with shuffled answers pass, let a wrong \\boxed value pass whenever the
correct number survived in the worked steps beside it, and a flat 0.011
tolerance let \\boxed{4.52} satisfy a verified 4.51. The box is what the
student trusts, so the hard gate reads only the boxes, problem by problem,
at the precision each answer is printed with.

Exit 0 = every verified value is boxed in its own problem (soft alignment
notes may still print when binding is degraded). Exit 1 = drift: a wrong or
missing boxed value, a swapped key, a segment/problem count mismatch, or a
key with no recognizable problem structure.
"""
import json
import re
import sys
import os
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _tex_segments import segment_spans, blank_comments  # noqa: E402

NUM = re.compile(r"-?\d+(?:\.\d+)?(?:/\d+)?")
_FRAC = re.compile(r"\\[dt]?frac\s*\{?(-?\d+(?:\.\d+)?)\}?\s*\{?(-?\d+(?:\.\d+)?)\}?")


def normalize_latex_numbers(text):
    """Rewrite text so the number regex sees actual values.

    - \\frac{a}{b} becomes a/b (stays contiguous for the fraction branch)
    - thousands separators drop, both plain 1,234 and LaTeX 1{,}234
    - a '-' after a letter, digit, ')' or '}' is binary subtraction, not a
      sign: '(x-3)' must yield 3, not -3, or a correct factored key
      false-fails against expected '(x - 3)*(x - 4)' (audit ak_factor).
      A leading sign ('= -4', '{-4}') is preserved.
    """
    text = _FRAC.sub(r"\1/\2", text)
    text = re.sub(r"(?<=\d),(?=\d{3})", "", text)
    text = re.sub(r"(?<=\d)\{,\}(?=\d{3})", "", text)
    text = re.sub(r"(?<=[A-Za-z0-9)\}])-", " ", text)
    return text


def boxed_answers(tex):
    """Each \\boxed{...}/\\ans{...}: (start offset, content), nesting-aware,
    in order. Offsets let the caller test whether a box lies inside a
    problem segment — the per-problem gate only applies when they all do."""
    out = []
    for m in re.finditer(r"\\(?:boxed|ans)\{", tex):
        i, depth, buf = m.end(), 1, []
        while i < len(tex) and depth:
            c = tex[i]
            depth += (c == "{") - (c == "}")
            if depth:
                buf.append(c)
            i += 1
        out.append((m.start(), "".join(buf)))
    return out


def num_tokens(text):
    """(value, raw_token) pairs for every number printed in `text`.

    The raw token is kept because matching is precision-aware: the written
    form decides how close a verified value must be (audit B3). The old
    set-of-round(x, 4) discarded exactly that information.
    """
    out = []
    for tok in NUM.findall(normalize_latex_numbers(text)):
        try:
            if "/" in tok:
                a, b = tok.split("/")
                out.append((float(a) / float(b), tok))
            else:
                out.append((float(tok), tok))
        except (ValueError, ZeroDivisionError):
            pass
    return out


def value_matches(v, val, tok):
    """Does verified value v match printed token tok (parsed value val)?

    Mirrors verify.py's rounds_to semantics without importing it (this
    checker stays dependency-free): a printed decimal matches only if v
    rounds half-up (the school convention) to it at its own written
    precision — so \\boxed{4.52} can never satisfy a verified 4.51, while
    5, 5.0 and 5.00 all mean the same answer. Integer tokens accept
    anything that rounds to them (within 0.5). Fraction tokens are exact
    up to half an ulp at 4 decimals, so a key printing 2/3 for a JSON
    value stored as 0.6667 still binds; anything coarser is drift.
    """
    if "/" in tok:
        return abs(v - val) <= 5.1e-5
    if "." in tok:
        decimals = len(tok.split(".")[-1])
        try:
            q = Decimal(1).scaleb(-decimals)
            return Decimal(repr(float(v))).quantize(q, rounding=ROUND_HALF_UP) \
                == Decimal(tok)
        except InvalidOperation:
            return abs(v - val) <= 0.5 * 10 ** (-decimals)
    return abs(v - val) <= 0.5


def any_match(v, tokens):
    return any(value_matches(v, val, tok) for val, tok in tokens)


def json_expected_nums(entry):
    found = set()

    def walk(v):
        if isinstance(v, bool):
            return
        if isinstance(v, (int, float)):
            found.add(float(v))
        elif isinstance(v, str):
            # same normalization as the printed side, so '(x - 3)*(x - 4)'
            # and '(x-3)(x-4)' extract the same values
            found.update(val for val, _ in num_tokens(v))
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


def main():
    # comments are blanked (length-preserving) so a commented-out \boxed or
    # '% \problem{...}' remark can neither count as an answer nor split a
    # segment; spans from segment_spans stay valid against this text
    tex = blank_comments(open(sys.argv[1]).read())
    data = json.load(open(sys.argv[2]))
    boxes = boxed_answers(tex)
    spans = segment_spans(tex)

    by_id = {}
    for e in data.get("problems", []):
        if isinstance(e, dict) and isinstance(e.get("id"), int):
            by_id.setdefault(e["id"], []).append(e)
    pc = data.get("problem_count")
    problem_count = pc if isinstance(pc, int) and pc > 0 else len(by_id)

    if not boxes:
        print("⚠ no \\boxed{}/\\ans{} answers found — box every final answer so "
              "printed answers can be bound to the verified JSON.")
        sys.exit(1)

    print(f"Answer-key binding: {sys.argv[1]}")
    if spans is None:
        # A key that cannot be segmented cannot be bound per problem, and a
        # whole-document fallback is exactly what let shuffled keys pass.
        print("  ❌ no problem structure found: use \\problem{...}, an "
              "enumerate \\item per problem, or one examplebox per worked "
              "example, so each printed answer can be bound to its problem.")
        sys.exit(1)

    segments = [tex[a:b] for a, b in spans]
    print(f"  {len(boxes)} boxed answers · {len(segments)} problem segments")

    if len(segments) != problem_count:
        print(f"  ❌ segment/problem count mismatch: the key splits into "
              f"{len(segments)} problem segment(s) but the verified JSON has "
              f"{problem_count} problems — give every problem its own "
              "segment (and boxed answer) so answers cannot shift.")
        sys.exit(1)

    # The hard per-problem gate assumes every box belongs to a segment. A key
    # that prints answers outside the list (answer-bank style) degrades to
    # the whole-document presence check — loudly, never silently.
    outside = [s for s, _ in boxes if not any(a <= s < b for a, b in spans)]
    strict = not outside
    if outside:
        print(f"  ⚠ {len(outside)} boxed answer(s) sit outside every problem "
              "segment — per-problem binding DEGRADED to whole-document "
              "presence. Move final answers into their problem's segment to "
              "restore the hard per-problem gate.")

    seg_boxes = []   # per segment: number tokens of its concatenated boxes
    for a, b in spans:
        content = " ".join(c for s, c in boxes if a <= s < b)
        seg_boxes.append(num_tokens(content))
    doc_tokens = num_tokens(tex)

    hard = []      # per-problem binding failure — wrong/missing boxed value
    soft = []      # degraded mode only: printed elsewhere, not in own segment
    for i in sorted(by_id):
        entries = by_id[i]
        if all(e.get("type") == "manual" for e in entries):
            continue
        expected = set().union(*(json_expected_nums(e) for e in entries))
        expected = {v for v in expected if abs(v) > 1e-9}  # skip trivial 0
        if not expected:
            continue
        seg = segments[i - 1] if i - 1 < len(segments) else ""
        for v in expected:
            if strict:
                if i - 1 < len(seg_boxes) and any_match(v, seg_boxes[i - 1]):
                    continue
                # diagnose, don't just fail: was the right number nearby?
                if any_match(v, num_tokens(seg)):
                    hard.append((i, v, "is in the worked steps but NOT in the "
                                 "\\boxed{}/\\ans{} answer — the boxed value "
                                 "is wrong; box the verified answer"))
                else:
                    # diagnosis is tighter than the gate: a coarse integer
                    # box within 0.5 must not misattribute a swap
                    others = [k + 1 for k, toks in enumerate(seg_boxes)
                              if k != i - 1
                              and any(abs(v - val) <= 1e-4 for val, _ in toks)]
                    if others:
                        hard.append((i, v, "is boxed under problem "
                                     f"{others[0]} instead — swapped or "
                                     "shifted key"))
                    else:
                        hard.append((i, v, "is not printed in this problem's "
                                     "segment — transcription drift"))
            else:
                if not any_match(v, doc_tokens):
                    hard.append((i, v, "appears NOWHERE in the answer key — "
                                 "transcription drift"))
                elif not any_match(v, num_tokens(seg)):
                    soft.append((i, v))

    for pid, v, why in hard:
        print(f"  ❌ problem {pid}: verified value {v:g} {why}.")
    for pid, v in soft:
        print(f"  ⚠ problem {pid}: verified value {v:g} not in its own segment "
              "(printed elsewhere) — check problem/answer alignment.")

    if hard:
        print(f"\n❌ {len(hard)} binding failure(s) — fix the key before "
              "delivering.")
        sys.exit(1)
    if soft:
        print(f"\n⚠ {len(soft)} alignment warning(s) — heuristic, review by eye.")
        sys.exit(0)
    if strict:
        print("\n✅ every verified answer is boxed in its own problem")
    else:
        print("\n✅ every verified answer appears in the answer key")


if __name__ == "__main__":
    main()
