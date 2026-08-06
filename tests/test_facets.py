#!/usr/bin/env python3
"""
test_facets.py — unit coverage for the facet plan gates, misconception traps,
and the interleave structure flag. Behavioral assertions on the teaching
messages (they are contract, not decoration — same discipline as
test_pipeline_fixes.py) plus the pure run/boundary math the fixtures can't
pin precisely.

Run: python3 tests/test_facets.py
"""
import contextlib
import io
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verify  # noqa: E402
import check_prose_consistency as cpc  # noqa: E402

FAILS = []


def check(name, cond):
    print(f"  {'✅' if cond else '❌'} {name}")
    if not cond:
        FAILS.append(name)


def run_data(data):
    """run_verification on an in-memory JSON → (exit code, combined output)."""
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(data, f)
        path = f.name
    out = io.StringIO()
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            rc = verify.run_verification(path)
    finally:
        os.unlink(path)
    return rc, out.getvalue()


def ev(i, facet=None, **extra):
    p = {"id": i, "type": "eval", "expr": f"x + {i}", "at": {"x": 1},
         "expected": i + 1}
    if facet:
        p["facet"] = facet
    p.update(extra)
    return p


print("Interleave window math (window = positions floor(n/3)+1..n):")
for n, want in ((12, 4), (13, 4), (14, 4), (20, 6)):
    boundary, _ = verify._interleave_violations(["a"] * n)
    check(f"n={n} → boundary {want}", boundary == want)

print("Run truncation at the boundary:")
# n=13, boundary 4: a 5-run at positions 3..7 has in-window portion 3 → legal
_, v = verify._interleave_violations(
    ["x", "x"] + ["y"] * 5 + ["z", "z", "z", "x", "y", "z"])
check("straddling run with in-window portion 3 → no violation", v == [])
# same shape shifted right: positions 4..8 → in-window portion 4 → violation
_, v = verify._interleave_violations(
    ["x", "x", "z"] + ["y"] * 5 + ["z", "z", "x", "y", "z"])
check("straddling run with in-window portion 4 → violation",
      len(v) == 1 and v[0][0] == "y" and v[0][3] == 4)
# an exact 3-run fully inside the window is legal
_, v = verify._interleave_violations(
    ["x", "y", "x", "y", "z", "z", "z", "x", "y"])
check("exact in-window 3-run → no violation", v == [])

print("All-or-none facet tagging (exit 1 with a teaching message):")
rc, out = run_data({"topic": "t", "problem_count": 2,
                    "problems": [ev(1, "ratio"), ev(2)]})
check("partial tagging exits 1", rc == 1)
check("message says tag every problem's facet or none",
      "tag every problem's facet or none" in out)

print("Facet plan gate messages:")
rc, out = run_data({"topic": "t", "problem_count": 1,
                    "facets": ["pythagorean"],
                    "problems": [ev(1, "pythagoras")]})
check("unlisted facet exits 1 and suggests the closest listed one",
      rc == 1 and "did you mean 'pythagorean'" in out)
rc, out = run_data({"topic": "t", "problem_count": 1,
                    "facets": ["ratio", "depression"],
                    "problems": [ev(1, "ratio")]})
check("orphan planned facet exits 1 naming the fix",
      rc == 1 and "facet 'depression' has no problems" in out)
rc, out = run_data({"topic": "t", "problem_count": 1,
                    "facets": ["ratio", "ratio"],
                    "problems": [ev(1, "ratio")]})
check("duplicate facets in the plan are rejected",
      rc == 1 and "unique" in out)
rc, out = run_data({"topic": "t", "problem_count": 1, "subtitle": "  ",
                    "problems": [ev(1)]})
check("blank subtitle is rejected", rc == 1 and "subtitle" in out)
rc, out = run_data({"topic": "t", "problem_count": 1,
                    "problems": [ev(1, "Bad_Slug")]})
check("non-kebab facet slug is a schema failure",
      rc == 1 and "lowercase-kebab" in out)

print("Interleave report paths:")
blocked = {"topic": "t", "problem_count": 14, "problems":
           [ev(i + 1, f) for i, f in enumerate(
               ["ratio", "pythagorean", "ratio", "pythagorean",
                "inverse", "inverse", "inverse", "inverse", "inverse",
                "ratio", "pythagorean", "ratio", "pythagorean", "ratio"])]}
rc, out = run_data(blocked)
check("blocked run flags exit 2 (manual review, not a block)", rc == 2)
check("violation names the run ids and facet",
      "'inverse'" in out and "ids [5, 6, 7, 8, 9]" in out)
check("violation suggests a concrete different-facet swap",
      "swap id 7 with id 10 (facet 'ratio')" in out)
check("facet mix line reports the max in-window run",
      "max in-window run: 5" in out)
rc, out = run_data(dict(blocked, format="drill"))
check("format drill waives the interleave check (exit 0)",
      rc == 0 and "interleave check waived" in out)
rc, out = run_data({"topic": "t", "problem_count": 12,
                    "problems": [ev(i + 1, "ratio") for i in range(12)]})
check("single facet is informational only (exit 0)",
      rc == 0 and "single facet 'ratio'" in out)
rc, out = run_data({"topic": "t", "problem_count": 12,
                    "problems": [ev(i + 1) for i in range(12)]})
check("12+ facetless problems get the skip warning, exit unchanged",
      rc == 0 and "interleave check skipped" in out)
check("10+ facetless problems get the declare-facets nudge",
      'no "facets" declared' in out)
rc, out = run_data({"topic": "t", "problem_count": 1, "format": "quiz",
                    "problems": [ev(1)]})
check("unknown format exits 1 naming the allowed value",
      rc == 1 and '"drill"' in out)

print("Facet histogram:")
rc, out = run_data({"topic": "t", "problem_count": 3,
                    "problems": [ev(1, "ratio"), ev(2, "ratio"),
                                 ev(3, "inverse")]})
check("histogram line printed next to the tag report",
      rc == 0 and "facets: ratio×2, inverse×1" in out)

print("Trap schema rejections teach the fix:")


def schema_error(problem):
    try:
        verify.check_schema(problem)
        return None
    except verify.VerifyInputError as e:
        return str(e)


msg = schema_error({"id": 1, "type": "manual", "desc": "sketch",
                    "traps": [{"desc": "x", "expr": "1"}]})
# A manual review flag still has nothing to be distinguishable FROM, so it
# still cannot carry traps. The wording changed with solution-set traps: the
# rule is no longer "a single comparable answer" — solve/zeros/solve_interval
# now take traps too, declaring the wrong ROOT SET via "exprs".
check("trap on manual → names the comparable-answer rule and the allowed types",
      msg is not None and "cannot carry traps" in msg
      and "comparable answer" in msg and "solve" in msg)
msg = schema_error({"id": 1, "type": "approx", "expr": "2+2", "expected": 4,
                    "traps": [{"desc": "x", "expr": "5", "wrong": 5}]})
check("unknown trap key → rejected with the trap shape",
      msg is not None and "unknown field" in msg and "wrong" in msg)
msg = schema_error({"id": 1, "type": "approx", "expr": "2+2", "expected": 4,
                    "traps": [{"desc": "  ", "expr": "5"}]})
check("blank trap desc rejected", msg is not None and "desc" in msg)
msg = schema_error({"id": 1, "type": "approx", "expr": "2+2", "expected": 4,
                    "traps": []})
check("empty traps list rejected", msg is not None and "non-empty" in msg)

print("Trap distinguishability semantics (check_traps):")
ok, info = verify.check_traps(
    {"id": 1, "type": "eval", "expr": "sin(x)", "at": {"x": "pi/3"},
     "expected": "sqrt(3)/2",
     "traps": [{"desc": "used cos instead of sin", "expr": "cos(pi/3)"}]})
check("symbolic expected: distinguishable trap passes "
      "(the naive rounds-to gate would false-fail here)", ok)
ok, info = verify.check_traps(
    {"id": 1, "type": "triangle", "given": {"a": 3, "b": 3, "C": 90},
     "solve_for": "A", "expected": 45.0,
     "traps": [{"desc": "swapped opposite and adjacent",
                "expr": "atan(3/3)*180/pi"}]})
check("indistinguishable trap fails with the change-the-givens message",
      not ok and "cannot distinguish" in info)
ok, info = verify.check_traps(
    {"id": 1, "type": "approx", "expr": "9*tan(35*pi/180)", "expected": 6.30,
     "tol": 0.01,
     "traps": [{"desc": "used cos", "expr": "9*cos(35*pi/180)",
                "value": 7.99}]})
check("printed value drifting from its own expr fails",
      not ok and "derive the printed number from the expr" in info)
ok, info = verify.check_traps(
    {"id": 1, "type": "approx", "expr": "2+2", "expected": 4,
     "traps": [{"desc": "kept a variable", "expr": "x + 1"}]})
check("non-numeric trap expr fails loudly", not ok and "fully numeric" in info)
ok, info = verify.check_traps(
    {"id": 1, "type": "approx", "expr": "2+2", "expected": 4,
     "traps": [{"desc": "typo", "expr": "qqjw(2)"}]})
check("disallowed trap expr fails through the allowlist",
      not ok and "bad expr" in info)
ok, info = verify.check_traps(
    {"id": 1, "type": "slope", "points": [[2, 1], [2, 9]],
     "expected": "undefined",
     "traps": [{"desc": "inverted", "expr": "0"}]})
check("non-comparable expected fails with a teaching message",
      not ok and "not numerically comparable" in info)

print("Trap tally is printed (every honored comparison is visible):")
rc, out = run_data({"topic": "t", "problem_count": 1, "problems": [
    {"id": 1, "type": "approx", "expr": "9*tan(35*pi/180)", "expected": 6.30,
     "tol": 0.01,
     "traps": [{"desc": "used cos instead of tan",
                "expr": "9*cos(35*pi/180)", "value": 7.37}]}]})
check("trap run passes with the declared/distinguishable tally",
      rc == 0 and "traps: 1 declared, all distinguishable" in out)

print("--schema documents the new fields (doc-drift guard):")
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    verify.print_schema("table")
table = buf.getvalue()
for token in ('"facets"', '"subtitle"', '"traps"', "facet"):
    check(f"schema table mentions {token}", token in table)
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    verify.print_schema("json")
machine = json.loads(buf.getvalue())
check("schema json lists top-level optional fields",
      machine.get("top_level_optional") == ["facets", "format", "subtitle"])
check("schema json lists the trap-allowed types",
      set(machine.get("traps_allowed_types", [])) == verify._TRAP_TYPES)
check("facet and traps are universal optional fields",
      {"facet", "traps"} <= set(machine["universal_optional"]))

print("Prose binder: desc excluded at every depth, trap numbers are givens:")
entry = {"id": 1, "type": "approx", "expr": "9*sin(35*pi/180)",
         "expected": 5.16,
         "traps": [{"desc": "used 3 instead of 4",
                    "expr": "9*cos(35*pi/180)", "value": 7.37}]}
nums = cpc.json_numbers(entry)
check("nested trap desc numbers do NOT count as givens",
      3.0 not in nums and 4.0 not in nums)
check("trap expr/value numbers DO count as givens",
      7.37 in nums and 9.0 in nums and 5.16 in nums)

# ── Solution-set traps ────────────────────────────────────────────────────
# solve/zeros/solve_interval were excluded from traps because "there is nothing
# to be distinguishable from on a root LIST". That is backwards for the topics
# where dropping a root IS the misconception. One reviewed case whose declared
# focus was "diagnosing incomplete root sets" could declare none of its six
# planted wrong answers, because every one of them was a set.
print("Solution-set traps (solve / zeros / solve_interval):")

ok, info = verify.check_traps(
    {"id": 1, "type": "solve", "expr": "x**2 - 9", "var": "x",
     "expected": [3, -3],
     "traps": [{"desc": "took only the positive square root",
                "exprs": ["3"], "value": [3]}]})
check("a dropped root is a distinguishable trap",
      ok and any("drops -3" in ln for ln in info))

ok, info = verify.check_traps(
    {"id": 1, "type": "solve", "expr": "x**2 - 9", "var": "x",
     "expected": [3, -3],
     "traps": [{"desc": "same set", "exprs": ["3", "-3"]}]})
check("a trap set equal to the answer fails with change-the-givens",
      not ok and "cannot distinguish" in info)

ok, info = verify.check_traps(
    {"id": 1, "type": "solve", "expr": "x**2 - 4", "var": "x",
     "expected": [2, -2],
     "traps": [{"desc": "extraneous root from squaring", "exprs": ["2", "-2", "5"]}]})
check("an extraneous root is expressible too",
      ok and any("adds 5" in ln for ln in info))

ok, info = verify.check_traps(
    {"id": 1, "type": "solve", "expr": "x**2 - 9", "var": "x",
     "expected": [3, -3],
     "traps": [{"desc": "drift", "exprs": ["3"], "value": [7]}]})
check("a printed set drifting from its own exprs fails",
      not ok and "does not match" in info)

msg = schema_error({"id": 1, "type": "solve", "expr": "x - 1", "var": "x",
                    "expected": [1],
                    "traps": [{"desc": "d", "expr": "2"}]})
check("a scalar expr on a solution-set type is rejected",
      msg is not None and "exprs" in msg)

msg = schema_error({"id": 1, "type": "eval", "expr": "2+2", "expected": 4,
                    "traps": [{"desc": "d", "exprs": ["5"]}]})
check("exprs on a scalar type is still rejected",
      msg is not None)

print()
if FAILS:
    print(f"❌ {len(FAILS)} facet/trap/interleave test(s) failed: {FAILS}")
    sys.exit(1)
print("✅ All facet/trap/interleave tests passed")
