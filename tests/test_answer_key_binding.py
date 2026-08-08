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
import json
import os
import subprocess
import sys
import tempfile

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
print("A negative decimal beside a symbolic answer:")
# A symbolic answer carries its sign in the printed expression, so those match
# on magnitude — that is deliberate and predates this. What was broken is that
# the magnitude mapping moved the VALUE and left the token text signed, and
# value_matches reads the text for a decimal to honour its written precision:
# Decimal('0.33') was compared against Decimal('-0.33'). Only negative decimals
# in symbolic problems were hit, and an eval author's fix was to change the
# problem's initial condition so the answer came out positive. The checker
# rewrote the mathematics.
_HEAD = (r"\documentclass[12pt]{article}" "\n" r"\input{worksheet-preamble}" "\n"
         r"\akheader{P}" "\n" r"\begin{document}" "\n"
         r"\aktitleblock{P}{Test}{}" "\n")
_SYMBOLIC = [{"id": 1, "type": "equiv", "expr": "2*x-1", "expected": "2*x - 1"},
             {"id": 1, "type": "approx", "expr": "-0.33", "expected": -0.33}]
_NUMERIC = [{"id": 1, "type": "approx", "expr": "-0.33", "expected": -0.33}]


def binds(problems, body):
    d = tempfile.mkdtemp()
    json.dump({"topic": "p", "problem_count": 1, "problems": problems},
              open(os.path.join(d, "v.json"), "w"))
    open(os.path.join(d, "ak.tex"), "w").write(
        _HEAD + body + "\n" + r"\end{document}" + "\n")
    return subprocess.run(
        [sys.executable, CHECKER, os.path.join(d, "ak.tex"),
         os.path.join(d, "v.json")], capture_output=True).returncode == 0


check("a correct negative decimal binds beside a symbolic answer",
      binds(_SYMBOLIC, r"\problem{$\ans{2x-1}$, value $\ans{-0.33}$}"))
check("a wrong magnitude still fails there",
      not binds(_SYMBOLIC, r"\problem{$\ans{2x-1}$, value $\ans{-0.91}$}"))
# Strict sign is kept exactly where a sign error IS the wrong answer.
check("a purely numeric problem still rejects a flipped sign",
      not binds(_NUMERIC, r"\problem{value $\ans{0.33}$}"))
check("and still accepts the correct negative",
      binds(_NUMERIC, r"\problem{value $\ans{-0.33}$}"))

print()
print("A detached minus sign:")
# "k = - 2" tokenises as +2, because a minus with a space after it cannot be
# told from the subtraction in "3|x-5| - 2" without parsing the expression.
# Both readings are defensible, so the checker cannot resolve it — but the
# generic message ("the boxed value is wrong") sent an author looking for an
# arithmetic slip that was not there. It now says what is actually different.
_NEG = [{"id": 1, "type": "eval", "expr": "a", "at": {"a": -2}, "expected": -2}]


def bind_msg(problems, body):
    d = tempfile.mkdtemp()
    json.dump({"topic": "p", "problem_count": 1, "problems": problems},
              open(os.path.join(d, "v.json"), "w"))
    open(os.path.join(d, "ak.tex"), "w").write(
        _HEAD + body + "\n" + r"\end{document}" + "\n")
    r = subprocess.run(
        [sys.executable, CHECKER, os.path.join(d, "ak.tex"),
         os.path.join(d, "v.json")], capture_output=True, text=True)
    return r.returncode, r.stdout


code, out = bind_msg(_NEG, r"\problem{$k = \ans{- 2}$}")
check("a detached sign still fails", code == 1)
check("and is diagnosed as a detached sign, not a wrong value",
      "without its sign" in out and "against the digit" in out)
check("an attached sign binds",
      bind_msg(_NEG, r"\problem{$k = \ans{-2}$}")[0] == 0)
# The diagnosis must not swallow a genuinely wrong answer.
code, out = bind_msg(_NEG, r"\problem{$k = \ans{-5}$}")
check("a genuinely wrong value is still transcription drift",
      code == 1 and "without its sign" not in out)

print()
print("A box is math mode, so its spaces vanish:")
# \akheader renews \ans to wrap its argument in \ensuremath, so
# \ans{no solution} reaches the student as "nosolution": clean log, every gate
# green, wrong on the page. Nothing else in the chain reads a box as prose.
# Found by an author who read their own PDF. Zero of the 300 recorded keys and
# 300 study guides trip this, so it is a hard fault rather than a warning.
from check_answer_key import lost_spaces  # noqa: E402

check("two real words are caught", lost_spaces("no solution") == ["no solution"])
check("wrapping them in \\text clears it",
      lost_spaces(r"\text{no solution}") == [])
# Single-letter runs are variable juxtaposition, not prose.
check("an equation is not prose", lost_spaces("x = 2") == [])
check("a function applied to a variable is not prose",
      lost_spaces(r"\sin x + \cos x") == [])
check("a fraction is not prose", lost_spaces(r"\dfrac{3}{8}") == [])
check("a unit macro beside a number is fine",
      lost_spaces(r"40 \text{cm}") == [])
check("a polynomial is not prose", lost_spaces("y = 2x + 3") == [])

print()
print("The JSON's SHAPE must not decide whether an answer is symbolic:")
# `verify.py` accepts "18 - 3*x/2" and ["18 - 3*x/2"] identically, and
# `--schema` prints the LIST form for `solve`. The old test read the top level
# only — isinstance(expected, str) — so the list form was "not symbolic", the
# magnitude branch never ran, and a key boxing y = -3/2 x + 18 tokenised to
# {-1.5, 18} against JSON numbers {18, 3, 2}. Eight binding failures on one
# recorded sheet, every one reading "the boxed value is wrong" at a correct
# answer key; unwrapping the list in the JSON cleared all eight without
# touching the key. That is a gate asking an author to edit verified data.
_LINE_BARE = [{"id": 1, "type": "solve", "equation": "Eq(3*x/2 + y, 18)",
               "var": "y", "expected": "18 - 3*x/2"}]
_LINE_LIST = [{"id": 1, "type": "solve", "equation": "Eq(3*x/2 + y, 18)",
               "var": "y", "expected": ["18 - 3*x/2"]}]
_KEY = r"\problem{$y = \ans{-\tfrac{3}{2}x + 18}$}"

check("the bare-string form binds (it always did)", binds(_LINE_BARE, _KEY))
check("the LIST form binds too — same mathematics, same verdict",
      binds(_LINE_LIST, _KEY))
# The widening must not swallow a real error in either form.
check("a wrong intercept still fails in the list form",
      not binds(_LINE_LIST, r"\problem{$y = \ans{-\tfrac{3}{2}x + 19}$}"))
check("a wrong slope still fails in the list form",
      not binds(_LINE_LIST, r"\problem{$y = \ans{-\tfrac{5}{2}x + 18}$}"))
# The walk goes to any depth, the way json_expected_nums already does.
check("a dict-valued expected is read the same way",
      binds([{"id": 1, "type": "system", "equations": ["Eq(y, 2*t)"],
              "vars": ["y"], "expected": {"y": "2*t"}}],
            r"\problem{$y = \ans{2t}$}"))
# ...and a list of purely NUMERIC strings stays non-symbolic, so strict sign
# still holds where a sign error IS the wrong answer.
_ROOTS = [{"id": 1, "type": "solve", "equation": "Eq(x**2 - 49, 0)",
           "var": "x", "expected": [7, -7]}]
check("a numeric solution set still rejects a key that boxes one sign only",
      not binds(_ROOTS, r"\problem{$x = \ans{7}$}"))

print()
print("\\pm prints BOTH signs, so a box holding it offers both values:")
# ["7*I", "-7*I"] boxed as \ans{x = \pm 7i} failed with "verified value -7 is
# boxed as 7 without its sign" — a sign complaint against the one notation that
# prints both signs. The symbolic fix above covers the complex case by
# magnitude; the REAL case keeps strict sign, so \pm has to be readable or the
# false failure is unavoidable.
_COMPLEX = [{"id": 1, "type": "solve", "equation": "Eq(x**2 + 49, 0)",
             "var": "x", "expected": ["7*I", "-7*I"]}]
check("a complex solution set binds to \\pm", binds(_COMPLEX, r"\problem{$x = \ans{\pm 7i}$}"))
check("the spelled-out form binds too",
      binds(_COMPLEX, r"\problem{$x = \ans{7i \text{ or } -7i}$}"))
check("a real solution set binds to \\pm", binds(_ROOTS, r"\problem{$x = \ans{\pm 7}$}"))
check("a \\pm fraction binds both readings",
      binds([{"id": 1, "type": "solve", "equation": "Eq(4*x**2 - 9, 0)",
              "var": "x", "expected": [1.5, -1.5]}],
            r"\problem{$x = \ans{\pm\tfrac{3}{2}}$}"))
check("\\pm does not excuse a wrong magnitude",
      not binds(_ROOTS, r"\problem{$x = \ans{\pm 8}$}"))
# A ± PAIR IS TWO ANSWERS. Magnitude matching would otherwise let a key print
# either root and pass: on the complex set above, changing the boxed 7i to 0i
# left the surviving -7i covering for it. Measured on the 600 recorded keys —
# a flat magnitude collapse lost 17 planted defects, all of this shape.
check("a solution set must print BOTH roots, not one of them",
      not binds(_COMPLEX, r"\problem{$x = \ans{0i \text{ or } x = -7i}$}"))
code, out = bind_msg(_COMPLEX, r"\problem{$x = \ans{7i}$}")
check("a half-printed solution set is named as a ± pair, not a wrong value",
      code == 1 and "± pair" in out and "only one sign is boxed" in out)
# ...but "the merged values happen to hold both signs" is NOT a ± pair. Both of
# these are real recorded entries that the merged-set reading false-failed.
check("a single expression yielding both signs is not a ± pair",
      binds([{"id": 1, "type": "diff", "expr": "sqrt(25 - x**2)", "order": 2,
              "expected": "-25/(25 - x**2)**(3/2)"}],
            r"\problem{$\ans{-\dfrac{25}{(25-x^2)^{3/2}}}$}"))
check("two entries that happen to disagree in sign are not a ± pair",
      binds([{"id": 1, "type": "equiv", "expr": "2*x + 8", "expected": "2*(x + 4)"},
             {"id": 1, "type": "solve", "expr": "2*x + 8", "var": "x",
              "expected": [-4]}],
            r"\problem{$\ans{2(x + 4)}$, $x = \ans{-4}$}"))

print()
print("Interval bookkeeping is not algebra:")
# `inequality` stores its answer as ["-oo", 18, "loopen"], and every one of
# those markers contains a letter. Reading them as "this answer is an
# expression" switches the boundary to magnitude matching — and an inequality's
# boundary sign IS its answer: b <= 18 and b <= -18 are different answers.
# Measured: counting them as symbolic lost 14 planted sign defects across the
# 600 keys and 600 study guides, every one an inequality.
_INEQ = [{"id": 1, "type": "inequality", "expr": "25*b - 450", "relation": "<=",
          "var": "b", "expected": ["-oo", 18, "loopen"]}]
check("a correct inequality boundary binds", binds(_INEQ, r"\problem{$\ans{b \leq 18}$}"))
check("a flipped boundary sign is still caught",
      not binds(_INEQ, r"\problem{$\ans{b \leq -18}$}"))

print()
print("An `equiv` answer is an EXPRESSION, and is reported as one:")
# expected "(x-4)**2 + (y+1)**2 - 25" boxed as \ans{25} produced THREE faults
# reading "verified value 1 ... 2 ... 4 is in the worked steps but NOT in the
# box — the boxed value is wrong". The boxed value was not wrong; the rule is
# that the whole rewritten form goes in the box. The author hunts an arithmetic
# error that does not exist, once per literal.
_EQUIV = [{"id": 1, "type": "equiv", "expr": "x**2 - 8*x + y**2 + 2*y - 8",
           "expected": "(x-4)**2 + (y+1)**2 - 25"}]

code, out = bind_msg(_EQUIV, r"\problem{Complete the square. $r^2 = \ans{25}$}")
check("a part-boxed equiv answer still fails", code == 1)
check("the message names the TYPE, not a wrong value",
      '"equiv"' in out and "EXPRESSION, not a value" in out)
check("it teaches the actual rule — box the whole rewritten form",
      "rewritten form" in out)
check("it does not accuse the box of holding a wrong value",
      "the boxed value is wrong" not in out)
check("one fault for the entry, not one per literal in the expression",
      out.count("❌ problem 1") == 1 and "1 binding failure" in out)
check("a correctly boxed rewritten form passes",
      binds(_EQUIV, r"\problem{$\ans{(x-4)^2 + (y+1)^2 = 25}$}"))
check("a dropped constant in the rewritten form still fails",
      not binds(_EQUIV, r"\problem{$\ans{(x-4)^2 + (y+1)^2 = 16}$}"))
check("a wrong centre in the rewritten form still fails",
      not binds(_EQUIV, r"\problem{$\ans{(x-3)^2 + (y+1)^2 = 25}$}"))
# A value another entry also claims keeps the ordinary diagnosis: the equiv
# rewording must not swallow a genuine numeric miss sitting beside it.
_MIXED_ENTRY = _EQUIV + [{"id": 1, "type": "approx", "expr": "sqrt(25)",
                          "expected": 5}]
code, out = bind_msg(_MIXED_ENTRY,
                     r"\problem{$\ans{(x-4)^2 + (y+1)^2 = 25}$, $r = \ans{9}$}")
check("a numeric answer beside an equiv answer is still diagnosed numerically",
      code == 1 and "verified value 5" in out)

print()
if FAILS:
    print(f"❌ {len(FAILS)} binding test(s) failed")
    sys.exit(1)
print("✅ all answer-key binding tests passed")
