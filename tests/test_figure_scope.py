#!/usr/bin/env python3
r"""test_figure_scope.py — pin both directions of check_layout's figure rule.

THE RULE. No problem may be left with NO figure while another problem's figure
carries values. On paper the problems run together, so a student with nothing
of their own to look at reads the labelled triangle a few lines up and
reasonably assumes it applies. The figure is correct and the sheet is wrong.

WHY THIS FILE. The rule has now been wrong three times, in three different
ways, all within one eval run:

  * Silently PASSING. pgfplots draws numeric tick labels by default and draws
    them as axis ticks, not as \node text, so the tikz scan never saw them. A
    worksheet with graphs on 3 of 12 problems passed the gate. Fixed by
    treating an axis as valued unless both tick sets are explicitly emptied.

  * Loudly FAILING, eight minutes later. That fix flagged a "plot a
    counterexample" problem whose axis is EMPTY — a blank numbered plane the
    student writes on. Its numbers are the grid's own scale, and scale is not
    another problem's data. A workspace was being called a figure.

  * Loudly FAILING again, on the count itself. The rule compared valued
    problems against ALL problems, so a sheet where every one of ten problems
    had its own graph failed because three of them were empty axes to plot on.
    What creates the ambiguity is the problem with nothing, so that is what is
    counted now.

All three are pinned here, because each fix is what exposed the next. The two
false-FAIL directions are the ones that cost most if they regress: a gate that
fails correct work teaches authors to degrade it, and the only edits that would
have satisfied these two were deleting the grids the problems needed.

Pure text parsing. Run: python3 tests/test_figure_scope.py
"""
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_layout import has_valued_figure  # noqa: E402

FAILS = []


def check(name, cond):
    print(f"  {'✅' if cond else '❌'} {name}")
    if not cond:
        FAILS.append(name)


def axis(opts, body=""):
    return (r"\begin{center}\begin{tikzpicture}" "\n"
            r"\begin{axis}[" + opts + "]\n" + body + "\n"
            r"\end{axis}\end{tikzpicture}\end{center}")


TICKED = "axis lines=center, xmin=-7, xmax=7, xtick={-6,-4,-2,2,4,6}, grid=both"

print("an empty plotting grid is workspace, not a figure")
check("a blank numbered plane carries no values",
      not has_valued_figure(axis(TICKED)))
check("whitespace and comments do not make it a figure",
      not has_valued_figure(axis(TICKED, "\n  % student plots here\n")))
check("an explicitly tick-free axis is still exempt",
      not has_valued_figure(axis(r"xtick=\empty, ytick=\empty")))

print()
print("an axis that draws anything is a figure again")
check("a plotted function is valued",
      has_valued_figure(axis(TICKED, r"\addplot[domain=-5:5]{2*x+1};")))
check("a drawn segment is valued",
      has_valued_figure(axis(TICKED, r"\draw (axis cs:1,1) -- (axis cs:4,5);")))
check("a placed label is valued",
      has_valued_figure(axis(TICKED, r"\node at (axis cs:2,3) {$P$};")))
check("a commented-out plot does not save it — the marks are still drawn",
      has_valued_figure(axis(TICKED, "% \\addplot {x};\n\\addplot {x};")))

print()
print("an axis the parser cannot read whole is assumed valued")
# The exemption is granted on evidence only: no \end{axis} means no body was
# read, and guessing "empty" there would be a silent PASS — the direction that
# already shipped a broken worksheet once.
check("an unterminated axis falls back to valued",
      has_valued_figure(r"\begin{tikzpicture}\begin{axis}[" + TICKED + "]"))
check("one empty axis plus one unreadable axis is still valued",
      has_valued_figure(axis(TICKED) + r"\begin{axis}[" + TICKED + "]"))

print()
print("the older branches still hold")
check("a tikz node with a number is valued",
      has_valued_figure(r"\begin{tikzpicture}\node at (0,0) {8 cm};"
                        r"\end{tikzpicture}"))
check("a value-free reference figure is not",
      has_valued_figure(r"\begin{tikzpicture}\node at (0,0) {$b$};"
                        r"\end{tikzpicture}") is False)
check("an included image is assumed valued",
      has_valued_figure(r"\includegraphics[width=5cm]{plot.png}"))

print()
print("the scope rule fires on the FIGURELESS problem, not the value-free one")

CHECKER = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "check_layout.py")
PLOTTED = axis(TICKED, r"\addplot[domain=-5:5]{2*x+1};")
BLANK = axis(TICKED)


def sheet(*problems):
    return "\n".join(rf"\problem[3cm]{{Problem {i}. {p}}}"
                     for i, p in enumerate(problems, 1))


def scope_fault(*problems):
    """The scope fault the CLI reports for a sheet of these problems, if any."""
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "ws_probe.tex")
        open(p, "w", encoding="utf-8").write(sheet(*problems))
        out = subprocess.run([sys.executable, CHECKER, p],
                             capture_output=True, text=True).stdout
    return next((ln for ln in out.splitlines()
                 if "carry no figure at all" in ln), None)


# The shape the pgfplots fix exists to catch: data on some problems, nothing
# at all on the others.
check("graphed problems beside figureless ones is a fault",
      scope_fault(PLOTTED, PLOTTED, "", "") is not None)
# The shape that fix wrongly broke: every problem has its own picture, some
# graph data and the rest are grids to plot on.
check("every problem carrying its own figure is clean",
      scope_fault(PLOTTED, PLOTTED, BLANK, BLANK) is None)
check("all-figureless is clean", scope_fault("", "", "") is None)
check("all-graphed is clean", scope_fault(PLOTTED, PLOTTED) is None)
# A blank grid is not a licence: it does not cover for a problem that has
# nothing, so one bare problem beside a graph is still a fault.
check("a blank grid does not excuse a problem with no figure",
      scope_fault(PLOTTED, BLANK, "") is not None)
# A macro-built figure is recognised as valued but is not a tikzpicture, so a
# narrow "has any picture" test called it valued AND figureless at once, and
# the rule reported all N problems in both counts on a fixture that had always
# passed. Anything valued is a figure, first and unconditionally.
check("a macro figure is not valued and figureless at the same time",
      scope_fault(r"\rtfig{$a=6$}{$b=8$}", r"\rtfig{$a=3$}{$b=4$}") is None)

print()
if FAILS:
    print(f"❌ {len(FAILS)} figure-scope check(s) failed: {FAILS}")
    sys.exit(1)
print("✅ figure scope: empty grids are workspace, drawn axes are figures")
