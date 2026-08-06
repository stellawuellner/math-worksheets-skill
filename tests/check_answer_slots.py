#!/usr/bin/env python3
r"""check_answer_slots.py — every printed response slot needs its own check.

Usage: python3 tests/check_answer_slots.py <ws_*.tex> <verify.json>

WHAT WENT WRONG. SKILL.md promised that "a partially-verified answer key can
never slip through", and verify.py enforced the rule it actually stated: every
problem id 1..N has at least one check. Those are not the same promise. The gate
counts PROBLEMS; the promise is about ANSWERS. A problem printing three blanks
satisfies a per-id gate with one entry, and the other two responses ship
unchecked with nothing anywhere reporting it.

A 300-case review found this in 172 cases — the largest single defect in the
system. Representative: a problem prints "write the number word AND the ones
digit" and verify.json covers only the digit; another prints (a)/(b)/(c) and
verifies (a). In several the unverified part IS the tagged skill, so the sheet's
declared purpose is the thing nobody checked.

WHAT THIS CHECKS. Per problem, the number of printed response slots against the
number of verify entries for that id. Slots are counted from the shipped
preamble's own macro semantics (templates/worksheet-preamble.tex):

  * \ansline, \ansblank and \answerline{...} each print one slot and each
    clears the auto-line flag;
  * \problem[<ws>]{...} with a POSITIVE workspace emits one \ansline itself,
    but only if nothing above cleared the flag — so it adds a slot exactly when
    the segment contains no explicit slot macro and no \noansline;
  * \scratchblank prints the same rule as \ansblank but is NOT an answer slot.
    It exists so a working-space blank (a scaling multiplier, a partial product
    a student carries) can stay on the page without claiming to be an answer.
    Using it is a claim: this blank holds no answer worth checking.

Counting entries, not slots, is deliberate on the JSON side: a `manual` entry is
a check. Declaring the diagnosis half of a find-and-fix item as `manual` is the
correct fix, not a workaround.

Exit 0 clean · 1 on any uncovered slot · 2 when zero problems parse (nothing was
checked — NOT a pass, mirroring the sibling checkers).
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _tex_segments import segment_spans, blank_comments  # noqa: E402
from check_prose_consistency import prose_numbers  # noqa: E402

# \ansline and \ansblank are whole macro names: \noansline does NOT match
# \\ansline, because there the substring is preceded by "no", not a backslash.
SLOT_RE = re.compile(r"\\(?:ansline|ansblank|answerline)(?![A-Za-z])")
NOANS_RE = re.compile(r"\\noansline(?![A-Za-z])")
SCRATCH_RE = re.compile(r"\\scratchblank(?![A-Za-z])")
PROBLEM_WS_RE = re.compile(r"\\problem(?:\[([^\]]*)\])?\{")
SUBPART_RE = re.compile(r"(?:^|[\s~{])\((a|b|c|d|e|f|g|h)\)", re.M)

# Types whose expected list lands in SEPARATE printed blanks. Measured against
# the corpus: crediting any list-valued expected also credits solve/zeros, whose
# root list is one answer on one line, and that silences real gaps.
_MULTI_SLOT_TYPES = frozenset({"compare", "midpoint", "intersection", "system"})
LEN_RE = re.compile(r"^\s*([-+]?[0-9]*\.?[0-9]+)\s*[a-z]*\s*$")


def positive_workspace(arg):
    """True when a \problem optional argument is a positive length."""
    if arg is None:
        return False
    m = LEN_RE.match(arg)
    if not m:  # a macro or expression we cannot read — assume no auto line
        return False
    try:
        return float(m.group(1)) > 0
    except ValueError:
        return False


def slots_in(segment):
    """Printed response slots in one problem segment."""
    explicit = len(SLOT_RE.findall(segment))
    if explicit or NOANS_RE.search(segment):
        return explicit
    m = PROBLEM_WS_RE.search(segment)
    return 1 if m and positive_workspace(m.group(1)) else 0


def values_pinned(entry):
    r"""How many printed BLANKS one entry can legitimately account for.

    A `compare` ordering three numbers pins three positions; a `system` pins the
    pair; `solve`/`zeros` pin every root. Counting entries alone flagged those
    as under-covered when they are exactly right — "write the three numbers in
    order: __ __ __" against one compare entry is a complete verification.

    Deliberately applied ONLY to printed slots, never to lettered sub-parts. A
    two-root `solve` covers two blanks, but it says nothing about a "(b) explain
    why" beside it, and letting arity satisfy sub-parts would turn this gate's
    biggest true-positive class into silence.

    RESTRICTED BY TYPE, and the restriction is the load-bearing part. Crediting
    every list-valued `expected` looks equivalent and is not: a `solve` returning
    [9, 21] is ONE answer written on ONE line, so crediting it with two blanks
    silenced curr-295 problem 12, where "(a) Solve … \ansline" is verified and
    "(b) … say whether she is right … \ansline" is not. The types below are the
    ones whose list elements really do land in separate printed blanks —
    an ordering fills its blanks one number each, a point fills (x, y).
    """
    if entry.get("type") not in _MULTI_SLOT_TYPES:
        return 1
    v = entry.get("expected")
    n = len(v) if isinstance(v, list) and v else 1
    # A relation compare prints the two operands AND the symbol between them.
    if entry.get("type") == "compare" and entry.get("order") == "relation":
        n = len(entry.get("values") or []) + 1
    return n


def subparts_in(segment):
    r"""How many lettered sub-parts the stem asks for.

    A problem written as "(a) … (b) … (c) …" asks for three responses whether
    or not it prints three blanks. This is the other half of the same defect:
    the printed-slot count catches "three blanks, one check", and this catches
    "three questions, one blank, one check" — which the review found more often.
    Counted only from a run starting at (a) with (b) present, so a stray "(a)"
    in prose or a figure label cannot manufacture a requirement.
    """
    letters = {m.group(1) for m in SUBPART_RE.finditer(segment)}
    if not {"a", "b"} <= letters:
        return 0
    n = 0
    for ch in "abcdefgh":
        if ch not in letters:
            break
        n += 1
    return n


# Types whose inputs are the problem's givens, so "answer smuggled in as an
# input" is expressible. eval/at is excluded deliberately: substitution problems
# have small integer answers that coincide with a stem number constantly, and
# including them took this from 14 notes to 82, almost all noise.
_INVERSE_TYPES = frozenset({"midpoint", "distance", "slope", "polygon_area",
                            "triangle"})
_INPUT_KEYS = ("points", "given")


def _numbers(x, out=None):
    out = [] if out is None else out
    if isinstance(x, bool):
        return out
    if isinstance(x, (int, float)):
        out.append(float(x))
    elif isinstance(x, str):
        try:
            out.append(float(x))
        except ValueError:
            pass
    elif isinstance(x, list):
        for y in x:
            _numbers(y, out)
    elif isinstance(x, dict):
        for y in x.values():
            _numbers(y, out)
    return out


def shortfall(segment, entries):
    r"""Responses this problem prints that its entries do not account for.

    THE single definition of "under-covered". It was briefly two — this gate
    decided one way and the answer key's \unchecked marking decided another, so
    a rule change moved the gate to 66 cases while the key still marked 86. They
    share the primitives; sharing those is not enough, because the DECISION is
    where the rules live. Both callers use this now.

    Returns (missing_count, description) with missing_count 0 when covered.
    """
    slots, parts = slots_in(segment), subparts_in(segment)
    have = len(entries)
    pinned = sum(values_pinned(e) for e in entries)
    open_graded = any(e.get("type") == "manual" for e in entries)
    short_slots = slots - pinned
    short_parts = 0 if open_graded else parts - have
    if short_slots <= 0 and short_parts <= 0:
        return 0, ""
    if short_parts >= short_slots:
        return short_parts, (f"asks {parts} lettered sub-part(s) but has {have} "
                             f"entr{'y' if have == 1 else 'ies'}")
    return short_slots, (f"prints {slots} response slot(s) but its entries pin "
                         f"{pinned} value(s)")


def given_as_answer_notes(segments, data):
    r"""ADVISORY ONLY — never fails the build. Read the note, don't obey it.

    The worst defect the 300-case review found was curr-326 problem 6: the stem
    gives midpoint M(3,5) and endpoint A(-1,2) and asks for B, and the check is
    midpoint([[-1,2],[7,8]]) == [3,5]. It feeds the ANSWER in as an input and
    verifies a GIVEN, so it cannot fail for any wrong answer — and because the
    Quick Answers bank is built from `expected`, the delivered key printed
    "6. 3, 5". A student with the correct (7,8) marks themselves wrong.

    The signature is mechanical: every expected value appears in the printed
    stem while some input coordinate does not. The PRECISION IS NOT. Measured
    over all 300 gated cases it fires on 14 entries of which one — curr-326 —
    is the real thing; curr-347 problem 10 legitimately checks that a rotation
    centre equals the printed intersection (2,3), which is the same shape and
    entirely correct. So this prints and moves on. A hard gate at 7% precision
    would train authors to ignore it, which is worse than not having it.
    """
    notes = []
    by_id = {}
    for e in data.get("problems", []):
        if isinstance(e, dict) and isinstance(e.get("id"), int):
            by_id.setdefault(e["id"], []).append(e)
    for i, seg in enumerate(segments, 1):
        stem = set(prose_numbers(seg))
        if not stem:
            continue

        def printed(v):
            return any(abs(v - s) < 1e-9 for s in stem)

        for e in by_id.get(i, []):
            if e.get("type") not in _INVERSE_TYPES:
                continue
            exp = _numbers(e.get("expected"))
            ins = []
            for k in _INPUT_KEYS:
                if k in e:
                    _numbers(e[k], ins)
            if not exp or not ins:
                continue
            if all(printed(v) for v in exp) and any(not printed(v) for v in ins):
                notes.append(
                    f"problem {i}: the {e['type']} check expects "
                    f"{e.get('expected')!r}, and every one of those numbers is "
                    f"already printed in the stem, while one of its inputs is "
                    f"not. If this is an inverse item (\"M is the midpoint, "
                    f"find B\"), the check is verifying a given and cannot "
                    f"fail — and the answer bank will print the given as the "
                    f"answer. If the answer genuinely equals a printed value, "
                    f"ignore this")
    return notes


def main():
    if len(sys.argv) != 3:
        print("Usage: check_answer_slots.py <ws.tex> <verify.json>",
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

    by_id = {}
    for e in data.get("problems", []):
        if isinstance(e, dict) and isinstance(e.get("id"), int):
            by_id.setdefault(e["id"], []).append(e)

    total_slots = sum(slots_in(s) for s in segments)
    print(f"Answer-slot coverage: {sys.argv[1]} "
          f"({len(segments)} problem segments, {total_slots} printed slot(s), "
          f"{sum(len(v) for v in by_id.values())} verify entr(y/ies))")

    faults = []
    for i, seg in enumerate(segments, 1):
        missing, asked = shortfall(seg, by_id.get(i, []))
        if not missing:
            continue
        faults.append(
            f"problem {i} {asked} — {missing} response(s) would ship "
            f"unchecked. Add one entry per response the problem asks for (use "
            f"\"manual\" for a written explanation, a sketch or a named "
            f"error), or, if a blank is working space rather than an answer, "
            f"print it with \\scratchblank")

    for note in given_as_answer_notes(segments, data):
        print(f"  ⚠ {note}.")

    if faults:
        for f in faults:
            print(f"  ❌ {f}.")
        print(f"\n❌ {len(faults)} problem(s) print more answers than the "
              "verification covers.")
        return 1
    print("✅ every printed response slot has a verify entry")
    return 0


if __name__ == "__main__":
    sys.exit(main())
