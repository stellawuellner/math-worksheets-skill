#!/usr/bin/env python3
r"""
test_preamble_layout.py — pin the PRINTED behaviour of the shipped preamble.

These are not source-lint rules: they compile a document and read the resulting
PDF, because the faults they cover are only visible on the page.

1. OBSERVANT ANSWER LINE. \problem auto-emits one "Answer: ____" when it has
   workspace. On a multi-part problem that single line is wrong: three
   sub-parts need three answers, and one trailing blank invites the student to
   commit a single value. \ansline/\ansblank/\answerline clear the auto-emit
   flag and \problem tests it AFTER typesetting the stem, so a stem that
   already carries answer locations suppresses the parent's line. Pinned by
   counting printed "Answer:" strings.

2. HEADER COLLISION. fancyhdr sets [L] and [R] at their natural widths, so a
   title longer than the leftover space printed straight through the Name/Date
   blanks — on every page, because a running head repeats. Both boxes are now
   shrink-to-fit within a reserved width. Pinned by reading word bounding
   boxes and asserting the title's right edge is left of the blanks.

3. DATE ON PAGE 1 ONLY. Continuation pages carry "(continued)", not a second
   set of Name/Date blanks.

4. THE LEVEL PRINTS ON THE KEY, NOT ON THE SHEET. \wstitleblock still accepts
   its course/level argument and no longer prints it: a grade label on the page
   a student holds tells them nothing they need, and tells a child working a
   grade off something unhelpful before they reach the mathematics.
   \aktitleblock keeps printing it, because that is the adult's document. The
   argument surviving in the signature is what makes a regression here silent
   in the source — every document still compiles either way — so it is pinned
   on the rendered page, from both directions.

5.5 WORKSPACE GLUE INSIDE A \problem STEM SURVIVES A PAGE BREAK — which is
   why check_layout must not call it "outside any minipage". \problem opens its
   minipage IN THE PREAMBLE, so a \vspace written in a stem has no
   \begin{minipage} beside it to count, and check_layout's minipage_depth_fn
   (which counts literal tokens in the body) read depth 0 and reported the
   space as glue that will vanish at a page break. It will not: the minipage is
   unbreakable, so the whole problem moves to the next page with its glue
   intact. That is the wrong diagnosis on the sheet shape SKILL.md teaches
   first, and 284 of the 600 recorded worksheets carry workspace glue in that
   exact position. Pinned from the page, in both directions: the in-stem glue
   is measured across a forced page boundary and must still be there, while the
   same glue OUTSIDE any minipage must be shown to disappear — otherwise this
   test would be pinning a rule that has stopped protecting anything.

5.6 A BLANK PLOTTING GRID IS WRITING SPACE. check_layout's work-space floor
   counts glue only, so a problem whose room to work is an empty coordinate
   plane measured 0cm and needed an artificial \problem[Ncm] adding blank paper
   under a grid the student writes on. A grid carrying DATA is still a figure
   and still fails the floor, which is the distinction has_valued_figure
   already draws.

6. COMMON-ERROR BLOCK FITS THE LINE. \commonerror opens a paragraph; it did not
   close one, so the closing full-width \rule of the generated "Common wrong
   answers" block joined the last entry's text line and overflowed it by ~200pt.
   Every answer key declaring a trap failed compile-ak, while the feature's own
   fixtures only ever checked the JSON. Three separate eval-run agents hit it
   before any test did. Pinned by compiling the block and reading the log.

Requires pdflatex (or tectonic) and pdftotext. Skips cleanly when absent.
Exit 0 all pinned, 1 on any regression.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES = os.path.join(ROOT, "templates")

DOC = r"""
\documentclass[12pt]{article}
\usepackage[margin=1in, top=0.75in, bottom=0.75in]{geometry}
\input{worksheet-preamble}
\wsheader{Slope, Slope-Intercept Form and Linear Function Modelling Practice Set}
\begin{document}
\wstitleblock{Slope and Slope-Intercept Form}{Algebra 1}{}
\problem[4cm]{Single-answer problem: it should get exactly one answer line.}
\problem[4cm]{Multi-part WITH workspace: the parent must NOT add its own line.
\begin{enumerate}[label=(\alph*), itemsep=2.5cm, leftmargin=1.5cm]
  \item first part \ansline
  \item second part \ansline
\end{enumerate}}
\newpage
\problem[4cm]{A page-two problem.}
\end{document}
"""

failures = []


# A minimal answer key carrying the generated block, entries then closing rule —
# byte-for-byte the shape render_quick_answers.py emits.
COMMON_ERROR_DOC = r"""
\documentclass[12pt]{article}
\usepackage[margin=1in, top=0.75in, bottom=0.75in]{geometry}
\input{worksheet-preamble}
\akheader{Trap Check}
\begin{document}
\aktitleblock{Trap Check}{Test}{}
\medskip\noindent{\small\textbf{Common wrong answers}}\par\nopagebreak
\vspace{2pt}\noindent\rule{\linewidth}{0.4pt}\par\nopagebreak
\commonerror{1}{7.37}{used cos instead of tan}
\commonerror{2}{12.9}{added the legs instead of using the hypotenuse}
\noindent\rule{\linewidth}{0.4pt}\medskip
\problem{$9\tan 35^\circ = \ans{6.30}$}
\end{document}
"""


LEVEL_KEY_DOC = r"""
\documentclass[12pt]{article}
\usepackage[margin=1in, top=0.75in, bottom=0.75in]{geometry}
\input{worksheet-preamble}
\akheader{Slope and Slope-Intercept Form}
\begin{document}
\aktitleblock{Slope and Slope-Intercept Form}{Algebra 1}{}
\problem{$m = \ans{3}$}
\end{document}
"""


# 5.5 — an unstarred workspace \vspace written INSIDE a \problem stem, with
# enough problems ahead of it to drive it onto a page boundary. If the glue
# were discarded at the break the two markers would end up a line apart.
GEOMETRY_LINE = (r"\usepackage[margin=1in, top=0.75in, bottom=0.75in]{geometry}")
STEM_GLUE_DOC = r"""
\documentclass[12pt]{article}
""" + GEOMETRY_LINE + r"""
\input{worksheet-preamble}
\wsheader{Stem glue at a page break}
\begin{document}
\wstitleblock{Stem glue at a page break}{Test}{}
\problem[5cm]{Filler one.}
\problem[5cm]{Filler two.}
\problem[5cm]{Filler three.}
\problem{STEMGLUEA marker, then five centimetres of unstarred glue in the stem.
\par\vspace{5cm}\noindent STEMGLUEB marker.}
\end{document}
"""

# The control: identical glue, no minipage anywhere near it, landing at the
# same break. This is the fault the rule exists for and it must still bite.
LOOSE_GLUE_DOC = r"""
\documentclass[12pt]{article}
""" + GEOMETRY_LINE + r"""
\begin{document}
\noindent Filler.\par\vspace{20cm}
\noindent LOOSEGLUEA marker.\par\vspace{5cm}
\noindent LOOSEGLUEB marker.
\end{document}
"""

# 5.6 — the same sheet twice: a blank plotting grid (a place to write) and a
# grid carrying plotted data (a figure to read). Only the first is workspace.
GRID_DOC = r"""
\documentclass[12pt]{article}
""" + GEOMETRY_LINE + r"""
\input{worksheet-preamble}
\wsheader{Grid}
\begin{document}
\wstitleblock{Grid}{Test}{}
\problem[5cm]{Solve $2x + 3 = 11$.}
\problem{Plot your counterexample on the grid below.
\begin{center}\begin{tikzpicture}
\begin{axis}[width=8cm, height=8cm, grid=both, xmin=-5, xmax=5, ymin=-5, ymax=5]
\end{axis}
\end{tikzpicture}\end{center}}
\end{document}
"""

VALUED_GRID_DOC = GRID_DOC.replace(
    r"\begin{axis}[width=8cm, height=8cm, grid=both, xmin=-5, xmax=5, ymin=-5, ymax=5]"
    "\n" r"\end{axis}",
    r"\begin{axis}[width=8cm, height=8cm, xmin=-5, xmax=5, ymin=-5, ymax=5]"
    "\n" r"\addplot {2*x + 1};" "\n" r"\end{axis}").replace(
    "Plot your counterexample on the grid below.",
    "Read the value of $y$ at $x = 2$ from this graph.")

# ...and the third case, which is why the exemption is an `axis` and nothing
# else: an AREA MODEL is a grid path too, and the student counts its squares
# rather than writing in them. It needs room beside it exactly as the floor
# says. Copied in shape from a recorded worksheet that a wider rule exempted.
AREA_MODEL_DOC = GRID_DOC.replace(
    r"\begin{axis}[width=8cm, height=8cm, grid=both, xmin=-5, xmax=5, ymin=-5, ymax=5]"
    "\n" r"\end{axis}",
    r"\draw[step=1, gray!55, thin] (0,0) grid (4,3);" "\n"
    r"\draw[thick] (0,0) rectangle (4,3);").replace(
    "Plot your counterexample on the grid below.",
    "Rosa cut this rectangle into two parts. Are they the same size?")

CM = 72.0 / 2.54          # PDF points per centimetre


def check(label, cond, detail=""):
    print(("  ok   " if cond else "  FAIL ") + label + ("" if cond else f" -- {detail}"))
    if not cond:
        failures.append(label)


def words_with_boxes(pdf, page):
    xml = subprocess.run(["pdftotext", "-bbox", "-f", str(page), "-l", str(page), pdf, "-"],
                         capture_output=True, text=True).stdout
    return [(float(a), float(b), float(c), t) for a, b, c, t in re.findall(
        r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="[\d.]+">([^<]*)</word>', xml)]


def main():
    engine = shutil.which("pdflatex") or shutil.which("tectonic")
    if not engine or not shutil.which("pdftotext"):
        print("test_preamble_layout: no LaTeX engine or pdftotext — skipped")
        return 0

    with tempfile.TemporaryDirectory() as d:
        for f in os.listdir(TEMPLATES):
            if f.endswith(".tex"):
                shutil.copy(os.path.join(TEMPLATES, f), d)
        tex = os.path.join(d, "t.tex")
        open(tex, "w").write(DOC)
        cmd = ([engine, "-interaction=nonstopmode", "t.tex"] if engine.endswith("pdflatex")
               else [engine, "t.tex"])
        subprocess.run(cmd, cwd=d, capture_output=True)
        pdf = os.path.join(d, "t.pdf")
        if not os.path.exists(pdf):
            print("  FAIL document did not compile")
            return 1

        print("1. observant answer line")
        p1 = subprocess.run(["pdftotext", "-f", "1", "-l", "1", pdf, "-"],
                            capture_output=True, text=True).stdout
        n = p1.count("Answer:")
        # problem 1 contributes 1; problem 2 contributes 2 (one per part) and
        # its parent must contribute none. A regression re-adds the parent's
        # line and makes this 4.
        check("multi-part parent adds no extra answer line", n == 3,
              f"expected 3 printed 'Answer:' on page 1, got {n}")

        print("2. header does not collide")
        w = words_with_boxes(pdf, 1)
        band = min(x[1] for x in w)
        head = [x for x in w if abs(x[1] - band) < 6]
        left = [x for x in head if x[3] not in ("Name:", "Date:")]
        right = [x for x in head if x[3] in ("Name:", "Date:")]
        check("Name/Date blanks present in the page-1 head", bool(right))
        if left and right:
            tmax = max(x[2] for x in left)
            bmin = min(x[0] for x in right)
            check("title clears the Name/Date blanks", tmax < bmin,
                  f"title right edge {tmax:.1f} overlaps first blank at {bmin:.1f}")

        print("3. date blanks on page 1 only")
        p2 = subprocess.run(["pdftotext", "-f", "2", "-l", "2", pdf, "-"],
                            capture_output=True, text=True).stdout
        check("page 2 has no second Date blank", "Date:" not in p2)
        check("page 2 carries the continuation marker", "(continued)" in p2)

        print("4. the level is on the key, not on the student's sheet")
        # \wstitleblock still TAKES the course/level argument, so a regression
        # is silent in the source: every document keeps compiling and the level
        # simply reappears in front of the child. Only the page shows it.
        check("the worksheet title block prints no grade level",
              "Algebra 1" not in p1, "the level printed on the student's sheet")
        lv = os.path.join(d, "lv.tex")
        with open(lv, "w") as fh:
            fh.write(LEVEL_KEY_DOC)
        lvcmd = ([engine, "-interaction=nonstopmode", "lv.tex"]
                 if engine.endswith("pdflatex") else [engine, "lv.tex"])
        subprocess.run(lvcmd, cwd=d, capture_output=True)
        lvpdf = os.path.join(d, "lv.pdf")
        if os.path.isfile(lvpdf):
            key = subprocess.run(["pdftotext", lvpdf, "-"],
                                 capture_output=True, text=True).stdout
            check("the answer key title block still prints it",
                  "Algebra 1" in key, "the adult lost the level entirely")
        else:
            check("the level-key probe compiles", False, "no PDF produced")

        print("5.5 workspace glue inside a \\problem stem survives a break")

        def build(doc, stem):
            path = os.path.join(d, stem + ".tex")
            with open(path, "w") as fh:
                fh.write(doc)
            cmd = ([engine, "-interaction=nonstopmode", stem + ".tex"]
                   if engine.endswith("pdflatex") else [engine, stem + ".tex"])
            subprocess.run(cmd, cwd=d, capture_output=True)
            out = os.path.join(d, stem + ".pdf")
            return out if os.path.isfile(out) else None

        def marker(pdf, text, pages=4):
            """(page, y) of a marker word, or None."""
            for pg in range(1, pages + 1):
                for x0, y0, x1, t in words_with_boxes(pdf, pg):
                    if t.strip(",.").strip() == text:
                        return pg, y0
            return None

        sg = build(STEM_GLUE_DOC, "stemglue")
        if not sg:
            check("the stem-glue probe compiles", False, "no PDF produced")
        else:
            a, b = marker(sg, "STEMGLUEA"), marker(sg, "STEMGLUEB")
            check("both stem-glue markers are on the page", a is not None and b is not None)
            if a and b:
                check("the problem moved to a page of its own (the minipage "
                      "cannot break)", a[0] == b[0], f"{a[0]} vs {b[0]}")
                gap = b[1] - a[1]
                check(f"the 5cm of unstarred glue is still there across the "
                      f"break ({gap / CM:.2f}cm)", gap >= 5.0 * CM,
                      f"measured {gap:.1f}pt, wanted >= {5.0 * CM:.1f}pt")

        lg = build(LOOSE_GLUE_DOC, "looseglue")
        if not lg:
            check("the loose-glue control compiles", False, "no PDF produced")
        else:
            a, b = marker(lg, "LOOSEGLUEA"), marker(lg, "LOOSEGLUEB")
            check("both loose-glue markers are on the page",
                  a is not None and b is not None)
            if a and b:
                # The control: the SAME 5cm, outside any minipage, at a break.
                # It must be gone, or the fault this rule reports is imaginary.
                check("the same glue OUTSIDE a minipage is discarded at the "
                      "break (so the rule still protects something)",
                      b[0] > a[0] and b[1] < 3.0 * CM,
                      f"after-marker landed on page {b[0]} at y={b[1]:.1f}pt")

        # ...and the checker must agree with the page.
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import check_layout  # noqa: E402
        def stranded_pair(doc):
            """(faults, stem notes) — tolerant of the pre-fix single-list
            return, so this assertion FAILS against the old checker instead of
            crashing on the signature."""
            res = check_layout.stranded_workspace(check_layout.strip_comments(doc))
            if isinstance(res, tuple) and len(res) == 2:
                return res
            return res, []

        stranded, in_stem = stranded_pair(STEM_GLUE_DOC)
        check("check_layout does not call stem glue 'outside any minipage'",
              not stranded, f"reported {stranded}")
        check("it reports it as a stem-placement note instead", len(in_stem) == 1)
        loose, _ = stranded_pair(LOOSE_GLUE_DOC)
        check("and the genuinely stranded glue is still a fault",
              any(cm == 5.0 for _, cm in loose), f"reported {loose}")

        print("5.6 a blank plotting grid counts as writing space")
        for doc, stem, want in ((GRID_DOC, "grid", 0),
                                (VALUED_GRID_DOC, "gridval", 1),
                                (AREA_MODEL_DOC, "gridarea", 1)):
            p = os.path.join(d, stem + "_ws.tex")
            with open(p, "w") as fh:
                fh.write(doc)
            rc = subprocess.run(
                [sys.executable, os.path.join(os.path.dirname(
                    os.path.abspath(__file__)), "check_layout.py"), p],
                capture_output=True, text=True)
            floor = "of WRITING space" in rc.stdout
            names = {"grid": "a blank plotting grid satisfies the work-space floor",
                     "gridval": "a grid carrying plotted data does not",
                     "gridarea": "an area model the student counts does not"}
            check(names[stem], floor == bool(want), rc.stdout[-400:])

        print("6. common-error block fits the line")
        ce = os.path.join(d, "ce.tex")
        with open(ce, "w") as fh:
            fh.write(COMMON_ERROR_DOC)
        cecmd = ([engine, "-interaction=nonstopmode", "ce.tex"]
                 if engine.endswith("pdflatex") else [engine, "ce.tex"])
        r = subprocess.run(cecmd, cwd=d, capture_output=True, text=True)
        log = os.path.join(d, "ce.log")
        text = open(log, encoding="utf-8", errors="replace").read() if os.path.isfile(log) else r.stdout
        over = [m for m in re.findall(r"Overfull \\hbox \(([0-9.]+)pt too wide\)", text)
                if float(m) > 2.0]
        check("a trap-bearing answer key has no overfull line",
              not over, f"overfull by {', '.join(over)}pt")
        cepdf = os.path.join(d, "ce.pdf")
        if os.path.isfile(cepdf):
            body = subprocess.run(["pdftotext", cepdf, "-"],
                                  capture_output=True, text=True).stdout
            check("the common-wrong-answer text still prints",
                  "used cos instead of tan" in body)



        # ── v3.6: the key breathes, the worksheet stays measured ────────────
        # \akheader turns on rubber inter-problem glue and \raggedbottom;
        # the worksheet keeps fixed 0.4cm. Pinned at the source level because
        # the rendered difference is glue, which a word-box read cannot see.
        pre_src = open(os.path.join(TEMPLATES, "worksheet-preamble.tex")).read()
        print("8.5 answer keys breathe; worksheets are measured")
        check("\\problem's ak leg is rubber and its ws leg is fixed",
              "plus 0.45cm" in pre_src and
              "\\else\\vspace{0.4cm}\\fi" in pre_src.replace(" ", ""))
        # exactly one \raggedbottom in the whole preamble, and it sits inside
        # \akheader's definition — position-checked against the \newcommand,
        # not against the word "akheader", which first appears in prose.
        ak_def = pre_src.index(r"\newcommand{\akheader}")
        ss_def = pre_src.index(r"\newcommand{\ssheader}")
        # count CODE occurrences only: the design comment above \akheader
        # also says \raggedbottom, and a comment is not a setting.
        code = "\n".join(l.split("%", 1)[0] for l in pre_src.split("\n"))
        check("\\akheader sets raggedbottom, and nothing else does",
              code.count(r"\raggedbottom") == 1
              and ak_def < pre_src.rindex(r"\raggedbottom") < ss_def)

        # ── \ans in a STUDY GUIDE, both authoring forms ──────────────────────
        # \akheader replaces \ans with a text-safe compact box; \ssheader does
        # not, so in an ss_ document \ans is the base definition. That was a
        # bare \boldsymbol -- math-only -- and every shipped exemplar happens to
        # write $\ans{...}$, so the text-mode path was never exercised until an
        # end-to-end build followed SKILL.md's prose ("print each result with
        # \ans{...}") instead of copying a template. The result was
        # "! Missing $ inserted", fatal, on compile-ss: the last gate of the
        # chain, with the error naming a line two away from the cause.
        # \ensuremath fixed it without changing math-mode output at all (visual
        # regression: 0 of 2304 cells moved on study_guide_boxes). Pinned from
        # both directions because a "simplification" back to \boldsymbol still
        # compiles every document that wraps it in $...$.
        print("8. \\ans works in a study guide in text mode AND math mode")
        ss = os.path.join(d, "ansmode.tex")
        open(ss, "w").write(
            "\\documentclass[12pt]{article}\n"
            "\\usepackage[margin=0.85in, top=0.7in, bottom=0.7in]{geometry}\n"
            "\\input{worksheet-preamble}\n\\ssheader{Modes}\n"
            "\\begin{document}\n\\sstitleblock{Modes}\n"
            "\\begin{examplebox}\n"
            "\\step{Strategy: clear the constant, then divide.}\n"
            "\\step{Text mode: \\ans{x = 31}}\n"
            "\\end{examplebox}\n"
            "\\begin{examplebox}\n"
            "\\step{Strategy: the same, keyed the documented way.}\n"
            "\\step{Math mode: $\\ans{x = 47}$}\n"
            "\\end{examplebox}\n"
            "\\end{document}\n")
        cmd2 = ([engine, "-interaction=nonstopmode", "ansmode.tex"]
                if engine.endswith("pdflatex") else [engine, "ansmode.tex"])
        r2 = subprocess.run(cmd2, cwd=d, capture_output=True, text=True)
        anspdf = os.path.join(d, "ansmode.pdf")
        # The weaker of the two: bare pdflatex in nonstopmode recovers from the
        # inserted $ and still emits a PDF, so this alone did NOT catch the bug
        # (measured, by reverting the macro). It is the log assertion below that
        # fires. Kept because build.sh's compile does treat it as fatal — the
        # real failure was `compile-ss FAIL ... no output PDF file produced` —
        # and an engine that stops harder should be caught here, not by a user.
        check("a study guide using \\ans in text mode compiles at all",
              os.path.isfile(anspdf),
              "through compile.sh this is the compile-ss gate failing outright")
        log2 = os.path.join(d, "ansmode.log")
        if os.path.isfile(log2):
            txt2 = open(log2, errors="replace").read()
            check("and does so with no 'Missing $ inserted'",
                  "Missing $ inserted" not in txt2,
                  "text-mode \\ans is being typeset as bare \\boldsymbol again")
        if os.path.isfile(anspdf):
            got = subprocess.run(["pdftotext", anspdf, "-"],
                                 capture_output=True, text=True).stdout
            check("both answers reach the page", "31" in got and "47" in got,
                  "check_answer_key.py binds study guides through \\ans, so an "
                  "answer that does not print cannot bind")


        # ── 9. The study-guide design system, on the page ────────────────────
        # The boxes gained title tabs (RULE / EXAMPLE / TRY IT / WATCH OUT) and
        # two evidence-based macros: \why (a printed self-explanation aside)
        # and \fadestep (a completion problem inside a try-it — the setup
        # shown, the finish left to the student; backwards-fading beats the
        # example-to-bare-problem jump on multi-step skills). Pinned from the
        # PDF because all four tabs are colorbox text a source lint cannot see
        # rendered, and because the environments were rewrapped (examplebox ->
        # exampleboxinner) — the one regression that must never happen is a
        # document-facing name changing, since check_answer_key.py segments
        # study guides by exactly these names.
        print("9. study-guide design system")
        sg = os.path.join(d, "sgdesign.tex")
        open(sg, "w").write(
            "\\documentclass[12pt]{article}\n"
            "\\usepackage[margin=0.85in, top=0.7in, bottom=0.7in]{geometry}\n"
            "\\input{worksheet-preamble}\n\\ssheader{Design}\n"
            "\\begin{document}\n\\sstitleblock{Design}\n"
            "\\begin{formulabox}$a^2+b^2=c^2$\\end{formulabox}\n"
            "\\begin{examplebox}\n"
            "\\step{Strategy: legs known, hypotenuse wanted.}\n"
            "\\step{$c = \\sqrt{9+16} = 5$}\n"
            "\\why{squaring makes both legs positive contributions.}\n"
            "\\step{So $\\ans{c = 5}$}\n"
            "\\end{examplebox}\n"
            "\\begin{tryitbox}\nLegs 6 and 8.\n"
            "\\fadestep{$c = \\sqrt{36 + 64}$}\n"
            "\\hfill\\rotatebox{180}{\\footnotesize check: $\\ans{c = 10}$}\n"
            "\\end{tryitbox}\n"
            "\\begin{watchoutbox}\nAdd squares, not legs.\n\\end{watchoutbox}\n"
            "\\end{document}\n")
        cmd3 = ([engine, "-interaction=nonstopmode", "sgdesign.tex"]
                if engine.endswith("pdflatex") else [engine, "sgdesign.tex"])
        subprocess.run(cmd3, cwd=d, capture_output=True)
        sgpdf = os.path.join(d, "sgdesign.pdf")
        check("a guide using every box and both new macros compiles",
              os.path.isfile(sgpdf))
        if os.path.isfile(sgpdf):
            body = subprocess.run(["pdftotext", sgpdf, "-"],
                                  capture_output=True, text=True).stdout
            for tab in ("RULE", "EXAMPLE", "TRY IT", "WATCH OUT"):
                check(f"the {tab} tab prints", tab in body)
            check("the why-aside prints with its label",
                  "why:" in body and "positive contributions" in body)
            check("the faded step prints setup and hand-off",
                  "Started for you:" in body and "Finish it:" in body)

    if failures:
        print(f"\n❌ {len(failures)} preamble layout regression(s)")
        return 1
    print("\n✅ preamble layout pinned")
    return 0


if __name__ == "__main__":
    sys.exit(main())
