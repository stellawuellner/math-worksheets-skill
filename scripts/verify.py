#!/usr/bin/env python3
"""
verify.py — Static SymPy verification for math worksheets.

Reads a structured JSON file of problems and answers. No user-generated
code is ever executed: every expression string is validated against a
strict token allowlist BEFORE it reaches the parser, so only numbers,
whitelisted function/variable names, and arithmetic operators are accepted.
Anything else (attribute access, underscores, quotes, brackets, unknown
identifiers) is rejected as a hard failure.

Input format: verify_TOPIC_DATE.json
  {
    "topic": "graphing polynomials",
    "problems": [
      {"id": 1, "type": "solve",  "expr": "x**2 - 5*x + 6",     "expected": [2, 3]},
      {"id": 2, "type": "factor", "expr": "x**2 - 7*x + 12",    "expected": "(x - 3)*(x - 4)"},
      {"id": 3, "type": "eval",   "expr": "(x-1)*(x+2)", "at": {"x": 0}, "expected": -2},
      {"id": 4, "type": "zeros",  "expr": "x*(x-3)**2",          "expected": [0, 3]},
      {"id": 5, "type": "expand", "expr": "(x+2)**3",            "expected": "x**3 + 6*x**2 + 12*x + 8"},
      {"id": 6, "type": "diff",   "expr": "x**3 - 4*x",          "expected": "3*x**2 - 4"},
      {"id": 7, "type": "integrate", "expr": "6*x**2",           "expected": "2*x**3"},
      {"id": 8, "type": "limit",  "expr": "sin(x)/x", "to": 0,   "expected": 1},
      {"id": 9, "type": "equiv",  "expr": "sin(x)**2 + cos(x)**2", "expected": "1"},
      {"id": 10, "type": "solve_interval", "expr": "2*sin(t) - 1", "var": "t",
                 "interval": [0, "2*pi"], "expected": ["pi/6", "5*pi/6"]},
      {"id": 11, "type": "manual", "desc": "Graph sketch — verify visually"}
    ]
  }

Supported types:
  solve          — solves expr=0 for var (default x), checks roots match expected list
  zeros          — like solve but duplicates collapse (multiplicity ignored)
  factor         — checks expected is equivalent to expr (form given factored)
  expand         — checks expected is equivalent to expr (form given expanded)
  eval           — evaluates expr at given variable values, checks result
  diff           — differentiates expr (optional "order", default 1), checks match
  integrate      — checks d/dvar(expected) == expr (omit the +C constant)
  limit          — limit of expr as var → "to"; optional "dir": "+", "-", "+-" (default)
  equiv          — checks expr and expected are the same function (trig identities etc.)
  solve_interval — solves expr=0 on [a, b) given as "interval": [a, b];
                   optional "unit": "deg" (interval and expected in degrees)
  approx         — numeric expr recomputed exactly, compared within "tol" (default 0.01)
  distance       — distance between two "points" [[x1,y1],[x2,y2]]; optional "tol"
  midpoint       — midpoint of two points; expected is an [x, y] pair
  slope          — slope through two points; expected value or "undefined"; optional "tol"
  polygon_area   — shoelace area of ≥3 "points" in order; optional "tol"
  triangle       — solve a triangle from 3 givens (sides a/b/c, angles A/B/C,
                   side a opposite angle A); checks "solve_for" against expected
                   within "tol" (default 0.01); "unit": "deg" (default) or "rad";
                   handles the ambiguous SSA case (accepts either triangle)
  manual         — flagged for human review, never fails automatically

Optional per-problem fields: "var" (default "x"), "note" (free text, ignored).
Unknown types or unknown/missing fields are HARD FAILURES — a typo must
never silently skip verification.

Exit codes:
  0 — all automated checks passed
  1 — one or more checks FAILED (fix answer key before compiling)
  2 — no failures, but some problems need manual review
"""

import cmath
import itertools
import json
import math
import os
import re
import sys

import sympy
from sympy import Symbol, simplify, trigsimp, nsimplify


class VerifyInputError(Exception):
    """Raised when the JSON input is malformed or an expression is disallowed."""


# ── Expression allowlist ──────────────────────────────────────────────────────
# Only these names may appear in expressions. Everything maps to a fixed sympy
# object, so a validated string can only ever build a mathematical expression.

_FUNCS = {name: getattr(sympy, name) for name in [
    "sin", "cos", "tan", "asin", "acos", "atan",
    "sec", "csc", "cot",
    "sinh", "cosh", "tanh", "asinh", "acosh", "atanh",
    "log", "ln", "exp", "sqrt", "Abs", "floor", "ceiling",
]}
_FUNCS["abs"] = sympy.Abs

_CONSTS = {"pi": sympy.pi, "E": sympy.E, "oo": sympy.oo}

# real=True matches the K-12/AP domain and lets Abs/ln/sqrt derivatives
# simplify (complex-root problems are out of allowlist scope — use manual)
_VARS = {v: Symbol(v, real=True) for v in
         "x y z t u v w a b c h k m n r s theta phi".split()}

_ALLOWED_NAMES = set(_FUNCS) | set(_CONSTS) | set(_VARS)
_SYMPY_LOCALS = {**_FUNCS, **_CONSTS, **_VARS}

# Tokens: numbers, names, ** or ^, arithmetic operators, parens, commas, space.
_TOKEN_RE = re.compile(r"\d+(?:\.\d+)?|[A-Za-z]+|\*\*|[+\-*/(),^]|\s+")

_MAX_EXPR_LEN = 500


def safe_parse(expr_str):
    """Validate expr_str against the token allowlist, then parse with sympy.

    Raises VerifyInputError on any disallowed character or name. Because the
    string is guaranteed to contain only numbers, whitelisted names, and
    arithmetic tokens, the subsequent sympify cannot execute anything.
    """
    if not isinstance(expr_str, str):
        raise VerifyInputError(
            f"expression must be a string, got {type(expr_str).__name__}")
    if len(expr_str) > _MAX_EXPR_LEN:
        raise VerifyInputError(f"expression longer than {_MAX_EXPR_LEN} chars")

    pos = 0
    names = []
    for m in _TOKEN_RE.finditer(expr_str):
        if m.start() != pos:
            raise VerifyInputError(
                f"disallowed character {expr_str[pos]!r} in {expr_str!r}")
        tok = m.group()
        if tok[0].isalpha():
            names.append(tok)
        pos = m.end()
    if pos != len(expr_str):
        raise VerifyInputError(
            f"disallowed character {expr_str[pos]!r} in {expr_str!r}")

    for name in names:
        if name not in _ALLOWED_NAMES:
            raise VerifyInputError(
                f"name {name!r} is not an allowed function or variable")

    normalized = expr_str.replace("^", "**")
    try:
        return sympy.sympify(normalized, locals=_SYMPY_LOCALS)
    except Exception as e:
        raise VerifyInputError(f"could not parse {expr_str!r}: {e}")


def parse_value(value):
    """Parse an expected value: JSON number → exact Rational, string → expr."""
    if isinstance(value, bool):
        raise VerifyInputError("booleans are not valid expected values")
    if isinstance(value, (int, float)):
        return nsimplify(value)
    if isinstance(value, str):
        return safe_parse(value)
    raise VerifyInputError(
        f"expected value must be a number or string, got {type(value).__name__}")


def parse_value_list(value):
    if not isinstance(value, list):
        value = [value]
    return [parse_value(v) for v in value]


# ── Equivalence checking ──────────────────────────────────────────────────────

_SAMPLES = [-2.31, -1.17, -0.53, 0.47, 1.23, 2.11, 3.07]


def _sample_points(free):
    if not free:
        return [()]
    if len(free) <= 2:
        return list(itertools.product(_SAMPLES, repeat=len(free)))
    return [tuple(_SAMPLES[(i + 2 * j) % len(_SAMPLES)]
                  for j in range(len(free)))
            for i in range(len(_SAMPLES))]


def numeric_equal(a, b, tol=1e-9):
    """Deterministic numeric spot-check at fixed sample points."""
    free = sorted(set(a.free_symbols) | set(b.free_symbols), key=str)
    valid = 0
    for point in _sample_points(free):
        subs = dict(zip(free, point))
        try:
            av = complex(sympy.N(a.subs(subs), 15))
            bv = complex(sympy.N(b.subs(subs), 15))
        except (TypeError, ValueError, ZeroDivisionError):
            continue
        if not (cmath.isfinite(av) and cmath.isfinite(bv)):
            continue
        if abs(av - bv) > tol * max(1.0, abs(av), abs(bv)):
            return False
        valid += 1
        if valid >= 6:
            return True
    return valid >= 3


def sym_equal(a, b):
    """True if a and b are the same function: symbolic first, numeric fallback."""
    if a == b:  # structural equality — also covers infinities, where a-b is nan
        return True
    try:
        d = simplify(a - b)
        if d == 0:
            return True
        if trigsimp(d) == 0:
            return True
    except Exception:
        pass
    return numeric_equal(a, b)


def multiset_equal(computed, expected):
    if len(computed) != len(expected):
        return False
    remaining = list(computed)
    for e in expected:
        for i, c in enumerate(remaining):
            if sym_equal(c, e):
                remaining.pop(i)
                break
        else:
            return False
    return True


def dedupe(values):
    unique = []
    for v in values:
        if not any(sym_equal(v, u) for u in unique):
            unique.append(v)
    return unique


def approx_equal(computed, expected, tol):
    try:
        c = float(sympy.N(computed, 15))
        e = float(sympy.N(expected, 15))
    except (TypeError, ValueError):
        return False
    return abs(c - e) <= tol


def get_tol(p, default=None):
    """Validated tolerance; None means exact comparison is required."""
    tol = p.get("tol", default)
    if tol is None:
        return None
    if isinstance(tol, bool) or not isinstance(tol, (int, float)) or tol <= 0:
        raise VerifyInputError("'tol' must be a positive number")
    return float(tol)


def compare_value(computed, expected, tol):
    """Exact symbolic comparison, or numeric within tol when tol is given."""
    if tol is None:
        return sym_equal(computed, expected)
    return approx_equal(computed, expected, tol)


def parse_points(raw, exactly=None, at_least=None):
    if not isinstance(raw, list):
        raise VerifyInputError("'points' must be a list of [x, y] pairs")
    if exactly is not None and len(raw) != exactly:
        raise VerifyInputError(f"'points' must contain exactly {exactly} points")
    if at_least is not None and len(raw) < at_least:
        raise VerifyInputError(f"'points' must contain at least {at_least} points")
    points = []
    for pt in raw:
        if not isinstance(pt, list) or len(pt) != 2:
            raise VerifyInputError("each point must be an [x, y] pair")
        points.append((parse_value(pt[0]), parse_value(pt[1])))
    return points


def get_unit(p, default):
    unit = p.get("unit", default)
    if unit not in ("deg", "rad"):
        raise VerifyInputError("'unit' must be 'deg' or 'rad'")
    return unit


# ── Triangle solver (law of sines / law of cosines, in fixed code) ────────────
# Convention: sides a, b, c are opposite angles A, B, C. Angles in radians
# internally. Returns a list of solutions (SSA can yield 0, 1, or 2).

_OPP = {"a": "A", "b": "B", "c": "C"}
_SIDE_OF = {v: k for k, v in _OPP.items()}


def _clamp(x):
    return max(-1.0, min(1.0, x))


def _angles_from_sides(sides):
    a, b, c = sides["a"], sides["b"], sides["c"]
    if a + b <= c or a + c <= b or b + c <= a:
        return None
    A = math.acos(_clamp((b * b + c * c - a * a) / (2 * b * c)))
    B = math.acos(_clamp((a * a + c * c - b * b) / (2 * a * c)))
    return {**sides, "A": A, "B": B, "C": math.pi - A - B}


def solve_triangle(sides, angles):
    """sides/angles: dicts of known values (angles in radians) → solution list."""
    if len(sides) + len(angles) != 3 or not sides:
        raise VerifyInputError(
            "'given' must contain exactly 3 values including at least one side")
    for k, v in sides.items():
        if v <= 0:
            raise VerifyInputError(f"side {k!r} must be positive")
    for k, v in angles.items():
        if not 0 < v < math.pi:
            raise VerifyInputError(f"angle {k!r} must be strictly between 0° and 180°")

    if len(sides) == 3:  # SSS
        sol = _angles_from_sides(sides)
        return [sol] if sol else []

    if len(sides) == 2:
        (ang_name, ang_val), = angles.items()
        missing = ({"a", "b", "c"} - set(sides)).pop()
        if _OPP[missing] == ang_name:  # SAS — angle included between known sides
            p_, q_ = sides.values()
            third = math.sqrt(p_ * p_ + q_ * q_ - 2 * p_ * q_ * math.cos(ang_val))
            sol = _angles_from_sides({**sides, missing: third})
            return [sol] if sol else []
        # SSA — known angle is opposite one of the known sides; may be ambiguous
        opp_side = _SIDE_OF[ang_name]
        if opp_side not in sides:
            raise VerifyInputError(
                f"angle {ang_name!r} must be opposite a given side or the missing side")
        other = (set(sides) - {opp_side}).pop()
        sin2 = sides[other] * math.sin(ang_val) / sides[opp_side]
        if sin2 > 1 + 1e-12:
            return []
        sin2 = min(sin2, 1.0)
        candidates = [math.asin(sin2)]
        if 1.0 - sin2 > 1e-12:
            candidates.append(math.pi - candidates[0])
        solutions = []
        for ang2 in candidates:
            third_ang = math.pi - ang_val - ang2
            if third_ang <= 1e-12:
                continue
            ratio = sides[opp_side] / math.sin(ang_val)
            third_ang_name = ({"A", "B", "C"} - {ang_name, _OPP[other]}).pop()
            solutions.append({
                **sides,
                _SIDE_OF[third_ang_name]: ratio * math.sin(third_ang),
                ang_name: ang_val,
                _OPP[other]: ang2,
                third_ang_name: third_ang,
            })
        return solutions

    # one side, two angles (ASA / AAS)
    (side_name, side_val), = sides.items()
    third_ang = math.pi - sum(angles.values())
    if third_ang <= 1e-12:
        return []
    missing_ang = ({"A", "B", "C"} - set(angles)).pop()
    all_angles = {**angles, missing_ang: third_ang}
    ratio = side_val / math.sin(all_angles[_OPP[side_name]])
    return [{
        "A": all_angles["A"], "B": all_angles["B"], "C": all_angles["C"],
        "a": ratio * math.sin(all_angles["A"]),
        "b": ratio * math.sin(all_angles["B"]),
        "c": ratio * math.sin(all_angles["C"]),
    }]


# ── Schema validation ─────────────────────────────────────────────────────────
# type → (required fields, optional fields). "id", "type", "note" always allowed.

SCHEMAS = {
    "solve":          ({"expr", "expected"}, {"var"}),
    "zeros":          ({"expr", "expected"}, {"var"}),
    "factor":         ({"expr", "expected"}, set()),
    "expand":         ({"expr", "expected"}, set()),
    "eval":           ({"expr", "at", "expected"}, set()),
    "diff":           ({"expr", "expected"}, {"var", "order"}),
    "integrate":      ({"expr", "expected"}, {"var"}),
    "limit":          ({"expr", "to", "expected"}, {"var", "dir"}),
    "equiv":          ({"expr", "expected"}, set()),
    "solve_interval": ({"expr", "interval", "expected"}, {"var", "unit"}),
    "approx":         ({"expr", "expected"}, {"tol"}),
    "distance":       ({"points", "expected"}, {"tol"}),
    "midpoint":       ({"points", "expected"}, set()),
    "slope":          ({"points", "expected"}, {"tol"}),
    "polygon_area":   ({"points", "expected"}, {"tol"}),
    "triangle":       ({"given", "solve_for", "expected"}, {"tol", "unit"}),
    "manual":         ({"desc"}, set()),
}


def check_schema(p):
    if not isinstance(p, dict):
        raise VerifyInputError("each problem must be a JSON object")
    if "id" not in p:
        raise VerifyInputError("problem is missing required field 'id'")
    ptype = p.get("type")
    if ptype not in SCHEMAS:
        raise VerifyInputError(
            f"unknown problem type {ptype!r} — allowed types: {sorted(SCHEMAS)}")
    required, optional = SCHEMAS[ptype]
    fields = set(p) - {"id", "type", "note"}
    missing = required - fields
    if missing:
        raise VerifyInputError(
            f"type {ptype!r} is missing required field(s): {sorted(missing)}")
    unknown = fields - required - optional
    if unknown:
        raise VerifyInputError(
            f"type {ptype!r} has unknown field(s): {sorted(unknown)}")
    return ptype


def get_var(p):
    v = p.get("var", "x")
    if v not in _VARS:
        raise VerifyInputError(
            f"variable {v!r} is not allowed — use one of: {sorted(_VARS)}")
    return _VARS[v]


# ── Per-type checks ───────────────────────────────────────────────────────────

def check_problem(p, ptype):
    """Returns (status, detail) where status is PASS/FAIL/MANUAL."""

    if ptype == "manual":
        return ("MANUAL", p["desc"])

    if ptype == "distance":
        (x1, y1), (x2, y2) = parse_points(p["points"], exactly=2)
        computed = sympy.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        expected = parse_value(p["expected"])
        ok = compare_value(computed, expected, get_tol(p))
        return ("PASS" if ok else "FAIL",
                f"distance{tuple(p['points'])} → {computed} (expected {p['expected']})")

    if ptype == "midpoint":
        (x1, y1), (x2, y2) = parse_points(p["points"], exactly=2)
        if not isinstance(p["expected"], list) or len(p["expected"]) != 2:
            raise VerifyInputError("midpoint 'expected' must be an [x, y] pair")
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ex, ey = parse_value(p["expected"][0]), parse_value(p["expected"][1])
        ok = sym_equal(mx, ex) and sym_equal(my, ey)
        return ("PASS" if ok else "FAIL",
                f"midpoint{tuple(p['points'])} → ({mx}, {my}) (expected {p['expected']})")

    if ptype == "slope":
        (x1, y1), (x2, y2) = parse_points(p["points"], exactly=2)
        expected_raw = p["expected"]
        vertical = sym_equal(x1, x2)
        wants_undefined = (isinstance(expected_raw, str)
                           and expected_raw.strip().lower() == "undefined")
        if vertical or wants_undefined:
            ok = vertical and wants_undefined
            return ("PASS" if ok else "FAIL",
                    f"slope{tuple(p['points'])} → "
                    f"{'undefined' if vertical else (y2 - y1) / (x2 - x1)} "
                    f"(expected {expected_raw})")
        computed = (y2 - y1) / (x2 - x1)
        ok = compare_value(computed, parse_value(expected_raw), get_tol(p))
        return ("PASS" if ok else "FAIL",
                f"slope{tuple(p['points'])} → {computed} (expected {expected_raw})")

    if ptype == "polygon_area":
        pts = parse_points(p["points"], at_least=3)
        shoelace = sum(pts[i][0] * pts[(i + 1) % len(pts)][1]
                       - pts[(i + 1) % len(pts)][0] * pts[i][1]
                       for i in range(len(pts)))
        computed = sympy.Abs(shoelace) / 2
        expected = parse_value(p["expected"])
        ok = compare_value(computed, expected, get_tol(p))
        return ("PASS" if ok else "FAIL",
                f"polygon_area({len(pts)} points) → {computed} "
                f"(expected {p['expected']})")

    if ptype == "triangle":
        given = p["given"]
        if not isinstance(given, dict):
            raise VerifyInputError("'given' must be an object like {\"a\": 7, \"C\": 34}")
        unknown_keys = set(given) - {"a", "b", "c", "A", "B", "C"}
        if unknown_keys:
            raise VerifyInputError(
                f"unknown 'given' key(s) {sorted(unknown_keys)} — use sides a/b/c "
                "and angles A/B/C (side a is opposite angle A)")
        unit = get_unit(p, default="deg")
        to_rad = (math.radians if unit == "deg" else float)
        sides = {k: float(sympy.N(parse_value(given[k])))
                 for k in ("a", "b", "c") if k in given}
        angles = {k: to_rad(float(sympy.N(parse_value(given[k]))))
                  for k in ("A", "B", "C") if k in given}
        solve_for = p["solve_for"]
        if solve_for not in ("a", "b", "c", "A", "B", "C"):
            raise VerifyInputError("'solve_for' must be one of a, b, c, A, B, C")
        if solve_for in given:
            raise VerifyInputError(f"'solve_for' {solve_for!r} is already given")
        solutions = solve_triangle(sides, angles)
        if not solutions:
            return ("FAIL", f"givens {given} do not form a valid triangle")
        candidates = [sol[solve_for] for sol in solutions]
        if solve_for in ("A", "B", "C") and unit == "deg":
            candidates = [math.degrees(v) for v in candidates]
        tol = get_tol(p, default=0.01)
        expected = float(sympy.N(parse_value(p["expected"])))
        ok = any(abs(c - expected) <= tol for c in candidates)
        shown = ", ".join(f"{c:.4f}" for c in candidates)
        ambiguous = (" — ambiguous SSA case, two triangles exist"
                     if len(solutions) > 1 else "")
        return ("PASS" if ok else "FAIL",
                f"triangle {given} → {solve_for} ∈ [{shown}] "
                f"(expected {p['expected']}, tol {tol}{ambiguous})")

    expr = safe_parse(p["expr"])

    if ptype == "approx":
        if expr.free_symbols:
            raise VerifyInputError(
                "approx 'expr' must be fully numeric (no variables) — "
                f"found {sorted(map(str, expr.free_symbols))}")
        tol = get_tol(p, default=0.01)
        expected = parse_value(p["expected"])
        ok = approx_equal(expr, expected, tol)
        return ("PASS" if ok else "FAIL",
                f"approx({p['expr']}) → {float(sympy.N(expr, 15)):.6g} "
                f"(expected {p['expected']}, tol {tol})")

    if ptype in ("solve", "zeros"):
        var = get_var(p)
        roots = sympy.solve(expr, var)
        expected = parse_value_list(p["expected"])
        if ptype == "zeros":
            roots = dedupe(roots)
            expected = dedupe(expected)
        ok = multiset_equal(roots, expected)
        return ("PASS" if ok else "FAIL",
                f"{ptype}({p['expr']}) → {roots} (expected {expected})")

    if ptype in ("factor", "expand", "equiv"):
        expected = parse_value(p["expected"])
        ok = sym_equal(expr, expected)
        return ("PASS" if ok else "FAIL",
                f"{ptype}({p['expr']}) ≟ {p['expected']}")

    if ptype == "eval":
        if not isinstance(p["at"], dict) or not p["at"]:
            raise VerifyInputError("'at' must be a non-empty object of var: value")
        subs = {}
        for name, val in p["at"].items():
            if name not in _VARS:
                raise VerifyInputError(f"variable {name!r} in 'at' is not allowed")
            subs[_VARS[name]] = parse_value(val)
        result = expr.subs(subs)
        expected = parse_value(p["expected"])
        ok = sym_equal(result, expected)
        return ("PASS" if ok else "FAIL",
                f"eval({p['expr']} at {p['at']}) → {result} (expected {expected})")

    if ptype == "diff":
        var = get_var(p)
        order = p.get("order", 1)
        if not isinstance(order, int) or not 1 <= order <= 6:
            raise VerifyInputError("'order' must be an integer between 1 and 6")
        derivative = sympy.diff(expr, var, order)
        expected = parse_value(p["expected"])
        ok = sym_equal(derivative, expected)
        return ("PASS" if ok else "FAIL",
                f"d^{order}/d{var}^{order}({p['expr']}) → {derivative} "
                f"(expected {expected})")

    if ptype == "integrate":
        # Verified in reverse: d/dvar(expected antiderivative) must equal the
        # integrand. Robust to form differences; omit the +C constant.
        var = get_var(p)
        expected = parse_value(p["expected"])
        back = sympy.diff(expected, var)
        ok = sym_equal(back, expr)
        return ("PASS" if ok else "FAIL",
                f"d/d{var}({p['expected']}) → {back} (integrand {p['expr']})")

    if ptype == "limit":
        var = get_var(p)
        to = parse_value(p["to"])
        direction = p.get("dir", "+-")
        if direction not in ("+", "-", "+-"):
            raise VerifyInputError("'dir' must be '+', '-', or '+-'")
        value = sympy.limit(expr, var, to, dir=direction)
        expected = parse_value(p["expected"])
        ok = sym_equal(value, expected)
        return ("PASS" if ok else "FAIL",
                f"limit({p['expr']}, {var}→{p['to']}, dir={direction}) → {value} "
                f"(expected {expected})")

    if ptype == "solve_interval":
        var = get_var(p)
        interval = p["interval"]
        if not isinstance(interval, list) or len(interval) != 2:
            raise VerifyInputError("'interval' must be a two-element list [a, b]")
        lo, hi = parse_value(interval[0]), parse_value(interval[1])
        expected = parse_value_list(p["expected"])
        # In degree mode the interval and expected roots are degrees; solve in
        # radians and convert, so pi/6 compares exactly against 30.
        unit = get_unit(p, default="rad")
        if unit == "deg":
            scale = sympy.pi / 180
            lo, hi = lo * scale, hi * scale
            expected = [e * scale for e in expected]
        domain = sympy.Interval(lo, hi, left_open=False, right_open=True)
        def in_unit(values):  # display roots in the unit the problem uses
            if unit == "deg":
                return [sympy.nsimplify(v * 180 / sympy.pi) for v in values]
            return values

        solset = sympy.solveset(expr, var, domain=domain)
        if solset is sympy.S.EmptySet:
            computed = []
        elif isinstance(solset, sympy.FiniteSet):
            computed = list(solset)
        else:
            # Solver couldn't enumerate — fall back to checking each expected
            # value is a genuine root inside the interval. Completeness (no
            # missed solutions) is NOT verified in this branch.
            ok = all(bool(domain.contains(e)) and sym_equal(expr.subs(var, e),
                                                            sympy.Integer(0))
                     for e in expected)
            return ("PASS" if ok else "FAIL",
                    f"roots of {p['expr']} on [{interval[0]}, {interval[1]}): "
                    f"checked {in_unit(expected)} as roots "
                    f"(completeness not verified — solver returned {solset})")
        ok = multiset_equal(computed, expected)
        return ("PASS" if ok else "FAIL",
                f"roots of {p['expr']} on [{interval[0]}, {interval[1]}) "
                f"→ {in_unit(computed)} (expected {in_unit(expected)})")

    raise VerifyInputError(f"unhandled type {ptype!r}")  # unreachable


# ── Driver ────────────────────────────────────────────────────────────────────

def run_verification(json_path):
    try:
        with open(json_path) as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"❌ Could not read verification file: {e}", file=sys.stderr)
        return 1

    if not isinstance(data, dict) or not isinstance(data.get("problems"), list):
        print("❌ Verification file must be an object with a 'problems' list.",
              file=sys.stderr)
        return 1

    problems = data["problems"]
    topic = data.get("topic", "unknown")

    print(f"Verifying: {topic} ({len(problems)} problems)\n")

    results = []
    for p in problems:
        pid = p.get("id", "?") if isinstance(p, dict) else "?"
        try:
            ptype = check_schema(p)
            status, detail = check_problem(p, ptype)
            results.append((pid, status, detail))
        except VerifyInputError as e:
            results.append((pid, "FAIL", f"invalid input: {e}"))
        except Exception as e:
            results.append((pid, "FAIL", f"error evaluating problem {pid}: {e}"))

    for pid, status, detail in results:
        icon = {"PASS": "✅", "FAIL": "❌", "MANUAL": "👁 "}.get(status, "?")
        print(f"  {icon} [{status}] Problem {pid}: {detail}")

    failures = [r for r in results if r[1] == "FAIL"]
    manuals = [r for r in results if r[1] == "MANUAL"]
    passes = [r for r in results if r[1] == "PASS"]

    print(f"\n{len(passes)} passed · {len(failures)} failed · {len(manuals)} manual")

    if failures:
        print("\n❌ Fix the answer key before compiling.")
        return 1
    if manuals:
        print("\n👁  Manual review needed for some problems — safe to compile.")
        return 2
    print("\n✅ All checks passed — safe to compile.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <verify_TOPIC_DATE.json>", file=sys.stderr)
        sys.exit(1)

    json_path = sys.argv[1]
    if not os.path.exists(json_path):
        print(f"Error: file not found: {json_path}", file=sys.stderr)
        sys.exit(1)

    sys.exit(run_verification(json_path))
