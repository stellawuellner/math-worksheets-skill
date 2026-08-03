#!/usr/bin/env python3
"""
test_pipeline_fixes.py — pins the pipeline-enforceability fixes (audit #4/#6/#9
+ bootstrap backlog): the explicit-tol clamp and its tol_reason valve, the
teaching allowlist rejections, --schema's completeness, and the friendly
missing-sympy path. Message-content assertions are deliberate: these messages
are the product (they teach the fix), so they are contract, not decoration.

Run: python3 tests/test_pipeline_fixes.py
"""
import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import verify  # noqa: E402

FAILS = []
VERIFY_PY = os.path.join(os.path.dirname(__file__), "..", "scripts", "verify.py")


def check(name, cond):
    print(f"  {'✅' if cond else '❌'} {name}")
    if not cond:
        FAILS.append(name)


def rejection_message(problem):
    """Run a problem expected to be rejected; return the error text."""
    try:
        verify.check_problem(problem, problem["type"])
        return None
    except verify.VerifyInputError as e:
        return str(e)


print("Explicit-tol clamp (audit #9 — 'tol': 2.0 waved an 18%-wrong answer through):")
oversize = {"id": 1, "type": "triangle", "given": {"a": 7, "B": 49, "C": 90},
            "solve_for": "b", "expected": 9.5, "tol": 2.0}
msg = rejection_message(oversize)
check("oversize tol without tol_reason → rejected", msg is not None)
check("rejection names the ceiling and both fixes",
      msg is not None and "tol_reason" in msg and "1%" in msg)
verify.WIDE_TOLS.clear()
with_reason = dict(oversize, expected=8.05,
                   tol_reason="estimation drill — compounding rounding")
check("same tol WITH tol_reason → check runs and passes",
      verify.check_problem(with_reason, "triangle")[0] == "PASS")
check("widened tol is tallied in WIDE_TOLS (never invisible)",
      len(verify.WIDE_TOLS) == 1 and verify.WIDE_TOLS[0][0] == 1)
check("integer expected keeps the 0.5 half-ulp floor (round-to-integer sheets)",
      verify.check_problem({"id": 1, "type": "approx", "expr": "22.1",
                            "expected": 22, "tol": 0.4}, "approx")[0] == "PASS")
check("sane explicit tol (within 1%) unaffected",
      verify.check_problem({"id": 1, "type": "approx", "expr": "9*tan(35*pi/180)",
                            "expected": 6.30, "tol": 0.01}, "approx")[0] == "PASS")
check("default-tol path (no explicit tol) never clamps",
      verify.check_problem({"id": 1, "type": "approx", "expr": "sqrt(2)",
                            "expected": 1.41}, "approx")[0] == "PASS")
check("empty tol_reason does not count as acknowledgement",
      rejection_message(dict(oversize, tol_reason="  ")) is not None)

print("Allowlist rejections teach the fix (audit backlog #12/#18):")


def parse_error(expr):
    try:
        verify.safe_parse(expr)
        return None
    except verify.VerifyInputError as e:
        return str(e)


check("rad() → points at the <deg>*pi/180 idiom",
      "pi/180" in (parse_error("7*tan(rad(65))") or ""))
check("deg() → points at 180/pi",
      "180/pi" in (parse_error("deg(2)") or ""))
check("arcsin → suggests asin", "asin" in (parse_error("arcsin(x)") or ""))
check("e → suggests capital E for Euler's number",
      "'E'" in (parse_error("2*e") or ""))
check("typo gets a close-match suggestion",
      "did you mean" in (parse_error("coss(x)") or ""))
check("any rejection lists the allowed vocabulary",
      "Allowed functions:" in (parse_error("qqjw(x)") or ""))

print("--schema (audit backlog #11 — the reference cannot go stale):")
# in-process (also keeps print_schema inside the coverage floor)
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    rc_table = verify.print_schema("table")
table = buf.getvalue()
check("schema table exits 0", rc_table == 0)
check(f"schema table lists all {len(verify.SCHEMAS)} types",
      all(f"| {t} |" in table for t in verify.SCHEMAS))
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    rc_json = verify.print_schema("json")
try:
    machine = json.loads(buf.getvalue())
except json.JSONDecodeError:
    machine = None
check("schema json is valid JSON with every type",
      rc_json == 0 and machine is not None
      and set(machine["types"]) == set(verify.SCHEMAS))
check("schema json carries the allowlist",
      machine is not None and set(machine["functions"]) == set(verify._FUNCS))
check("unknown schema mode is a usage error", verify.print_schema("nope") == 1)
# and through the real CLI, so the argv wiring is exercised too
r = subprocess.run([sys.executable, VERIFY_PY, "--schema"],
                   capture_output=True, text=True)
check("verify.py --schema CLI exits 0 and is complete",
      r.returncode == 0 and all(f"| {t} |" in r.stdout for t in verify.SCHEMAS))

print("EXAMPLES are verified data, not illustration (every example must run):")
bad = []
for t in verify.SCHEMAS:
    ex = verify.EXAMPLES.get(t)
    if ex is None:
        bad.append(f"{t}: no example")
        continue
    try:
        ptype = verify.check_schema(ex)
        status, _ = verify.check_problem(ex, ptype)
        if status not in ("PASS", "MANUAL"):
            bad.append(f"{t}: example {status}")
    except Exception as e:  # noqa: BLE001 — any crash is a failed example
        bad.append(f"{t}: {e}")
check("every type's canonical example passes its own check", not bad)
for b in bad:
    print(f"      · {b}")

print("Missing-sympy path (audit backlog #2/#10 — no raw traceback):")
with tempfile.TemporaryDirectory() as td:
    # a sympy that cannot import simulates the bare interpreter
    with open(os.path.join(td, "sympy.py"), "w") as f:
        f.write("raise ImportError('forced by test_pipeline_fixes')\n")
    env = dict(os.environ, PYTHONPATH=td)
    r = subprocess.run([sys.executable, VERIFY_PY, "--schema"],
                       capture_output=True, text=True, env=env)
    check("sympy-less run exits 1 (not a traceback crash)", r.returncode == 1)
    check("sympy-less run teaches the interpreter-specific install command",
          "-m pip install sympy" in r.stderr and "Traceback" not in r.stderr)

print()
print("Bookkeeping fields are not printed givens:")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
import check_prose_consistency as prose  # noqa: E402

# A "difficulty": 3 tag donated 3 to the set of numbers the prose is allowed to
# print, so a stem showing a stray 3 that nothing verifies could not be reported
# as drift. Found because one stem flagged a phantom value in isolation and went
# quiet in the real run; the only difference was the difficulty tag. The failure
# direction is a silent pass, which is the direction every other checker here is
# careful about. "standard" was the same leak and worse: "3.OA.C.7" donated a 3
# and a 7 to every problem carrying it.
_ENTRY = {"id": 1, "type": "eval", "expr": "a*b", "at": {"a": 7, "b": 2},
          "expected": 14, "difficulty": 3, "workspace_cm": 5.0,
          "standard": "3.OA.C.7", "word_problem": True}
_givens = prose.json_numbers(_ENTRY)
check("the mathematics still donates its givens", {7.0, 2.0, 14.0} <= _givens)
check("a difficulty tag does not", 3.0 not in _givens)
check("nor a workspace declaration", 5.0 not in _givens)
check("nor the digits of a standards code", 7.0 in _givens and 3.0 not in _givens)

# THE RULE, asserted rather than trusted. The first version of this list was
# written by analogy and excluded "points" — which sounds like an effort-marker
# score and is in fact the coordinate list for distance/midpoint/slope/
# polygon_area. Every coordinate-geometry problem flagged its own coordinates.
# A name any verify TYPE declares carries mathematics and cannot be bookkeeping;
# the only exceptions are tol/tol_reason, machinery for the comparison rather
# than anything a student reads.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
_declared = {f for req, opt in verify.SCHEMAS.values() for f in set(req) | set(opt)}
_leaked = sorted((prose._BOOKKEEPING - prose._TOLERANCE_MACHINERY) & _declared)
check(f"no type-declared field is treated as bookkeeping{'' if not _leaked else ' — ' + str(_leaked)}",
      not _leaked)
check("a slope problem's coordinates are still givens",
      {-2.0, 1.0, 2.0, 3.0} <= prose.json_numbers(
          {"id": 1, "type": "slope", "points": [[-2, 1], [2, 3]],
           "expected": "1/2", "difficulty": 3}))

print()
print("Inverse notation is a name, not a number:")
check("$f^{-1}(x)$ contributes no phantom 1",
      prose.prose_numbers(r"Find $f^{-1}(x)$ and evaluate $f^{-1}(8)$.") == {8.0})
# A general exponent CAN be a printed given, so only the -1 is stripped.
check("a real exponent survives",
      prose.prose_numbers(r"A square of side $3$ has area $3^2$.") == {2.0, 3.0})

print()
print("A thousands separator is punctuation inside one numeral:")
# "47{,}308" scanned as 47 and 308, so a grade 4-5 place-value worksheet
# reported 15.4% matched and could not have detected a real mistyped given
# anywhere on the sheet. check_answer_key has stripped both spellings all
# along; only this side was missing them.
check("the LaTeX spelling is one number",
      prose.prose_numbers(r"The town has $47{,}308$ people.") == {47308.0})
check("the plain spelling is the same number",
      prose.prose_numbers(r"The town has $47,308$ people.") == {47308.0})
check("and matches the unseparated form",
      prose.prose_numbers(r"$47308$") == prose.prose_numbers(r"$47{,}308$"))
# The lookahead needs exactly three digits, so ordinary commas are untouched.
check("a coordinate pair is not merged",
      prose.prose_numbers(r"Points $(3,4)$ and $(5,6)$.") == {3.0, 4.0, 5.0, 6.0})
check("a comma-separated list is not merged",
      prose.prose_numbers(r"$1, 2, 3$") == {1.0, 2.0, 3.0})

print()
if FAILS:
    print(f"❌ {len(FAILS)} pipeline-fix test(s) failed: {FAILS}")
    sys.exit(1)
print("✅ All pipeline-fix tests passed")
