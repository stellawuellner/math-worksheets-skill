#!/usr/bin/env python3
r"""test_cli_contracts.py — the command-line surface build.sh actually calls.

Every script here is invoked BY PATH from build.sh or by an author debugging a
gate, so the __main__ dispatch, the usage text, and the file-error messages are
contract, not plumbing. They were also dark: coverage.sh runs the suites
in-process, and an `if __name__ == "__main__"` block only executes under a
__main__ run. runpy.run_path(run_name="__main__") gives exactly that, in
process, so these tests count — and more importantly, they pin the behaviour
an author sees at the shell: the exit code and the sentence that teaches the
fix.

The rule for what belongs here: a case must assert something a shell caller
depends on. No case exists only to turn a line green.
"""
import contextlib
import io
import json
import os
import runpy
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")
FAILS = []


def check(label, cond, detail=""):
    print(f"  {'✅' if cond else '❌'} {label}")
    if not cond:
        FAILS.append(f"{label}{': ' + detail if detail else ''}")


def run_cli(script, argv):
    """Run scripts/<script> as __main__ with argv, capturing exit and output."""
    out, err = io.StringIO(), io.StringIO()
    old_argv = sys.argv
    code = 0
    try:
        sys.argv = [os.path.join(SCRIPTS, script)] + list(argv)
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                runpy.run_path(os.path.join(SCRIPTS, script),
                               run_name="__main__")
            except SystemExit as e:
                code = e.code if isinstance(e.code, int) else (0 if e.code is None else 1)
    finally:
        sys.argv = old_argv
    return code, out.getvalue(), err.getvalue()


print("verify.py CLI:")
code, out, err = run_cli("verify.py", ["--schema"])
check("--schema exits 0 and prints the type table",
      code == 0 and "problem types" in out and "| approx |" in out)
code, out, err = run_cli("verify.py", ["--schema", "json"])
ok = code == 0
try:
    schema = json.loads(out)
except ValueError:
    ok = False
    schema = {}
check("--schema json is valid JSON with the top-level contract",
      ok and schema.get("top_level_optional") == ["facets", "format",
                                                  "subtitle", "pages"])
code, out, err = run_cli("verify.py", [])
check("no arguments exits 1 with usage on stderr",
      code == 1 and "Usage:" in err)
code, out, err = run_cli("verify.py", ["/nonexistent/verify_x.json"])
check("a missing file exits 1 and names the path",
      code == 1 and "file not found" in err and "/nonexistent/" in err)

print("\npage_budget.py CLI:")
with tempfile.TemporaryDirectory() as d:
    vj = os.path.join(d, "verify_t.json")
    json.dump({"topic": "t", "problem_count": 2, "problems": [
        {"id": 1, "type": "eval", "expr": "1+1", "expected": 2},
        {"id": 2, "type": "eval", "expr": "2+2", "expected": 4}]},
        open(vj, "w"))
    code, out, err = run_cli("page_budget.py",
                             [vj, "--type-size", "17pt",
                              "--accessible", "both", "--max-pages"])
    check("--type-size/--accessible parse and yield an integer cap",
          code == 0 and out.strip().isdigit(), f"{code} {out!r} {err!r}")
    cap_17 = int(out.strip()) if out.strip().isdigit() else 0
    code, out, err = run_cli("page_budget.py", [vj, "--max-pages"])
    cap_12 = int(out.strip()) if out.strip().isdigit() else 99
    check("17pt 'both' is never allowed fewer pages than 12pt plain",
          cap_17 >= cap_12, f"17pt={cap_17} 12pt={cap_12}")
    # --from-tex pointing at a file that does not exist must fall back to the
    # defaults, not crash: build.sh calls this before compile, when a typo'd
    # path is exactly the kind of input it gets.
    code, out, err = run_cli("page_budget.py",
                             [vj, "--from-tex", os.path.join(d, "no.tex"),
                              "--max-pages"])
    check("--from-tex with a missing file falls back instead of crashing",
          code == 0 and out.strip().isdigit(), f"{code} {err!r}")

print("\nrender_quick_answers.py CLI:")
code, out, err = run_cli("render_quick_answers.py", ["only-one-arg"])
check("wrong arity exits 1 with usage",
      code == 1 and "Usage:" in err)
with tempfile.TemporaryDirectory() as d:
    vj = os.path.join(d, "verify_t.json")
    open(vj, "w").write("{not json")
    ak = os.path.join(d, "ak_t.tex")
    open(ak, "w").write("\\input{qa_t}\n")
    code, out, err = run_cli("render_quick_answers.py", [vj, ak])
    check("unreadable JSON exits 1 and says so",
          code == 1 and "Error reading input" in err)
    code, out, err = run_cli("render_quick_answers.py",
                             [os.path.join(d, "missing.json"), ak])
    check("a missing verify file exits 1 through the same door",
          code == 1 and "Error reading input" in err)

print("\nrender_meta.py / render_figures.py CLI:")
code, out, err = run_cli("render_meta.py", [])
check("render_meta with no args exits nonzero with usage",
      code != 0 and ("Usage" in err or "usage" in err.lower()), f"{code} {err!r}")
code, out, err = run_cli("render_figures.py", [])
check("render_figures with no args exits nonzero with usage",
      code != 0 and ("Usage" in err or "usage" in err.lower()), f"{code} {err!r}")



# ── The environment guards, exercised in-process ─────────────────────────────
# verify.py's import guard and version floor are the two messages an author in
# a broken environment actually reads, and both were dark: the guard cannot
# fire while sympy imports, and the floor cannot fire while the installed
# sympy is current. Both are reachable in-process by executing verify.py's
# source under a doctored sys.modules — no subprocess, so coverage sees it,
# and the assertion is on the MESSAGE, which has been wrong before (audit
# D1b: the pip command must name the exact interpreter, because `pip3
# install sympy` routinely feeds a different python than the one that failed).
print("\nenvironment guards (doctored sys.modules):")


def run_verify_source(sympy_stub):
    src = open(os.path.join(SCRIPTS, "verify.py")).read()
    err = io.StringIO()
    saved = {k: sys.modules.get(k) for k in ("sympy", "mpmath")}
    code = None
    try:
        sys.modules["sympy"] = sympy_stub
        if sympy_stub is None:
            sys.modules.pop("sympy", None)
            sys.modules["sympy"] = None  # import raises ImportError
        with contextlib.redirect_stderr(err):
            try:
                exec(compile(src, os.path.join(SCRIPTS, "verify.py"), "exec"),
                     {"__name__": "verify_guard_probe"})
            except SystemExit as e:
                code = e.code
    finally:
        for k, v in saved.items():
            if v is None:
                sys.modules.pop(k, None)
            else:
                sys.modules[k] = v
    return code, err.getvalue()


code, err = run_verify_source(None)
check("with no sympy, verify.py exits 1 and teaches the exact fix",
      code == 1 and "cannot import" in err
      and f"{sys.executable} -m pip install sympy" in err, err[:200])

import types  # noqa: E402
old_sympy = sys.modules["sympy"] if "sympy" in sys.modules else __import__("sympy")
stub = types.ModuleType("sympy")
for name in dir(old_sympy):
    setattr(stub, name, getattr(old_sympy, name))
stub.__version__ = "1.9"
code, err = run_verify_source(stub)
check("below the floor, verify.py refuses and says the failures are silent",
      code == 1 and "older than" in err and "silent" in err, err[:200])

print()
if FAILS:
    print(f"❌ {len(FAILS)} CLI-contract check(s) failed:")
    for x in FAILS:
        print(f"   {x}")
    sys.exit(1)
print("✅ the shell-facing contracts hold")

print("\nrender_figures on a non-verify JSON:")
with tempfile.TemporaryDirectory() as d:
    nv = os.path.join(d, "verify_x.json")
    open(nv, "w").write('{"just": "an object"}')
    code2, out2, err2 = run_cli("render_figures.py", [nv])
    check("a JSON without a problems list is refused with the shape named",
          code2 == 1 and "problems" in err2, err2[:150])

print("\nthe machine-check floor at the CLI:")
with tempfile.TemporaryDirectory() as d:
    av = os.path.join(d, "verify_allmanual.json")
    json.dump({"topic": "proofs", "problem_count": 2, "problems": [
        {"id": 1, "type": "manual", "desc": "two-column proof"},
        {"id": 2, "type": "manual", "desc": "construction"}]}, open(av, "w"))
    code3, out3, err3 = run_cli("verify.py", [av])
    check("an all-manual sheet without the acknowledgement exits 1 and "
          "teaches allow_all_manual",
          code3 == 1 and "allow_all_manual" in err3, err3[:160])
    json.dump({"topic": "proofs", "problem_count": 2, "allow_all_manual": True,
               "problems": [
                   {"id": 1, "type": "manual", "desc": "two-column proof"},
                   {"id": 2, "type": "manual", "desc": "construction"}]},
              open(av, "w"))
    code3, out3, err3 = run_cli("verify.py", [av])
    check("with the acknowledgement it exits 2 (manual review), not 1",
          code3 == 2, f"{code3} {err3[:120]}")
