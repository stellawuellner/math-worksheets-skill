#!/usr/bin/env python3
r"""test_overprint.py — pin the overprinting detector's two failure directions.

A detector like this is only worth having if BOTH directions hold. Miss a real
collision and it is decoration; fire on ordinary typesetting and everyone learns
to ignore it, which is worse than not having it — the reflex answer to a noisy
check is to stop reading it.

So this pins:
  - a deliberate collision is caught (two nodes driven onto each other)
  - a clean document stays clean
  - the three noise classes calibration removed stay removed: a radical over its
    argument, a composed relation (congruence is a tilde stacked on an equals),
    and punctuation kerning into its neighbour

Calibration record: across 450 PDFs this repository had already produced and
gated, the tuned detector fires on exactly one, and that one has a genuine
caption collision confirmed by looking at the rendered page. Before the noise
rules it fired on 77.

Requires pdflatex/tectonic and pdftotext; skips cleanly without them.
"""
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tests"))
import check_overprint as op  # noqa: E402

FAILS = []
TEMPLATES = os.path.join(ROOT, "templates")

HEAD = r"""\documentclass[12pt]{article}
\usepackage[margin=1in, top=0.75in, bottom=0.75in]{geometry}
\input{worksheet-preamble}
\wsheader{Overprint Probe}
\begin{document}
\wstitleblock{Overprint Probe}{Test}{}
"""

COLLIDING = HEAD + r"""
\problem[2cm]{Two captions driven onto each other:
\begin{center}\begin{tikzpicture}
\node at (0,0) {Two lengths multiplied};
\node at (0.3,0) {Three lengths multiplied};
\end{tikzpicture}\end{center}}
\end{document}
"""

# Every construction calibration proved innocent, in one document: a radical
# whose box covers its argument, a congruence built by stacking two marks, a
# fraction, subscripts and superscripts, and an ellipsis kerning into a word.
CLEAN = HEAD + r"""
\problem[2cm]{Evaluate $\sqrt{x^2 + y_1}$ and $\dfrac{a+b}{c-d}$.}
\problem[2cm]{Given $\triangle ABC \cong \triangle DEF$, name the parts.}
\problem[2cm]{Continue the pattern $2, 4, 6, \ldots$ and explain.}
\end{document}
"""


def check(label, cond, detail=""):
    print(f"  {'✅' if cond else '❌'} {label}")
    if not cond:
        FAILS.append(f"{label}{': ' + detail if detail else ''}")


def build(tex, workdir, name):
    d = os.path.join(workdir, name)
    os.makedirs(d, exist_ok=True)
    for f in os.listdir(TEMPLATES):
        if f.endswith(".tex"):
            shutil.copy(os.path.join(TEMPLATES, f), d)
    open(os.path.join(d, "p.tex"), "w").write(tex)
    eng = shutil.which("pdflatex") or shutil.which("tectonic")
    cmd = ([eng, "-interaction=nonstopmode", "p.tex"] if eng.endswith("pdflatex")
           else [eng, "p.tex"])
    subprocess.run(cmd, cwd=d, capture_output=True)
    pdf = os.path.join(d, "p.pdf")
    return pdf if os.path.isfile(pdf) else None


def faults(pdf):
    out = []
    for w, h, words in op.words_by_page(pdf):
        out += op.page_faults(w, h, words, op.OVERLAP)
    return out


def main():
    if not (shutil.which("pdflatex") or shutil.which("tectonic")) \
            or not shutil.which("pdftotext"):
        print("test_overprint: no LaTeX engine or pdftotext — skipped")
        return 0

    print("unit rules")
    check("a radical is treated as an overlay, not a collision",
          op.is_overlay("√"))
    check("an ellipsis is treated as kerning, not a collision",
          op.is_overlay("..."))
    check("an ordinary word is not an overlay", not op.is_overlay("lengths"))
    # congruence: a tilde stacked on an equals, same x-run, both single marks
    tilde = (100.0, 200.0, 108.0, 204.0, "∼")
    equals = (100.0, 203.0, 108.0, 209.0, "=")
    check("a composed relation is not a collision", op.composed_glyph(tilde, equals))
    word_a = (100.0, 200.0, 140.0, 210.0, "Three")
    word_b = (102.0, 200.0, 142.0, 210.0, "lengths")
    check("two overlapping words are NOT excused as a composed glyph",
          not op.composed_glyph(word_a, word_b))

    with tempfile.TemporaryDirectory() as tmp:
        print("rendered documents")
        bad = build(COLLIDING, tmp, "collide")
        if not bad:
            check("the colliding probe compiles", False, "no PDF produced")
        else:
            f = faults(bad)
            check("a deliberate collision is caught", len(f) >= 1,
                  "the detector saw nothing")
            check("it is reported as overprinting",
                  any(k == "overprint" for k, _ in f))

        good = build(CLEAN, tmp, "clean")
        if not good:
            check("the clean probe compiles", False, "no PDF produced")
        else:
            f = faults(good)
            check("radicals, congruence, fractions and ellipses stay clean",
                  not f, "; ".join(m for _, m in f)[:200])

    print()
    if FAILS:
        print(f"❌ {len(FAILS)} overprint test(s) failed:")
        for x in FAILS:
            print(f"   {x}")
        return 1
    print("✅ overprint detector catches collisions and ignores typesetting")
    return 0


if __name__ == "__main__":
    sys.exit(main())
