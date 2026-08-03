#!/usr/bin/env python3
r"""test_render_quick_answers.py — property tests for
scripts/render_quick_answers.py.

Construction is the guarantee for the quick-answer bank, so the CONSTRUCTOR
is what gets tested: every rendering rule (numeric-verbatim via Decimal,
sympify->latex with the "---" no-injection fallback, lists, dicts,
manual-only, multi-entry ids), the adaptive column thresholds, byte-for-byte
determinism, the two preflight teaching failures, and the curriculum block —
the level and standards codes that appear on the ANSWER KEY only, derived from
the verify JSON and the key's own title block rather than typed. The strict-binding
invariant (an \input'd bank never degrades check_answer_key.py) is locked by
the ak_qa_good.tex fixture in run_tests.sh.
"""
import json
import os
import sys
import tempfile
from decimal import Decimal

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import render_quick_answers as rqa  # noqa: E402

FAILS = []


def check(name, cond):
    print(f"  {'✅' if cond else '❌'} {name}")
    if not cond:
        FAILS.append(name)


print("rendering rules:")
check("Decimal keeps the JSON's written precision (6.30, not 6.3)",
      rqa._fmt(Decimal("6.30")) == "6.30")
check("int verbatim", rqa._fmt(5) == "5")
check("string via sympify->latex",
      rqa._fmt("(x-3)*(x-4)") == r"$\left(x - 4\right) \left(x - 3\right)$")
check("probability fraction typesets",
      rqa._fmt("3/8") == r"$\frac{3}{8}$")
check("sympify failure falls back to --- (never raw injection)",
      rqa._fmt("x = 2 or x = 3") == "---")
check("injection-shaped string falls back to ---",
      rqa._fmt(r"\input{/etc/passwd}") == "---")
check("list comma-joined", rqa._fmt([2, 3]) == "2, 3")
check("dict as var = value pairs",
      rqa._fmt({"x": 3, "y": 2}) == "$x = $ 3, $y = $ 2")
check("bool is not a bankable value", rqa._fmt(True) == "---")

print("per-problem entries:")
check("manual-only id prints ---",
      rqa.render_entry([{"type": "manual", "desc": "proof"}]) == "---")
check("multi-entry id joins all expected values",
      rqa.render_entry([{"expected": 5}, {"expected": [Decimal("2.5"), 4]}])
      == "5, 2.5, 4")

print("adaptive columns (thresholds 12 / 20):")
check("4 columns for short entries", rqa.column_count(["1234567890ab"]) == 4)
check("3 columns at 13..20 chars", rqa.column_count(["1234567890abc"]) == 3)
check("2 columns past 20 chars", rqa.column_count(["x" * 21]) == 2)

print("render():")
data = {"problem_count": 3, "problems": [
    {"id": 1, "type": "approx", "expr": "1", "expected": Decimal("6.30")},
    {"id": 2, "type": "solve", "expr": "x-2", "expected": [2]},
    {"id": 3, "type": "manual", "desc": "sketch"},
]}
text = rqa.render(data)
check("one numbered entry per problem id 1..problem_count",
      "1.~6.30" in text and "2.~2" in text and "3.~---" in text)
body = "\n".join(l for l in text.split("\n") if not l.startswith("%"))
check("entries are plain text — no \\ans/\\boxed in the bank",
      "\\ans" not in body and "\\boxed" not in body)
check("multicols wrapper with the computed column count",
      "\\begin{multicols}{4}" in text)
check("deterministic: identical input, identical bytes",
      text == rqa.render(data))
try:
    rqa.render({"problems": []})
    check("empty JSON is a ValueError", False)
except ValueError:
    check("empty JSON is a ValueError", True)

print("preflight (the two silent-failure classes):")
good = "\\input{worksheet-preamble}\n\\input{qa_demo}\n"
check("both \\inputs present -> clean", rqa.preflight(good, "qa_demo.tex") == [])
faults = rqa.preflight("\\input{worksheet-preamble}\n", "qa_demo.tex")
check("missing bank \\input names the exact line to add",
      len(faults) == 1 and "\\input{qa_demo}" in faults[0])
faults = rqa.preflight("\\input{qa_demo}\n", "qa_demo.tex")
check("hand-rolled preamble names the template",
      len(faults) == 1 and "worksheet-preamble" in faults[0])
check("path-qualified \\input{/tmp/qa_demo.tex} also satisfies preflight",
      rqa.preflight("\\input{worksheet-preamble}\n"
                    "\\input{/tmp/qa_demo.tex}\n", "qa_demo.tex") == [])

print("main() CLI:")
tmp = tempfile.mkdtemp()
jp = os.path.join(tmp, "verify_demo.json")
with open(jp, "w") as f:
    # written by hand, not json.dump: the trailing zero in 6.30 is the point
    f.write('{"problem_count": 1, "problems": ['
            '{"id": 1, "type": "approx", "expr": "1", "expected": 6.30}]}')
akp = os.path.join(tmp, "ak_demo.tex")
with open(akp, "w") as f:
    f.write("\\input{worksheet-preamble}\n\\input{qa_demo}\n")
rc = rqa.main(["rqa", jp, akp])
out = os.path.join(tmp, "qa_demo.tex")
check("exit 0 and default qa_<stem>.tex beside the JSON",
      rc == 0 and os.path.exists(out))
check("bank prints the float at its JSON-written precision",
      "1.~6.30" in open(out).read())
check("usage error is exit 1", rqa.main(["rqa"]) == 1)
check("unreadable input is exit 1",
      rqa.main(["rqa", os.path.join(tmp, "nope.json"), akp]) == 1)
with open(akp, "w") as f:
    f.write("\\input{worksheet-preamble}\n")
check("preflight failure is exit 1 via the CLI", rqa.main(["rqa", jp, akp]) == 1)

print()

# ── degenerate bank (eval run) ───────────────────────────────────────────────
# Verifying "find the inverse" by equiv on the composition passes every gate and
# makes every expected value literally "x", so the grader's quick-reference
# reads "x, x, x, x". The JSON is correct, the binding is correct, and the
# printed artifact is useless — no gate saw it. Found by an eval agent.
import contextlib as _ctx, io as _io   # noqa: E402
print("degenerate answer bank")


def _stderr_of(data):
    err = _io.StringIO()
    with _ctx.redirect_stderr(err):
        rqa.render(data)
    return err.getvalue()


_deg = {"problem_count": 4, "problems": [
    {"id": i, "type": "equiv", "expr": "f", "expected": "x"} for i in range(1, 5)]}
_var = {"problem_count": 4, "problems": [
    {"id": i, "type": "equiv", "expr": "f", "expected": f"{i}*x+1"} for i in range(1, 5)]}
check("an all-identical bank warns", "WARNING" in _stderr_of(_deg))
check("a varied bank stays silent", "WARNING" not in _stderr_of(_var))

print()
print("curriculum block (answer key only)")

# The level and the standards codes are the ADULT's information: what does this
# sheet cover, and where does it sit? They are built from the verify JSON and
# the key's own \aktitleblock rather than typed, so the section cannot disagree
# with the tags the verifier actually checked.
_curr = {"problem_count": 3, "problems": [
    {"id": 1, "type": "equiv", "expr": "x", "expected": "x",
     "standard": "5.NF.B.4", "difficulty": 2},
    {"id": 2, "type": "equiv", "expr": "x", "expected": "2*x",
     "standard": "5.NF.B.4", "difficulty": 3},
    {"id": 3, "type": "equiv", "expr": "x", "expected": "3*x",
     "standard": "4.MD.A.3", "difficulty": 5}]}
_out = rqa.render(_curr, "Grade 4--5")
check("the level prints on the key", r"\textbf{Level:}~Grade 4--5" in _out)
check("a code lists every problem carrying it",
      r"5.NF.B.4 \textit{-- problems 1, 2}" in _out)
check("a single-problem code says 'problem', not 'problems'",
      r"4.MD.A.3 \textit{-- problem 3}" in _out)
check("the difficulty range spans the tagged checks",
      "Difficulty 2--5 of 5 across 3 tagged checks" in _out)
check("the section is headed Curriculum", r"\textbf{Curriculum}" in _out)

# Nothing to say and nothing printed: an untagged bank must not emit a bare
# heading with two rules and no content between them.
_bare = {"problem_count": 2, "problems": [
    {"id": i, "type": "equiv", "expr": "x", "expected": f"{i}*x"} for i in (1, 2)]}
check("an untagged, unlevelled key prints no empty section",
      r"\textbf{Curriculum}" not in rqa.render(_bare, ""))
check("codes alone still print without a level",
      r"\textbf{Curriculum}" in rqa.render(_curr, "")
      and "Level:" not in rqa.render(_curr, ""))

# The level is read out of the key's own title block, so the two can never
# disagree — there is no second place to type it.
check("the level is parsed from \\aktitleblock's second argument",
      rqa.AKTITLE_RE.search(r"\aktitleblock{Volume}{Grade 4--5}{}").group(1)
      == "Grade 4--5")
check("a level-less key parses to no level",
      rqa.AKTITLE_RE.search(r"\aktitleblock{Volume}{}{}").group(1) == "")
# The level is reprinted verbatim because it is the SAME string \aktitleblock
# already expands on the same page — escaping it turned a live \quad into four
# literal characters in the middle of a course name.
check("markup in a level survives as markup",
      r"Geometry \quad Proof" in rqa.render(_curr, r"Geometry \quad Proof"))
# A standards code is data from the verify JSON, not markup from the document,
# so that one stays escaped.
check("a standards code is still escaped",
      r"\&" in rqa.render({"problem_count": 1, "problems": [
          {"id": 1, "type": "equiv", "expr": "x", "expected": "x",
           "standard": "4.MD & 5.MD"}]}, ""))

if FAILS:
    print(f"❌ {len(FAILS)} quick-answer test(s) failed")
    sys.exit(1)
print("✅ All quick-answer tests passed")
