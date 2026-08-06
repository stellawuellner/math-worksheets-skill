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
check("string via safe_parse->latex, in the author's own order",
      rqa._fmt("(x-3)*(x-4)") == r"$\left(x - 3\right) \left(x - 4\right)$")
check("probability fraction typesets",
      rqa._fmt("3/8") == r"$\frac{3}{8}$")
check("a non-expression prints as itself, not as --- (see defect 1/4 below)",
      rqa._fmt("x = 2 or x = 3") == "x = 2 or x = 3")
check("injection-shaped string is escaped, never injected",
      rqa._fmt(r"\input{/etc/passwd}")
      == r"\textbackslash{}input\{/etc/passwd\}")
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

print()
# ── the 300-case post-eval review of _fmt ────────────────────────────────────
# Every defect below was found in a DELIVERED answer key and traces to one line:
# "$" + sympy.latex(sympy.sympify(v)) + "$", plus a "---" that meant two
# opposite things at once. Each check here is a case that shipped wrong.
print("post-eval review — defect 1: verified relations must not vanish")

# 63 cases. sympify("<") raises, so a VERIFIED compare printed "---" — the SAME
# glyph a manual-only id prints. On curr-154 the signalling was exactly
# inverted: three verified relations printed "---" and three genuinely manual
# items printed nothing a grader could distinguish from them.
check("a verified relation typesets as the relation", rqa._fmt("<") == "$<$")
check("every compare relation survives",
      [rqa._fmt(r) for r in ("<", ">", "=", "<=", ">=")]
      == ["$<$", "$>$", "$=$", r"$\le$", r"$\ge$"])
_rel = rqa.render_entry([{"type": "compare", "expected": "<"}])
_man = rqa.render_entry([{"type": "manual", "desc": "proof"}])
check("verified and manual no longer print the same glyph", _rel != _man)
check("--- stays reserved for 'no machine check exists'", _man == "---")

print("post-eval review — defect 2: python builtins must never typeset")

# 5 cases. sympify("open") SUCCEEDS and hands back the builtin, whose repr
# sympy dutifully typesets: curr-184's delivered key printed
# "2. -oo, -3, <built-in function open>" on four rows. safe_parse's allowlist
# rejects the name outright, so the printer never sees a non-mathematical object.
for _b in ("open", "print", "eval", "exec", "__import__"):
    check(f"builtin {_b!r} never reaches the printer",
          "built-in" not in rqa._fmt(_b))
check("a rejected name prints as the word it is", rqa._fmt("open") == "open")
check("an inequality's interval spec prints as an interval",
      rqa.render_entry([{"type": "inequality", "relation": "<",
                         "expected": ["-oo", -3, "open"]}])
      == r"$(-\infty, -3)$")

print("post-eval review — defect 3: the author's form must survive")

# 37 cases, six of them a WRONG factor answer: sympify canonicalises, and
# Mul flattening distributes the coefficient, so a completely factored
# 3*(x-3)*(x+3) came out as (x+3)(3x-9) on a sheet whose directions read
# "Factor completely". evaluate=False is what preserves the author's form.
check("an unreduced fraction stays unreduced", rqa._fmt("9/12") == r"$\frac{9}{12}$")
check("25/30 is not silently reduced to 5/6",
      rqa._fmt("25/30") == r"$\frac{25}{30}$")
check("a mixed number stays a mixed number",
      rqa._fmt("2 + 3/4") == r"$2 + \frac{3}{4}$")
check("a completely factored answer stays completely factored",
      rqa._fmt("3*(x-3)*(x+3)")
      == r"$3 \left(x - 3\right) \left(x + 3\right)$")
check("a factored answer is not expanded",
      rqa._fmt("6*(2*n-3)") == r"$6 \left(2 n - 3\right)$")

print("post-eval review — defect 4: a label is not an expression")

# 1 case, and it evaded BOTH obvious guards: sympify("20-29") SUCCEEDS and
# returns a valid sympy Number, so curr-446 id 8's histogram bin label "20-29"
# was banked as -9.
check("a bin label prints as the label", rqa._fmt("20-29") == "20-29")
check("a decimal-range label survives too", rqa._fmt("2.5-3.5") == "2.5-3.5")
check("real subtraction still computes as mathematics",
      rqa._fmt("29-20") == "$29 - 20$")

print("post-eval review — defect 5: a verified empty solution set")

# 5+1 cases. A verified "no solution" (expected []) joined to the empty string:
# curr-390 row 10 printed the dangling "10. 0," and curr-262 printed "---",
# claiming nobody had checked an answer the verifier had proved.
check("a verified empty solution set prints the empty set",
      rqa.render_entry([{"type": "solve", "expected": []}]) == r"$\emptyset$")
check("no solution is never confused with no check",
      rqa.render_entry([{"type": "solve", "expected": []}]) != "---")
_dangle = rqa.render_entry([{"expected": 0}, {"type": "solve", "expected": []}])
check("no dangling comma on a mixed empty/non-empty id",
      _dangle == r"0, $\emptyset$")

print("post-eval review — defect 6: a partially manual id says so")

# 6 cases. The "---" was guarded by "if not vals", so an id mixing a machine
# check with a manual entry showed no manual marker at all — the grader read a
# complete answer where half of it was never checked.
check("a machine + manual id still shows the manual marker",
      rqa.render_entry([{"type": "approx", "expected": 5},
                        {"type": "manual", "desc": "sketch"}]) == "5, ---")
check("an all-machine id carries no manual marker",
      rqa.render_entry([{"type": "approx", "expected": 5},
                        {"type": "approx", "expected": 7}]) == "5, 7")

print("post-eval review — defect 7: multi-slot answers are labelled")

# 9 cases. Values were joined in verify.json ARRAY order with no labels:
# curr-334 asks for "AC and BD" and printed "2. 2.83, 8.49" with BD first;
# curr-427's rows 5 and 11 were correct only by coincidence of declaration
# order. The label has to come from the JSON entry, so order stops mattering.
_slots = rqa.render_entry([{"type": "approx", "expected": 2.83, "slot": "BD"},
                           {"type": "approx", "expected": 8.49, "slot": "AC"}])
check("each slot is named by its own JSON label",
      _slots == "BD = 2.83, AC = 8.49")
check("a slot label is escaped, not injected",
      "\\textbackslash{}" in rqa.render_entry(
          [{"expected": 1, "slot": r"\bad"}]))
check("an unlabelled entry is unchanged",
      rqa.render_entry([{"expected": 2.83}]) == "2.83")
# "slot" is READ here but not yet ACCEPTED by verify.py's strict schema, so the
# labels cannot reach a real sheet until _UNIVERSAL_FIELDS learns the field.
# This check is the reminder: it flips to a pass the moment that lands.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import verify  # noqa: E402
print("     (follow-up) verify.py accepts a 'slot' label:",
      "yes" if "slot" in verify._UNIVERSAL_FIELDS else
      "NOT YET — add \"slot\" to _UNIVERSAL_FIELDS in scripts/verify.py")

print("post-eval review — defect 8: minus signs, ln, points, units, cents")

check("a negative integer uses a real minus, not a text hyphen",
      rqa._fmt(-3) == "$-3$" and rqa._fmt(Decimal("-6.30")) == "$-6.30$")
check("a positive integer stays plain text", rqa._fmt(7) == "7")
check("ln prints as ln, not log",
      rqa._fmt("ln(x)") == r"$\ln{\left(x \right)}$")
check("log still prints as log", rqa._fmt("log(x)").startswith(r"$\log"))
check("a midpoint prints as a bracketed pair",
      rqa._fmt([5, 2], "midpoint") == "(5, 2)")
check("a solution list is still a comma-joined list", rqa._fmt([5, 2]) == "5, 2")
check("a declared answer_unit is printed with the value",
      rqa.render_entry([{"type": "approx", "expected": Decimal("6.30"),
                         "answer_unit": "ft"}]) == "6.30 ft")
check("a squared unit typesets its exponent",
      rqa.render_entry([{"type": "polygon_area", "expected": 17,
                         "answer_unit": "cm^2"}]) == "17 cm$^{2}$")
check("money keeps its cents", rqa._fmt("12.50") == "12.50")

# The bank must stay PLAIN TEXT whatever the new renderings emit: check_answer_key.py
# binds only boxed answers inside problem segments, and never resolves \input.
_mixed = {"problem_count": 6, "problems": [
    {"id": 1, "type": "compare", "values": ["1/2", "0.6"], "order": "relation",
     "expected": "<"},
    {"id": 2, "type": "inequality", "relation": "<", "expr": "x+3",
     "expected": ["-oo", -3, "open"]},
    {"id": 3, "type": "solve", "expr": "x**2+1", "expected": []},
    {"id": 4, "type": "approx", "expr": "9", "expected": Decimal("6.30"),
     "answer_unit": "ft"},
    {"id": 5, "type": "manual", "desc": "sketch"},
    {"id": 6, "type": "read_data", "data": {}, "query": "mode",
     "expected": "20-29"}]}
_mtext = rqa.render(_mixed)
_mbody = "\n".join(l for l in _mtext.split("\n") if not l.startswith("%"))
check("the new renderings still emit no \\ans/\\boxed",
      "\\ans" not in _mbody and "\\boxed" not in _mbody)
check("every id still gets exactly one numbered line",
      all(f"\n{i}.~" in "\n" + _mtext for i in range(1, 7)))
check("only the manual id prints ---",
      "5.~---" in _mtext and "1.~$<$" in _mtext and "6.~20-29" in _mtext)

# ── Unchecked answers must be visible to the instructor ────────────────────
# The bank had two states: a value, or "---" for a manual item. A printed
# response with NO verify entry produced neither — the row just looked
# complete. 172 of 300 reviewed cases shipped an answer nothing verified, and a
# grader reading "2. 18" had no way to know the sheet also asked for a number
# word that nobody checked. Marks appear ONLY when a worksheet was supplied and
# coverage was actually measured; they are evidence, not decoration.
print("Unchecked-answer marking (three states: verified / judgement / unchecked):")

_WS = r"""\input{worksheet-preamble}
\begin{document}
\problem{Find AC~\ansblank\ and BD~\ansblank}
\problem[4cm]{Write the number word~\ansblank\ and the ones digit~\ansblank}
\problem[3cm]{Prove the triangles are congruent.\noansline}
\end{document}
"""
_cov = {"topic": "t", "problem_count": 3, "problems": [
    {"id": 1, "type": "distance", "points": [[0, 0], [2, 2]],
     "expected": "2*sqrt(2)", "slot": "AC"},
    {"id": 1, "type": "distance", "points": [[0, 0], [6, 6]],
     "expected": "6*sqrt(2)", "slot": "BD"},
    {"id": 2, "type": "eval", "expr": "10+8", "expected": 18},
    {"id": 3, "type": "manual", "desc": "two-column proof"}]}

_with = rqa.render(_cov, ws_tex=_WS)
_without = rqa.render(_cov)

check("a problem with an uncovered printed slot is marked unchecked",
      "2.~18~\\unchecked" in _with)
check("a fully covered problem carries NO mark",
      "1.~AC = " in _with and "\\unchecked" not in _with.split("2.~")[0])
check("a manual id still prints --- and is not called unchecked",
      "3.~---" in _with)
check("the note tallies what is machine-checked",
      "1 of 3 problem" in _with and "machine-checked" in _with)
check("the note names the unchecked problem so acting on it needs no digging",
      "problem 2" in _with and "NO machine guarantee" in _with)
check("the note names the judgement problem separately",
      "only you can judge" in _with and "problem 3" in _with)
# Without a worksheet the renderer cannot know how many responses are printed,
# so it must not claim anything is unchecked. It CAN still see which ids are
# manual — that is in the JSON — and saying so costs nothing.
check("without a worksheet nothing is claimed to be unchecked",
      "\\unchecked" not in _without)
check("manual items are still reported without a worksheet",
      "only you can judge" in _without and "problem 3" in _without)
# Comments are stripped first, as elsewhere in this file: the generated header
# TALKS about \ans/\boxed to explain why the bank must not use them.
_wbody = "\n".join(l for l in _with.split("\n") if not l.startswith("%"))
check("marking still emits no \\ans/\\boxed",
      "\\ans" not in _wbody and "\\boxed" not in _wbody)

_clean = {"topic": "t", "problem_count": 1, "problems": [
    {"id": 1, "type": "eval", "expr": "1+1", "expected": 2}]}
_cws = ("\\input{worksheet-preamble}\n\\begin{document}\n"
        "\\problem[3cm]{Add.}\n\\end{document}\n")
check("a fully verified sheet prints no legend at all (no warning fatigue)",
      "What is verified" not in rqa.render(_clean, ws_tex=_cws))


if FAILS:
    print(f"❌ {len(FAILS)} quick-answer test(s) failed")
    sys.exit(1)
print("✅ All quick-answer tests passed")
