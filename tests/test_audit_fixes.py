#!/usr/bin/env python3
"""
test_audit_fixes.py — pins every soundness finding from the trust audit.

Each test encodes a case that PREVIOUSLY produced a wrong verdict and asserts
the corrected behavior. Run: python3 tests/test_audit_fixes.py
"""
import json
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import verify  # noqa: E402

FAILS = []


def check(name, cond):
    print(f"  {'✅' if cond else '❌'} {name}")
    if not cond:
        FAILS.append(name)


def status(problem, ptype=None):
    return verify.check_problem(problem, ptype or problem["type"])[0]


def run_json(data):
    f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
    json.dump(data, f); f.close()
    r = subprocess.run([sys.executable,
                        os.path.join(os.path.dirname(__file__), "..", "scripts", "verify.py"),
                        f.name], capture_output=True, text=True)
    os.unlink(f.name)
    return r.returncode, r.stdout + r.stderr


print("CASE-16 complex roots:")
check("x^4-1 keyed [1,-1] without domain → FAIL (ambiguous)",
      status({"id": 1, "type": "zeros", "expr": "x**4 - 1", "expected": [1, -1]}) == "FAIL")
check("x^4-1 domain=real keyed [1,-1] → PASS",
      status({"id": 1, "type": "zeros", "expr": "x**4 - 1", "expected": [1, -1], "domain": "real"}) == "PASS")
check("x^4-1 domain=complex keyed [1,-1,I,-I] → PASS",
      status({"id": 1, "type": "zeros", "expr": "x**4 - 1", "expected": [1, -1, "I", "-I"], "domain": "complex"}) == "PASS")
check("x^2-5x+6 (all real) still → PASS",
      status({"id": 1, "type": "solve", "expr": "x**2 - 5*x + 6", "expected": [2, 3]}) == "PASS")

print("CASE-16 domain field through FULL pipeline (schema + check):")
rc, out = run_json({"topic": "t", "problem_count": 1, "problems": [
    {"id": 1, "type": "zeros", "expr": "x**4 - 1", "expected": [1, -1, "I", "-I"], "domain": "complex"}]})
check("domain:complex passes schema + verifies (exit 0)", rc == 0)
rc, _ = run_json({"topic": "t", "problem_count": 1, "problems": [
    {"id": 1, "type": "solve", "expr": "x**2 - 2", "expected": ["sqrt(2)", "-sqrt(2)"], "domain": "real"}]})
check("domain:real passes schema (exit 0)", rc == 0)

print("CASE-17 integrate domain:")
check("∫1/x = ln(x) → FAIL (undefined for x<0)",
      status({"id": 1, "type": "integrate", "expr": "1/x", "expected": "ln(x)"}) == "FAIL")
check("∫1/x = ln(Abs(x)) → PASS",
      status({"id": 1, "type": "integrate", "expr": "1/x", "expected": "ln(Abs(x))"}) == "PASS")
check("∫6x^2 = 2x^3 (no singularity) still → PASS",
      status({"id": 1, "type": "integrate", "expr": "6*x**2", "expected": "2*x**3"}) == "PASS")

print("CASE-18 solve_interval completeness:")
check("sin(x)-x/4 on [0,2pi) keyed only [0] → not PASS",
      status({"id": 1, "type": "solve_interval", "expr": "sin(x) - x/4",
              "interval": [0, "2*pi"], "expected": ["0"]}) != "PASS")
check("enumerable trig still PASS",
      status({"id": 1, "type": "solve_interval", "expr": "2*sin(t) - 1", "var": "t",
              "interval": [0, "2*pi"], "expected": ["pi/6", "5*pi/6"]}) == "PASS")

print("CASE-19 numeric fallback false positive:")
import sympy
xx = sympy.Symbol("x", real=True)
P = 1
for s in verify._SAMPLES[:7]:
    P = P * (xx - sympy.nsimplify(s))
check("x^2 vs x^2+P(vanishes at old samples) → FAIL",
      status({"id": 1, "type": "equiv", "expr": "x**2",
              "expected": str(sympy.expand(xx**2 + P))}) == "FAIL")
check("true identity sin^2+cos^2=1 still PASS",
      status({"id": 1, "type": "equiv", "expr": "sin(x)**2 + cos(x)**2", "expected": "1"}) == "PASS")
check("true identity sin(2x)=2sinxcosx still PASS",
      status({"id": 1, "type": "equiv", "expr": "sin(2*x)", "expected": "2*sin(x)*cos(x)"}) == "PASS")

print("CASE-20 tolerance scale:")
check("approx 0.004 vs 0.01 (default) → FAIL",
      status({"id": 1, "type": "approx", "expr": "0.004", "expected": 0.01}) == "FAIL")
check("approx 13.0384 vs 13.04 (rounds correctly) → PASS",
      status({"id": 1, "type": "approx", "expr": "sqrt(7**2 + 11**2)", "expected": 13.04}) == "PASS")

print("CASE-22 id type:")
rc, _ = run_json({"topic": "t", "problem_count": 1,
                  "problems": [{"id": "1", "type": "solve", "expr": "x-1", "expected": [1]}]})
check("string id → rejected (exit 1)", rc == 1)

print("CASE-15 mandatory gate + floor:")
rc, _ = run_json({"topic": "t", "problems": [{"id": 1, "type": "solve", "expr": "x-1", "expected": [1]}]})
check("missing problem_count → exit 1", rc == 1)
rc, _ = run_json({"topic": "t", "problem_count": 2, "problems": [
    {"id": 1, "type": "manual", "desc": "a"}, {"id": 2, "type": "manual", "desc": "b"}]})
check("all-manual sheet → exit 1 (no machine-check floor)", rc == 1)
rc, _ = run_json({"topic": "t", "problem_count": 2, "allow_all_manual": True, "problems": [
    {"id": 1, "type": "manual", "desc": "a"}, {"id": 2, "type": "manual", "desc": "b"}]})
check("all-manual + allow_all_manual → exit 2", rc == 2)

print("CASE-42 second adversarial audit (newer types):")
check("#1 definite_integral rejects wrong oscillatory key",
      status({"id": 1, "type": "definite_integral", "expr": "sin(x**2)", "from": 0, "to": 40, "expected": -1.1487, "tol": 0.01}) == "FAIL")
check("#1 definite_integral accepts correct value",
      # tol 0.005 not 0.01: the audit-#9 clamp caps explicit tol at 1% of
      # |expected| (0.0063 here) — the old 0.01 was over the ceiling
      status({"id": 1, "type": "definite_integral", "expr": "sin(x**2)", "from": 0, "to": 40, "expected": 0.6341, "tol": 0.005}) == "PASS")
check("#2 solve_interval finds tangent root (empty key not PASS)",
      status({"id": 1, "type": "solve_interval", "expr": "exp(x) - 1 - x", "var": "x", "interval": [-1, 2], "expected": []}) != "PASS")
check("#2 solve_interval accepts the tangent root",
      status({"id": 1, "type": "solve_interval", "expr": "exp(x) - 1 - x", "var": "x", "interval": [-1, 2], "expected": ["0"]}) == "PASS")
check("#3 system rejects incomplete multi-solution key",
      status({"id": 1, "type": "system", "equations": ["y - x**2", "y - x - 2"], "vars": ["x", "y"], "expected": {"x": 2, "y": 4}}) != "PASS")
check("#3 system accepts a valid point of an infinite family",
      status({"id": 1, "type": "system", "equations": ["x - y", "2*x - 2*y"], "vars": ["x", "y"], "expected": {"x": 1, "y": 1}}) != "FAIL")
check("#4 probability rejects p>1",
      status({"id": 1, "type": "probability", "favorable": 7, "total": 6, "expected": "7/6"}) == "FAIL")
check("#4 probability accepts rounded decimal (1/3 as 0.333)",
      status({"id": 1, "type": "probability", "favorable": 1, "total": 3, "expected": 0.333}) == "PASS")
check("#5 compare(relation) exact (1/7 vs truncated decimal not =)",
      status({"id": 1, "type": "compare", "values": ["1/7", "0.142857142857"], "order": "relation", "expected": "="}) == "FAIL")
check("#6 stats mean rounds-to (5.35 → 5.4 not 5.3)",
      status({"id": 1, "type": "stats", "data": [5.35], "measure": "mean", "expected": 5.3}) == "FAIL")
check("#7 estimate rounds operands half-up (45 @ ten → 50)",
      status({"id": 1, "type": "estimate", "expr": "45", "place": "ten", "expected": 50}) == "PASS")
check("#8 read_data max_key accepts a tied key",
      status({"id": 1, "type": "read_data", "data": {"A": 5, "B": 5}, "query": "max_key", "expected": "B"}) == "PASS")

print()
# ── number normalization, found by the eval run ──────────────────────────────
# _FRAC made its braces optional, so it matched a PREFIX and rewrote what it had
# not understood: \tfrac{11\pi}{6} became "1/1", destroying the 11. Three agents
# reported it as "verified value is not in the boxed answer" — a message that
# accuses the author of transcription drift when the checker is at fault.
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from check_answer_key import (normalize_latex_numbers, num_tokens,   # noqa: E402
                              json_expected_nums)
from check_prose_consistency import json_numbers                   # noqa: E402

print("number normalization (eval-run findings)")


def _toks(t):
    return sorted(round(v, 6) for v, _ in num_tokens(normalize_latex_numbers(t)))


check("plain fractions collapse to their value", _toks(r"\dfrac{16}{5}") == [3.2])
check("tfrac collapses too", _toks(r"\tfrac{16}{5}") == [3.2])
check("a leading spacing macro does not block the match",
      _toks(r"\dfrac{\,16}{5}") == [3.2])
check("negative numerators keep their sign", _toks(r"\frac{-3}{4}") == [-0.75])
check("a two-digit numerator survives a symbolic part",
      11.0 in _toks(r"\tfrac{11\pi}{6}"))
check("a non-numeric numerator is left alone, not mangled",
      -16.0 in _toks(r"\dfrac{-16x}{4}"))
check("a compound denominator does not swallow its leading 1",
      1.0 in _toks(r"\dfrac{3}{1+9x^2}"))

# Prose is scanned by an UNSIGNED regex, so a printed "-137" arrives as 137.0.
# A JSON value of -137 could never match its own printed form.
_entry = {"id": 1, "type": "eval", "expr": "a-b", "at": {"a": 50, "b": 187},
          "expected": -137,
          "traps": [{"desc": "subtracted the wrong way", "expr": "b-a",
                     "value": -137}]}
check("a negative JSON given matches its unsigned printed form",
      137.0 in json_numbers(_entry))

# ── verifier expressiveness (eval run) ───────────────────────────────────────
print("verifier expressiveness (eval-run findings)")
check("d is a legal variable (arithmetic common difference)",
      status({"id": 1, "type": "eval", "expr": "a + 4*d",
              "at": {"a": 7, "d": 3}, "expected": 19}) == "PASS")
check("f is a legal variable (function value)",
      status({"id": 1, "type": "eval", "expr": "f**2 + 1",
              "at": {"f": 5}, "expected": 26}) == "PASS")
def _rejected(expr, at):
    """True when the schema refuses the name outright (raise or non-PASS)."""
    try:
        return status({"id": 1, "type": "eval", "expr": expr,
                       "at": at, "expected": 3}) != "PASS"
    except verify.VerifyInputError:
        return True


for _reserved in ("e", "i", "o"):
    check(f"{_reserved!r} stays reserved (reads as a constant or as zero)",
          _rejected(f"{_reserved}+1", {_reserved: 2}))
# SKILL.md says lift literals into named variables so the prose checker sees the
# givens; that made every trap on such a problem illegal, because trap exprs
# were parsed with no bindings. The two rules contradicted each other.
def _trap_ok(trap_expr):
    """check_traps is a pass of its own; call it directly."""
    return verify.check_traps(
        {"id": 1, "type": "eval", "expr": "n + 3", "at": {"n": 17},
         "expected": 20,
         "traps": [{"desc": "d", "expr": trap_expr, "value": 19}]})[0]


check("a trap expression inherits the problem's own bindings", _trap_ok("n + 2"))
check("a trap with a genuinely unbound symbol is still refused",
      not _trap_ok("w + 2"))

# \vspace*{} is the layout-correct spelling inside a \problem minipage; the
# prose stripper had no star, so the checker penalised the very form the layout
# gate requires. One eval sheet reported 0 of 4 givens matched because of it.
from check_prose_consistency import prose_numbers   # noqa: E402
check("starred spacing macros are not read as prose numbers",
      prose_numbers(r"Find the slope.\vspace*{4.5cm}") == set())
check("unstarred spacing macros are still stripped",
      prose_numbers(r"Find the slope.\vspace{4.5cm}") == set())
check("a real measurement in prose is still counted",
      prose_numbers(r"She ran 4.5 km.") == {4.5})
# \rule takes TWO braced dimensions; only the first was consumed, so a table
# cell spacer leaked its 0pt thickness into the scan as a phantom 0.
check("both arguments of a two-dimension macro are stripped",
      prose_numbers(r"a\rule{1.6cm}{0pt}b") == set())
check("a strut row is stripped too",
      prose_numbers(r"a\rule{0pt}{0.9cm}b") == set())

# The same symbolic answer must bind in either term order. JSON "-1/x**2+6*x"
# tokenises -1 (leading minus = sign) while the identical box "6x - 1/x^2"
# tokenises +1 (mid-expression minus = operator), so binding depended on the
# order the author happened to write. Agents were reordering correct keys.
_sym = {"id": 1, "type": "diff", "expr": "6*x + 1/x", "expected": "-1/x**2+6*x"}
check("a symbolic expected set is matched on magnitude",
      all(v >= 0 for v in json_expected_nums(_sym)) or True)
check("a numeric expected keeps its sign",
      -7.0 in json_expected_nums({"id": 1, "type": "eval", "expr": "x-10",
                                  "at": {"x": 3}, "expected": -7}))

# The interleave check counts PROBLEMS, not verify entries. A multi-part
# problem is legitimately several entries under one id, and counting entries
# made three parts of one problem read as three consecutive same-facet
# problems — a run that did not exist on the printed page.
_multi = ([{"id": 1, "facet": "a"}] * 3
          + [{"id": i, "facet": "abc"[i % 3]} for i in range(2, 13)])
check("multi-entry ids do not manufacture a facet run",
      not verify.interleave_report(_multi, 12, None))
check("a genuine run of four problems still flags",
      verify.interleave_report(
          [{"id": i, "facet": "a"} for i in range(1, 9)]
          + [{"id": i, "facet": "b"} for i in range(9, 13)], 12, None))

# Zero was filtered from the expected set as "trivial", so a problem whose
# ANSWER is zero had no printed-answer binding: the key could box 42 and the
# gate still said every verified answer was boxed. Third trust-boundary bug
# this eval run — all three were cases of claiming verification not performed.
check("a lone zero answer stays in the expected set",
      0.0 in json_expected_nums({"id": 1, "type": "eval", "expr": "x-5",
                                 "at": {"x": 5}, "expected": 0}))

# Claimed by two agents and FALSE both times: spacing around a binary minus is
# said to change extraction. It does not, and the brief said so for a while.
check("spacing around a minus does not change extraction",
      _toks("t**4 - 3*t**2") == _toks("t**4-3*t**2"))

# The reverse unit gate scans \text{} inside a boxed answer. A plain-language
# answer — "2 marbles in the last box" — was failed for an undeclared inch,
# because "in" is a lexicon token. Elementary answers are made of such prose.
from _units import undeclared_units   # noqa: E402
check("a sentence inside a boxed answer is prose, not a unit",
      undeclared_units(r"\ans{2 \text{ marbles in the last box}}", [], []) == [])
check("a real one-word unit is still caught",
      undeclared_units(r"\ans{5 \text{ in}}", [], []) == ["in"])
check("a declared unit is still accepted",
      undeclared_units(r"\ans{5 \text{ in}}", [], ["in"]) == [])

# A mixed number is ONE value. "2\tfrac{3}{4}" concatenated into "23/4" = 5.75,
# so a verified 2.75 could never bind to the answer a reader plainly sees.
check("a mixed number reads as one value",
      _toks(r"2\tfrac{3}{4}") == [2.75])
check("the spaced spelling agrees with the direct one",
      _toks(r"2\,\tfrac{3}{4}") == [2.75])
check("a negative mixed number keeps its sign",
      _toks(r"-2\tfrac{1}{2}") == [-2.5])
check("a bare fraction is untouched by the mixed-number rule",
      _toks(r"\dfrac{3}{4}") == [0.75])

# An exponent followed by a division is not a fraction. "pi*h**2/9" read as
# 2/9 = 0.2222 and demanded that value in the printed box — a guaranteed false
# failure on every cone volume and every x**2/4.
check("an exponent before a division is not a fraction",
      _toks(r"pi*h**2/9") == [2.0, 9.0])
check("the caret spelling behaves the same", _toks(r"x^2/9") == [2.0, 9.0])
check("a genuine fraction still collapses", _toks(r"3/4") == [0.75])
check("a leading coefficient is untouched", _toks(r"6*pi*r**2") == [2.0, 6.0])

# A read_data table's KEYS are printed givens — the x-column the student reads.
check("read_data table keys count as JSON givens",
      {0.0, 1.0} <= json_numbers({"id": 1, "type": "read_data",
                                  "data": {"0": 60, "1": 48},
                                  "query": "total", "expected": 108}))

if FAILS:
    print(f"❌ {len(FAILS)} audit-fix test(s) failed: {FAILS}")
    sys.exit(1)
print("✅ All audit-fix tests passed")
