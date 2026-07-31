#!/usr/bin/env python3
r"""
visual_regression.py — render each shipped document to an image and compare it
against an approved baseline, so a layout change that no rule anticipated still
cannot ship silently.

Usage:
  python3 tests/visual_regression.py            # check every case
  python3 tests/visual_regression.py --approve  # re-record baselines

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


def engine():
    return shutil.which("pdflatex") or shutil.which("tectonic")


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
    subprocess.run(cmd, cwd=d, capture_output=True)
    pdf = os.path.join(d, "c.pdf")
    if not os.path.exists(pdf):
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


def main():
    approve = "--approve" in sys.argv
    if not engine() or not shutil.which("pdftoppm"):
        print("visual_regression: no LaTeX engine or pdftoppm — skipped")
        return 0

    os.makedirs(BASELINE, exist_ok=True)
    workdir = os.path.join("/tmp", "mws_visual")
    shutil.rmtree(workdir, ignore_errors=True)
    os.makedirs(workdir)

    failures, recorded = [], 0
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
