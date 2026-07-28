#!/usr/bin/env python3
r"""test_render_quick_answers.py — property tests for
scripts/render_quick_answers.py.

Construction is the guarantee for the quick-answer bank, so the CONSTRUCTOR
is what gets tested: every rendering rule (numeric-verbatim via Decimal,
sympify->latex with the "---" no-injection fallback, lists, dicts,
manual-only, multi-entry ids), the adaptive column thresholds, byte-for-byte
determinism, and the two preflight teaching failures. The strict-binding
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
if FAILS:
    print(f"❌ {len(FAILS)} quick-answer test(s) failed")
    sys.exit(1)
print("✅ All quick-answer tests passed")
