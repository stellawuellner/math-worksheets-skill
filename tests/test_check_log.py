#!/usr/bin/env python3
"""
test_check_log.py — pins the log-hygiene gate (scripts/check_log.py).

compile.sh printed "PDF ready" over logs full of undefined references,
missing characters, and 246pt-overfull lines (audit: log hygiene). CI has no
LaTeX engine, so the gate is tested the way compile.sh uses it: against saved
log snippets — a known-bad log must FAIL and a known-good one must PASS.
Run: python3 tests/test_check_log.py
"""
import contextlib
import importlib.util
import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CHECK_LOG = os.path.join(HERE, "..", "scripts", "check_log.py")
BAD = os.path.join(HERE, "fixtures", "texlog_bad.log")
OK = os.path.join(HERE, "fixtures", "texlog_ok.log")

# check_log.py lives in scripts/ (next to compile.sh, its only caller) rather
# than on any package path — load it by file so the scan logic is unit-tested
# in-process, not only through subprocess exit codes
spec = importlib.util.spec_from_file_location("check_log", CHECK_LOG)
check_log = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_log)

FAILS = []


def check(name, cond):
    print(f"  {'✅' if cond else '❌'} {name}")
    if not cond:
        FAILS.append(name)


def run(args, env_extra=None):
    env = dict(os.environ)
    if env_extra:
        env.update(env_extra)
    return subprocess.run([sys.executable, CHECK_LOG, *args],
                          capture_output=True, text=True, env=env)


def main_rc(*argv):
    """check_log.main() in-process (so coverage sees it), output swallowed —
    the ❌ lines it prints are EXPECTED here and would misread as test noise."""
    with contextlib.redirect_stdout(io.StringIO()), \
         contextlib.redirect_stderr(io.StringIO()):
        return check_log.main(["check_log.py", *argv])


print("scan(): rule-by-rule")
bad_text = open(BAD).read()
ok_text = open(OK).read()
failures, warnings = check_log.scan(bad_text, 2.0)
fail_lines = [line for line, _ in failures]
check("bad log: undefined-reference warning FAILS",
      any("Reference `fig:triangle'" in l for l in fail_lines))
check("bad log: 'There were undefined references' FAILS",
      any("There were undefined references" in l for l in fail_lines))
check("bad log: Missing character FAILS",
      any(l.startswith("Missing character") for l in fail_lines))
check("bad log: 246pt overfull hbox FAILS",
      any("246.32002pt" in l for l in fail_lines))

failures, warnings = check_log.scan(ok_text, 2.0)
warn_lines = [line for line, _ in warnings]
check("ok log: zero failures", not failures)
check("ok log: 0.5pt overfull hbox is only a warning (threshold pins at 2pt)",
      any("0.50000pt" in l for l in warn_lines))
check("ok log: overfull VBOX warns, never fails (noisy on full pages)",
      any("\\vbox" in l for l in warn_lines))

failures, _ = check_log.scan(ok_text, 0.1)
check("ok log at 0.1pt threshold: the 0.5pt hbox now FAILS (threshold is live)",
      any("0.50000pt" in l for l, _ in failures))

print("main(): exit codes as compile.sh consumes them (in-process)")
check("bad fixture -> exit 1", main_rc(BAD) == 1)
check("ok fixture -> exit 0", main_rc(OK) == 0)
os.environ["OVERFULL_PT"] = "500"
check("OVERFULL_PT=500 still exit 1 (references fail regardless of overfull)",
      main_rc(BAD) == 1)
os.environ["OVERFULL_PT"] = "not-a-number"
check("garbage OVERFULL_PT -> exit 2 (config error, not a pass)",
      main_rc(OK) == 2)
del os.environ["OVERFULL_PT"]
check("missing file -> exit 2 (usage error, not a pass)",
      main_rc(BAD + ".nope") == 2)
check("no args -> exit 2", main_rc() == 2)

print("CLI: the same contract through the real interpreter boundary")
check("subprocess: bad fixture -> exit 1", run([BAD]).returncode == 1)
check("subprocess: ok fixture -> exit 0", run([OK]).returncode == 0)

print()
if FAILS:
    print(f"❌ {len(FAILS)} check(s) failed")
    sys.exit(1)
print("✅ all check_log tests passed")
