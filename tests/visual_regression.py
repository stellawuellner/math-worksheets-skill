#!/usr/bin/env python3
r"""
visual_regression.py — render each shipped document to an image and compare it
against an approved baseline, so a layout change that no rule anticipated still
cannot ship silently.

Usage:
  python3 tests/visual_regression.py            # check every case
  python3 tests/visual_regression.py --approve  # re-record baselines
  python3 tests/visual_regression.py --approve --rebase-environment
                                                # ...and adopt this machine's
                                                #    rendering as the reference

WHY THIS EXISTS
Every layout fault this project has fixed was found the same way: a human looked
at a PDF and saw something ugly. The header title printing through the Name/Date
blanks, the study guide spilling a third page, the answer line under a
three-part problem, the four study-guide boxes collapsing to identical gray in
print — none of them was visible to a checker that reads only the source, and
each one shipped at least once. Rules were then written for each, but a rule can
only catch the fault it was written for. This catches the ones nobody has
thought of yet, because it compares the actual printed page.

HOW IT WORKS
Each case is a small .tex exercising one part of the design system. It is
compiled, rasterised to grayscale at low DPI, and reduced to a 48x48 grid of
ink density that is committed as a small text file. Grayscale on purpose: it is
how most worksheets are printed, so a change that survives only in colour fails
here, which is the correct outcome. The grid keeps a baseline at ~2KB instead of
a ~0.5MB raster, stays reviewable in a diff, and reports WHERE on the page
something moved rather than only that it did.

WHAT A FAILURE MEANS
A diff is not automatically a bug: an intended design change also moves ink.
The workflow is: read the reported region, look at the document, and either fix
the regression or re-approve with --approve and commit the new baseline in the
same change as the design edit. The baseline is a record of what the output
looked like when a human last approved it.

WHY THE ENVIRONMENT IS CHECKED FIRST
An ink signature is a property of a font and rasteriser stack, not only of the
design. A different TeX Live release, a substituted font, another poppler — any
of them moves cells without a line of the design changing. That has already
happened once here: a branch arrived with seven re-recorded baselines that
failed this harness at 6.6%, while the same branch's CODE rendered at 0/2304
against the previous baselines. The baselines had moved; the rendering had not.

Committing that would have made every later contributor's first run red, and
the reflex answer to a red baseline is --approve, which is precisely the
rubber-stamp this harness exists to prevent. So the environment is compared
before the pages are, two ways: the recorded engine and rasteriser versions,
and two canary documents that exercise both font stacks the cases use. When the
local environment does not match the one the baselines were recorded in, the
page comparison is reported but NOT enforced, and --approve refuses to run.
Set MWS_VISUAL_STRICT=1 (CI does) to make a drifted environment a hard failure
instead, so the gate cannot quietly stop testing anything.

Requires a LaTeX engine and pdftoppm (poppler). Skips cleanly when absent, so
CI without a TeX install stays green rather than falsely red.
Exit 0 = every case matches. 1 = at least one differs. 2 = harness error.
"""
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES = os.path.join(ROOT, "templates")
BASELINE = os.path.join(ROOT, "tests", "baseline")
DPI = 72
# Anti-aliasing jitter between engine/poppler versions moves a few edge pixels
# by a shade. Only differences that a reader could see should fail, so a pixel
# counts as changed when it moves more than this, and the case fails when
# enough pixels change to be a visible mark rather than a rendering nuance.
GRID = 48                   # 48x48 ink-density cells per page
CELL_TOLERANCE = 6          # a cell must shift this much (of 99) to count
# A single page-wide threshold is the wrong model: the running head occupies
# about a seventh of the page, so a title printing straight through the
# Name/Date blanks moves under 1% of the page's cells and would slip under any
# global bar loose enough to tolerate rendering jitter. Each band is therefore
# judged against its own size, and the page also has a global bar for diffuse
# change. Measured against the real regressions: the header collision moves ~6%
# of the head band, the colour-only box revert moves ~3% of the whole page.
CHANGED_FRACTION = 0.010    # 1% of all cells: diffuse change
BAND_FRACTION = 0.025       # 2.5% of one band: localised change (clean runs sit at 0%)
BANDS = (("head", 0.00, 0.07), ("body", 0.07, 0.93), ("foot", 0.93, 1.00))

ENVIRONMENT_FILE = os.path.join(BASELINE, "ENVIRONMENT.txt")
# The canary is a compatibility probe, not a design check, so it is judged on a
# raw cell count rather than the design thresholds. Same-environment runs sit at
# 0-3 cells of 2304 (antialiasing). Measured against forced font substitutions,
# the worst canary moves 31 cells (mathptmx), 192 (helvet) and 147 (lmodern) —
# and in every one of those the canary trips whenever ANY case moves, which is
# the property that matters: the probe must never say "same machine" about a
# stack that would fail a case. 12 clears the noise floor by 4x and sits 2.6x
# under the tightest real substitution.
CANARY_CELLS = 12

PREAMBLE = r"""\documentclass[12pt]{article}
\usepackage[margin=%s]{geometry}
\input{worksheet-preamble}
"""

CASES = {
    # the header collision that shipped: a long title beside the Name/Date
    # blanks, plus a continuation page that must not repeat the Date blank
    "header_long_title": PREAMBLE % "1in, top=0.75in, bottom=0.75in" + r"""
\wsheader{Slope, Slope-Intercept Form and Linear Function Modelling Practice}
\begin{document}
\wstitleblock{Slope and Slope-Intercept Form}{Algebra 1 (Grade 8)}{}
\problem[4cm]{Find the slope of the line through $(1,2)$ and $(4,11)$.}
\problem[4cm]{For $y=2x+3$, find $y$ when $x=6$.}
\newpage
\problem[4cm]{A problem on the continuation page.}
\end{document}
""",
    # the observant answer line: one line for the single-answer problem, one per
    # part for the multi-part problem, and none for the multi-part parent
    "answer_lines": PREAMBLE % "1in, top=0.75in, bottom=0.75in" + r"""
\wsheader{Answer Lines}
\begin{document}
\wstitleblock{Answer line placement}{Test}{}
\problem[3cm]{Single answer.}
\problem[3cm]{Multi-part with workspace:
\begin{enumerate}[label=(\alph*), itemsep=2cm, leftmargin=1.5cm]
  \item first part \ansline
  \item second part \ansline
\end{enumerate}}
\problem[3cm]{Sketch the graph.\noansline}
\end{document}
""",
    # the four study-guide boxes: must stay distinguishable with colour removed
    "study_guide_boxes": PREAMBLE % "0.85in, top=0.7in, bottom=0.7in" + r"""
\ssheader{Quadratics}
\begin{document}
\sstitleblock{Factoring Trinomials}
\skillheading{Skill 1 --- Factoring Trinomials (a = 1)}
\begin{formulabox}\textbf{Rule / Formula:}\\[4pt]
$x^2 + bx + c = (x+p)(x+q)$ where $p+q=b$ and $p\cdot q=c$
\end{formulabox}
\begin{examplebox}\textbf{Example:} \quad Factor $x^2-7x+12$
\step{Product $+12$ with sum $-7$: both numbers are negative.}
\step{$-3$ and $-4$ give $\ans{(x-3)(x-4)}$}
\end{examplebox}
\begin{tryitbox}\textbf{Try it:} \quad Factor $x^2-9x+20$\\[2pt]
\rotatebox{180}{\footnotesize check: $\ans{(x-4)(x-5)}$}\end{tryitbox}
\begin{watchoutbox}\textbf{(!) Watch out:} Signs matter.\end{watchoutbox}
\end{document}
""",
    # large print + dyslexia-friendly: 17pt sans, wider blanks, 1.5 leading.
    # A student entitled to large print is exactly the one who cannot afford a
    # silent layout regression, so the mode gets its own baseline.
    "accessible_both": r"""\documentclass[17pt]{extarticle}
\usepackage[margin=1in, top=0.75in, bottom=0.75in]{geometry}
\input{worksheet-preamble}
\accessiblemode{both}
\wsheader{Slope Practice}
\begin{document}
\wstitleblock{Slope and Intercepts}{Algebra 1}{}
\problem[4cm]{A line rises 3 units over a run of 2. Find the slope.}
\problem[4cm]{Emphasis: \emph{bold, never italic}.}
\end{document}
""",
    # decimal comma and \times for the countries that use A4
    "locale_eu": PREAMBLE % "1in, top=0.75in, bottom=0.75in" + r"""
\mwslocale{eu}
\wsheader{Slope Practice}
\begin{document}
\wstitleblock{Decimals and products}{Algebra 1}{}
\problem[3cm]{A line rises \dec{3.75} over a run of \dec{2.5}, giving $a \mtimes b$.}
\end{document}
""",
    # the answer key head, which must use the full width now that the redundant
    # right-hand label is gone
    "answer_key_head": PREAMBLE % "1in, top=0.75in, bottom=0.75in" + r"""
\akheader{Slope and Slope-Intercept Form}
\begin{document}
\aktitleblock{Slope and Slope-Intercept Form}{Algebra 1 (Grade 8)}{}
\problem{Slope through $(1,2)$ and $(4,11)$: $m=\ans{3}$}
\end{document}
""",
}

# Two documents whose only job is to answer "does this machine rasterise the way
# the baselines were recorded?" — one per font stack the cases use. Each packs a
# pangram, digits, bold, emphasis and dense math into a small area, so a
# substituted face or a changed rasteriser shows up as many moved cells rather
# than a few. They are deliberately NOT design cases: nothing here is a layout
# decision anyone would revisit, which is what lets a canary diff be read as
# "different machine" rather than "different design".
CANARY_BODY = (r"The quick brown fox jumps over the lazy dog 0123456789. "
               r"\textbf{Bold weight 0123456789.} \emph{Emphasis sample.} "
               r"$f(x)=\frac{3x^2-7x+12}{\sqrt{x-1}}$, "
               r"$\int_0^\pi \sin\theta \, d\theta = 2$, $m=\frac{y_2-y_1}{x_2-x_1}$")

CANARIES = {
    # the serif stack: everything except the accessibility modes
    "canary_serif": PREAMBLE % "1in, top=0.75in, bottom=0.75in" + r"""
\wsheader{Environment canary}
\begin{document}
\wstitleblock{Environment canary}{Serif stack}{}
\problem[1cm]{""" + CANARY_BODY + r"""\ansline}
\end{document}
""",
    # the sans stack: extarticle at 17pt with sfmath, where a missing or
    # substituted sans face would otherwise surface only as a case regression
    "canary_sans": r"""\documentclass[17pt]{extarticle}
\usepackage[margin=1in, top=0.75in, bottom=0.75in]{geometry}
\input{worksheet-preamble}
\accessiblemode{both}
\wsheader{Environment canary}
\begin{document}
\wstitleblock{Environment canary}{Sans stack}{}
\problem[1cm]{""" + CANARY_BODY + r"""\ansline}
\end{document}
""",
}


def engine():
    return shutil.which("pdflatex") or shutil.which("tectonic")


def tool_version(cmd, *args):
    """First line of a tool's version banner, on stdout or stderr."""
    try:
        r = subprocess.run([cmd, *args], capture_output=True, text=True)
    except OSError as exc:
        return f"unavailable ({exc})"
    out = (r.stdout.strip() or r.stderr.strip()).splitlines()
    return out[0].strip() if out else "unknown"


def environment():
    """Describe the rendering stack the ink signatures depend on.

    Harness parameters are recorded alongside the tool versions because they
    change the signature just as surely as a font does: re-tuning GRID or
    CELL_TOLERANCE invalidates every baseline, and that should announce itself
    rather than show up as a mystery diff.
    """
    eng = engine() or ""
    return {
        "engine": tool_version(eng, "--version") if eng else "none",
        "raster": tool_version("pdftoppm", "-v"),
        "grid": str(GRID),
        "dpi": str(DPI),
        "tolerance": str(CELL_TOLERANCE),
    }


def write_environment(env):
    with open(ENVIRONMENT_FILE, "w") as fh:
        fh.write(
            "# Rendering environment the baselines in this directory were\n"
            "# recorded in. visual_regression.py compares it against the local\n"
            "# machine before it compares any page, because an ink-density\n"
            "# signature belongs to a font and rasteriser stack as much as to a\n"
            "# design. Do not edit by hand: re-record with\n"
            "#   python3 tests/visual_regression.py --approve --rebase-environment\n")
        for k, v in env.items():
            fh.write(f"{k}\t{v}\n")


def read_environment():
    if not os.path.exists(ENVIRONMENT_FILE):
        return None
    env = {}
    for line in open(ENVIRONMENT_FILE):
        if line.startswith("#") or "\t" not in line:
            continue
        k, v = line.rstrip("\n").split("\t", 1)
        env[k] = v
    return env or None


def render(name, tex, workdir):
    """Compile one case and return its pages as parsed PGM rasters."""
    d = os.path.join(workdir, name)
    os.makedirs(d, exist_ok=True)
    for f in os.listdir(TEMPLATES):
        if f.endswith(".tex"):
            shutil.copy(os.path.join(TEMPLATES, f), d)
    open(os.path.join(d, "c.tex"), "w").write(tex)
    eng = engine()
    cmd = ([eng, "-interaction=nonstopmode", "c.tex"] if eng.endswith("pdflatex")
           else [eng, "c.tex"])
    compiled = subprocess.run(cmd, cwd=d, capture_output=True, text=True)
    pdf = os.path.join(d, "c.pdf")
    if not os.path.exists(pdf):
        output = (compiled.stdout + "\n" + compiled.stderr).strip()
        tail = "\n".join(output.splitlines()[-12:])
        print(f"  compile failed for {name} (exit {compiled.returncode})", file=sys.stderr)
        if tail:
            print(tail, file=sys.stderr)
        return None
    # -gray gives PGM (P5), which parses in a few lines of pure Python: no
    # image library and no extra binary beyond poppler, which the repo already
    # relies on for pdftotext/pdfinfo.
    subprocess.run(["pdftoppm", "-r", str(DPI), "-gray", pdf,
                    os.path.join(d, "p")], capture_output=True)
    return [read_pgm(os.path.join(d, f)) for f in
            sorted(os.listdir(d)) if f.startswith("p-") and f.endswith(".pgm")]


def read_pgm(path):
    """Parse a binary PGM into (width, height, pixels)."""
    data = open(path, "rb").read()
    fields, idx = [], 0
    while len(fields) < 4:
        while idx < len(data) and data[idx:idx + 1].isspace():
            idx += 1
        if data[idx:idx + 1] == b"#":
            while idx < len(data) and data[idx:idx + 1] != b"\n":
                idx += 1
            continue
        start = idx
        while idx < len(data) and not data[idx:idx + 1].isspace():
            idx += 1
        fields.append(data[start:idx])
    idx += 1
    w, h = int(fields[1]), int(fields[2])
    return w, h, data[idx:idx + w * h]


def signature(page):
    """Reduce a page to a GRID x GRID map of ink density (0-99 per cell).

    The baseline is committed to the repo, so it must be small and reviewable
    in a diff: a full raster is ~0.5MB per page, this is ~2KB of text. It is
    also more useful than a raw image compare — a changed cell says WHERE on
    the page something moved, so a report can name the region (a header
    collision lights up the top band, a page-fill change lights the bottom).
    """
    w, h, px = page
    out = []
    for gy in range(GRID):
        row = []
        y0, y1 = gy * h // GRID, (gy + 1) * h // GRID
        for gx in range(GRID):
            x0, x1 = gx * w // GRID, (gx + 1) * w // GRID
            ink = n = 0
            for y in range(y0, y1, 2):          # sample every other line
                base = y * w
                for x in range(x0, x1, 2):
                    ink += 255 - px[base + x]
                    n += 1
            row.append(min(99, round(ink / max(1, n) / 255 * 99)))
        out.append(row)
    return out


def sig_text(sig):
    return "\n".join(" ".join(f"{v:2d}" for v in row) for row in sig) + "\n"


def sig_read(path):
    return [[int(v) for v in line.split()]
            for line in open(path).read().strip().splitlines()]


def band_of(gy):
    for name, lo, hi in BANDS:
        if lo * GRID <= gy < hi * GRID or (hi == 1.0 and gy >= lo * GRID):
            return name
    return "body"


def region_name(gy, gx):
    side = "left" if gx < GRID / 3 else ("right" if gx > GRID * 2 / 3 else "centre")
    return f"{band_of(gy)}-{side}"


def compare(sig, ref):
    """Compare two signatures.

    Returns (verdict, detail) where verdict is True when the page is unchanged
    within tolerance. Judged globally AND per band, so a fault confined to the
    running head is caught at the same sensitivity as one spread over the body.
    """
    # zip() would silently compare only the overlap, so a baseline recorded at a
    # different GRID would read as "unchanged" over the rows it happens to share.
    if len(ref) != len(sig) or any(len(a) != len(b) for a, b in zip(sig, ref)):
        return False, (f"baseline shape {len(ref)}x{len(ref[0]) if ref else 0} does not "
                       f"match this harness ({GRID}x{GRID}) — re-record with --approve")
    changed, regions, per_band = 0, {}, {b[0]: 0 for b in BANDS}
    band_cells = {b[0]: 0 for b in BANDS}
    for gy, (a, b) in enumerate(zip(sig, ref)):
        band = band_of(gy)
        for gx, (va, vb) in enumerate(zip(a, b)):
            band_cells[band] += 1
            if abs(va - vb) > CELL_TOLERANCE:
                changed += 1
                per_band[band] += 1
                k = region_name(gy, gx)
                regions[k] = regions.get(k, 0) + 1
    total = GRID * GRID
    busiest = ", ".join(f"{k} ({v})" for k, v in
                        sorted(regions.items(), key=lambda kv: -kv[1])[:3])
    reasons = []
    if changed / total > CHANGED_FRACTION:
        reasons.append(f"{changed}/{total} cells changed page-wide "
                       f"({changed/total*100:.1f}%)")
    for name, _, _ in BANDS:
        n, cells = per_band[name], max(1, band_cells[name])
        if n / cells > BAND_FRACTION:
            reasons.append(f"{n}/{cells} cells changed in the {name} band "
                           f"({n/cells*100:.1f}%)")
    if not reasons:
        return True, f"{changed}/{total} cells moved"
    return False, "; ".join(reasons) + (f" — busiest: {busiest}" if busiest else "")


def canary_drift(workdir, record):
    """Render the canaries and report how far this machine sits from the record.

    Returns (list of drift descriptions, number of baselines recorded). An empty
    list means the local stack renders the way the baselines were recorded, so
    a page diff can honestly be read as a design change.
    """
    drift, recorded = [], 0
    for name, tex in sorted(CANARIES.items()):
        pages = render(name, tex, workdir)
        if not pages:
            drift.append(f"{name}: did not compile — the local TeX install is "
                         f"missing something the design system needs")
            continue
        ref_path = os.path.join(BASELINE, f"{name}-1.txt")
        sig = signature(pages[0])
        if record or not os.path.exists(ref_path):
            open(ref_path, "w").write(sig_text(sig))
            recorded += 1
            continue
        ref = sig_read(ref_path)
        if len(ref) != len(sig) or any(len(a) != len(b) for a, b in zip(sig, ref)):
            drift.append(f"{name}: baseline was recorded at a different grid size")
            continue
        moved = sum(1 for a, b in zip(sig, ref)
                    for va, vb in zip(a, b) if abs(va - vb) > CELL_TOLERANCE)
        if moved > CANARY_CELLS:
            drift.append(f"{name}: {moved}/{GRID * GRID} cells differ from the "
                         f"recorded rendering (tolerance {CANARY_CELLS})")
    return drift, recorded


def main():
    approve = "--approve" in sys.argv
    rebase = "--rebase-environment" in sys.argv
    strict = os.environ.get("MWS_VISUAL_STRICT") == "1"
    if rebase and not approve:
        print("--rebase-environment only means anything with --approve",
              file=sys.stderr)
        return 2
    if not engine() or not shutil.which("pdftoppm"):
        print("visual_regression: no LaTeX engine or pdftoppm — skipped")
        return 0

    os.makedirs(BASELINE, exist_ok=True)
    workdir = os.path.join("/tmp", "mws_visual")
    shutil.rmtree(workdir, ignore_errors=True)
    os.makedirs(workdir)

    # Establish whether this machine may speak for the baselines at all, before
    # a single page is judged.
    env_now = environment()
    env_ref = read_environment()
    bootstrap = env_ref is None
    drift = [] if bootstrap else [
        f"{k}: baselines recorded with {env_ref.get(k, 'unrecorded')!r}, "
        f"this machine has {env_now[k]!r}"
        for k in env_now if env_ref.get(k) != env_now[k]]
    canary_fail, canary_recorded = canary_drift(workdir, record=bootstrap or (approve and rebase))
    drift += canary_fail
    if bootstrap or (approve and rebase):
        write_environment(env_now)

    if drift and approve and not rebase:
        print("❌ refusing to re-record baselines from a different environment:")
        for d in drift:
            print(f"  • {d}")
        print("\n  Baselines recorded here would fail on the machine that recorded\n"
              "  the current ones, and the usual response to that is another blind\n"
              "  --approve. If you really do mean to move the reference rendering\n"
              "  onto this machine, re-run with --rebase-environment and commit it\n"
              "  on its own, separately from any design change, so the two are\n"
              "  never confused.")
        return 2

    failures, recorded = [], canary_recorded
    for name, tex in sorted(CASES.items()):
        pages = render(name, tex, workdir)
        if not pages:
            failures.append(f"{name}: did not compile")
            continue
        refs = sorted(f for f in os.listdir(BASELINE)
                      if f.startswith(f"{name}-") and f.endswith(".txt"))
        if not approve and refs and len(refs) != len(pages):
            failures.append(
                f"{name}: PAGE COUNT changed — baseline {len(refs)} page(s), "
                f"now {len(pages)}. This is the study-guide-spill class of "
                f"fault; check the page budget before re-approving.")
        for i, page in enumerate(pages, 1):
            sig = signature(page)
            ref_path = os.path.join(BASELINE, f"{name}-{i}.txt")
            if approve or not os.path.exists(ref_path):
                open(ref_path, "w").write(sig_text(sig))
                recorded += 1
                print(f"  recorded  {name} page {i}")
                continue
            ok, detail = compare(sig, sig_read(ref_path))
            if ok:
                print(f"  ok        {name} page {i} ({detail})")
            else:
                failures.append(f"{name} page {i}: {detail}")

    if approve:
        print(f"\n✅ recorded {recorded} baseline page(s) in tests/baseline/ — "
              f"review the documents and commit these with the design change")
        if rebase:
            print("   the reference environment now names this machine "
                  f"({env_now['engine']}, {env_now['raster']})")
        return 0

    if drift:
        # Not a regression and not a pass: this machine simply cannot answer the
        # question. Say so plainly, show the page comparison as information, and
        # do not spend the contributor's afternoon on a red build they did not
        # cause — unless the caller asked for strictness, which is how CI keeps
        # a drifted environment from quietly disabling the gate.
        print("\n⚠️  rendering environment differs from the one the baselines "
              "were recorded in:")
        for d in drift:
            print(f"  • {d}")
        if failures:
            print("\n  Page differences seen (informational — they may be the "
                  "environment,\n  not the design):")
            for f in failures:
                print(f"    • {f}")
        else:
            print("\n  No page differences seen even so.")
        if strict:
            print("\n❌ MWS_VISUAL_STRICT=1: a drifted environment is a failure "
                  "here, because\n  an advisory gate tests nothing. Re-record on "
                  "this machine with\n  --approve --rebase-environment and commit "
                  "the result on its own.")
            return 1
        print("\n  The visual gate did NOT run. Baselines are recorded against one\n"
              "  font and rasteriser stack; comparing across stacks reports the\n"
              "  machine, not the design. Do not --approve from here — that is how\n"
              "  a baseline set gets replaced by an unrelated environment's.\n"
              "  Authoritative runs happen in CI (see .github/workflows/tests.yml).")
        return 0

    if failures:
        print("\n❌ visual regressions:")
        for f in failures:
            print(f"  • {f}")
        print("\n  A diff is not automatically a bug. If the change is intended, "
              "re-run with\n  --approve and commit the new baseline alongside the "
              "design edit.")
        return 1
    print("\n✅ visual output matches the approved baselines")
    return 0


if __name__ == "__main__":
    sys.exit(main())
