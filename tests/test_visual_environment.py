#!/usr/bin/env python3
"""Pin the environment guard in visual_regression.py.

The guard exists because of a specific incident: a branch arrived carrying
seven re-recorded baselines that failed the harness at 6.6%, while the same
branch's code rendered at 0/2304 against the previous baselines. The baselines
had been recorded on a different font and rasteriser stack; the design had not
moved at all. Merging them would have made every later contributor's first run
red, and the reflex answer to a red baseline is --approve.

So the guard's behaviour is itself a contract, and it is tested here rather
than only in the harness it protects. Rendering is stubbed, so these checks run
in milliseconds and — more to the point — run on a machine with no TeX at all,
which is where the rest of the suite already lives.
"""
import contextlib
import io
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import visual_regression as vr  # noqa: E402

FAILS = []


def check(name, condition, detail=""):
    print(f"  {'✅' if condition else '❌'} {name}")
    if not condition:
        FAILS.append(f"{name}{': ' + detail if detail else ''}")


def fake_page(ink):
    """A GRID x GRID page whose every cell carries `ink` (0-255 grey)."""
    w = h = vr.GRID * 2
    return w, h, bytes([255 - ink]) * (w * h)


def run(argv, pages, env, strict=False):
    """Drive main() with rendering, environment and $CWD-free state stubbed."""
    real = (vr.render, vr.engine, vr.environment, shutil.which,
            sys.argv, os.environ.get("MWS_VISUAL_STRICT"))
    out = io.StringIO()
    try:
        vr.render = lambda name, tex, workdir: [fake_page(pages(name))]
        vr.engine = lambda: "/usr/bin/pdflatex"
        vr.environment = lambda: dict(env)
        shutil.which = lambda tool: "/usr/bin/" + tool
        sys.argv = ["visual_regression.py", *argv]
        os.environ["MWS_VISUAL_STRICT"] = "1" if strict else "0"
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            rc = vr.main()
    finally:
        (vr.render, vr.engine, vr.environment, shutil.which,
         sys.argv, prior) = real
        if prior is None:
            os.environ.pop("MWS_VISUAL_STRICT", None)
        else:
            os.environ["MWS_VISUAL_STRICT"] = prior
    return rc, out.getvalue()


HOME = {"engine": "pdfTeX 1.40.25", "raster": "pdftoppm 24.02.0",
        "grid": str(vr.GRID), "dpi": str(vr.DPI),
        "tolerance": str(vr.CELL_TOLERANCE)}
AWAY = dict(HOME, raster="pdftoppm 99.0.0")

# Every document renders at ink level 40 on the machine that recorded the
# baselines; "elsewhere" everything shifts, canaries included, which is what a
# different font stack does.
same = lambda name: 40
elsewhere = lambda name: 60
# A design change moves one case and leaves the canaries alone — the one
# situation in which a page diff is genuinely about the design.
design_change = lambda name: 60 if name == "answer_lines" else 40

tmp = tempfile.mkdtemp()
vr.BASELINE = os.path.join(tmp, "baseline")
vr.ENVIRONMENT_FILE = os.path.join(vr.BASELINE, "ENVIRONMENT.txt")

print("Bootstrap:")
rc, out = run([], same, HOME)
check("a first run records baselines and an environment record", rc == 0)
check("the environment record is written", os.path.exists(vr.ENVIRONMENT_FILE))
check("a canary baseline is recorded per font stack",
      all(os.path.exists(os.path.join(vr.BASELINE, f"{c}-1.txt")) for c in vr.CANARIES))
check("the recorded environment reads back identically", vr.read_environment() == HOME)

rc, out = run([], same, HOME)
check("the same machine then passes cleanly",
      rc == 0 and "matches the approved baselines" in out)

print("A different machine cannot fail, approve, or be ignored:")
rc, out = run([], elsewhere, AWAY)
check("drift is advisory, not a red build", rc == 0)
check("drift says the gate did not run", "did NOT run" in out)
check("drift names the tool that moved", "pdftoppm 99.0.0" in out)
check("page diffs are shown but marked informational",
      "informational" in out and "❌" not in out)

rc, out = run([], elsewhere, AWAY, strict=True)
check("MWS_VISUAL_STRICT turns drift into a failure", rc == 1)
check("strict mode explains why an advisory gate is not enough",
      "tests nothing" in out)

# The incident itself: same declared versions, different rendering. Version
# strings alone would call this machine identical; the canary is what catches it.
rc, out = run([], elsewhere, HOME)
check("a version-identical machine that renders differently is still caught",
      rc == 0 and "did NOT run" in out)
check("the canary is what reports it", "canary_" in out)

before = {f: open(os.path.join(vr.BASELINE, f)).read() for f in os.listdir(vr.BASELINE)}
rc, out = run(["--approve"], elsewhere, AWAY)
check("--approve is refused from a drifted environment", rc == 2)
check("the refusal names --rebase-environment as the deliberate route",
      "--rebase-environment" in out)
check("a refused --approve leaves every baseline untouched",
      before == {f: open(os.path.join(vr.BASELINE, f)).read()
                 for f in os.listdir(vr.BASELINE)})

rc, out = run(["--rebase-environment"], same, HOME)
check("--rebase-environment alone is rejected", rc == 2)

print("Approval still works where it should:")
rc, out = run([], design_change, HOME)
check("a real design change on the recording machine still fails", rc == 1)
check("it is reported as a regression, not as drift",
      "visual regressions" in out and "did NOT run" not in out)
rc, out = run(["--approve"], design_change, HOME)
check("--approve is allowed on the recording machine", rc == 0)
rc, out = run([], design_change, HOME)
check("the approved change then passes", rc == 0)

rc, out = run(["--approve", "--rebase-environment"], elsewhere, AWAY)
check("--rebase-environment adopts the new machine deliberately", rc == 0)
check("it says whose rendering is now the reference", "reference environment" in out)
check("the environment record follows", vr.read_environment() == AWAY)
rc, out = run([], elsewhere, AWAY)
check("the rebased machine is now the clean one", rc == 0)

print("Shape mismatches cannot pass silently:")
ok, detail = vr.compare([[0] * vr.GRID] * vr.GRID, [[0] * vr.GRID] * (vr.GRID // 2))
check("a baseline with fewer rows is rejected, not partially compared",
      not ok and "shape" in detail)
ok, detail = vr.compare([[0] * vr.GRID] * vr.GRID,
                        [[0] * (vr.GRID // 2)] * vr.GRID)
check("a baseline with fewer columns is rejected too",
      not ok and "shape" in detail)

shutil.rmtree(tmp, ignore_errors=True)

print()
if FAILS:
    print(f"❌ {len(FAILS)} visual-environment guard test(s) failed:")
    for failure in FAILS:
        print(f"   {failure}")
    sys.exit(1)
print("✅ Visual-environment guard behaves as contracted")
