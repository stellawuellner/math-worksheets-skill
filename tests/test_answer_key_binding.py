#!/usr/bin/env python3
"""
test_answer_key_binding.py — pins the per-problem answer-key gate (audit
B1/B2/B3) and the shared segmenter it relies on.

Each fixture case previously produced a wrong verdict — shuffled keys passed,
a wrong \\boxed value passed whenever the correct number sat in the worked
steps beside it, \\boxed{4.52} satisfied a verified 4.51, and enumerate-style
keys were never segmented at all ('? problem segments'). The messages are
asserted too: error messages teach the fix, so they are contract.

Run: python3 tests/test_answer_key_binding.py
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _tex_segments import segment_spans, blank_comments  # noqa: E402
from check_answer_key import num_tokens, value_matches  # noqa: E402

CHECKER = os.path.join(HERE, "check_answer_key.py")
FIXTURES = os.path.join(HERE, "fixtures")

FAILS = []


def check(name, cond):
    print(f"  {'✅' if cond else '❌'} {name}")
    if not cond:
        FAILS.append(name)


def run(texf, jsonf):
    r = subprocess.run(
        [sys.executable, CHECKER,
         os.path.join(FIXTURES, texf), os.path.join(FIXTURES, jsonf)],
        capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


print("Fixture verdicts and messages:")
code, out = run("ak_bind_good.tex", "ak_bind.json")
check("good enumerate key passes", code == 0)
check("good key reports real segment count", "3 problem segments" in out)
check("'?' segment placeholder is gone", "? problem segments" not in out)

code, out = run("ak_bind_shuffled.tex", "ak_bind.json")
check("shuffled key (right values, wrong problems) fails", code == 1)
check("shuffle is diagnosed as a swap", "swapped or shifted" in out)

code, out = run("ak_bind_masked.tex", "ak_bind.json")
check("wrong box masked by correct worked step fails", code == 1)
check("masked failure names problem 2", "problem 2" in out)
check("masked failure blames the box, not the steps",
      "NOT in the \\boxed{}/\\ans{} answer" in out)

code, out = run("ak_bind_precision.tex", "ak_bind.json")
check("4.52 boxed for verified 4.51 fails", code == 1)
check("precision failure names problem 2", "problem 2" in out)

code, out = run("ak_bind_nested.tex", "ak_bind_nested.json")
check("nested parts-enumerate does not over-split", code == 0)
check("nested key sees 2 segments, not 4", "2 problem segments" in out)

code, out = run("ak_bind_symbolic.tex", "ak_bind_symbolic.json")
check("correct factored key passes (binary minus, audit ak_factor)", code == 0)

code, out = run("ss_bind_good.tex", "ss_bind.json")
check("paired examplebox/tryitbox study guide segments and passes", code == 0)
check("study guide sees one segment per box (example + try-it)",
      "4 problem segments" in out)

code, out = run("ss_bind_notryit.tex", "ss_bind.json")
check("worked examples with zero try-its fail the pairing rule", code == 1)
check("pairing failure teaches the tryitbox fix", "add a tryitbox" in out)

code, out = run("ss_tryit_missing.tex", "ss_tryit.json")
check("a section whose tryitbox is absent fails", code == 1)
check("missing try-it is blamed on its examplebox", "has no try-it" in out)

code, out = run("ss_tryit_wrongans.tex", "ss_tryit.json")
check("a try-it printing 16 for verified 15 fails value binding", code == 1)
check("wrong try-it answer names its problem", "problem 4" in out)

code, out = run("ss_tryit_good.tex", "ss_tryit_roleswap.json")
check("role tags on the wrong positions fail", code == 1)
check("role mismatch names the entry and box", "role" in out and "tryit" in out)

code, out = run("ak_bind_unstructured.tex", "ak_bind.json")
check("unsegmentable key fails", code == 1)
check("unstructured message teaches the three shapes", "examplebox" in out)

code, out = run("ak_bind_shortkey.tex", "ak_bind.json")
check("segment/problem count mismatch fails", code == 1)
check("count mismatch names both counts", "2 problem segment" in out and "3 problems" in out)

code, out = run("ak_bind_outside.tex", "ak_bind.json")
check("answer-bank key degrades loudly instead of hard-failing", code == 0)
check("degradation is announced", "DEGRADED" in out)

print("Segmenter edge cases:")
spans = segment_spans(
    r"\begin{enumerate}\item one \begin{itemize}\item bullet\end{itemize}"
    r"\item two\end{enumerate}")
check("itemize bullets inside an item do not split", len(spans) == 2)
spans = segment_spans(r"\problem[8cm]{first} work \problem{second} work")
check("optional-argument \\problem[len]{...} is recognized", len(spans) == 2)
check("commented-out structure is ignored",
      segment_spans("no structure here\n% \\problem{ghost}\n") is None)
check("escaped \\% is not a comment",
      "kept" in blank_comments(r"100\% kept"))

print("Precision-aware value matching:")
check("5 matches printed 5.00", value_matches(5.0, 5.0, "5.00"))
check("5.0 matches printed 5", value_matches(5.0, 5.0, "5"))
check("4.51 rejects printed 4.52", not value_matches(4.51, 4.52, "4.52"))
check("4.515 rounds half-up to printed 4.52", value_matches(4.515, 4.52, "4.52"))
check("2/3 binds a value stored to 4 places",
      value_matches(0.6667, 2 / 3, "2/3"))

print()
print("A mixed number is ONE value, in every notation it is written in:")


def vals(s):
    return sorted(round(v, 6) for v, _ in num_tokens(s))


# The LaTeX form, as a student reads it on the page.
check(r"2\tfrac{3}{4} is 2.75, not 23/4", vals(r"$2\tfrac{3}{4}$") == [2.75])
check("thin space between the parts does not split it",
      vals(r"$\,2\,\tfrac{3}{4}$") == [2.75])
check("the sign belongs to the whole mixed number",
      vals(r"$-2\tfrac{3}{4}$") == [-2.75])
# The JSON form, as sympy has to be told it: there is no mixed-number syntax,
# so a verify file writes 2 3/4 as "2 + 3/4". Reading that as two answers is
# what made a correct key fail once the printed side was fixed.
check('"2 + 3/4" is the same 2.75', vals("2 + 3/4") == [2.75])
check("a sum form is plain addition, so -2 + 3/4 is -1.25",
      vals("-2 + 3/4") == [-1.25])
check("both notations meet in the middle",
      vals(r"$2\,\tfrac{3}{4}$") == vals("2 + 3/4"))
# An ordering of mixed numbers — the shape that actually failed, three of them
# in one box against a JSON list of three sum-form expecteds.
check("an ordering of mixed numbers keeps three values",
      vals(r"\ans{\,2\,\tfrac{1}{2} > 2\,\tfrac{3}{8} > \tfrac{9}{4}}")
      == [2.25, 2.375, 2.5])
# ...and the combination must not eat an exponent or a coefficient.
check("x**2 + 1/2 is still 2 and 0.5, not 2.5",
      vals("x**2 + 1/2") == [0.5, 2.0])
check("a factored form is untouched",
      vals("(x - 3)*(x - 4)") == [3.0, 4.0])

print()
if FAILS:
    print(f"❌ {len(FAILS)} binding test(s) failed")
    sys.exit(1)
print("✅ all answer-key binding tests passed")
