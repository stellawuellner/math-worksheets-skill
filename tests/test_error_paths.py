#!/usr/bin/env python3
"""
test_error_paths.py — exercise the verifier's input-validation branches.

Every malformed input must be rejected (VerifyInputError → FAIL), never crash
the process and never pass. This both hardens the error handling and drives
coverage of the validation code that happy/fail fixtures don't reach.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import verify  # noqa: E402

FAILS = []


def rejects(name, problem, ptype=None):
    """A malformed problem must raise VerifyInputError inside check_problem."""
    try:
        verify.check_problem(problem, ptype or problem["type"])
        FAILS.append(f"{name}: expected VerifyInputError, got a verdict")
        print(f"  ❌ {name} (no error raised)")
    except verify.VerifyInputError:
        print(f"  ✅ {name}")
    except Exception as e:
        FAILS.append(f"{name}: wrong exception {type(e).__name__}: {e}")
        print(f"  ❌ {name} ({type(e).__name__}: {e})")


print("Expression allowlist / parsing:")
rejects("non-string expr", {"id": 1, "type": "solve", "expr": 5, "expected": [1]})
rejects("disallowed name", {"id": 1, "type": "eval", "expr": "os", "at": {"x": 0}, "expected": 0})
rejects("attribute access", {"id": 1, "type": "eval", "expr": "x.real", "at": {"x": 0}, "expected": 0})
rejects("over-long expr", {"id": 1, "type": "eval", "expr": "1+" * 300 + "1", "at": {"x": 0}, "expected": 1})
rejects("bad expected type", {"id": 1, "type": "eval", "expr": "x", "at": {"x": 1}, "expected": [1, 2]})
rejects("boolean expected", {"id": 1, "type": "eval", "expr": "x", "at": {"x": 1}, "expected": True})

print("Tolerances / values:")
rejects("negative tol", {"id": 1, "type": "approx", "expr": "1", "expected": 1, "tol": -1})
rejects("bool tol", {"id": 1, "type": "approx", "expr": "1", "expected": 1, "tol": True})
rejects("approx with variable", {"id": 1, "type": "approx", "expr": "x + 1", "expected": 1})

print("Geometry:")
rejects("distance not 2 points", {"id": 1, "type": "distance", "points": [[0, 0]], "expected": 0})
rejects("point not a pair", {"id": 1, "type": "distance", "points": [[0], [1, 1]], "expected": 0})
rejects("midpoint bad expected", {"id": 1, "type": "midpoint", "points": [[0, 0], [2, 2]], "expected": 1})
rejects("polygon <3 points", {"id": 1, "type": "polygon_area", "points": [[0, 0], [1, 1]], "expected": 0})

print("Triangle:")
rejects("triangle bad given key", {"id": 1, "type": "triangle", "given": {"x": 5, "b": 6, "c": 7}, "solve_for": "A", "expected": 1})
rejects("triangle not 3 givens", {"id": 1, "type": "triangle", "given": {"a": 5, "b": 6}, "solve_for": "A", "expected": 1})
rejects("triangle no side", {"id": 1, "type": "triangle", "given": {"A": 30, "B": 60, "C": 90}, "solve_for": "a", "expected": 1})
rejects("triangle bad unit", {"id": 1, "type": "triangle", "given": {"a": 5, "b": 6, "c": 7}, "solve_for": "A", "expected": 1, "unit": "grad"})
rejects("triangle solve_for given", {"id": 1, "type": "triangle", "given": {"a": 5, "b": 6, "c": 7}, "solve_for": "a", "expected": 5})
rejects("triangle negative side", {"id": 1, "type": "triangle", "given": {"a": -5, "b": 6, "c": 7}, "solve_for": "A", "expected": 1})

print("solve / domain / var:")
rejects("bad domain", {"id": 1, "type": "solve", "expr": "x-1", "expected": [1], "domain": "rational"})
rejects("bad var", {"id": 1, "type": "solve", "expr": "x-1", "var": "q9", "expected": [1]})
rejects("diff bad order", {"id": 1, "type": "diff", "expr": "x**2", "order": 0, "expected": "0"})
rejects("limit bad dir", {"id": 1, "type": "limit", "expr": "1/x", "to": 0, "dir": "up", "expected": "oo"})
rejects("eval bad at", {"id": 1, "type": "eval", "expr": "x", "at": [], "expected": 0})

print("system / series / inequality:")
rejects("system eqs not list", {"id": 1, "type": "system", "equations": "x-1", "vars": ["x"], "expected": {"x": 1}})
rejects("system bad var", {"id": 1, "type": "system", "equations": ["q-1"], "vars": ["q9"], "expected": {"x": 1}})
rejects("system expected not obj", {"id": 1, "type": "system", "equations": ["x-1"], "vars": ["x"], "expected": [1]})
rejects("inequality bad relation", {"id": 1, "type": "inequality", "expr": "x-1", "relation": "!=", "expected": [1, "oo", "open"]})
rejects("bad interval spec len", {"id": 1, "type": "inequality", "expr": "x-1", "relation": ">", "expected": [1, "oo"]})

print("stats / probability / read_data / estimate / compare:")
rejects("stats empty data", {"id": 1, "type": "stats", "data": [], "measure": "mean", "expected": 0})
rejects("stats bad measure", {"id": 1, "type": "stats", "data": [1, 2], "measure": "geomean", "expected": 1})
rejects("probability zero total", {"id": 1, "type": "probability", "favorable": 1, "total": 0, "expected": "1/2"})
rejects("read_data bad table query", {"id": 1, "type": "read_data", "data": {"a": 1}, "query": "median", "expected": 1})
rejects("read_data bad list query", {"id": 1, "type": "read_data", "data": [1, 2], "query": "median", "expected": 1})
rejects("read_data bad data type", {"id": 1, "type": "read_data", "data": 5, "query": "total", "expected": 5})
rejects("estimate bad place", {"id": 1, "type": "estimate", "expr": "47", "place": "dozen", "expected": 50})
rejects("compare too few values", {"id": 1, "type": "compare", "values": [1], "expected": [1]})
rejects("compare bad order", {"id": 1, "type": "compare", "values": [1, 2], "order": "random", "expected": [1, 2]})

print()
if FAILS:
    print(f"❌ {len(FAILS)} error-path test(s) failed:")
    for f in FAILS:
        print(f"   {f}")
    sys.exit(1)
print("✅ All error-path tests passed")
