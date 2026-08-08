#!/usr/bin/env python3
"""test_tikz_libraries.py — the preamble's TikZ/pgfplots libraries actually work.

Two things rot silently and this catches both.

A library named in the preamble but absent from the TeX install fails at
\\usetikzlibrary time, which takes down EVERY document in the run — not one
figure. The failure looks like a broken document rather than a missing package,
so it is worth a direct check.

And a snippet documented in references/latex-templates.md is a promise: an
author transcribes it expecting a figure. If pgfplots' syntax moves under it,
the author gets a compile error on a sheet whose mathematics is correct, with
no way to tell that the guidance is what broke. Every snippet below is the one
the reference prints.

Skipped when no LaTeX engine is on PATH, like the other rendering suites.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES = os.path.join(ROOT, "templates")
REFERENCE = os.path.join(ROOT, "references", "latex-templates.md")
PREAMBLE = os.path.join(TEMPLATES, "worksheet-preamble.tex")

FAILS = []


def check(name, cond, extra=""):
    print(f"  {'✅' if cond else '❌'} {name}" + (f" — {extra}" if extra else ""))
    if not cond:
        FAILS.append(name)


# ── every library the preamble claims is really loadable ────────────────────
print("the preamble's declared libraries load:")
# Comments are stripped BEFORE the braces are matched, not after. The preamble
# annotates each library with a trailing % note, and one of those notes is
# "% -{Stealth} number lines..." — whose closing brace ended the non-greedy
# match three libraries early. Found by this test failing on its own parser.
pre = re.sub(r"(?<!\\)%[^\n]*", "", open(PREAMBLE, encoding="utf-8").read())


def declared(macro):
    """Names inside \\usetikzlibrary{...} / \\usepgfplotslibrary{...}."""
    m = re.search(re.escape(macro) + r"\{([^}]*)\}", pre, re.S)
    return [n.strip() for n in m.group(1).split(",") if n.strip()] if m else []


TIKZ = declared("\\usetikzlibrary")
PGFP = declared("\\usepgfplotslibrary")
check("the preamble declares tikz libraries", len(TIKZ) >= 5, str(TIKZ))
check("the preamble declares pgfplots libraries", len(PGFP) >= 1, str(PGFP))
# The three the geometric figure macros are built on must never be dropped:
# render_figures.py emits \pic {angle=...} and coordinate arithmetic.
for need in ("calc", "angles", "quotes"):
    check(f"{need} is still declared — the figure macros need it", need in TIKZ)


# ── the documented snippets still compile ───────────────────────────────────
def fenced_latex_blocks(md, heading):
    """The ```latex block(s) under one '### heading' section."""
    body = md.split("### " + heading, 1)
    if len(body) < 2:
        return []
    section = re.split(r"\n### ", body[1])[0]
    return re.findall(r"```latex\n(.*?)```", section, re.S)


SNIPPETS = [
    "Box plot — `boxplot prepared`, matching `stats`",
    "Area between two curves — matches `definite_integral`",
    "Shaded area model (fractions, percent, probability)",
    "Number line — matches `inequality` / `compare`",
    "Brace annotating a part — bar models, ratio and part-whole problems",
    "Two displays for a compare item",
]

engine = shutil.which("pdflatex") or shutil.which("tectonic")
if not engine:
    print("\n  ·  skipped: no LaTeX engine on PATH")
else:
    print("\nthe snippets references/latex-templates.md prints do compile:")
    md = open(REFERENCE, encoding="utf-8").read()
    work = tempfile.mkdtemp(prefix="tikzlib")
    for f in os.listdir(TEMPLATES):
        if f.endswith(".tex"):
            shutil.copy(os.path.join(TEMPLATES, f), work)
    for heading in SNIPPETS:
        blocks = fenced_latex_blocks(md, heading)
        if not blocks:
            check(f"{heading.split('—')[0].strip()}: snippet found in the "
                  "reference", False, "no ```latex block under that heading")
            continue
        name = re.sub(r"[^a-z]", "", heading.lower())[:16]
        doc = ("\\documentclass[12pt]{article}\n"
               "\\usepackage[margin=1in]{geometry}\n"
               "\\input{worksheet-preamble}\n\\begin{document}\n"
               + "\n".join(blocks) + "\n\\end{document}\n")
        open(os.path.join(work, name + ".tex"), "w", encoding="utf-8").write(doc)
        cmd = ([engine, "-interaction=nonstopmode", name + ".tex"]
               if engine.endswith("pdflatex") else [engine, name + ".tex"])
        subprocess.run(cmd, cwd=work, capture_output=True)
        pdf = os.path.join(work, name + ".pdf")
        log = os.path.join(work, name + ".log")
        errs = []
        if os.path.isfile(log):
            errs = [ln for ln in open(log, errors="replace") if ln.startswith("! ")]
        check(f"{heading.split('—')[0].strip()}",
              os.path.isfile(pdf) and not errs,
              "; ".join(e.strip() for e in errs[:2])[:160])

    # The box plot is the one where a WRONG figure compiles perfectly, so it
    # gets a content check as well as a compile check: the reference must show
    # `boxplot prepared` and must NOT hand pgfplots a raw table to quartile
    # itself. verify.py's stats uses school median-of-halves; pgfplots
    # interpolates, and on [4,6,7,9,11,12,18] they differ (9 vs 8).
    bp = "\n".join(fenced_latex_blocks(md, SNIPPETS[0]))
    check("the box-plot template uses `boxplot prepared`, not a raw table",
          "boxplot prepared" in bp and "table[" not in bp, bp[:120])
    for value in ("lower quartile=6", "median=9", "upper quartile=12"):
        check(f"it passes verify.py's own summary ({value})", value in bp)

# ── the figure house style compiles, every style and macro of it ─────────────
# tests/fixtures/house_style_probe.tex exercises all of: the wsgraph layer set
# and every ws* graph/chart style, the dot plot / stem-leaf / pictogram macros,
# the geometry marks, \gridtrifig, all five solid macros, and the full K-4
# model set. A style that breaks takes down every document in a run, and a
# macro that breaks takes down every sheet that uses the documented way to
# draw its model — this is the same "documented snippet is a promise" contract
# as the section above, at the scale of the whole house style.
if not engine:
    print("\n  ·  house-style probe skipped: no LaTeX engine on PATH")
else:
    print("\nthe figure house style compiles end to end:")
    work2 = tempfile.mkdtemp(prefix="housestyle")
    for f in os.listdir(TEMPLATES):
        if f.endswith(".tex"):
            shutil.copy(os.path.join(TEMPLATES, f), work2)
    shutil.copy(os.path.join(ROOT, "tests", "fixtures",
                             "house_style_probe.tex"),
                os.path.join(work2, "probe.tex"))
    cmd = ([engine, "-interaction=nonstopmode", "probe.tex"]
           if engine.endswith("pdflatex") else [engine, "probe.tex"])
    subprocess.run(cmd, cwd=work2, capture_output=True)
    log2 = os.path.join(work2, "probe.log")
    errs2 = [ln for ln in open(log2, errors="replace")
             if ln.startswith("! ")] if os.path.isfile(log2) else ["no log"]
    check("house_style_probe.tex compiles with zero errors",
          os.path.isfile(os.path.join(work2, "probe.pdf")) and not errs2,
          "; ".join(e.strip() for e in errs2[:2])[:160])
    # Style names the probe and the docs promise — a rename must fail loudly.
    pre2 = open(PREAMBLE, encoding="utf-8").read()
    for style in ("wsaxisbase", "wsgrid", "wsgridwide", "wsgridq1",
                  "wsfuntall", "wstrig", "wsbar", "wshist", "wsboxplot",
                  "wscurve", "wsasym", "wsopen", "wsclosed"):
        check(f"preamble defines {style}", style + "/.style" in pre2)
    mac = open(os.path.join(TEMPLATES, "figure-macros.tex"),
               encoding="utf-8").read()
    for m in ("congtick", "parallelmark", "gridtrifig", "cylfig", "conefig",
              "prismfig", "pyrfig", "cylnetfig", "tenframefig", "arrayfig",
              "basetenfig", "clockfig", "fraclinefig", "ineqlinefig",
              "tapefig", "coinrowfig"):
        check(f"figure-macros defines \\{m}",
              "\\newcommand{\\" + m + "}" in mac)

print()
if FAILS:
    print(f"❌ {len(FAILS)} tikz-library test(s) failed: {FAILS}")
    sys.exit(1)
print("✅ All tikz/pgfplots library tests passed")
