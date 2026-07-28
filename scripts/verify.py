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
  solve          — roots of expr=0 over ℂ; non-real roots are NOT dropped —
                   if any exist, "domain":"real"/"complex" must be declared
  zeros          — like solve but duplicates collapse (multiplicity ignored)
  factor/expand  — checks expected is equivalent to expr
  eval           — evaluates expr at given values (complex ok via I)
  diff           — differentiates expr (optional "order", default 1)
  integrate      — d/dvar(expected)==expr AND expected defined wherever the
                   integrand is (rejects ln(x) for 1/x — use ln(Abs(x)))
  limit          — limit of expr as var → "to"; optional "dir"
  equiv          — expr and expected are the same function
  solve_interval — roots of expr=0 on [a, b); optional "unit":"deg". If the
                   solver cannot enumerate, returns MANUAL (completeness unproven)
  approx         — numeric expr vs expected within scale-aware default tol
                   (rounds-to semantics) or explicit "tol"
  distance/midpoint/slope/polygon_area — coordinate geometry from raw "points"
  triangle       — solve a triangle from 3 givens; "unit":"deg" default; SSA-aware
  system         — solve "equations"(each =0) for "vars"; expected {var: value}
  series         — summation(term, var, from..to) vs expected (finite/infinite)
  inequality     — solution set of expr <relation> 0 vs an interval spec
  stats          — mean/median/mode/range/sum/variance/stdev/q1/q3/iqr of "data"
  probability    — favorable/total as an exact fraction
  read_data      — read/compute a value from a chart/table whose "data" is in JSON
  definite_integral — ∫ from..to by independent mpmath quadrature
  estimate       — round numbers in expr to "place", then evaluate
  compare        — order "values" (asc/desc) or a relation (<,>,=)
  manual         — flagged for human review, never fails automatically

Universal optional fields: "var" (default x), "note", "standard", "difficulty",
"bloom", "figure" (declarative figure spec — scripts/render_figures.py draws it
from these same givens). Top-level "problem_count" is REQUIRED (coverage gate).
Unknown types or fields are HARD FAILURES. A sheet with zero machine checks
fails unless "allow_all_manual": true.

Exit codes: 0 all passed · 1 a check FAILED (or gate violation) · 2 manual review
needed (safe to compile).
"""

import cmath
import collections
import itertools
import json
import math
import os
import re
import statistics
import sys
from decimal import Decimal, ROUND_HALF_UP

import sympy
import mpmath
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
    "log", "ln", "exp", "sqrt", "Abs", "floor", "ceiling", "factorial",
]}
_FUNCS["abs"] = sympy.Abs

_CONSTS = {"pi": sympy.pi, "E": sympy.E, "oo": sympy.oo, "I": sympy.I}

# real=True matches the K-12/AP domain and lets Abs/ln/sqrt derivatives
# simplify (complex-root problems are out of allowlist scope — use manual)
_VARS = {v: Symbol(v, real=True) for v in
         "x y z t u v w a b c h k m n r s theta phi".split()}

_ALLOWED_NAMES = set(_FUNCS) | set(_CONSTS) | set(_VARS)
_SYMPY_LOCALS = {**_FUNCS, **_CONSTS, **_VARS}

# Tokens: numbers (including leading-decimal like .5), names, ** or ^,
# arithmetic operators, parens, commas, space.
_TOKEN_RE = re.compile(r"\d+(?:\.\d+)?|\.\d+|[A-Za-z]+|\*\*|[+\-*/(),^]|\s+")

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
# A broad, irrational sample grid. Points are transcendental multiples so an
# adversary cannot precompute a low-degree polynomial that vanishes at all of
# them (see CASE-19 / the audit's 7-fixed-point false positive).

_SAMPLES = [round(math.pi * k / 7 - 1.5, 6) for k in range(1, 12)] + \
           [round(math.e * k / 5 - 2.0, 6) for k in range(1, 8)]
_MIN_VALID_VOTES = 8   # require many agreeing evaluations, not 3


def _sample_points(free):
    if not free:
        return [()]
    if len(free) == 1:
        return [(s,) for s in _SAMPLES]
    if len(free) == 2:
        return list(itertools.product(_SAMPLES[:9], repeat=2))
    return [tuple(_SAMPLES[(i + 3 * j) % len(_SAMPLES)]
                  for j in range(len(free)))
            for i in range(len(_SAMPLES))]


def numeric_equal(a, b, tol=1e-9):
    """Deterministic numeric spot-check over a broad irrational grid.

    Only reached when the symbolic layer cannot resolve a-b (transcendental
    cases). Requires many agreeing evaluations; a handful of coincidental
    agreements is not enough.
    """
    free = sorted(set(a.free_symbols) | set(b.free_symbols), key=str)
    valid = 0
    for point in _sample_points(free):
        subs = dict(zip(free, point))
        try:
            av = complex(sympy.N(a.subs(subs), 20))
            bv = complex(sympy.N(b.subs(subs), 20))
        except (TypeError, ValueError, ZeroDivisionError):
            continue
        if not (cmath.isfinite(av) and cmath.isfinite(bv)):
            continue
        if abs(av - bv) > tol * max(1.0, abs(av), abs(bv)):
            return False
        valid += 1
    return valid >= _MIN_VALID_VOTES


_TRANSCENDENTAL = (sympy.sin, sympy.cos, sympy.tan, sympy.asin, sympy.acos,
                   sympy.atan, sympy.sec, sympy.csc, sympy.cot, sympy.exp,
                   sympy.log, sympy.sinh, sympy.cosh, sympy.tanh)


def sym_equal(a, b):
    """True iff a and b are the same function.

    Structural, then simplify/trigsimp. If the difference is a NON-transcendental
    (polynomial/rational/algebraic) expression that did not reduce to zero, that
    is a definitive inequality — return False rather than fall through to numeric
    sampling, which is what let a crafted vanishing polynomial produce a false
    positive (audit 1c). Numeric sampling is a last resort only for genuinely
    transcendental differences SymPy could not close.
    """
    if a == b:  # structural — also covers infinities, where a-b is nan
        return True
    try:
        d = simplify(a - b)
        if d == 0 or trigsimp(d) == 0:
            return True
        de = sympy.expand(a - b)
        if de == 0:
            return True
        # A nonzero POLYNOMIAL/RATIONAL difference is a definitive inequality —
        # do not sample (this is what killed the crafted-vanishing-poly false
        # positive). Differences involving Abs/sign/sqrt/transcendentals are NOT
        # decided here (simplify may miss real-domain identities like
        # sign(x)/Abs(x) == 1/x), so they fall through to numeric sampling.
        try:
            fs = de.free_symbols
            if fs and de.is_rational_function(*fs):
                return False
        except (TypeError, ValueError):
            pass
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
    """Validated EXPLICIT tolerance; None means fall back to default logic."""
    tol = p.get("tol", default)
    if tol is None:
        return None
    if isinstance(tol, bool) or not isinstance(tol, (int, float)) or tol <= 0:
        raise VerifyInputError("'tol' must be a positive number")
    return float(tol)


def _decimals_of(expected_raw):
    s = repr(expected_raw) if isinstance(expected_raw, float) else str(expected_raw)
    if "." in s and s.replace(".", "").replace("-", "").isdigit():
        return len(s.split(".")[-1])
    return 0


def round_half_up(value, decimals):
    """Decimal round-half-up (the school convention), not banker's rounding."""
    q = Decimal(1).scaleb(-decimals)
    return Decimal(str(float(sympy.N(value, 25)))).quantize(q, rounding=ROUND_HALF_UP)


def rounds_to(computed, expected_raw):
    """True iff `computed`, rounded (half-up) to the precision `expected_raw` is
    written with, equals `expected_raw`. Precise 'does it round to the stated
    value' — avoids the half-ulp band that let an exact midpoint pass either way
    (audit #6). For an integer-valued expected, compares within a tight tol."""
    decimals = _decimals_of(expected_raw)
    if decimals == 0 and float(sympy.N(expected_raw)) == int(sympy.N(expected_raw)):
        # integer answer: exact-ish
        return abs(float(sympy.N(computed)) - float(sympy.N(expected_raw))) < 1e-9
    try:
        return round_half_up(computed, decimals) == Decimal(str(expected_raw))
    except Exception:
        return abs(float(sympy.N(computed)) - float(sympy.N(expected_raw))) \
            <= 0.5 * 10 ** (-decimals)


def default_tol(expected_raw):
    """Scale-appropriate tolerance when no explicit 'tol' is given.

    A fixed absolute 0.01 is scale-blind (0.004 vs 0.01 wrongly passed — audit
    1f/B2). Instead: for a value written with decimals, accept anything that
    rounds to it (half a unit in the last place); for an integer-valued answer,
    use a tight relative tolerance.
    """
    s = repr(expected_raw) if isinstance(expected_raw, float) else str(expected_raw)
    if "." in s and s.replace(".", "").replace("-", "").isdigit():
        decimals = len(s.split(".")[-1])
        return 0.5 * 10 ** (-decimals)
    try:
        return max(5e-4 * abs(float(expected_raw)), 1e-9)
    except (TypeError, ValueError):
        return 1e-6


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


def count_real_roots(expr, var, lo, hi, n=2000):
    """Numerically enumerate real roots of expr in [lo, hi) via mpmath: scan for
    sign changes on a fine grid, refine each with findroot, keep only genuine
    zeros (|f|≈0, excludes asymptote crossings like tan), dedupe. Returns a
    sorted list of float roots, or None if the function can't be evaluated
    numerically over the interval (caller then stays conservative)."""
    try:
        f = sympy.lambdify(var, expr, modules="mpmath")
    except Exception:
        return None
    a, b = float(sympy.N(lo)), float(sympy.N(hi))
    xs = [a + (b - a) * i / n for i in range(n + 1)]
    try:
        ys = [f(x) for x in xs]
    except Exception:
        return None
    roots = []

    def refine(guess):
        try:
            r = mpmath.findroot(f, guess)
        except Exception:
            return
        rr = float(mpmath.re(r))
        if not (a - 1e-9 <= rr < b):             # right-open interval
            return
        if abs(mpmath.re(f(rr))) > 1e-6:          # asymptote, not a zero
            return
        if all(abs(rr - e) > 1e-6 for e in roots):
            roots.append(rr)

    absy = [abs(mpmath.re(y)) if mpmath.isfinite(y) else None for y in ys]
    for i in range(n):
        y0, y1 = ys[i], ys[i + 1]
        if mpmath.isfinite(y0) and mpmath.isfinite(y1):
            if mpmath.re(y0) == 0 or (mpmath.re(y0) * mpmath.re(y1) < 0):  # sign change
                refine((xs[i] + xs[i + 1]) / 2)
        # Tangent (even-multiplicity) roots don't change sign — detect a local
        # minimum of |f| that dips near zero and refine there (audit #2).
        if 0 < i < n and absy[i] is not None and absy[i - 1] is not None \
                and absy[i + 1] is not None:
            if absy[i] <= absy[i - 1] and absy[i] <= absy[i + 1] and absy[i] < 1e-3:
                refine(xs[i])
    return sorted(roots)


def parse_interval_spec(spec):
    """Build a SymPy real set from a JSON interval spec (allowlist-safe).

    spec is a list of intervals, each [lo, hi, openness] where openness is one
    of "open", "closed", "loopen" (lo open, hi closed), "hiopen". lo/hi may be
    numbers or the strings "oo"/"-oo". A single interval may be given unwrapped.
    """
    if spec and not isinstance(spec[0], list):
        spec = [spec]
    result = sympy.S.EmptySet
    for iv in spec:
        if len(iv) != 3:
            raise VerifyInputError("each interval must be [lo, hi, openness]")
        lo = parse_value(iv[0]) if iv[0] not in ("-oo", "oo") else \
            (-sympy.oo if iv[0] == "-oo" else sympy.oo)
        hi = parse_value(iv[1]) if iv[1] not in ("-oo", "oo") else \
            (-sympy.oo if iv[1] == "-oo" else sympy.oo)
        lopen = iv[2] in ("open", "loopen")
        hopen = iv[2] in ("open", "hiopen")
        result = result.union(sympy.Interval(lo, hi, left_open=lopen, right_open=hopen))
    return result


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
    "solve":          ({"expr", "expected"}, {"var", "domain"}),
    "zeros":          ({"expr", "expected"}, {"var", "domain"}),
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
    "system":         ({"equations", "vars", "expected"}, set()),
    "series":         ({"term", "from", "to", "expected"}, {"var"}),
    "inequality":     ({"expr", "relation", "expected"}, {"var"}),
    "stats":          ({"data", "measure", "expected"}, {"tol"}),
    "probability":    ({"favorable", "total", "expected"}, set()),
    "read_data":      ({"data", "query", "expected"}, {"key", "tol"}),
    "definite_integral": ({"expr", "from", "to", "expected"}, {"var", "tol"}),
    "estimate":       ({"expr", "place", "expected"}, set()),
    "compare":        ({"values", "expected"}, {"order"}),
    "manual":         ({"desc"}, set()),
}

_RELATIONS = {"<": sympy.StrictLessThan, "<=": sympy.LessThan,
              ">": sympy.StrictGreaterThan, ">=": sympy.GreaterThan}


def validate_figure(p, ptype):
    """Validate the optional 'figure' object scripts/render_figures.py draws.

    The whole point of rendered figures is a SINGLE source of givens, so on a
    'triangle' problem the figure may only be the opt-in marker — any value
    inside it would be a second copy of the givens, i.e. the retyping drift
    this pipeline exists to prevent. A 'right_triangle' figure carries its own
    givens (the approx expr has no structure to draw from), so those are
    geometry-checked here through the same solve_triangle that verifies
    triangle problems, and literal-checked against 'expr' so the drawing can
    only show numbers the arithmetic check actually used.
    """
    fig = p.get("figure")
    if fig is None:
        return
    if not isinstance(fig, dict):
        raise VerifyInputError(
            "'figure' must be an object like {\"kind\": \"triangle\"}")
    kind = fig.get("kind")
    if kind not in ("triangle", "right_triangle"):
        raise VerifyInputError(
            f"figure 'kind' must be 'triangle' or 'right_triangle', got {kind!r}")
    if ptype == "triangle":
        if kind != "triangle" or set(fig) != {"kind"}:
            raise VerifyInputError(
                "on a 'triangle' problem, 'figure' must be exactly "
                '{"kind": "triangle"} — render_figures.py draws from the '
                "problem's own 'given' dict, never from a second copy")
        return
    if kind == "triangle":
        raise VerifyInputError(
            "figure kind 'triangle' only applies to type 'triangle' problems "
            "(they render automatically from their 'given' dict)")
    if ptype != "approx":
        raise VerifyInputError(
            "figure kind 'right_triangle' only applies to 'approx' problems — "
            "the figure values are literal-checked against 'expr'")
    unknown = set(fig) - {"kind", "given", "solve_for", "unknown"}
    if unknown:
        raise VerifyInputError(
            f"figure has unknown field(s): {sorted(unknown)}")
    given = fig.get("given")
    if (not isinstance(given, dict) or len(given) != 2
            or set(given) - {"a", "b", "c", "A", "B"}):
        raise VerifyInputError(
            "figure 'given' must hold exactly two of a/b/c/A/B "
            "(the right angle C is implied)")
    for k, v in given.items():
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            raise VerifyInputError(
                f"figure given {k!r} must be a plain number so it can be "
                "literal-matched against 'expr'")
    solve_for = fig.get("solve_for")
    if solve_for not in {"a", "b", "c", "A", "B"} or solve_for in given:
        raise VerifyInputError(
            "figure 'solve_for' must be one of a/b/c/A/B and not already given")
    unk = fig.get("unknown", "?")
    if not isinstance(unk, str) or not re.fullmatch(r"[A-Za-z?]{1,3}", unk):
        raise VerifyInputError(
            "figure 'unknown' must be a short letter name like \"x\"")
    expr_nums = {float(t) for t in
                 re.findall(r"\d+(?:\.\d+)?|\.\d+", str(p.get("expr", "")))}
    for k, v in given.items():
        if float(v) not in expr_nums:
            raise VerifyInputError(
                f"figure value {k}={v} does not appear as a literal in expr "
                f"{p.get('expr')!r} — the figure would print a number this "
                "check never verified")
    sides = {k: float(given[k]) for k in "abc" if k in given}
    angles = {k: math.radians(float(given[k])) for k in "AB" if k in given}
    angles["C"] = math.pi / 2
    if not solve_triangle(sides, angles):
        raise VerifyInputError(
            f"figure givens {given} do not form a right triangle "
            "(a leg cannot exceed the hypotenuse)")


def check_schema(p):
    if not isinstance(p, dict):
        raise VerifyInputError("each problem must be a JSON object")
    if "id" not in p:
        raise VerifyInputError("problem is missing required field 'id'")
    # id must be an integer — the coverage gate and the difficulty-ramp report
    # both assume it; a string id silently broke the ramp report (audit §4).
    if not isinstance(p["id"], int) or isinstance(p["id"], bool):
        raise VerifyInputError(f"problem 'id' must be an integer, got {p['id']!r}")
    ptype = p.get("type")
    if ptype not in SCHEMAS:
        raise VerifyInputError(
            f"unknown problem type {ptype!r} — allowed types: {sorted(SCHEMAS)}")
    required, optional = SCHEMAS[ptype]
    # "standard" (e.g. CCSS "8.EE.C.8" / AP "CHA-3.A") and "difficulty" (1-5)
    # are universal optional tags — reported in the summary, never gating.
    # "figure" is the declarative figure spec render_figures.py draws from.
    fields = set(p) - {"id", "type", "note", "standard", "difficulty", "bloom",
                       "figure"}
    missing = required - fields
    if missing:
        raise VerifyInputError(
            f"type {ptype!r} is missing required field(s): {sorted(missing)}")
    unknown = fields - required - optional
    if unknown:
        raise VerifyInputError(
            f"type {ptype!r} has unknown field(s): {sorted(unknown)}")
    validate_figure(p, ptype)
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
        tol = get_tol(p) or default_tol(p["expected"])
        expected = float(sympy.N(parse_value(p["expected"])))
        ok = any(abs(c - expected) <= tol for c in candidates)
        shown = ", ".join(f"{c:.4f}" for c in candidates)
        ambiguous = (" — ambiguous SSA case, two triangles exist"
                     if len(solutions) > 1 else "")
        return ("PASS" if ok else "FAIL",
                f"triangle {given} → {solve_for} ∈ [{shown}] "
                f"(expected {p['expected']}, tol {tol}{ambiguous})")

    if ptype == "system":
        eqs_raw, vars_raw = p["equations"], p["vars"]
        if not isinstance(eqs_raw, list) or not isinstance(vars_raw, list):
            raise VerifyInputError("'equations' and 'vars' must be lists")
        for v in vars_raw:
            if v not in _VARS:
                raise VerifyInputError(f"variable {v!r} is not allowed")
        syms = [_VARS[v] for v in vars_raw]
        eqs = [safe_parse(e) for e in eqs_raw]   # each expr is treated as =0
        # expected: a dict (one solution) or a list of dicts (all solutions).
        # Every solution must assign ALL vars (audit #3: a key listing only x
        # must not pass on an unchecked y).
        exp_raw = p["expected"]
        exp_list = exp_raw if isinstance(exp_raw, list) else [exp_raw]
        want_list = []
        for sol in exp_list:
            if not isinstance(sol, dict) or set(sol) != set(vars_raw):
                raise VerifyInputError(
                    f"each system solution must assign exactly {vars_raw}")
            want_list.append({_VARS[k]: parse_value(v) for k, v in sol.items()})
        # VALIDITY: each claimed solution must satisfy every equation (handles
        # infinite families correctly — a valid particular point substitutes to 0).
        def satisfies(assign):
            return all(sym_equal(e.subs(assign), sympy.Integer(0)) for e in eqs)
        if not all(satisfies(a) for a in want_list):
            return ("FAIL", f"system{eqs_raw}: a listed solution does not satisfy "
                    f"all equations (expected {exp_raw})")
        # COMPLETENESS: compare against SymPy's full solution set when it is a
        # finite list; parametric/infinite families can't be counted → MANUAL.
        sols = sympy.solve(eqs, syms, dict=True)
        finite = sols and all(
            all(not v.free_symbols for v in sol.values()) for sol in sols)
        if finite:
            if len(sols) != len(want_list):
                return ("MANUAL",
                        f"system{eqs_raw}: {len(sols)} solution(s) exist but key "
                        f"lists {len(want_list)} — verify completeness by hand")
            return ("PASS", f"system{eqs_raw} → all {len(sols)} solution(s) verified")
        return ("MANUAL",
                f"system{eqs_raw}: listed solution(s) valid but the system has a "
                "parametric/infinite family — verify completeness by hand")

    if ptype == "stats":
        data = p["data"]
        if not isinstance(data, list) or not data:
            raise VerifyInputError("stats 'data' must be a non-empty list")
        vals = [parse_value(v) for v in data]
        measure = p["measure"]
        if measure == "mean":
            result = sum(vals) / len(vals)
        elif measure == "sum":
            result = sum(vals)
        elif measure == "median":
            s = sorted(vals, key=lambda e: float(sympy.N(e)))
            n = len(s)
            result = s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2
        elif measure == "range":
            fs = [float(sympy.N(v)) for v in vals]
            result = parse_value(max(fs)) - parse_value(min(fs))
        elif measure == "mode":
            counts = collections.Counter(float(sympy.N(v)) for v in vals)
            top = max(counts.values())
            modes = sorted(k for k, c in counts.items() if c == top)
            if len(modes) != 1:
                return ("MANUAL", f"mode is not unique ({modes}) — review by hand")
            result = parse_value(modes[0])
        elif measure in ("variance", "stdev", "q1", "q3", "iqr"):
            fs = [float(sympy.N(v)) for v in vals]
            if measure == "variance":
                result = parse_value(statistics.pvariance(fs))
            elif measure == "stdev":
                result = parse_value(statistics.pstdev(fs))
            else:
                # School "median of halves" quartiles (Tukey hinges): split at
                # the median; for odd n exclude the median from both halves.
                s = sorted(fs)
                n = len(s)
                lower, upper = s[:n // 2], s[(n + 1) // 2:]
                if not lower or not upper:
                    return ("MANUAL", "too few data points for quartiles")
                q1, q3 = statistics.median(lower), statistics.median(upper)
                result = parse_value({"q1": q1, "q3": q3, "iqr": q3 - q1}[measure])
        else:
            raise VerifyInputError(
                "'measure' must be mean/median/mode/range/sum/variance/stdev/q1/q3/iqr")
        expected = parse_value(p["expected"])
        # stdev/variance/quartiles are usually rounded → scale-aware default tol
        tol = get_tol(p)
        if tol is not None:
            ok = compare_value(result, expected, tol)
        elif measure in ("mean", "variance", "stdev", "q1", "q3", "iqr"):
            ok = rounds_to(result, p["expected"])   # precise rounds-to (audit #6)
        else:
            ok = compare_value(result, expected, None)
        return ("PASS" if ok else "FAIL",
                f"{measure}({data}) → {result} (expected {p['expected']})")

    if ptype == "probability":
        fav, tot = parse_value(p["favorable"]), parse_value(p["total"])
        # Validity: 0 <= favorable <= total, total > 0 (audit #4 — an impossible
        # probability like 7/6 or a negative one must be rejected).
        if not (tot.is_positive):
            raise VerifyInputError("probability 'total' must be positive")
        if fav.is_negative or (fav - tot).is_positive:
            return ("FAIL", f"P = {p['favorable']}/{p['total']} is not a valid "
                    "probability (need 0 ≤ favorable ≤ total)")
        result = sympy.Rational(fav, tot) if fav.is_integer and tot.is_integer \
            else fav / tot
        expected = parse_value(p["expected"])
        # accept the exact fraction OR a correctly-rounded decimal (1/3 vs 0.333)
        ok = sym_equal(result, expected) or (
            not isinstance(p["expected"], str) and rounds_to(result, p["expected"]))
        return ("PASS" if ok else "FAIL",
                f"P = {p['favorable']}/{p['total']} → {result} "
                f"(expected {p['expected']})")

    if ptype == "estimate":
        # Round each numeric OPERAND in the expression to "place", THEN evaluate —
        # front-end estimation. Rounding the string literals (not the folded
        # result) and using round-half-up is what the school task means (audit #7).
        places = {"thousand": 1000, "hundred": 100, "ten": 10, "whole": 1,
                  "tenth": sympy.Rational(1, 10), "hundredth": sympy.Rational(1, 100)}
        place = p["place"]
        step = places.get(place)
        if step is None:
            if isinstance(place, (int, float)) and not isinstance(place, bool) and place > 0:
                step = sympy.Rational(str(place))
            else:
                raise VerifyInputError(
                    f"'place' must be one of {sorted(places)} or a positive number")

        def round_literal(m):
            v = sympy.Rational(m.group(0))
            q = round_half_up(v / step, 0)
            return str(sympy.Rational(int(q)) * step)

        rounded_str = re.sub(r"\d+(?:\.\d+)?", round_literal, p["expr"])
        result = sympy.nsimplify(sympy.N(safe_parse(rounded_str)))
        expected = parse_value(p["expected"])
        ok = sym_equal(result, expected)
        return ("PASS" if ok else "FAIL",
                f"estimate({p['expr']} @ {place} → {rounded_str}) → {result} "
                f"(expected {p['expected']})")

    if ptype == "compare":
        vals_raw = p["values"]
        if not isinstance(vals_raw, list) or len(vals_raw) < 2:
            raise VerifyInputError("'values' must be a list of at least two items")
        vals = [parse_value(v) for v in vals_raw]
        order = p.get("order", "asc")
        if order in ("asc", "desc"):
            keyed = sorted(range(len(vals)),
                           key=lambda i: float(sympy.N(vals[i])),
                           reverse=(order == "desc"))
            # expected: the values in sorted order (as given tokens)
            want = parse_value_list(p["expected"])
            got = [vals[i] for i in keyed]
            ok = len(want) == len(got) and all(sym_equal(a, b)
                                               for a, b in zip(got, want))
            return ("PASS" if ok else "FAIL",
                    f"compare({vals_raw}, {order}) → {got} (expected {p['expected']})")
        elif order == "relation":
            # expected is "<", ">", or "=" for values[0] vs values[1]. Compare
            # EXACTLY (audit #5 — a float tol conflated 1/7 with a truncated
            # decimal); values were parsed to exact SymPy numbers.
            a, b = vals[0], vals[1]
            if sym_equal(a, b):
                rel = "="
            else:
                rel = "<" if (a - b).is_negative else ">"
            ok = rel == str(p["expected"]).strip()
            return ("PASS" if ok else "FAIL",
                    f"compare({vals_raw[0]} vs {vals_raw[1]}) → {rel} "
                    f"(expected {p['expected']})")
        else:
            raise VerifyInputError("'order' must be 'asc', 'desc', or 'relation'")

    if ptype == "read_data":
        # A chart/table's data lives in the JSON (the SAME data pgfplots renders,
        # so the figure and the check share one source of truth). The question
        # reads or computes a value from it. Closes data-representational topics.
        data = p["data"]
        query = p["query"]
        if isinstance(data, dict):          # category → value (bar/pictogram/table)
            table = {k: parse_value(v) for k, v in data.items()}
            if query == "value":
                result = table[p["key"]]
            elif query == "total":
                result = sum(table.values())
            elif query in ("max_value", "min_value"):
                result = (max if query == "max_value" else min)(
                    table.values(), key=lambda e: float(sympy.N(e)))
            elif query in ("max_key", "min_key"):
                # Ties: ANY key holding the extreme value is a valid answer
                # (audit #8 — don't reject B when A and B are both maxima).
                target = (max if query == "max_key" else min)(
                    float(sympy.N(v)) for v in table.values())
                winners = {k for k, v in table.items()
                           if abs(float(sympy.N(v)) - target) < 1e-12}
                ok = str(p["expected"]) in winners
                return ("PASS" if ok else "FAIL",
                        f"{query}({data}) → {sorted(winners)} "
                        f"(expected {p['expected']})")
            elif query == "difference":
                a, b = p["key"]
                result = table[a] - table[b]
            else:
                raise VerifyInputError(
                    "table 'query' must be value/total/max_value/min_value/"
                    "max_key/min_key/difference")
        elif isinstance(data, list):        # numeric series (line plot / tally)
            vals = [parse_value(v) for v in data]
            if query == "total":
                result = sum(vals)
            elif query == "count":
                result = sympy.Integer(len(vals))
            elif query == "max_value":
                result = max(vals, key=lambda e: float(sympy.N(e)))
            elif query == "min_value":
                result = min(vals, key=lambda e: float(sympy.N(e)))
            else:
                raise VerifyInputError("list 'query' must be total/count/max_value/min_value")
        else:
            raise VerifyInputError("read_data 'data' must be an object or a list")
        expected = parse_value(p["expected"])
        ok = compare_value(result, expected, get_tol(p))
        return ("PASS" if ok else "FAIL",
                f"{query}({data}) → {result} (expected {p['expected']})")

    if ptype == "definite_integral":
        var = get_var(p)
        integrand = safe_parse(p["expr"])
        lo, hi = parse_value(p["from"]), parse_value(p["to"])
        expected = parse_value(p["expected"])
        tol = get_tol(p) or max(default_tol(p["expected"]), 1e-6)
        # Prefer SymPy's EXACT definite integral as the authority. Only fall
        # back to numerics if it can't, and then require the quadrature to
        # CONVERGE (two panel counts agree) — a single mpmath.quad call is
        # unreliable for oscillatory integrands (audit #1). If numerics don't
        # converge, return MANUAL rather than trust a wrong number.
        exact = None
        try:
            val = sympy.integrate(integrand, (var, lo, hi))
            if val.is_finite and not val.has(sympy.Integral):
                exact = val
        except Exception:
            exact = None
        if exact is not None:
            ok = abs(float(sympy.N(exact)) - float(sympy.N(expected))) <= tol
            return ("PASS" if ok else "FAIL",
                    f"∫[{p['from']},{p['to']}] {p['expr']} d{var} = {exact} "
                    f"(expected {p['expected']})")
        f = sympy.lambdify(var, integrand, modules="mpmath")
        a, b = float(sympy.N(lo)), float(sympy.N(hi))
        try:
            coarse = mpmath.quad(f, [a, (a + b) / 2, b])
            mid = (2 * a + b) / 3, (a + 2 * b) / 3
            fine = mpmath.quad(f, [a, mid[0], (a + b) / 2, mid[1], b])
        except Exception:
            return ("MANUAL", f"∫ {p['expr']}: numeric integration failed — verify by hand")
        if abs(coarse - fine) > max(tol, 1e-6):
            return ("MANUAL",
                    f"∫[{p['from']},{p['to']}] {p['expr']}: quadrature did not "
                    f"converge ({float(coarse):.5g} vs {float(fine):.5g}) — verify by hand")
        ok = abs(fine - float(sympy.N(expected))) <= tol
        return ("PASS" if ok else "FAIL",
                f"∫[{p['from']},{p['to']}] {p['expr']} d{var} ≈ {float(fine):.6g} "
                f"(expected {p['expected']}, tol {tol:g})")

    if ptype == "series":
        var = get_var(p)
        term = safe_parse(p["term"])
        lo = parse_value(p["from"])
        hi = parse_value(p["to"])
        total = sympy.summation(term, (var, lo, hi))
        expected = parse_value(p["expected"])
        ok = sym_equal(total, expected)
        return ("PASS" if ok else "FAIL",
                f"sum({p['term']}, {var}={p['from']}..{p['to']}) → {total} "
                f"(expected {p['expected']})")

    expr = safe_parse(p["expr"])

    if ptype == "approx":
        if expr.free_symbols:
            raise VerifyInputError(
                "approx 'expr' must be fully numeric (no variables) — "
                f"found {sorted(map(str, expr.free_symbols))}")
        tol = get_tol(p) or default_tol(p["expected"])
        expected = parse_value(p["expected"])
        ok = approx_equal(expr, expected, tol)
        return ("PASS" if ok else "FAIL",
                f"approx({p['expr']}) → {float(sympy.N(expr, 15)):.6g} "
                f"(expected {p['expected']}, tol {tol:g})")

    if ptype in ("solve", "zeros"):
        var = get_var(p)
        # Solve over ℂ with an unrestricted symbol so non-real roots are not
        # silently dropped (audit 1a: x**4-1 keyed [1,-1] must not pass).
        z = sympy.Dummy("z")
        all_roots = sympy.solve(expr.subs(var, z), z)
        real_roots = [r for r in all_roots if r.is_real]
        nonreal = [r for r in all_roots if r.is_real is False]
        domain = p.get("domain", "real")
        if domain not in ("real", "complex"):
            raise VerifyInputError("'domain' must be 'real' or 'complex'")
        # When non-real roots exist the intent is ambiguous — force an explicit
        # decision instead of quietly comparing against reals only.
        if nonreal and "domain" not in p:
            return ("FAIL",
                    f"{ptype}({p['expr']}) has non-real roots {nonreal}; set "
                    f'"domain":"complex" to require all roots or "domain":"real" '
                    "to restrict — refusing to guess intent")
        roots = all_roots if domain == "complex" else real_roots
        expected = parse_value_list(p["expected"])
        if ptype == "zeros":
            roots = dedupe(roots)
            expected = dedupe(expected)
        ok = multiset_equal(roots, expected)
        return ("PASS" if ok else "FAIL",
                f"{ptype}({p['expr']}, domain={domain}) → {roots} "
                f"(expected {expected})")

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
        # Domain guard (audit 1b): ln(x) is NOT a valid antiderivative of 1/x
        # over the reals — it is undefined where 1/x is fine (x<0). Reject an
        # antiderivative that is non-real at a point where the integrand is real.
        domain_note = ""
        if ok:
            for s in (-1.3, -0.6, -2.1):
                try:
                    iv = complex(sympy.N(expr.subs(var, s), 15))
                    ev = complex(sympy.N(expected.subs(var, s), 15))
                except (TypeError, ValueError, ZeroDivisionError):
                    continue
                if cmath.isfinite(iv) and abs(iv.imag) < 1e-9:  # integrand real here
                    if not cmath.isfinite(ev) or abs(ev.imag) > 1e-9:
                        ok = False
                        domain_note = (f" — antiderivative undefined/non-real at "
                                       f"{var}={s} where integrand is real; "
                                       "use Abs() form")
                        break
        return ("PASS" if ok else "FAIL",
                f"d/d{var}({p['expected']}) → {back} (integrand {p['expr']}){domain_note}")

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
            # Solver couldn't enumerate symbolically. Each listed root must be
            # genuine (a bogus one FAILs). For completeness, enumerate roots
            # numerically with mpmath (CASE-34) — if the numeric count matches
            # the key's count and each is real-verified, PASS with completeness
            # established; otherwise stay MANUAL rather than silently pass.
            # Use mpmath's numerically-enumerated roots as the authority
            # (transcendental keys are inherently approximate). Match each
            # listed root to a found root within a school tolerance; PASS only
            # when every listed root matches AND the counts are equal
            # (completeness). A listed value matching no found root → FAIL
            # (bogus). Count mismatch or inconclusive enumeration → MANUAL.
            numeric = count_real_roots(expr, var, lo, hi)
            exp_floats = sorted(float(sympy.N(e)) for e in expected)
            match_tol = 1e-2
            if numeric is None:
                return ("MANUAL",
                        f"roots of {p['expr']} on [{interval[0]}, {interval[1]}): "
                        "numeric enumeration inconclusive — review by hand")
            bogus = [ef for ef in exp_floats
                     if not any(abs(nr - ef) < match_tol for nr in numeric)]
            if bogus:
                return ("FAIL",
                        f"roots of {p['expr']} on [{interval[0]}, {interval[1]}): "
                        f"listed value(s) {bogus} are not roots (numeric roots: "
                        f"{[round(r,4) for r in numeric]})")
            if len(exp_floats) == len(numeric):
                return ("PASS",
                        f"roots of {p['expr']} on [{interval[0]}, {interval[1]}) "
                        f"→ {in_unit(expected)} (completeness numerically "
                        f"confirmed: {len(numeric)} roots)")
            return ("MANUAL",
                    f"roots of {p['expr']} on [{interval[0]}, {interval[1]}): key "
                    f"lists {len(exp_floats)} but numeric enumeration found "
                    f"{len(numeric)} ({[round(r,4) for r in numeric]}) — review by hand")
        ok = multiset_equal(computed, expected)
        return ("PASS" if ok else "FAIL",
                f"roots of {p['expr']} on [{interval[0]}, {interval[1]}) "
                f"→ {in_unit(computed)} (expected {in_unit(expected)})")

    if ptype == "inequality":
        var = get_var(p)
        lhs = safe_parse(p["expr"])   # expr already moved to LHS, compared to 0
        rel = p["relation"]
        if rel not in _RELATIONS:
            raise VerifyInputError(f"'relation' must be one of {sorted(_RELATIONS)}")
        computed = sympy.solveset(_RELATIONS[rel](lhs, 0), var,
                                  domain=sympy.S.Reals)
        # expected: a set expression over the allowlist, e.g. "Interval.open(4, oo)"
        # is not allowlist-safe, so accept an interval spec [[lo, hi, openness], ...]
        expected_set = parse_interval_spec(p["expected"])
        ok = computed == expected_set
        return ("PASS" if ok else "FAIL",
                f"solve {p['expr']} {rel} 0 → {computed} (expected {expected_set})")

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

    # Coverage gate is MANDATORY (audit 3b: it was optional, so a partial key
    # could pass with the field simply omitted). Every worksheet problem id
    # 1..N must have at least one check.
    problem_count = data.get("problem_count")
    if problem_count is None:
        print("❌ 'problem_count' is required — set it to the number of problems "
              "on the worksheet so coverage can be enforced.", file=sys.stderr)
        return 1
    if not isinstance(problem_count, int) or problem_count < 1:
        print("❌ 'problem_count' must be a positive integer.", file=sys.stderr)
        return 1
    ids = {p["id"] for p in problems if isinstance(p, dict) and isinstance(p.get("id"), int)}
    missing = [i for i in range(1, problem_count + 1) if i not in ids]
    if missing:
        print(f"❌ Coverage gap: problem_count={problem_count} but no checks "
              f"for problem id(s) {missing}. Every worksheet problem needs "
              "at least one check (use type 'manual' if unverifiable).",
              file=sys.stderr)
        return 1

    print(f"Verifying: {topic} ({len(problems)} problems) · "
          f"SymPy {sympy.__version__}\n")

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

    # Tag report: standards coverage + difficulty ramp (informational)
    stds = {}
    diffs = []
    for p in problems:
        if isinstance(p, dict):
            if p.get("standard"):
                stds[p["standard"]] = stds.get(p["standard"], 0) + 1
            if isinstance(p.get("difficulty"), int):
                diffs.append((p.get("id"), p["difficulty"]))
    blooms = {}
    for p in problems:
        if isinstance(p, dict) and p.get("bloom"):
            blooms[p["bloom"]] = blooms.get(p["bloom"], 0) + 1
    if blooms:
        order = ["recall", "apply", "analyze", "justify"]
        print("bloom mix: " + ", ".join(f"{k}×{blooms[k]}" for k in order if k in blooms))
    if stds:
        print("standards: " + ", ".join(f"{k}×{v}" for k, v in sorted(stds.items())))
    if diffs:
        ramp = [d for _, d in sorted(diffs, key=lambda x: x[0])]  # ids are ints
        drops = sum(1 for a, b in zip(ramp, ramp[1:]) if b < a - 1)
        note = " ⚠ ramp drops >1 level mid-sheet" if drops else ""
        print(f"difficulty ramp: {ramp}{note}")

    machine_checked = len(passes) + len(failures)

    if failures:
        print("\n❌ Fix the answer key before compiling.")
        return 1
    # Machine-check floor (audit §2): a sheet where NOTHING was CAS-verified
    # must not report "safe" on the strength of manual flags alone, unless the
    # author explicitly acknowledges it.
    if machine_checked == 0 and not data.get("allow_all_manual"):
        print(f"\n❌ 0 of {len(problems)} problems were machine-verified — every "
              "check is 'manual'. Add real checks, or set \"allow_all_manual\": "
              "true to acknowledge an entirely hand-checked sheet.", file=sys.stderr)
        return 1
    if manuals:
        print(f"\n👁  {len(manuals)} problem(s) need manual review "
              f"({machine_checked} machine-verified) — safe to compile.")
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
