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
if FAILS:
    print(f"❌ {len(FAILS)} audit-fix test(s) failed: {FAILS}")
    sys.exit(1)
print("✅ All audit-fix tests passed")
