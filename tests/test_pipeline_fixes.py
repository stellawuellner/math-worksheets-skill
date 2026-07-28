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
if FAILS:
    print(f"❌ {len(FAILS)} pipeline-fix test(s) failed: {FAILS}")
    sys.exit(1)
print("✅ All pipeline-fix tests passed")
