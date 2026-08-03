#!/usr/bin/env python3
r"""test_figure_scope.py — pin both directions of check_layout's figure rule.

THE RULE. A worksheet may not carry a figure holding problem values on some
problems and not others. On paper the problems run together, and a student
reading problem 7 applies the figure sitting next to it — which belongs to
problem 8. Either every problem gets its own valued figure, or the shared
labelling moves into a value-free reference figure.

WHY THIS FILE. `has_valued_figure` has now been wrong in BOTH directions, one
after the other, eight minutes apart in the same eval run:

  * Silently PASSING. pgfplots draws numeric tick labels by default and draws
    them as axis ticks, not as \node text, so the tikz scan never saw them. A
    worksheet with graphs on 3 of 12 problems passed the gate. Fixed by
    treating an axis as valued unless both tick sets are explicitly emptied.

  * Loudly FAILING. That fix then flagged a "plot a counterexample" problem
    whose axis is EMPTY — a blank numbered plane the student writes on. Its
    numbers are the grid's own scale, and scale is not another problem's data,
    so there is nothing to misapply. A workspace was being called a figure.

Both directions matter and they pull against each other, so both are pinned
here. The second is the one that costs most if it regresses: a gate that fails
correct work teaches authors to degrade it — the way to satisfy this one is to
delete the grid the problem needs.

Pure text parsing. Run: python3 tests/test_figure_scope.py
"""
import os
import sys

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
if FAILS:
    print(f"❌ {len(FAILS)} figure-scope check(s) failed: {FAILS}")
    sys.exit(1)
print("✅ figure scope: empty grids are workspace, drawn axes are figures")
