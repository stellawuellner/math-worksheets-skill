#!/usr/bin/env python3
r"""test_ssa_figure_labels.py — the ambiguous-SSA figure must be readable for
every triangle it accepts, not just the one in the reference drawing.

WHAT WENT WRONG. The swing figure placed the fixed side's label at a flat 0.55
along that side, a fraction chosen because it cleared the arc labels in the
reference figure. Nothing else about the drawing is fixed: where the second
candidate vertex lands on the base, and where 0.55 of the fixed side lands, both
move with the givens. For many valid triangles the "?" arc at the dashed apex
printed on top of "b = N".

Measured across twelve valid SSA parameterisations: SEVEN of twelve collided.
It had not been shipping constantly only because check_overprint blocks it at
the gate — so the cost landed on authors, who could do nothing but change the
givens, on a topic whose entire point is this figure. An eval author probing ten
triangles found one and reported it; a wider spread found it is the common case.

WHY IT IS FIXABLE. A pic label's position is not a mystery: `angle radius=7mm,
angle eccentricity=1.6` puts it 1.12cm from the vertex along the bisector of its
two rays. So the arc labels can be located and the side label placed where there
is room. 0.55 is still tried first, so every figure that was already clean is
byte-identical.

This test renders real figures through the shipped renderer and reads the
resulting PDF, because that is the only thing that answers the question. The
geometry check runs without LaTeX.

Requires pdflatex/tectonic and pdftotext for the rendered half; skips cleanly.
"""
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tests"))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import check_overprint as op  # noqa: E402

TEMPLATES = os.path.join(ROOT, "templates")
RENDERER = os.path.join(ROOT, "scripts", "render_figures.py")
FAILS = []

# Twelve valid ambiguous-SSA triangles spanning the shape of the case: small and
# large given angles, near-degenerate and comfortable swings. Seven of these
# collided before the label position was computed.
CASES = [(15, 30, 20), (15, 26, 25), (15, 22, 28), (15, 24, 30), (12, 20, 30),
         (10, 18, 25), (14, 25, 22), (16, 28, 26), (11, 19, 32), (13, 23, 27),
         (8, 10, 30), (9, 16, 29)]


def check(label, cond, detail=""):
    print(f"  {'✅' if cond else '❌'} {label}")
    if not cond:
        FAILS.append(f"{label}{': ' + detail if detail else ''}")


def spec():
    problems = []
    for i, (a, b, A) in enumerate(CASES, 1):
        ratio = b * math.sin(math.radians(A)) / a
        expected = round(math.degrees(math.asin(ratio)), 2) if ratio <= 1 else 0
        problems.append({"id": i, "type": "triangle",
                         "given": {"a": a, "b": b, "A": A},
                         "solve_for": "B", "expected": expected,
                         "workspace_cm": 10})
    return {"topic": "ssa", "problem_count": len(CASES), "problems": problems}


def main():
    engine = shutil.which("pdflatex") or shutil.which("tectonic")
    if not engine or not shutil.which("pdftotext"):
        print("test_ssa_figure_labels: no LaTeX engine or pdftotext — skipped")
        return 0

    with tempfile.TemporaryDirectory() as d:
        for f in os.listdir(TEMPLATES):
            if f.endswith(".tex"):
                shutil.copy(os.path.join(TEMPLATES, f), d)
        json.dump(spec(), open(os.path.join(d, "verify_ssa.json"), "w"))
        r = subprocess.run([sys.executable, RENDERER, "verify_ssa.json",
                            "figs_ssa.tex"], cwd=d, capture_output=True, text=True)
        check(f"the renderer draws all {len(CASES)} triangles",
              r.returncode == 0, r.stderr.strip()[:200])
        if r.returncode != 0:
            return 1

        # One figure per page, so a reported collision names its triangle.
        body = "\n".join(rf"\problem[1cm]{{Triangle {i}: \probfig{{{i}}}}}\newpage"
                         for i in range(1, len(CASES) + 1))
        open(os.path.join(d, "p.tex"), "w").write(
            r"\documentclass[12pt]{article}" "\n"
            r"\usepackage[margin=1in, top=0.75in, bottom=0.75in]{geometry}" "\n"
            r"\input{worksheet-preamble}" "\n" r"\input{figure-macros}" "\n"
            r"\input{figs_ssa}" "\n" r"\wsheader{SSA probe}" "\n"
            r"\begin{document}" "\n" r"\wstitleblock{SSA probe}{X}{}" "\n"
            + body + "\n" r"\end{document}" "\n")
        cmd = ([engine, "-interaction=nonstopmode", "p.tex"]
               if engine.endswith("pdflatex") else [engine, "p.tex"])
        subprocess.run(cmd, cwd=d, capture_output=True)
        pdf = os.path.join(d, "p.pdf")
        if not os.path.isfile(pdf):
            check("the probe document compiles", False, "no PDF produced")
            return 1

        pages = op.words_by_page(pdf)
        if pages is None:
            check("the probe PDF is readable", False)
            return 1
        collided = []
        for n, (w, h, words) in enumerate(pages, 1):
            faults = op.page_faults(w, h, words, op.OVERLAP)
            if faults and n <= len(CASES):
                collided.append(f"{CASES[n - 1]}: {faults[0][1]}")
        check(f"no label collides in any of the {len(CASES)} triangles",
              not collided,
              f"{len(collided)} collided — " + "; ".join(collided[:3]))

    print()
    if FAILS:
        print(f"❌ {len(FAILS)} SSA figure check(s) failed:")
        for x in FAILS:
            print(f"   {x}")
        return 1
    print("✅ every accepted SSA triangle draws a readable figure")
    return 0


if __name__ == "__main__":
    sys.exit(main())
