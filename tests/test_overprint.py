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
  - a FIGURE LABEL printed on top of another figure label is caught, and the
    innocent same-column stacks it must not be confused with stay silent
  - the AMBIGUOUS-SSA coverage boundary, in both directions: the label-over-
    label collision at the swing apex is caught, and the label-over-PATH one at
    a flat angle is not (see SSA_MEASURED and the SSA section of main())

Calibration record: across 450 PDFs this repository had already produced and
gated, the tuned detector fires on exactly one, and that one has a genuine
caption collision confirmed by looking at the rendered page. Before the noise
rules it fired on 77.

FIGURE-LABEL CALIBRATION (`stacked_label`). The 0.45 area threshold is a prose
number and misses figure labels entirely: a `?` dropped onto a length digit
hides the digit while covering only 0.19-0.30 of the smaller box, because most
of a word box is leading, not ink. The geometry below is measured, not invented
— every tuple in GEOMETRY is copied out of `pdftotext -bbox` on a real PDF in
evals/runs, and each was checked by rendering the page to PNG and looking at it:

  caught   curr-428 worksheet p3   '?' over '9'    vertical interpenetration .45
  caught   curr-428 worksheet p4   '?' over '25'                             .34
  silent   curr-428 worksheet p6   'B' with subscript '2'   (adjacent, not stacked)
  silent   curr-127 answer_key p1  \frac{8}{23}                              .22
  silent   curr-463 answer_key p1  two crowded fraction lines                .26
  silent   curr-202 answer_key p2  \sqrt[3]{} index over the surd            .38
  silent   curr-431 answer_key p3  denominator over a degree mark            .22
  silent   curr-200 answer_key p3  \underbrace label under its brace         .31

The last three are the ones that make a naive rule cry wolf. curr-202 and
curr-431 are poppler radical-boxing artifacts on visually clean pages — the
surd is mis-decoded as a word and its box swallows what it covers. They are
rejected by font size: everything TeX legitimately stacks is set smaller than
what it sits over, while a stray label is set at full size.

Over all 900 PDFs in evals/runs the rule fires on two pages, both curr-428,
both confirmed by eye. Before it, the detector fired on none of them.

Requires pdflatex/tectonic and pdftotext; skips cleanly without them.
"""
import json
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
# The last two problems are the figure-label rule's own noise cases: a cube
# root, whose index poppler reports as a word overlapping the surd by 0.38, and
# an underbrace, whose label sits squarely under the brace.
CLEAN = HEAD + r"""
\problem[2cm]{Evaluate $\sqrt{x^2 + y_1}$ and $\dfrac{a+b}{c-d}$.}
\problem[2cm]{Given $\triangle ABC \cong \triangle DEF$, name the parts.}
\problem[2cm]{Continue the pattern $2, 4, 6, \ldots$ and explain.}
\problem[2cm]{Simplify $\sqrt[3]{\dfrac{8}{125}}$ and $\dfrac{3}{x^2}$.}
\problem[2cm]{Name the parts of
  $\underbrace{2x + 5}_{\text{lower bound}} \le 17$.}
\end{document}
"""

# The defect this rule exists for, reproduced. A `?` marker set at the same size
# as a length label and dropped onto it — the geometry of the SSA figures in
# curr-428, where the arc's "?" landed on the digit of a side label. 0.24cm puts
# the two baselines 6.8pt apart, which is what the real figure produced (6.97pt
# on curr-428 p4), and the `?`'s dot lands inside the `2`. The boxes then share
# 39% of the smaller: a genuine, unreadable collision that the 0.45 prose
# threshold does not see. If this probe ever starts passing the prose threshold
# it has stopped testing the label rule — hence the explicit assertion below.
COLLIDING_LABEL = HEAD + r"""
\problem[3cm]{A length label with a marker dropped onto it:
\begin{center}\begin{tikzpicture}
\node at (0,0) {25};
\node at (-0.04,0.24) {?};
\end{tikzpicture}\end{center}}
\end{document}
"""

# Boxes copied verbatim from `pdftotext -bbox` on PDFs in evals/runs, so the
# rule is pinned against measured typesetting rather than against a guess about
# what typesetting looks like. (x0, y0, x1, y1, text); see the module docstring
# for which page each came from and how each was verified.
GEOMETRY = [
    # (label, word a, word b, must_flag)
    ("a '?' marker printed on a length digit (curr-428 p3)",
     (337.545, 181.880091, 343.073084, 192.496309, "?"),
     (339.298626, 187.770091, 345.151892, 198.386309, "9"), True),
    ("a '?' marker printed on a two-digit length (curr-428 p4)",
     (334.881, 190.977091, 340.409084, 201.593309, "?"),
     (335.586626, 197.949091, 347.293158, 208.565309, "25"), True),
    ("a subscript beside its base (curr-428 p6, $B_2$)",
     (301.08, 199.56, 309.97, 210.17, "B"),
     (309.97, 204.11, 314.21, 211.19, "2"), False),
    ("a fraction's numerator over its denominator (curr-127 p1)",
     (324.298, 185.403751, 328.532514, 192.481199, "8"),
     (324.298, 190.895751, 332.767028, 197.973199, "23"), False),
    ("two crowded fraction lines (curr-463 p1)",
     (349.321, 199.239751, 354.087917, 206.317199, "x"),
     (347.099, 204.444751, 355.568028, 211.522199, "25"), False),
    ("a cube root's index over the surd (curr-202 p2)",
     (151.904, 562.580792, 163.8592, 570.23212, "q"),
     (154.893, 568.225546, 158.545911, 573.533654, "3"), False),
    ("a denominator over a degree mark (curr-431 p3)",
     (176.586, 95.084751, 181.352917, 102.162199, "x"),
     (177.218, 100.622425, 181.452514, 108.146199, "◦"), False),
    ("an underbrace over its label (curr-200 p3)",
     (247.798, 112.985792, 258.55768, 120.63712, "{z"),
     (235.179, 118.448751, 254.475409, 125.526199, "lower"), False),
]


# ── the ambiguous-SSA coverage boundary ──────────────────────────────────────
# evals/AUTHORING.md carries a KNOWN-OPEN note saying the SSA swing label defect
# is ungated and is bounded by "prefer A >= 30 degrees on ambiguous-SSA
# problems". An author hit a genuine collision at A = 44 degrees, so neither
# half holds. Re-measured here by rendering:
#
#   A = 44, a = 310, b = 400   the "?" arc label at the near apex B_2 lands on
#                              the "0" of the swing side's "a = 310" label. Two
#                              WORD boxes, 54% overlap of the smaller — above
#                              the 0.45 prose threshold, so the ORDINARY rule
#                              catches it. Confirmed by rendering the page to
#                              PNG: the label reads "a = 310?".
#   A = 15/25 (the AUTHORING.md cases)  the swing label lands on the BASE LINE,
#                              a TikZ path. No second word box exists, so this
#                              gate is silent — correctly, and permanently.
#
# The two look identical on the page and are opposite here. That is the fact
# the docs have to state, and it is what these boxes pin. Copied verbatim from
# `pdftotext -bbox` on the rendered probe.
SSA_MEASURED = (
    (320.917828, 229.391085, 337.281478, 239.078365, "310"),
    (334.368, 229.011085, 339.519277, 238.698365, "?"),
)

# The same two givens, as scripts/render_figures.py takes them, for the
# end-to-end render below. A = 44 must flag; A = 15 must not.
SSA_CASES = [
    ({"A": 44, "a": 310, "b": 400}, True,
     "A = 44 deg — label ON label at the swing apex, above the 'prefer A >= 30' bound"),
    ({"A": 15, "a": 30, "b": 20}, False,
     "A = 15 deg — label on the base PATH, which no word-box gate can see"),
]

SSA_DOC_HEAD = HEAD + "\\input{figs_ssa.tex}\n"


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


def ssa_probe(given, workdir, name):
    r"""Render ONE ambiguous-SSA swing figure from its givens and compile it.

    The figure is built by scripts/render_figures.py from the same `given` dict
    verify.py checks, so this probe is the real renderer's output rather than a
    hand-placed imitation of it — the point is what authors actually get.
    Returns the PDF path, or None when the renderer cannot run (no sympy).
    """
    d = os.path.join(workdir, name)
    os.makedirs(d, exist_ok=True)
    for f in os.listdir(TEMPLATES):
        if f.endswith(".tex"):
            shutil.copy(os.path.join(TEMPLATES, f), d)
    vj = os.path.join(d, "verify_ssa.json")
    with open(vj, "w") as fh:
        json.dump({"topic": "ssa", "problem_count": 1,
                   "problems": [{"id": 1, "type": "triangle", "given": given,
                                 "solve_for": "B", "expected": 0}]}, fh)
    r = subprocess.run(
        [sys.executable, os.path.join(ROOT, "scripts", "render_figures.py"),
         vj, os.path.join(d, "figs_ssa.tex")], capture_output=True, text=True)
    if r.returncode != 0 or not os.path.isfile(os.path.join(d, "figs_ssa.tex")):
        return None
    open(os.path.join(d, "p.tex"), "w").write(
        SSA_DOC_HEAD + "\\problem[3cm]{Solve the triangle. \\probfig{1}}\n"
        "\\end{document}\n")
    eng = shutil.which("pdflatex") or shutil.which("tectonic")
    cmd = ([eng, "-interaction=nonstopmode", "p.tex"] if eng.endswith("pdflatex")
           else [eng, "p.tex"])
    subprocess.run(cmd, cwd=d, capture_output=True)
    pdf = os.path.join(d, "p.pdf")
    return pdf if os.path.isfile(pdf) else None


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

    print("figure labels, on geometry measured off real pages")
    for label, a, b, must_flag in GEOMETRY:
        got = op.stacked_label(a, b)
        check(f"{'flagged' if must_flag else 'silent'}: {label}", got == must_flag,
              f"stacked_label returned {got}")
    # The whole point: these sit under the prose threshold, so the page-level
    # check has to catch them through the label rule or not at all.
    for label, a, b, must_flag in GEOMETRY:
        if not must_flag:
            continue
        f = op.overlap_fraction(a[:4], b[:4])
        check(f"under the prose threshold, so only the label rule sees it "
              f"({f * 100:.0f}% < {op.OVERLAP * 100:.0f}%)", f < op.OVERLAP)
        onpage = op.page_faults(612.0, 792.0, [a, b], op.OVERLAP)
        check(f"reported as a page fault: {label}",
              any(k == "overprint" for k, _ in onpage),
              f"page_faults returned {onpage}")

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

        marker = build(COLLIDING_LABEL, tmp, "label")
        if not marker:
            check("the marker-on-label probe compiles", False, "no PDF produced")
        else:
            pair = [w for _, _, ws in op.words_by_page(marker) for w in ws
                    if w[4].strip() in ("?", "25")]
            worst = max((op.overlap_fraction(x[:4], y[:4])
                         for x in pair for y in pair if x is not y), default=0.0)
            check(f"the probe stays under the prose threshold, so only the "
                  f"label rule can catch it ({worst * 100:.0f}% < "
                  f"{op.OVERLAP * 100:.0f}%)",
                  0.0 < worst < op.OVERLAP, f"measured {worst:.3f}")
            f = faults(marker)
            check("a marker printed on a figure label is caught", len(f) >= 1,
                  "the detector saw nothing")

        print("ambiguous-SSA coverage, on geometry measured off a rendered page")
        a, b = SSA_MEASURED
        frac = op.overlap_fraction(a[:4], b[:4])
        check(f"the A = 44 deg swing-apex collision is above the PROSE "
              f"threshold, so the ordinary rule catches it — it is not an "
              f"unseen figure defect ({frac * 100:.0f}% >= "
              f"{op.OVERLAP * 100:.0f}%)",
              frac >= op.OVERLAP, f"measured {frac:.3f}")
        check("and it is reported as a page fault",
              any(k == "overprint" for k, _ in
                  op.page_faults(612.0, 792.0, [a, b], op.OVERLAP)))

        print("...and end to end, through the real figure renderer")
        for given, must_flag, why in SSA_CASES:
            pdf = ssa_probe(given, tmp, "ssa%s" % given["A"])
            if pdf is None:
                print(f"  ·  skipped ({why}): renderer unavailable")
                continue
            got = bool(faults(pdf))
            check(f"{'flagged' if must_flag else 'silent'}: {why}",
                  got == must_flag,
                  f"faults: {faults(pdf)}")

        # The vertex-crowding fix, pinned on the geometry that motivated it.
        # A = 15, a = 25, b = 26 collided TWICE before it: "C" on the "26" of
        # its own fixed-side label (63% of the smaller) and "A" on "B_2" (66%).
        # The second was the commonest fault in the whole figure — 10 of the 12
        # collisions in a 33-geometry sweep — because B_2 slides toward A on a
        # thin triangle and the centroid anchor aims its label down-LEFT, onto
        # A. Both are VERTEX labels, which no placement rule modelled.
        print("...and the vertex-crowding fix holds on the geometry that "
              "motivated it")
        thin = ssa_probe({"A": 15, "a": 25, "b": 26}, tmp, "ssathin")
        if thin is None:
            print("  ·  skipped: renderer unavailable")
        else:
            f = faults(thin)
            check("A = 15, a = 25, b = 26 no longer overprints its vertex "
                  "labels", not f, "; ".join(m for _, m in f)[:200])
            # A gate that has stopped seeing a fault and a fault that is gone
            # look identical from here, so assert the fix moved the LABEL, not
            # just the verdict: B_2 must now be placed away from A along the
            # base rather than back toward it.
            fig = open(os.path.join(tmp, "ssathin", "figs_ssa.tex")).read()
            b2 = [ln for ln in fig.splitlines() if "B_2" in ln]
            check("B_2's label is shifted away from A, not toward it",
                  bool(b2) and "xshift=6.0pt" in b2[0], b2[0] if b2 else "")

            # ADJACENCY, which this gate is structurally unable to report.
            # The page used to read "b = 26C": "26" ended at 301.85pt and "C"
            # started at 301.23 — 0.6pt of overlap, 8% of the C, against a 45%
            # rule. So assert the measured GAP, not the verdict. Standing the
            # vertex letters off along the outward angle bisector and pushing a
            # thin figure's side labels further off their own side opens it to
            # about +0.7pt with 8.6pt of vertical daylight.
            box = {}
            for _pw, _ph, words in op.words_by_page(thin):
                for x0, y0, x1, y1, t in words:
                    box.setdefault(t, []).append((x0, y0, x1, y1))
            if "26" in box and "C" in box:
                lab, vert = box["26"][0], box["C"][0]
                check("the apex letter and the side label it sits beside do "
                      "not touch — measured, because the 45% rule cannot see "
                      "a 0.6pt overlap",
                      vert[0] - lab[2] > 0.0,
                      f"'26' ends {lab[2]:.2f}, 'C' starts {vert[0]:.2f}")
            else:
                check("the probe printed both '26' and 'C'", False, str(sorted(box)[:12]))

        good = build(CLEAN, tmp, "clean")
        if not good:
            check("the clean probe compiles", False, "no PDF produced")
        else:
            f = faults(good)
            check("radicals, congruence, fractions, cube roots, underbraces "
                  "and ellipses stay clean",
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
