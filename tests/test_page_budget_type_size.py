#!/usr/bin/env python3
r"""test_page_budget_type_size.py — the large-print budget, measured not guessed.

SKILL.md offers 14pt/17pt large-print and dyslexia-friendly output and said "the
page budget adapts automatically; larger type simply means more pages". It did
not adapt at all: page_budget.py knew about paper size and nothing about type
size, so an accessible sheet was charged against 12pt constants. Measured on a
prose-heavy ten-problem sheet: 4 pages at 12pt against a ceiling of 4, and 5
pages at 17pt. The gate failed a correct large-print worksheet, and the only
edits that would have satisfied it were cutting problems or shortening stems —
the compression page_budget.py exists to refuse.

The scale factors are MEASURED, and this file is how they were measured. It
typesets one identical paragraph in each documented configuration, reads the
height straight out of TeX, and checks page_budget.py's table against it. They
have to be measured because they are not derivable from the point size:
\accessiblemode raises leading on top of it, so 14pt large-print text runs 1.69x
tall where its point size alone suggests 1.17x.

Requires pdflatex/tectonic; skips cleanly without one. The table check runs
either way, since a table that contradicts itself needs no LaTeX to catch.

Run: python3 tests/test_page_budget_type_size.py
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import page_budget as pb  # noqa: E402

TEMPLATES = os.path.join(ROOT, "templates")
FAILS = []

# One paragraph, long enough to wrap several times at every size — the height
# ratio of a single short line is dominated by rounding to whole lines.
STEM = ("A community garden committee is planning three rectangular plots along "
        "the south fence. The first plot is twice as long as it is wide, the "
        "second is three metres longer than the first on every side, and the "
        "third has the same perimeter as the first two combined. Write an "
        "expression for the total area, explain in a sentence what each term "
        "of your expression represents, and say which plot the committee "
        "should build first if it wants the most growing space per metre of "
        "fencing.")

DOC = r"""\documentclass[%s]{%s}
\usepackage[margin=1in, top=0.75in, bottom=0.75in]{geometry}
\input{worksheet-preamble}
%s
\wsheader{Height Probe}
\begin{document}
\wstitleblock{Height Probe}{X}{}
\newlength{\hgt}
\setbox0=\vbox{\hsize=\linewidth %s}
\setlength{\hgt}{\ht0}\addtolength{\hgt}{\dp0}
\typeout{STEMHEIGHT=\the\hgt}
\noindent Measured.
\end{document}
"""

# How far a measured ratio may sit from the shipped factor. Line breaking is
# discrete, so a paragraph gains a whole line at a time; 8% is under half a line
# on this paragraph at every size, and wide enough that a font update does not
# fail the suite for a rounding difference.
TOL = 0.08


def check(label, cond, detail=""):
    print(f"  {'✅' if cond else '❌'} {label}")
    if not cond:
        FAILS.append(f"{label}{': ' + detail if detail else ''}")


def height(engine, workdir, size, mode):
    cls = "article" if size == "12pt" else "extarticle"
    acc = "" if mode == "none" else r"\accessiblemode{%s}" % mode
    d = os.path.join(workdir, f"{size}_{mode}")
    os.makedirs(d, exist_ok=True)
    for f in os.listdir(TEMPLATES):
        if f.endswith(".tex"):
            shutil.copy(os.path.join(TEMPLATES, f), d)
    open(os.path.join(d, "p.tex"), "w").write(DOC % (size, cls, acc, STEM))
    cmd = ([engine, "-interaction=nonstopmode", "p.tex"]
           if engine.endswith("pdflatex") else [engine, "p.tex"])
    subprocess.run(cmd, cwd=d, capture_output=True)
    log = os.path.join(d, "p.log")
    if not os.path.isfile(log):
        return None
    m = re.search(r"STEMHEIGHT=([\d.]+)pt",
                  open(log, encoding="utf-8", errors="replace").read())
    return float(m.group(1)) if m else None


def main():
    print("the table is self-consistent")
    base = pb.TEXT_SCALE[("12pt", "none")]
    check("12pt plain is the 1.0 baseline", base == 1.0)
    for size in ("12pt", "14pt", "17pt"):
        plain = pb.TEXT_SCALE[(size, "none")]
        for mode in ("large", "dyslexia", "both"):
            check(f"{size} {mode} is at least as tall as {size} plain",
                  pb.TEXT_SCALE[(size, mode)] >= plain)
    check("a bigger point size is never charged less",
          pb.TEXT_SCALE[("12pt", "none")] < pb.TEXT_SCALE[("14pt", "none")]
          < pb.TEXT_SCALE[("17pt", "none")])
    # An unmeasured combination must round UP, never down: charging a document
    # less than it costs is how the gate failed a correct sheet in the first
    # place, only in the other direction.
    check("an unmeasured mode falls back to the largest for its size",
          pb.text_scale("17pt", "enormous") == max(
              v for (sz, _), v in pb.TEXT_SCALE.items() if sz == "17pt"))
    check("an unmeasured size falls back to the 12pt baseline",
          pb.text_scale("23pt", "none") == 1.0)

    print()
    print("only text scales — workspace and figures are physical")
    p = {"id": 1, "type": "eval", "workspace_cm": 6.0}
    small, large = pb.problem_cost(p, 1.0), pb.problem_cost(p, 2.17)
    check("a declared 6cm workspace is charged 6cm at every type size",
          abs((large - small) - (pb.OVERHEAD_CM + pb.STEM_CM) * 1.17) < 0.01,
          f"12pt {small:.2f}cm vs 17pt {large:.2f}cm")

    print()
    print("the shipped factors match what TeX actually sets")
    engine = shutil.which("pdflatex") or shutil.which("tectonic")
    if not engine:
        print("  ·  no LaTeX engine — measurement skipped")
    else:
        with tempfile.TemporaryDirectory() as tmp:
            ref = height(engine, tmp, "12pt", "none")
            if not ref:
                check("the 12pt probe compiles", False, "no height in the log")
            else:
                for (size, mode), factor in sorted(pb.TEXT_SCALE.items()):
                    h = height(engine, tmp, size, mode)
                    if h is None:
                        check(f"{size} {mode} compiles", False, "no height")
                        continue
                    ratio = h / ref
                    check(f"{size} {mode}: shipped {factor:.2f}, "
                          f"measured {ratio:.2f}",
                          abs(ratio - factor) <= TOL * factor,
                          f"drifted by {abs(ratio - factor) / factor * 100:.0f}%")

    print()
    if FAILS:
        print(f"❌ {len(FAILS)} type-size check(s) failed:")
        for x in FAILS:
            print(f"   {x}")
        return 1
    print("✅ the page budget charges large print for the space it takes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
