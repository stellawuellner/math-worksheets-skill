#!/usr/bin/env python3
"""
test_render_figures.py — property-tests for scripts/render_figures.py.

CI has NO LaTeX engine, so nothing here compiles .tex. Instead the tests parse
the EMITTED TikZ text and assert the properties that make rendered figures
trustworthy:

  * to-scale by construction — every drawn side, de-normalized by the figure's
    scale, reproduces the solve_triangle solution (and hence the JSON givens)
    to 1e-3;
  * labels show ONLY given values plus "?" (or the declared unknown) on
    solve_for — never a computed answer;
  * the ambiguous SSA case draws BOTH apexes, each matching one solution;
  * a given right angle prints as a square mark, not a "90" label;
  * impossible or drifting figures refuse to render with a teaching message.

Run: python3 tests/test_render_figures.py   (needs sympy, like verify.py)
"""

import io
import json
import math
import os
import re
import sys
import tempfile
from contextlib import redirect_stderr, redirect_stdout

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import render_figures as rf   # noqa: E402
import verify                 # noqa: E402
from verify import solve_triangle  # noqa: E402

FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures")
FAILS = []


def check(name, cond):
    print(f"  {'✅' if cond else '❌'} {name}")
    if not cond:
        FAILS.append(name)


def render(problems):
    """Run the renderer in-process; returns (exit code, figs text, output)."""
    tmp = tempfile.mkdtemp()
    jp = os.path.join(tmp, "verify_t.json")
    with open(jp, "w") as f:
        json.dump({"topic": "t", "problem_count": len(problems),
                   "problems": problems}, f)
    out = os.path.join(tmp, "figs_t.tex")
    so, se = io.StringIO(), io.StringIO()
    with redirect_stdout(so), redirect_stderr(se):
        rc = rf.main([jp, out])
    figs = open(out).read() if os.path.exists(out) else ""
    return rc, figs, so.getvalue() + se.getvalue()


def blocks(figs):
    parts = re.split(r"% >>> probfig (\d+)\n", figs)
    return {int(n): chunk for n, chunk in zip(parts[1::2], parts[2::2])}


def coords(block):
    return {m.group(1): (float(m.group(2)), float(m.group(3)))
            for m in re.finditer(
                r"\\coordinate \((\w+)\) at \((-?[\d.]+),(-?[\d.]+)\);", block)}


def labels(block):
    out = [m.group(1) for m in
           re.finditer(r"\\node\[[^\]]*\] at \([^)]*\) \{([^{}]*)\};", block)]
    out += [m.group(1) for m in re.finditer(r'"([^"]*)"', block)]
    return out


def label_numbers(block):
    ns = set()
    for lab in labels(block):
        # subscripts are point names (B_1/B_2), not printed quantities
        lab = re.sub(r"_\{?\d+\}?", "", lab)
        ns |= {float(n) for n in re.findall(r"\d+(?:\.\d+)?", lab)}
    return ns


def dist(p, q):
    return math.hypot(p[0] - q[0], p[1] - q[1])


RIGHT_MARK_RE = re.compile(
    r"\\draw \(-?[\d.]+,-?[\d.]+\) -- \(-?[\d.]+,-?[\d.]+\) "
    r"-- \(-?[\d.]+,-?[\d.]+\);")


def to_scale(name, block, given, unit="deg"):
    """Every drawn side, de-normalized, must equal the solved side to 1e-3."""
    sides, angles = rf._split_given(given, unit)
    sol = solve_triangle(sides, angles)[0]
    s = rf.TARGET_CM / max(sol["a"], sol["b"], sol["c"])
    c = coords(block)
    drawn = {"a": dist(c["B"], c["C"]), "b": dist(c["A"], c["C"]),
             "c": dist(c["A"], c["B"])}
    for k in "abc":
        check(f"{name}: drawn {k} = {sol[k]:.4f} after de-normalization",
              abs(drawn[k] / s - sol[k]) <= 1e-3)
    check(f"{name}: longest drawn side is {rf.TARGET_CM}cm",
          abs(max(drawn.values()) - rf.TARGET_CM) <= 1e-3)
    return sol, s, c


demo = json.load(open(os.path.join(FIXTURES, "figs_demo.json")))["problems"]
rc, figs, out = render(demo)
check("figs_demo renders (exit 0)", rc == 0)
b = blocks(figs)
check("one \\probfig block per figured problem", sorted(b) == [1, 2, 3, 4, 5, 6])
check("dispatcher macro emitted",
      "\\newcommand{\\probfig}[1]{\\csname probfig#1\\endcsname}" in figs)
check("emitted file is ASCII (pdflatex fallback must compile it)",
      all(ord(ch) < 128 for ch in figs))

print("SSS (7, 8, 9):")
to_scale("SSS", b[1], {"a": 7, "b": 8, "c": 9})
check("SSS: all three given sides labelled",
      all(f"${k} = {v}$" in b[1] for k, v in (("a", 7), ("b", 8), ("c", 9))))
check("SSS: solve_for angle A marked '?'", '"$?$"' in b[1] and "--A--" in b[1])

print("SAS (a=7, b=11, C=34):")
sol, s, c = to_scale("SAS", b[2], {"a": 7, "b": 11, "C": 34})
va = (c["A"][0] - c["C"][0], c["A"][1] - c["C"][1])
vb = (c["B"][0] - c["C"][0], c["B"][1] - c["C"][1])
drawn_c = math.degrees(math.acos(
    (va[0] * vb[0] + va[1] * vb[1])
    / (math.hypot(*va) * math.hypot(*vb))))
check("SAS: drawn angle C measures 34 degrees", abs(drawn_c - 34) <= 0.05)
check("SAS: given angle arc labelled", "$34^\\circ$" in b[2])
check("SAS: solve_for side labelled '?'", "$c = ?$" in b[2])
check("SAS: computed answer 6.51 NOT printed anywhere",
      "6.5" not in b[2])

print("ASA with a given right angle (A=90, B=35, c=12):")
to_scale("ASA", b[3], {"A": 90, "B": 35, "c": 12})
check("ASA: right-angle square mark present", RIGHT_MARK_RE.search(b[3]))
check("ASA: no '90' printed — the mark IS the value", 90.0 not in label_numbers(b[3]))
check("ASA: the other given angle keeps its arc", "$35^\\circ$" in b[3])

print("ambiguous SSA (a=6, b=8, A=40) — swing figure:")
sides, angles = rf._split_given({"a": 6, "b": 8, "A": 40}, "deg")
sol1, sol2 = solve_triangle(sides, angles)
s = rf.TARGET_CM / max(sol1["c"], 8.0, 6.0)
c = coords(b[4])
check("SSA: both apexes drawn", "B1" in c and "B2" in c)
check("SSA: solid apex matches solution 1 (c=9.220)",
      abs(c["B1"][0] / s - sol1["c"]) <= 1e-3 and abs(c["B1"][1]) <= 1e-9)
check("SSA: dashed apex matches solution 2 (c=3.037)",
      abs(c["B2"][0] / s - sol2["c"]) <= 1e-3 and abs(c["B2"][1]) <= 1e-9)
check("SSA: shared vertex C matches b*cos/sin(A)",
      abs(c["C"][0] / s - 8 * math.cos(math.radians(40))) <= 1e-3
      and abs(c["C"][1] / s - 8 * math.sin(math.radians(40))) <= 1e-3)
check("SSA: swing side drawn dashed", "dashed" in b[4])
check("SSA: swinging side labelled on BOTH positions", b[4].count("$a = 6$") == 2)
check("SSA: solve_for B marked '?' at both apexes", b[4].count('"$?$"') == 2)

print("right_triangle figure on approx (b=9, A=35):")
sol = solve_triangle({"b": 9.0}, {"A": math.radians(35), "C": math.pi / 2})[0]
s = rf.TARGET_CM / max(sol["a"], sol["b"], sol["c"])
c = coords(b[5])
drawn = {"a": dist(c["B"], c["C"]), "b": dist(c["A"], c["C"]),
         "c": dist(c["A"], c["B"])}
for k in "abc":
    check(f"RT: drawn {k} = {sol[k]:.4f} after de-normalization",
          abs(drawn[k] / s - sol[k]) <= 1e-3)
check("RT: right-angle mark at the implied C", RIGHT_MARK_RE.search(b[5]))
check("RT: unknown labelled with its declared name", "{$x$}" in b[5])
check("RT: given leg labelled bare", "{$9$}" in b[5])
check("RT: computed answer 6.30 NOT printed", "6.3" not in b[5])

print("right_triangle figure on eval (write-the-ratio: a=8, b=15 via 'at'):")
# same renderer path as approx — the figure object is consumed independent of
# the problem's verification type; only the number BINDING source differs
# (eval carries the numbers in its 'at' dict, not as expr literals)
sol = solve_triangle({"a": 8.0, "b": 15.0}, {"C": math.pi / 2})[0]
s = rf.TARGET_CM / max(sol["a"], sol["b"], sol["c"])
c = coords(b[6])
drawn = {"a": dist(c["B"], c["C"]), "b": dist(c["A"], c["C"]),
         "c": dist(c["A"], c["B"])}
for k in "abc":
    check(f"eval-RT: drawn {k} = {sol[k]:.4f} after de-normalization",
          abs(drawn[k] / s - sol[k]) <= 1e-3)
check("eval-RT: right-angle mark at the implied C", RIGHT_MARK_RE.search(b[6]))
check("eval-RT: both legs labelled bare", "{$8$}" in b[6] and "{$15$}" in b[6])
check("eval-RT: asked-about angle keeps its declared name",
      '"$A$"' in b[6])
check("eval-RT: computed hypotenuse 17 NOT printed",
      17.0 not in label_numbers(b[6]))

print("labels never show a non-given number (all blocks):")
givens = {1: {7, 8, 9}, 2: {7, 11, 34}, 3: {35, 12}, 4: {6, 8, 40},
          5: {9, 35}, 6: {8, 15}}
for pid, allowed in givens.items():
    check(f"problem {pid}: label numbers {sorted(label_numbers(b[pid]))} "
          f"⊆ givens {sorted(allowed)}",
          label_numbers(b[pid]) <= {float(v) for v in allowed})

print("error paths (a wrong figure must refuse to render):")
tri = {"id": 1, "type": "triangle", "given": {"a": 1, "b": 2, "c": 99},
       "solve_for": "A", "expected": 1}
rc, figs, out = render([tri])
check("impossible triangle: nonzero exit", rc != 0)
check("impossible triangle: teaching message names the rule",
      "does not form a valid triangle" in out and "shorter than" in out)
check("impossible triangle: NO figs file written", figs == "")

rc, _, out = render([{"id": 1, "type": "approx", "expr": "9*tan(35*pi/180)",
                      "expected": 6.3, "tol": 0.01,
                      "figure": {"kind": "right_triangle",
                                 "given": {"b": 9, "A": 40},
                                 "solve_for": "a"}}])
check("kind (b) value missing from expr: nonzero exit", rc != 0)
check("kind (b) mismatch message names the value", "A=40" in out)

# same binding rule on the eval path: a figure value that is neither an expr
# literal nor an 'at' value must refuse to render
rc, _, out = render([{"id": 1, "type": "eval", "expr": "a/b",
                      "at": {"a": 8, "b": 15}, "expected": "8/15",
                      "figure": {"kind": "right_triangle",
                                 "given": {"a": 8, "b": 16},
                                 "solve_for": "A"}}])
check("eval figure value missing from 'at': nonzero exit", rc != 0)
check("eval mismatch message names the value and the 'at' source",
      "b=16" in out and "'at'" in out)

rc, _, out = render([{"id": 1, "type": "approx", "expr": "2*pi*3",
                      "expected": 18.85, "tol": 0.01,
                      "figure": {"kind": "circle", "given": {"a": 3},
                                 "solve_for": "b"}}])
check("unknown figure kind: nonzero exit", rc != 0)
check("unknown kind message points at the template fallback",
      "latex-templates.md" in out)

rc, _, out = render([
    {"id": 1, "type": "triangle", "given": {"a": 7, "b": 8, "c": 9},
     "solve_for": "A", "expected": 48.19},
    {"id": 1, "type": "triangle", "given": {"a": 7, "b": 8, "c": 10},
     "solve_for": "A", "expected": 44.05}])
check("same id, DIFFERENT givens: nonzero exit", rc != 0)
check("conflict message says to split the ids", "separate problem ids" in out)

rc, figs, _ = render([
    {"id": 1, "type": "triangle", "given": {"a": 7, "b": 8, "c": 9},
     "solve_for": "B", "expected": 60.0},
    {"id": 1, "type": "triangle", "given": {"a": 7, "b": 8, "c": 9},
     "solve_for": "C", "expected": 71.79}])
check("same id, SAME givens: one merged figure", rc == 0
      and len(blocks(figs)) == 1)
check("merged figure marks BOTH solve_fors '?'",
      blocks(figs)[1].count('"$?$"') == 2)

with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
    check("no arguments: usage error", rf.main([]) != 0)
    check("unreadable file: error, not crash",
          rf.main(["/nonexistent/verify_x.json"]) != 0)

print("no-figure sheets still get a valid (empty) figs shell:")
rc, figs, _ = render([{"id": 1, "type": "solve", "expr": "x**2 - 4",
                       "expected": [2, -2]}])
check("exit 0 with no figured problems", rc == 0)
check("dispatcher present, zero blocks",
      "\\csname probfig#1\\endcsname" in figs and not blocks(figs))

print("default output naming (verify_ -> figs_):")
check("verify_algebra_2026.json -> figs_algebra_2026.tex",
      rf.default_out_path("/tmp/verify_algebra_2026.json")
      == "/tmp/figs_algebra_2026.tex")

print("verify.py accepts the 'figure' field (was: unknown-field hard fail):")
ok_marker = {"id": 1, "type": "triangle", "given": {"a": 7, "b": 8, "c": 9},
             "solve_for": "A", "expected": 48.19,
             "figure": {"kind": "triangle"}}
try:
    verify.check_schema(ok_marker)
    check("triangle + opt-in marker passes schema", True)
except verify.VerifyInputError as e:
    check(f"triangle + opt-in marker passes schema ({e})", False)
# eval joined the figure allowlist (write-the-ratio problems are verified as
# eval and inherently need the triangle they read from — the 'at' values are
# the binding source)
ok_ratio = {"id": 1, "type": "eval", "expr": "a/b",
            "at": {"a": 8, "b": 15}, "expected": "8/15",
            "figure": {"kind": "right_triangle", "given": {"a": 8, "b": 15},
                       "solve_for": "A", "unknown": "A"}}
try:
    verify.check_schema(ok_ratio)
    check("eval + right_triangle figure (at-bound) passes schema", True)
except verify.VerifyInputError as e:
    check(f"eval + right_triangle figure passes schema ({e})", False)
for bad in (
    {**ok_marker, "figure": {"kind": "triangle", "a": 7}},   # duplicated given
    {**ok_marker, "figure": {"kind": "sphere"}},             # unknown kind
    {"id": 1, "type": "solve", "expr": "x - 1", "expected": [1],
     "figure": {"kind": "right_triangle", "given": {"a": 1, "b": 1},
                "solve_for": "c"}},                          # wrong type
):
    try:
        verify.check_schema(bad)
        check(f"schema rejects {bad['figure']}", False)
    except verify.VerifyInputError:
        check(f"schema rejects {bad['figure']} on type {bad['type']}", True)

print()
if FAILS:
    print(f"❌ {len(FAILS)} check(s) failed")
    sys.exit(1)
print("✅ all render_figures checks passed")
