#!/usr/bin/env python3
"""
test_figure_convention.py — one right-triangle labelling convention, everywhere.

Why: templates/figure-macros.tex's \\refrt is the mandated value-free
reference figure — it TEACHES students how every triangle on the sheet is
labelled — and it sits on the same page as figures scripts/render_figures.py
constructs. The two once disagreed (\\refrt marked the right angle at B,
making b the hypotenuse; the renderer puts it at C, hypotenuse c), so one
worksheet taught two contradictory conventions. This test parses BOTH sources
as text and fails if they ever diverge again.

The parse is anchored, not guesswork:
  * scripts/render_figures.py declares RIGHT_ANGLE_VERTEX = "C" (a real
    constant its construction code uses — checked here too, so the constant
    cannot rot into decoration);
  * every right-angle-mark \\draw in figure-macros.tex (and in the taught
    examples in references/latex-templates.md) carries the load-bearing
    trailing comment "% right angle mark", and the marked vertex is the
    coordinate name the \\draw starts from.

Pure text parsing — no sympy, no LaTeX engine — so it runs anywhere CI does.
Run: python3 tests/test_figure_convention.py
"""

import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
RENDERER = os.path.join(ROOT, "scripts", "render_figures.py")
MACROS = os.path.join(ROOT, "templates", "figure-macros.tex")
TEMPLATES_DOC = os.path.join(ROOT, "references", "latex-templates.md")

FAILS = []


def check(name, cond, detail=""):
    print(f"  {'✅' if cond else '❌'} {name}")
    if not cond:
        if detail:
            print("     " + detail)
        FAILS.append(name)


def read(path):
    with open(path) as f:
        return f.read()


# the anchor in the .tex sources: a right-angle mark is drawn FROM its vertex
# coordinate and its \draw line ends in the load-bearing comment
MARK_RE = re.compile(r"\\draw \(([ABC])\)[^\n%]*% right angle mark")
CONST_RE = re.compile(r'^RIGHT_ANGLE_VERTEX = "([ABC])"$', re.M)

renderer_src = read(RENDERER)
macros_src = read(MACROS)
doc_src = read(TEMPLATES_DOC)

# 1. The renderer's declared convention.
m = CONST_RE.search(renderer_src)
check("render_figures.py declares RIGHT_ANGLE_VERTEX", m is not None,
      "scripts/render_figures.py must keep the RIGHT_ANGLE_VERTEX = \"...\" "
      "constant — it is the anchor this test (and the macro comments) point "
      "at. Restore it rather than inlining the letter.")
renderer_vertex = m.group(1) if m else None

# 2. The constant must be what the construction code actually uses — a
#    constant nobody reads is decoration, and the parse here would be a lie.
check("RIGHT_ANGLE_VERTEX drives the right_triangle construction",
      "angles[RIGHT_ANGLE_VERTEX] = math.pi / 2" in renderer_src
      and "{RIGHT_ANGLE_VERTEX: (\"right\",)}" in renderer_src,
      "scripts/render_figures.py's _render_right_triangle_figure must place "
      "the implied right angle and its square mark via RIGHT_ANGLE_VERTEX, "
      "not a hard-coded letter — otherwise this test checks a constant the "
      "renderer ignores.")

# 3. Every right-angle mark in the shipped macros agrees with the renderer.
macro_marks = MARK_RE.findall(macros_src)
check("figure-macros.tex has right-angle marks to check (\\rtfig + \\refrt)",
      len(macro_marks) >= 2,
      "expected at least two \"% right angle mark\" \\draw lines in "
      "templates/figure-macros.tex — that trailing comment is load-bearing "
      "(it is how this test finds the marks); do not drop or reword it.")
for i, v in enumerate(macro_marks):
    check(f"figure-macros.tex mark {i + 1}: right angle at {renderer_vertex}",
          v == renderer_vertex,
          f"templates/figure-macros.tex marks the right angle at {v} but "
          f"scripts/render_figures.py constructs it at {renderer_vertex} "
          "(RIGHT_ANGLE_VERTEX) — one worksheet would teach two "
          "contradictory labelling conventions. The renderer is the source "
          "of truth (its figures come from verified data): move the macro's "
          "mark, vertex names, and side letters to match it.")

# 4. The taught examples in the reference doc agree too — a doc example is
#    what generations copy, so it drifts worksheets just as effectively.
doc_marks = MARK_RE.findall(doc_src)
check("latex-templates.md has a right-angle-mark example to check",
      len(doc_marks) >= 1,
      "expected a \"% right angle mark\" \\draw line in the right-triangle "
      "template of references/latex-templates.md.")
for i, v in enumerate(doc_marks):
    check(f"latex-templates.md example {i + 1}: right angle at {renderer_vertex}",
          v == renderer_vertex,
          f"references/latex-templates.md shows the right angle at {v} but "
          f"scripts/render_figures.py constructs it at {renderer_vertex} "
          "(RIGHT_ANGLE_VERTEX) — fix the doc example to match the renderer.")

# 5. \refrt's own comment states which side is the hypotenuse; it must be the
#    side OPPOSITE the right-angle vertex (lowercase letter, and the named
#    edge must not touch that vertex).
hyp = re.search(
    r"([abc]) = ([ABC])([ABC]) \(opposite ([ABC]), the hypotenuse\)",
    macros_src)
check("figure-macros.tex documents the hypotenuse", hyp is not None,
      "templates/figure-macros.tex's \\refrt comment must state the "
      "convention in the parseable form "
      "\"c = AB (opposite C, the hypotenuse)\".")
if hyp and renderer_vertex:
    side, e1, e2, opp = hyp.groups()
    ok = (opp == renderer_vertex and side == renderer_vertex.lower()
          and renderer_vertex not in (e1, e2))
    check(f"hypotenuse is {renderer_vertex.lower()}, opposite {renderer_vertex}",
          ok,
          f"\\refrt's comment says hypotenuse {side} = {e1}{e2} opposite "
          f"{opp}, but with the right angle at {renderer_vertex} the "
          f"hypotenuse must be {renderer_vertex.lower()} (the side opposite "
          f"{renderer_vertex}, not touching it).")

print()
if FAILS:
    print(f"❌ {len(FAILS)} convention check(s) failed")
    sys.exit(1)
print("✅ figure labelling convention agrees across renderer, macros, and docs")
