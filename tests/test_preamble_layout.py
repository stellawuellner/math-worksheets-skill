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

5. COMMON-ERROR BLOCK FITS THE LINE. \commonerror opens a paragraph; it did not
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

        print("5. common-error block fits the line")
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

    if failures:
        print(f"\n❌ {len(failures)} preamble layout regression(s)")
        return 1
    print("\n✅ preamble layout pinned")
    return 0


if __name__ == "__main__":
    sys.exit(main())
