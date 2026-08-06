#!/usr/bin/env python3
r"""test_answer_slots.py — the slot-coverage gate must count ANSWERS, not problems.

WHAT WENT WRONG. SKILL.md promised "a partially-verified answer key can never
slip through" and the gate enforced "every problem id has at least one check".
Those differ whenever a problem asks for more than one response, which is most
worksheets. 172 of 300 reviewed cases shipped a printed answer nothing verified.

Every case below is drawn from a real one:
  * "write the number word AND the ones digit" — two blanks, one entry;
  * "(a) between which two whole numbers … (b) rational or irrational?
    (c) rounded to two places, and explain why" — three sub-parts, one entry
    (curr-201 problem 3, shipped);
  * "(a) explain why … (b) write it in lowest terms" — the explain half needs a
    manual entry, and got none (curr-201 problem 6, shipped);
  * a four-part always-true/counterexample item with one entry (curr-334
    problem 3, shipped inside a case the review otherwise held up as a model).

And the two directions it must NOT fire in: a `\scratchblank` is working space,
and a `\noansline` problem with no sub-parts asks for nothing on an answer line.
"""
import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECKER = os.path.join(ROOT, "tests", "check_answer_slots.py")
FAILS = []


def check(label, cond, detail=""):
    print(f"  {'✅' if cond else '❌'} {label}")
    if not cond:
        FAILS.append(f"{label}{': ' + detail if detail else ''}")


def run(body, problems, count=None):
    """Build a one-off worksheet + verify JSON, return the checker's exit code."""
    with tempfile.TemporaryDirectory() as d:
        tex = os.path.join(d, "ws_t.tex")
        js = os.path.join(d, "verify_t.json")
        open(tex, "w").write(
            "\\documentclass{article}\n\\input{worksheet-preamble}\n"
            "\\begin{document}\n" + body + "\n\\end{document}\n")
        json.dump({"topic": "t",
                   "problem_count": count or max(p["id"] for p in problems),
                   "problems": problems}, open(js, "w"))
        r = subprocess.run([sys.executable, CHECKER, tex, js],
                           capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr


def entry(i, **kw):
    e = {"id": i, "type": "eval", "expr": "1+1", "expected": 2}
    e.update(kw)
    return e


def main():
    # 1. Two printed blanks, one entry — the shipped defect.
    rc, out = run(r"\problem{Write the number word~\ansblank\ and the ones "
                  r"digit~\ansblank}", [entry(1)])
    check("two blanks with one entry fails", rc == 1, out.strip()[-160:])

    # 2. Same problem, both responses declared — must pass.
    rc, out = run(r"\problem{Write the number word~\ansblank\ and the ones "
                  r"digit~\ansblank}", [entry(1), entry(1)])
    check("two blanks with two entries passes", rc == 0, out.strip()[-160:])

    # 3. Lettered sub-parts outnumber the entries (curr-201 problem 3).
    rc, out = run(r"\problem[5cm]{The number 20 is not a perfect square. "
                  r"\textbf{(a)} Between which two whole numbers does it lie? "
                  r"\textbf{(b)} Rational or irrational? \textbf{(c)} Round it "
                  r"to two places and explain why that is a different number.}",
                  [entry(1)])
    check("three sub-parts with one entry fails", rc == 1, out.strip()[-160:])

    # 4. A manual entry counts as a check — declaring the explain half fixes it.
    rc, out = run(r"\problem[5cm]{\textbf{(a)} Explain why a repeating decimal "
                  r"can be rational. \textbf{(b)} Write it in lowest terms.}",
                  [entry(1), {"id": 1, "type": "manual",
                              "desc": "explanation of why it is rational"}])
    check("a manual entry satisfies a prose sub-part",
          rc == 0, out.strip()[-160:])

    # 5. \noansline does not exempt a sub-parted stem (curr-334 problem 3).
    rc, out = run(r"\problem{For each, write always true or not always true. "
                  r"\textbf{(a)} A rectangle is a parallelogram. "
                  r"\textbf{(b)} A parallelogram is a rectangle. "
                  r"\textbf{(c)} Perpendicular diagonals mean a rhombus. "
                  r"\textbf{(d)} A square is a rhombus.\noansline}",
                  [entry(1)])
    check("four sub-parts behind \\noansline still fail",
          rc == 1, out.strip()[-160:])

    # 6. \scratchblank is working space, not an answer.
    rc, out = run(r"\problem{Scale by~\scratchblank\ then give the length"
                  r"~\ansblank}", [entry(1)])
    check("\\scratchblank is not counted as an answer slot",
          rc == 0, out.strip()[-160:])

    # 7. A stray "(a)" in prose must not manufacture a requirement: the run has
    #    to start at (a) AND include (b), or nothing is asked.
    rc, out = run(r"\problem[3cm]{Use figure (a) to find the area.}",
                  [entry(1)])
    check("a lone (a) reference does not fire", rc == 0, out.strip()[-160:])

    # 8. The auto answer line \problem emits on a positive workspace counts.
    rc, out = run(r"\problem[4cm]{Find the area.}", [], count=1)
    check("the auto-emitted answer line needs an entry",
          rc == 1, out.strip()[-160:])

    print()
    if FAILS:
        print(f"❌ {len(FAILS)} answer-slot check(s) failed:")
        for x in FAILS:
            print(f"   {x}")
        return 1
    print("✅ the slot gate counts answers, not problems")
    return 0


if __name__ == "__main__":
    sys.exit(main())
