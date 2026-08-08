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
# an explicit tol above the 1%/half-ulp ceiling is a one-field gate bypass
# (audit #9) — rejected without a tol_reason acknowledgement
rejects("oversize tol", {"id": 1, "type": "approx", "expr": "1", "expected": 1.0, "tol": 5})
rejects("oversize tol, blank reason", {"id": 1, "type": "approx", "expr": "1", "expected": 1.0, "tol": 5, "tol_reason": ""})
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
# 'unit' is the deg/rad ANGLE MODE, never a measurement unit — a measurement
# accidentally landing there (the answer_unit confusion) must stay rejected
rejects("triangle unit 'ft' (answer_unit confusion)", {"id": 1, "type": "triangle", "given": {"a": 5, "b": 6, "c": 7}, "solve_for": "A", "expected": 1, "unit": "ft"})
rejects("solve_interval unit 'ft' (answer_unit confusion)", {"id": 1, "type": "solve_interval", "expr": "2*sin(t) - 1", "var": "t", "interval": [0, 360], "unit": "ft", "expected": [30, 150]})
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

# ── The raise paths a coverage read found dark ───────────────────────────────
# Every case here was an UNCOVERED `raise VerifyInputError` when measured
# (2026-08-08): validation that had never once fired in a test. That matters
# beyond the percentage: these messages are the UX of the gate — each one
# teaches an author the fix — and this project has already shipped teaching
# messages that were wrong until something exercised them. Each case asserts
# the MESSAGE as well as the raise, because "raised something" does not pin
# "taught the right fix".


def schema_rejects(name, problem, needle):
    """check_schema must refuse, and say why with the expected words."""
    try:
        verify.check_schema(problem)
        FAILS.append(f"{name}: check_schema accepted it")
        print(f"  ❌ {name} (accepted)")
    except verify.VerifyInputError as e:
        if needle in str(e):
            print(f"  ✅ {name}")
        else:
            FAILS.append(f"{name}: message {e} lacks {needle!r}")
            print(f"  ❌ {name} (wrong message: {e})")
    except Exception as e:  # noqa: BLE001 — a crash is exactly the bug
        FAILS.append(f"{name}: {type(e).__name__}: {e}")
        print(f"  ❌ {name} ({type(e).__name__})")


def rejects_saying(name, problem, needle, ptype=None, via=None):
    """The named validator must refuse with the expected words. `via` selects
    the entry point: traps and figures are validated by their own functions,
    called from main() before check_problem ever runs — routing everything at
    check_problem quietly asserts nothing for them, which is exactly how this
    suite's first draft went green on seven cases the validator never saw."""
    fn = via or (lambda pr, pt: verify.check_problem(pr, pt))
    try:
        fn(problem, ptype or problem["type"])
        FAILS.append(f"{name}: accepted")
        print(f"  ❌ {name} (accepted)")
    except verify.VerifyInputError as e:
        if needle in str(e):
            print(f"  ✅ {name}")
        else:
            FAILS.append(f"{name}: message {e} lacks {needle!r}")
            print(f"  ❌ {name} (wrong message: {e})")
    except Exception as e:  # noqa: BLE001
        FAILS.append(f"{name}: {type(e).__name__}: {e}")
        print(f"  ❌ {name} ({type(e).__name__})")


print("Schema-level shapes:")
schema_rejects("a problem that is not an object", ["id", 1], "must be a JSON object")
schema_rejects("a problem with no id", {"type": "eval"}, "missing required field 'id'")
schema_rejects("a non-integer id", {"id": "one", "type": "eval"}, "must be an integer")
schema_rejects("an unknown type", {"id": 1, "type": "quadrature"}, "allowed types")
schema_rejects("a misspelled field",
               {"id": 1, "type": "eval", "expr": "x", "at": {"x": 1},
                "expected": 1, "expcted": 2}, "unknown field")
schema_rejects("workspace_cm that is not a number",
               {"id": 1, "type": "eval", "expr": "x", "at": {"x": 1},
                "expected": 1, "workspace_cm": "tall"}, "number of centimetres")
schema_rejects("workspace_cm past the page",
               {"id": 1, "type": "eval", "expr": "x", "at": {"x": 1},
                "expected": 1, "workspace_cm": 40}, "between 0 and 24")
schema_rejects("word_problem that is not a boolean",
               {"id": 1, "type": "eval", "expr": "x", "at": {"x": 1},
                "expected": 1, "word_problem": "yes"}, "true or false")

print("Geometry input shapes:")
rejects_saying("points that are not even a list",
               {"id": 1, "type": "distance", "points": "1,2 3,4",
                "expected": 1}, "list of [x, y] pairs")
rejects_saying("a point that is not a pair",
               {"id": 1, "type": "distance", "points": [[1, 2], [3]],
                "expected": 1}, "an [x, y] pair")
rejects_saying("triangle 'given' that is not an object",
               {"id": 1, "type": "triangle", "given": [7, 11, 34],
                "solve_for": "c", "expected": 6.5}, "'given' must be an object")
rejects_saying("triangle solve_for outside a..C",
               {"id": 1, "type": "triangle", "given": {"a": 7, "b": 11, "C": 34},
                "solve_for": "q", "expected": 6.5}, "one of a, b, c, A, B, C")
rejects_saying("a 0-degree given angle",
               {"id": 1, "type": "triangle", "given": {"a": 7, "b": 11, "C": 0},
                "solve_for": "c", "expected": 1}, "strictly between")
rejects_saying("an 'at' variable outside the allowlist",
               {"id": 1, "type": "eval", "expr": "x", "at": {"x": 1, "q9": 2},
                "expected": 1}, "not allowed")
rejects_saying("an interval that is not [a, b]",
               {"id": 1, "type": "solve_interval", "expr": "sin(t)", "var": "t",
                "interval": [0], "expected": [0]}, "two-element list")

def _via_traps(pr, pt):
    verify.validate_traps(pr, pt)


def _via_figure(pr, pt):
    verify.validate_figure(pr, pt)


print("Trap declaration shapes:")
_BASE = {"id": 1, "type": "approx", "expr": "9*2", "expected": 18}
rejects_saying("a trap that is not an object",
               dict(_BASE, traps=["used cos"]), "must be a JSON object",
               via=_via_traps)
rejects_saying("a scalar-shape trap using 'exprs'",
               dict(_BASE, traps=[{"desc": "d", "exprs": ["9*3"]}]),
               "wrong", ptype="approx", via=_via_traps)
rejects_saying("a trap expr that is not a string",
               dict(_BASE, traps=[{"desc": "d", "expr": 27}]),
               "must be an expression string", via=_via_traps)
rejects_saying("an empty trap value string",
               dict(_BASE, traps=[{"desc": "d", "expr": "9*3", "value": " "}]),
               "must not be empty", via=_via_traps)
def trap_check_fails(name, problem, needle):
    """check_traps reports through a (False, message) tuple, not a raise —
    that tuple is what build.sh's verify gate prints, so the MESSAGE is the
    contract here exactly as it is on the raising validators."""
    ok, msg = verify.check_traps(problem)
    if ok is False and needle in str(msg):
        print(f"  ✅ {name}")
    else:
        FAILS.append(f"{name}: got ({ok!r}, {str(msg)[:80]!r})")
        print(f"  ❌ {name}")


trap_check_fails("a set-shape trap entry that cannot parse",
                 {"id": 1, "type": "solve", "expr": "x**2 - 4",
                  "expected": [2, -2],
                  "traps": [{"desc": "dropped a root", "exprs": ["import os"]}]},
                 "entry")
trap_check_fails("a set-shape trap value that is not numeric",
                 {"id": 1, "type": "solve", "expr": "x**2 - 4",
                  "expected": [2, -2],
                  "traps": [{"desc": "kept x", "exprs": ["2"],
                             "value": ["x + 1"]}]},
                 "fully numeric")
trap_check_fails("a scalar trap whose expected is not comparable",
                 {"id": 1, "type": "approx", "expr": "9*2",
                  "expected": "roughly 18",
                  "traps": [{"desc": "d", "expr": "9*3"}]},
                 "not numerically comparable")

print("Figure declaration shapes:")
_EVAL = {"id": 1, "type": "eval", "expr": "a/b", "at": {"a": 8, "b": 15},
         "expected": "8/15"}
rejects_saying("a figure that is not an object",
               dict(_EVAL, figure="right_triangle"), "must be an object",
               via=_via_figure)
rejects_saying("a figure with unknown fields",
               dict(_EVAL, figure={"kind": "right_triangle",
                                   "given": {"a": 8, "b": 15},
                                   "solve_for": "c", "colour": "red"}),
               "unknown field", via=_via_figure)
rejects_saying("a figure given that is not two of a/b/c/A/B",
               dict(_EVAL, figure={"kind": "right_triangle",
                                   "given": {"a": 8}, "solve_for": "c"}),
               "exactly two", via=_via_figure)
rejects_saying("a figure given that is not a plain number",
               dict(_EVAL, figure={"kind": "right_triangle",
                                   "given": {"a": "8", "b": 15},
                                   "solve_for": "c"}),
               "plain number", via=_via_figure)
rejects_saying("a figure solve_for already among the givens",
               dict(_EVAL, figure={"kind": "right_triangle",
                                   "given": {"a": 8, "b": 15},
                                   "solve_for": "a"}),
               "not already given", via=_via_figure)
rejects_saying("a figure unknown that is not a short name",
               dict(_EVAL, figure={"kind": "right_triangle",
                                   "given": {"a": 8, "b": 15},
                                   "solve_for": "c",
                                   "unknown": "the missing side"}),
               "short letter name", via=_via_figure)
rejects_saying("figure kind triangle on a non-triangle problem",
               dict(_EVAL, figure={"kind": "triangle",
                                   "given": {"a": 8, "b": 15},
                                   "solve_for": "c"}),
               "only applies", via=_via_figure)
rejects_saying("figure givens that cannot form a right triangle",
               dict(_EVAL, figure={"kind": "right_triangle",
                                   "given": {"a": 15, "c": 8},
                                   "solve_for": "b"}),
               "right triangle", via=_via_figure)

print("read_data query shapes:")
_RD = {"id": 1, "type": "read_data", "data": {"Mon": 4, "Tue": 7},
       "expected": 4}
rejects_saying("a value query with no key",
               dict(_RD, query="value"), "needs \"key\"")
rejects_saying("a difference key naming a missing category",
               dict(_RD, query="difference", key=["Mon", "Fri"], expected=3),
               "not a category")

# ── FAIL branches with taught messages (dark until now) ─────────────────────
# These are not rejections of malformed input; they are wrong-mathematics
# verdicts whose MESSAGE does the teaching. Each was written for a failure an
# eval author actually hit, and none had a test pinning the words.


def fails_saying(name, problem, needle):
    status, detail = verify.check_problem(problem, problem["type"])
    txt = detail if isinstance(detail, str) else " ".join(map(str, detail))
    if status == "FAIL" and needle in txt:
        print(f"  ✅ {name}")
    else:
        FAILS.append(f"{name}: ({status}, {txt[:90]!r})")
        print(f"  ❌ {name}")


print("Wrong-mathematics verdicts that must teach:")
fails_saying("an inconsistent system keyed 'infinitely many'",
             {"id": 1, "type": "system",
              "equations": ["x + y - 1", "x + y - 3"], "vars": ["x", "y"],
              "expected": "infinitely many"},
             "inconsistent")
fails_saying("a listed solution that does not satisfy every equation",
             {"id": 1, "type": "system",
              "equations": ["x + y - 1", "x + y - 3"], "vars": ["x", "y"],
              "expected": [{"x": 1, "y": 0}]},
             "does not satisfy")
fails_saying("an estimate whose rounding zeroes an operand names the "
             "zeroed number instead of computing nonsense",
             {"id": 1, "type": "estimate", "expr": "63+4", "place": "ten",
              "expected": 70},
             "0")

status, detail = verify.check_problem(
    {"id": 1, "type": "stats", "measure": "q1", "data": [5], "expected": 5},
    "stats")
check_line = "quartiles on too few points go to MANUAL, never a guessed number"
if status == "MANUAL":
    print(f"  ✅ {check_line}")
else:
    FAILS.append(f"{check_line}: {status}")
    print(f"  ❌ {check_line}")

rejects_saying("a nonsense estimate place is refused with the menu",
               {"id": 1, "type": "estimate", "expr": "63+29",
                "place": "dozen", "expected": 90}, "place")
rejects_saying("a nonsense stats measure is refused with the menu",
               {"id": 1, "type": "stats", "measure": "midhinge",
                "data": [1, 2, 3], "expected": 2}, "measure")
