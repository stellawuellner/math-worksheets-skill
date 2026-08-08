#!/usr/bin/env python3
"""
test_verify.py — the numeric-comparison defect family, pinned.

The curriculum run recorded FIVE separate occasions on which an author changed
correct mathematics to satisfy a comparison defect in this file: a trend line
9.4−0.4x rewritten to 9.5−0.5x, the free-fall model 4.9t² rewritten to 5t², a
rate 1.2 rewritten to 1.25, a root 499.999999999999 rejected against 500, and a
JSON shape changed to unwrap a one-element list. Every case below FAILED before
the fix and passes after; every "still fails" case is here because the fix must
not buy those passes with a false accept.

Grouped exactly as the finding is:
  A. exact float comparison
  B. symbolic and complex answers as second-class citizens
  C. answers the schema could not express at all
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import sympy   # noqa: E402
import verify  # noqa: E402


def _raises_input(fn):
    """True when fn() raises VerifyInputError — a rejection, not a crash."""
    try:
        fn()
    except verify.VerifyInputError:
        return True
    except Exception:
        return False
    return False

FAILS = []


def _run(problem):
    """(status, detail) through the same door run_verification() uses, so a
    schema rejection is a verdict rather than an exception."""
    try:
        ptype = verify.check_schema(problem)
        status, detail = verify.check_problem(problem, ptype)
    except verify.VerifyInputError as e:
        return ("INPUT", str(e))
    if status == "PASS" and problem.get("traps"):
        ok, info = verify.check_traps(problem)
        if not ok:
            return ("TRAPFAIL", info)
        return (status, " | ".join(info))
    return (status, detail)


def check(name, cond, extra=""):
    print(f"  {'✅' if cond else '❌'} {name}" + (f"  [{extra}]" if not cond else ""))
    if not cond:
        FAILS.append(name)


def expect(name, problem, want):
    status, detail = _run(problem)
    check(name, status == want, f"got {status}: {detail}")
    return detail


def expect_says(name, problem, want, *needles):
    detail = expect(name, problem, want)
    for needle in needles:
        check(f"{name} — message says {needle!r}", needle in detail, detail)


# ── A. A decimal literal makes exactness meaningless ─────────────────────────
print("A. decimal literals: tolerant where the arithmetic is binary, exact "
      "where it is not:")

expect("eval 9.4-0.4x at x=20 → 1.4 (the rewritten trend line)",
       {"id": 1, "type": "eval", "expr": "9.4 - 0.4*x", "at": {"x": 20},
        "expected": 1.4}, "PASS")
expect("eval sqrt(d/4.9) at d=78.4 → 4 (the rewritten free-fall model)",
       {"id": 1, "type": "eval", "expr": "sqrt(d/4.9)", "at": {"d": 78.4},
        "expected": 4}, "PASS")
expect("eval 1.2*x at x=6 → 7.2 (the rate rewritten to 1.25)",
       {"id": 1, "type": "eval", "expr": "1.2*x", "at": {"x": 6},
        "expected": 7.2}, "PASS")
expect("eval 1.2*x at x=10 → 12 kept passing (it always did — float luck)",
       {"id": 1, "type": "eval", "expr": "1.2*x", "at": {"x": 10},
        "expected": 12}, "PASS")
expect("solve sqrt(9.8*d)-70 → 500 (the root reported as 499.999999999999)",
       {"id": 1, "type": "solve", "expr": "sqrt(9.8*d) - 70", "var": "d",
        "expected": 500}, "PASS")
expect("series with a float term matches an exact rational",
       {"id": 1, "type": "series", "term": "0.1*n", "from": 1, "to": 3,
        "var": "n", "expected": 0.6}, "PASS")
expect("expand with float coefficients (0.010000000000000002 vs 0.01)",
       {"id": 1, "type": "expand", "expr": "(x+0.1)**2",
        "expected": "x**2 + 0.2*x + 0.01"}, "PASS")
expect("system with decimal coefficients (residual -2.8e-17, not 0)",
       {"id": 1, "type": "system", "equations": ["0.1*x + 0.2*y - 0.5",
                                                 "0.3*x - 0.1*y - 0.1"],
        "vars": ["x", "y"], "expected": {"x": 1, "y": 2}}, "PASS")
expect("distance with decimal coordinates",
       {"id": 1, "type": "distance", "points": [[0, 0], [0.3, 0.4]],
        "expected": 0.5}, "PASS")

print("  … and a wrong answer still fails, decimals or not:")
expect("a wrong decimal answer fails",
       {"id": 1, "type": "eval", "expr": "9.4 - 0.4*x", "at": {"x": 20},
        "expected": 1.8}, "FAIL")
expect("a wrong exact answer fails",
       {"id": 1, "type": "eval", "expr": "(x-1)*(x+2)", "at": {"x": 0},
        "expected": -3}, "FAIL")
expect("a wrong expansion fails even though both sides carry decimals",
       {"id": 1, "type": "expand", "expr": "(x+0.1)**2",
        "expected": "x**2 + 0.2*x + 0.02"}, "FAIL")
expect("an irrational root keyed as a rounded decimal still fails "
       "(a root list has no written precision to round to)",
       {"id": 1, "type": "solve", "expr": "x**2 - 2",
        "expected": [1.41, -1.41]}, "FAIL")
expect("a wrong system solution still fails under decimal coefficients",
       {"id": 1, "type": "system", "equations": ["0.1*x + 0.2*y - 0.5",
                                                 "0.3*x - 0.1*y - 0.1"],
        "vars": ["x", "y"], "expected": {"x": 2, "y": 1}}, "FAIL")

print("  … and the failure message names the COMPARISON, not the key:")
detail = expect("a failing decimal comparison is reported as a real difference",
                {"id": 1, "type": "eval", "expr": "9.4 - 0.4*x",
                 "at": {"x": 20}, "expected": 1.8}, "FAIL")
check("it says decimals were present", "decimal literals present" in detail,
      detail)
check("it says the difference is real", "difference is real" in detail, detail)
check("it prints the expected value AS WRITTEN, not as Rational(7,5)",
      "1.8" in detail and "9/5" not in detail, detail)
detail = expect("an exact failure carries no decimal note",
                {"id": 1, "type": "eval", "expr": "(x-1)*(x+2)",
                 "at": {"x": 0}, "expected": -3}, "FAIL")
check("no decimal note on an exact comparison",
      "decimal literals present" not in detail, detail)

print("  … and the trap gate and the real check now model the same rule:")
expect("a trap inside the problem's own decimal band is still refused",
       {"id": 1, "type": "eval", "expr": "9.4 - 0.4*x", "at": {"x": 20},
        "expected": 1.4,
        "traps": [{"desc": "read the intercept off by a hair",
                   "expr": "9.44 - 0.4*x"}]}, "TRAPFAIL")


# ── B. Symbolic and complex answers ──────────────────────────────────────────
print("\nB. symbolic and complex answers are first-class:")

expect_says("equiv carries traps (x^4·x^3 = x^12 is the classic error)",
            {"id": 1, "type": "equiv", "expr": "x**4*x**3", "expected": "x**7",
             "traps": [{"desc": "multiplied the exponents",
                        "exprs": ["x**12"], "value": ["x**12"]}]},
            "PASS", "multiplied the exponents", "x**12")
expect("expand carries traps (the undistributed outer product)",
       {"id": 1, "type": "expand", "expr": "(x+2)*(x-5)",
        "expected": "x**2 - 3*x - 10",
        "traps": [{"desc": "multiplied first and last only",
                   "exprs": ["x**2 - 10"]}]}, "PASS")
expect("factor carries traps",
       {"id": 1, "type": "factor", "expr": "x**2 - 5*x + 6",
        "expected": "(x-2)*(x-3)",
        "traps": [{"desc": "signs from the sum, not the product",
                   "exprs": ["(x+2)*(x+3)"]}]}, "PASS")
expect_says("a symbolic trap equivalent to the answer is refused",
            {"id": 1, "type": "factor", "expr": "x**2 - 9",
             "expected": "(x-3)*(x+3)",
             "traps": [{"desc": "reordered the factors",
                        "exprs": ["(x+3)*(x-3)"]}]},
            "TRAPFAIL", "EQUIVALENT", "cannot distinguish")
expect("a symbolic trap whose printed form drifts from its exprs is refused",
       {"id": 1, "type": "equiv", "expr": "x**4*x**3", "expected": "x**7",
        "traps": [{"desc": "multiplied the exponents", "exprs": ["x**12"],
                   "value": ["x**43"]}]}, "TRAPFAIL")
expect_says("a scalar 'expr' on a symbolic type is refused, and says so",
            {"id": 1, "type": "equiv", "expr": "x**4*x**3", "expected": "x**7",
             "traps": [{"desc": "multiplied the exponents", "expr": "x**12"}]},
            "INPUT", "'exprs'", "STRING")
expect_says("a numeric list on a symbolic type is refused with the shape",
            {"id": 1, "type": "factor", "expr": "x**2 - 9",
             "expected": "(x-3)*(x+3)",
             "traps": [{"desc": "half-factored", "exprs": [3]}]},
            "INPUT", "LIST of expression STRINGS")

expect("a complex trap 'value' can be declared",
       {"id": 1, "type": "eval", "expr": "(2+I)*(1-2*I)", "at": {"x": 0},
        "expected": "4 - 3*I",
        "traps": [{"desc": "treated i^2 as +1", "expr": "2 - 4*I + I - 2",
                   "value": "-3*I"}]}, "PASS")
expect("a complex trap 'value' that drifts from its expr is still refused",
       {"id": 1, "type": "eval", "expr": "(2+I)*(1-2*I)", "at": {"x": 0},
        "expected": "4 - 3*I",
        "traps": [{"desc": "treated i^2 as +1", "expr": "2 - 4*I + I - 2",
                   "value": "1 - 3*I"}]}, "TRAPFAIL")
expect_says("a trap 'value' that is neither number nor string is refused",
            {"id": 1, "type": "approx", "expr": "9*tan(35*pi/180)",
             "expected": 6.30, "tol": 0.01,
             "traps": [{"desc": "used cos", "expr": "9*cos(35*pi/180)",
                        "value": {"re": 7}}]},
            "INPUT", "plain number, or a string")

expect_says("a literal equation solves for var in terms of the other symbols",
            {"id": 1, "type": "solve", "expr": "x*y - 5", "var": "y",
             "expected": "5/x"},
            "PASS", "in terms of x", "literal equation")
expect("a literal equation with a decidable real root works too",
       {"id": 1, "type": "solve", "expr": "3*y - 7 - x", "var": "y",
        "expected": "(x+7)/3"}, "PASS")
expect("a wrong inverse still fails",
       {"id": 1, "type": "solve", "expr": "3*y - 7 - x", "var": "y",
        "expected": "(x-7)/3"}, "FAIL")
expect_says("non-real roots in ONE variable still force a domain declaration",
            {"id": 1, "type": "solve", "expr": "x**4 - 1", "expected": [1, -1]},
            "FAIL", "non-real roots")


# ── C. Answers the schema could not express ──────────────────────────────────
print("\nC. answers that are not values:")

expect_says("an identity is an identity, not an empty solution set",
            {"id": 1, "type": "solve", "expr": "2*(x+3) - 2*x - 6",
             "expected": []},
            "FAIL", "IDENTITY", "[] for an identity AND for a contradiction")
expect('an identity keyed "all real numbers" passes',
       {"id": 1, "type": "solve", "expr": "2*(x+3) - 2*x - 6",
        "expected": "all real numbers"}, "PASS")
expect_says("a contradiction keyed [] passes and is named",
            {"id": 1, "type": "solve", "expr": "2*(x+3) - 2*x - 7",
             "expected": []}, "PASS", "CONTRADICTION")
expect('a contradiction keyed "no solution" passes',
       {"id": 1, "type": "solve", "expr": "2*(x+3) - 2*x - 7",
        "expected": "no solution"}, "PASS")
expect_says('"no solution" on an equation that HAS roots fails',
            {"id": 1, "type": "solve", "expr": "x**2 - 4",
             "expected": "no solution"},
            "FAIL", "not constant")

expect_says("a dependent system can say infinitely many",
            {"id": 1, "type": "system", "equations": ["x - y", "2*x - 2*y"],
             "vars": ["x", "y"], "expected": "infinitely many"},
            "PASS", "infinitely many")
expect("an inconsistent system keyed [] still passes",
       {"id": 1, "type": "system", "equations": ["x + y - 1", "x + y - 3"],
        "vars": ["x", "y"], "expected": []}, "PASS")
expect_says("a determinate system keyed 'infinitely many' fails",
            {"id": 1, "type": "system", "equations": ["x + y - 5", "x - y - 1"],
             "vars": ["x", "y"], "expected": "infinitely many"},
            "FAIL", "exactly 1")
expect_says("an unknown system 'expected' string teaches the four shapes",
            {"id": 1, "type": "system", "equations": ["x + y - 5"],
             "vars": ["x", "y"], "expected": "dunno"},
            "INPUT", "infinitely many")

expect_says("a divergent integral is reported as divergent",
            {"id": 1, "type": "definite_integral", "expr": "1/x**2",
             "from": 0, "to": 3, "expected": "oo"}, "PASS", "DIVERGES")
expect_says("a divergent integral keyed with a finite value fails",
            {"id": 1, "type": "definite_integral", "expr": "1/x**2",
             "from": 0, "to": 3, "expected": 9},
            "FAIL", "does not converge")
expect("an absolute-value integrand integrates through its corner",
       {"id": 1, "type": "definite_integral", "expr": "Abs(t**2-4)",
        "var": "t", "from": 0, "to": 3, "expected": "23/3"}, "PASS")
expect("and a wrong value for it still fails",
       {"id": 1, "type": "definite_integral", "expr": "Abs(t**2-4)",
        "var": "t", "from": 0, "to": 3, "expected": 5}, "FAIL")
expect("a genuinely non-convergent quadrature is still MANUAL",
       {"id": 1, "type": "definite_integral", "expr": "sin(exp(x))",
        "from": 0, "to": 8, "expected": 0.3, "tol": 1e-4}, "MANUAL")

expect_says("a decimal endpoint ABOVE 2*pi no longer pulls the root at 2*pi "
            "inside the interval, and the report says it was read as 2*pi",
            {"id": 1, "type": "solve_interval", "expr": "sin(t)", "var": "t",
             "interval": [0, 6.2832], "expected": [0, "pi"]},
            "PASS", "read as 2*pi", "write it exactly")
expect("a decimal endpoint BELOW 2*pi no longer drops a root just under it",
       {"id": 1, "type": "solve_interval", "expr": "sin(t) - 1", "var": "t",
        "interval": ["-2*pi", 6.2831], "expected": ["pi/2", "-3*pi/2"]}, "PASS")
expect("an ordinary decimal endpoint is left alone",
       {"id": 1, "type": "solve_interval", "expr": "t - 1", "var": "t",
        "interval": [0, 2.5], "expected": [1]}, "PASS")
expect("the exact endpoint works",
       {"id": 1, "type": "solve_interval", "expr": "sin(t)", "var": "t",
        "interval": [0, "2*pi"], "expected": [0, "pi"]}, "PASS")
expect("a degree-mode interval is untouched by that rule",
       {"id": 1, "type": "solve_interval", "expr": "2*sin(t) - 1", "var": "t",
        "interval": [0, 360], "unit": "deg", "expected": [30, 150]}, "PASS")

expect_says("read_data 'difference' names the field and the pair rule",
            {"id": 1, "type": "read_data", "data": {"Thu": 3, "Fri": 5},
             "query": "difference", "key": "Fri", "expected": 2},
            "INPUT", "two-element list", "Fri")
expect("the pair form works",
       {"id": 1, "type": "read_data", "data": {"Thu": 3, "Fri": 5},
        "query": "difference", "key": ["Fri", "Thu"], "expected": 2}, "PASS")
expect_says("a 'value' query with no key names the field",
            {"id": 1, "type": "read_data", "data": {"Thu": 3, "Fri": 5},
             "query": "value", "expected": 3}, "INPUT", '"key"')
expect_says("a 'value' query with a key that is not in the data says so",
            {"id": 1, "type": "read_data", "data": {"Thu": 3, "Fri": 5},
             "query": "value", "key": "Sat", "expected": 3},
            "INPUT", "not a category")


# ── An equiv answer may be written as the equation the student writes ────────
# The bank printed "(x-3)^2 + (y+5)^2 - 16" on a sheet asking for centre-radius
# form: faithful to the JSON and still a subtraction where the student wrote an
# equation. Splitting the trailing constant off when printing was measured and
# rejected — 253 of the corpus's 479 equiv answers carry a bare numeric term and
# nearly all are plain simplifications that would be corrupted into equations.
# The author declares it instead.
print("\nequiv accepts the equation form, on both sides:")

CIRCLE = "x**2 + y**2 - 6*x + 10*y + 18"
expect("centre-radius keyed as an equation → PASS",
       {"id": 1, "type": "equiv", "expr": CIRCLE,
        "expected": "(x-3)**2 + (y+5)**2 = 16"}, "PASS")
expect("the same equation with the wrong radius still FAILs",
       {"id": 1, "type": "equiv", "expr": CIRCLE,
        "expected": "(x-3)**2 + (y+5)**2 = 25"}, "FAIL")
expect("expr may be an equation too",
       {"id": 1, "type": "equiv", "expr": "x**2 + y**2 - 6*x + 10*y = -18",
        "expected": "(x-3)**2 + (y+5)**2 = 16"}, "PASS")
expect("a vertex-form answer is an EXPRESSION and is untouched",
       {"id": 1, "type": "equiv", "expr": "x**2 + 6*x + 5",
        "expected": "(x+3)**2 - 4"}, "PASS")
expect("a JSON-number expected still parses (10 corpus entries key equiv to an int)",
       {"id": 1, "type": "equiv", "expr": "25 + 5*w - (18 + 5*w)",
        "expected": 7}, "PASS")

expect_says("'=' on a type that is not equiv names the schema rule, not a typo",
            {"id": 1, "type": "solve", "expr": "x = 5", "expected": [5]},
            "INPUT", "only the 'equiv' type accepts")
expect_says("two '=' signs are rejected",
            {"id": 1, "type": "equiv", "expr": "x**2",
             "expected": "y = x = 2"},
            "INPUT", "more than one '='")
expect_says("an empty side is rejected",
            {"id": 1, "type": "equiv", "expr": "x**2", "expected": "x**2 ="},
            "INPUT", "empty side")

ok, info = verify.check_traps(
    {"id": 1, "type": "equiv", "expr": CIRCLE,
     "expected": "(x-3)**2 + (y+5)**2 = 16",
     "traps": [{"desc": "did not balance the completed square",
                "exprs": ["(x-3)**2 + (y+5)**2 = 18"]}]})
check("a trap may be an equation too", ok)

# The bank is the artifact this exists for: it must print the equation.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import render_quick_answers as _bank   # noqa: E402
check("the answer bank prints the equation, not the =0 rearrangement",
      _bank._fmt("(x-3)**2 + (y+5)**2 = 16", "equiv").endswith("= 16$"))
check("an expression answer is still printed as an expression",
      "=" not in _bank._fmt("(x+3)**2 - 4", "equiv"))


# ── Defensive branches in the comparison layer ───────────────────────────────
# These are the fallbacks that keep a malformed key producing a VERDICT rather
# than a traceback. They are unreachable from any well-formed problem, which is
# exactly why they need direct tests: a crash here takes down a whole build on
# input the schema layer is supposed to have already rejected.
print("\nthe comparison layer degrades instead of crashing:")

check("a trailing disallowed character is named, not swallowed",
      _raises_input(lambda: verify.safe_parse("2 + 3 @")))
# _written_precision returns the VALUE when the key is a plain written decimal,
# and None when it has no written precision to read — "23/3" and "sqrt(3)/2"
# are exact, and handing either to a rounding comparison would invent a
# precision the author never wrote.
check("a key with no written precision reads as None",
      verify._written_precision("no solution") is None)
check("a symbolic key has no written precision either",
      verify._written_precision("sqrt(3)/2") is None)
check("a written decimal reads back as its value",
      verify._written_precision("1.400") == 1.4)
check("an exact Rational rounds to the decimal it was written as",
      verify.rounds_to(sympy.Rational(7, 5), "1.4"))
check("and does not round to a different written value",
      not verify.rounds_to(sympy.Rational(7, 5), "1.5"))

# carries_decimal walks containers, because an expected value may be a list
# (roots), a dict (a system's solution) or a bare string.
check("carries_decimal sees a decimal inside a list",
      verify.carries_decimal([sympy.Float("1.5"), sympy.Integer(2)]))
check("carries_decimal sees a decimal inside a dict",
      verify.carries_decimal({"x": sympy.Float("0.25")}))
check("carries_decimal is False when every part is exact",
      not verify.carries_decimal([sympy.Rational(1, 2), sympy.Integer(3)]))

# relative_equal is the last line before a verdict: infinities and NaN have no
# meaningful difference, so they compare structurally.
check("relative_equal compares infinities structurally",
      verify.relative_equal(sympy.oo, sympy.oo))
check("relative_equal rejects opposite infinities",
      not verify.relative_equal(sympy.oo, -sympy.oo))


# ── The shipped documentation is generated from the enforced rules ───────────
print("\n--schema states every shape that was reported as undocumented:")
import io               # noqa: E402
import contextlib       # noqa: E402

buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    verify.print_schema("table")
schema = buf.getvalue()
for needle, why in [
        ("LIST of expression STRINGS", "solution-set trap exprs shape"),
        ('["5", "-2"], NOT [5, -2]', "the exact rejection five reports hit"),
        ("wrong REWRITTEN FORM", "symbolic trap shape"),
        ("STRING for a value a number cannot hold", "complex trap value"),
        ("all real numbers", "identity as an answer"),
        ("infinitely many", "dependent system as an answer"),
        ("Decimal literals", "the comparison rule itself")]:
    check(f"--schema documents {why}", needle in schema)

print()
if FAILS:
    print(f"❌ {len(FAILS)} verify comparison test(s) failed: {FAILS}")
    sys.exit(1)
print("✅ All numeric/symbolic comparison tests passed")
