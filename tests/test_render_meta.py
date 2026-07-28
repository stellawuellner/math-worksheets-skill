#!/usr/bin/env python3
r"""test_render_meta.py — property tests for scripts/render_meta.py.

Construction is the guarantee for effort markers, so what needs proving is
the CONSTRUCTOR: the validation gate (render_meta.py is the ONE place the
difficulty tag becomes gating — verify.py never range-checks it, so a
difficulty of 7 would otherwise render seven stars), the emitted bodies
(star count == difficulty, "(D pts)" text, computed \totalpoints), the
marker lines _probmeta.py parses, and byte-for-byte determinism.
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_meta  # noqa: E402
from _probmeta import probmeta_ids, META_CALL_RE, PTS_CALL_RE  # noqa: E402

FAILS = []


def check(name, cond):
    print(f"  {'✅' if cond else '❌'} {name}")
    if not cond:
        FAILS.append(name)


def data(problems, count=None):
    d = {"problems": problems}
    if count is not None:
        d["problem_count"] = count
    return d


def rejects(name, d, want_ids):
    try:
        render_meta.collect_difficulties(d)
        check(name, False)
    except ValueError as e:
        # the teaching message must NAME the offending ids
        check(name, all(str(i) in str(e) for i in want_ids))


print("validation gate (exit-1 paths, offending ids named):")
rejects("difficulty 7 (out of range)",
        data([{"id": 1, "difficulty": 7}], 1), [1])
rejects('difficulty "hard" (non-integer)',
        data([{"id": 1, "difficulty": "hard"}], 1), [1])
rejects("missing difficulty tag",
        data([{"id": 1, "difficulty": 2}, {"id": 2}], 2), [2])
rejects("boolean difficulty",
        data([{"id": 1, "difficulty": True}], 1), [1])
rejects("conflicting multi-entry tags",
        data([{"id": 1, "difficulty": 3}, {"id": 1, "difficulty": 4}], 1), [1])
rejects("problem_count beyond tagged ids",
        data([{"id": 1, "difficulty": 2}], 3), [2, 3])

print("emission:")
ok = data([{"id": 1, "difficulty": 1}, {"id": 2, "difficulty": 3},
           {"id": 3, "difficulty": 5}], 3)
text = render_meta.render(ok, "verify_demo.json", "meta_demo.tex")
check("marker lines parse back to the full id set",
      probmeta_ids(text) == {1, 2, 3})
check("star count equals difficulty (3 stars for difficulty 3)",
      "\\csname probmeta2\\endcsname{\\;{\\footnotesize\\ensuremath"
      "{\\bigstar\\bigstar\\bigstar}}}" in text)
check("point body prints the difficulty",
      "\\csname probpts3\\endcsname{\\;{\\footnotesize(5 pts)}}" in text)
check("\\totalpoints is the computed sum (1+3+5=9), never hand-typed",
      "\\newcommand{\\totalpoints}{9}" in text)
check("both dispatchers are emitted (self-contained file)",
      "\\newcommand{\\probmeta}[1]{\\csname probmeta#1\\endcsname}" in text
      and "\\newcommand{\\probpts}[1]{\\csname probpts#1\\endcsname}" in text)
check("ASCII-only emission (pdflatex fallback)",
      all(ord(c) < 128 for c in text))
check("deterministic: identical input, identical bytes",
      text == render_meta.render(ok, "verify_demo.json", "meta_demo.tex"))
check("call regexes match the documented call form",
      META_CALL_RE.search("x \\probmeta{3} y").group(1) == "3"
      and PTS_CALL_RE.search("x \\probpts{12} y").group(1) == "12")

print("main() CLI:")
tmp = tempfile.mkdtemp()
good_json = os.path.join(tmp, "verify_demo.json")
with open(good_json, "w") as f:
    import json
    json.dump(ok, f)
rc = render_meta.main(["render_meta.py", good_json])
default_out = os.path.join(tmp, "meta_demo.tex")
check("exit 0 and default meta_<stem>.tex beside the JSON",
      rc == 0 and os.path.exists(default_out))
bad_json = os.path.join(tmp, "verify_bad.json")
with open(bad_json, "w") as f:
    json.dump(data([{"id": 1, "difficulty": 9}], 1), f)
rc = render_meta.main(["render_meta.py", bad_json])
check("exit 1 on a garbage tag, no file written",
      rc == 1 and not os.path.exists(os.path.join(tmp, "meta_bad.tex")))
check("usage error is exit 1", render_meta.main(["render_meta.py"]) == 1)
check("unreadable input is exit 1",
      render_meta.main(["render_meta.py", os.path.join(tmp, "nope.json")]) == 1)

print()
if FAILS:
    print(f"❌ {len(FAILS)} render_meta test(s) failed")
    sys.exit(1)
print("✅ All render_meta tests passed")
