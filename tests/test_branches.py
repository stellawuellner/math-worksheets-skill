#!/usr/bin/env python3
"""
test_branches.py — exercise verifier branches the fixtures don't reach
(numeric fallbacks, display modes, verdict variants). Behavioral assertions,
not just coverage — each checks the branch does the right thing.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import verify  # noqa: E402

FAILS = []


def expect(name, problem, want, ptype=None):
    got = verify.check_problem(problem, ptype or problem["type"])[0]
    ok = (got != want[1:]) if want.startswith("!") else (got == want)
    print(f"  {'✅' if ok else '❌ got ' + got} {name}")
    if not ok:
        FAILS.append(name)


print("definite_integral numeric fallback (SymPy can't integrate symbolically):")
expect("∫ exp(sin(x)) 0..1 numeric → PASS",
       {"id": 1, "type": "definite_integral", "expr": "exp(sin(x))", "from": 0, "to": 1, "expected": 1.63187, "tol": 1e-3}, "PASS")
expect("∫ highly oscillatory non-convergent → MANUAL",
       {"id": 1, "type": "definite_integral", "expr": "sin(exp(x))", "from": 0, "to": 8, "expected": 0.3, "tol": 1e-4}, "MANUAL")

print("stats variants:")
expect("sum", {"id": 1, "type": "stats", "data": [2, 4, 6], "measure": "sum", "expected": 12}, "PASS")
expect("even-length median", {"id": 1, "type": "stats", "data": [1, 2, 3, 4], "measure": "median", "expected": "5/2"}, "PASS")
expect("mode non-unique → MANUAL", {"id": 1, "type": "stats", "data": [1, 1, 2, 2], "measure": "mode", "expected": 1}, "MANUAL")
expect("q1 school convention (1..9 → 2.5)", {"id": 1, "type": "stats", "data": [1, 2, 3, 4, 5, 6, 7, 8, 9], "measure": "q1", "expected": 2.5}, "PASS")

print("compare / read_data variants:")
expect("compare desc", {"id": 1, "type": "compare", "values": [1, 5, 3], "order": "desc", "expected": [5, 3, 1]}, "PASS")
expect("compare relation =", {"id": 1, "type": "compare", "values": ["1/2", "0.5"], "order": "relation", "expected": "="}, "PASS")
expect("read_data list count", {"id": 1, "type": "read_data", "data": [3, 7, 2], "query": "count", "expected": 3}, "PASS")
expect("read_data list min", {"id": 1, "type": "read_data", "data": [3, 7, 2], "query": "min_value", "expected": 2}, "PASS")
expect("read_data table min_value", {"id": 1, "type": "read_data", "data": {"a": 5, "b": 2}, "query": "min_value", "expected": 2}, "PASS")

print("solve_interval degree-mode display + limit dir:")
expect("solve_interval deg mode", {"id": 1, "type": "solve_interval", "expr": "2*sin(t) - 1", "var": "t", "interval": [0, 360], "unit": "deg", "expected": [30, 150]}, "PASS")
expect("limit one-sided", {"id": 1, "type": "limit", "expr": "1/x", "to": 0, "dir": "+", "expected": "oo"}, "PASS")

print("system MANUAL (infinite family) + estimate tenth:")
expect("system infinite family → MANUAL", {"id": 1, "type": "system", "equations": ["x - y", "2*x - 2*y"], "vars": ["x", "y"], "expected": {"x": 1, "y": 1}}, "MANUAL")
expect("estimate to tenth", {"id": 1, "type": "estimate", "expr": "5.73 + 3.28", "place": "tenth", "expected": "9.0"}, "PASS")

print()
if FAILS:
    print(f"❌ {len(FAILS)} branch test(s) failed: {FAILS}")
    sys.exit(1)
print("✅ All branch tests passed")
