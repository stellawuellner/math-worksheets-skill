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

    # 9. One entry can pin several BLANKS: ordering three numbers into three
    #    blanks is completely verified by a single compare entry.
    rc, out = run(r"\problem{Write them in order: \ansblank\ \ansblank\ \ansblank}",
                  [{"id": 1, "type": "compare", "values": [3, 5, 7],
                    "order": "asc", "expected": [3, 5, 7]}])
    check("a list-valued entry covers the blanks it fills",
          rc == 0, out.strip()[-160:])

    # 10. ...but arity must NOT satisfy a lettered sub-part. A two-root solve
    #     covers two blanks and says nothing about the "explain why" beside it.
    #     Letting arity count here would silence this gate's largest true-
    #     positive class.
    rc, out = run(r"\problem[5cm]{\textbf{(a)} Solve $x^2-5x+6=0$. "
                  r"\textbf{(b)} Explain why a quadratic can have two roots.}",
                  [{"id": 1, "type": "solve", "expr": "x**2-5*x+6",
                    "var": "x", "expected": [2, 3]}])
    check("arity does not excuse an unanswered sub-part",
          rc == 1, out.strip()[-160:])

    # 11. A manual rubric routinely covers every open sub-part of a problem, and
    #     counting entries against letters called that under-covered. Measured
    #     over the corpus this was 5 of 9 sampled false positives.
    rc, out = run(r"\problem[6cm]{\textbf{(a)} Explain why circumference doubles. "
                  r"\textbf{(b)} Explain why area quadruples. "
                  r"\textbf{(c)} Compute the area of B.\noansline}",
                  [entry(1), {"id": 1, "type": "manual",
                              "desc": "Open explanation, parts (a) and (b)"}])
    check("a manual entry covers the open sub-parts beside it",
          rc == 0, out.strip()[-160:])

    # 12. ...but a manual must NOT silence a printed blank. This is curr-213 p8:
    #     three blanks, one of which holds a value nothing verifies.
    rc, out = run(r"\problem{Expand~\ansblank\ then find $a$~\ansblank\ "
                  r"then explain~\ansblank}",
                  [entry(1), {"id": 1, "type": "manual", "desc": "explanation"}])
    check("a manual does not excuse an unverified printed blank",
          rc == 1, out.strip()[-160:])

    # 13. THE FALSE NEGATIVE I SHIPPED. Crediting every list-valued expected
    #     looks equivalent to crediting the multi-slot types and is not: a solve
    #     returning [9, 21] is one answer on one line. This is curr-295 p12,
    #     where (a) is solved and (b) is an open question on its own \ansline.
    rc, out = run(r"\problem{\textbf{(a)} Solve.~\ansline\ "
                  r"\textbf{(b)} Say whether she is right.~\ansline}",
                  [{"id": 1, "type": "solve", "expr": "x**2-30*x+189",
                    "var": "x", "expected": [9, 21]}])
    check("a solve root list does not cover a second answer line",
          rc == 1, out.strip()[-160:])

    # 14. The 202-case class: an open ask with no manual entry must fail even
    #     when the slot arithmetic is satisfied.
    rc, out = run(r"\problem[5cm]{Solve the equation, then explain why the "
                  r"rejected root cannot work.~\ansline}", [entry(1)])
    check("an open ask with no manual entry fails",
          rc == 1 and "manual" in out, out.strip()[-160:])

    # 15. The same ask WITH a manual entry passes — one rubric covers it.
    rc, out = run(r"\problem[5cm]{Solve the equation, then explain why the "
                  r"rejected root cannot work.~\ansline}",
                  [entry(1), {"id": 1, "type": "manual",
                              "desc": "why the rejected root fails the domain"}])
    check("the same ask with a manual entry passes", rc == 0,
          out.strip()[-160:])

    # 16. "Plot it if it helps" is scaffolding, not a demand.
    rc, out = run(r"\problem[4cm]{Find the distance. Sketch the points on the "
                  r"grid if it helps.}", [entry(1)])
    check("optional draw-if-it-helps scaffolding does not fire", rc == 0,
          out.strip()[-160:])

    # 17. The Priya class: a manual desc naming someone absent from the
    #     problem is a stale rubric and must fail.
    #     The name must sit mid-sentence: sentence-initial capitals are
    #     indistinguishable from sentence case ("Explain why…") and are a
    #     documented boundary of the lint — the real corpus instance fired on
    #     a mid-sentence recurrence.
    rc, out = run(r"\problem[4cm]{Explain which part of the plot answers each "
                  r"question.\noansline}",
                  [{"id": 1, "type": "manual",
                    "desc": "Grade whether Priya's respacing argument holds"}])
    check("a stale desc naming an absent person fails",
          rc == 1 and "Priya" in out, out.strip()[-160:])

    # 18. A multi-word proper term is vocabulary, not a name — must not fire.
    rc, out = run(r"\problem[4cm]{Explain why reversing the bounds flips the "
                  r"sign of the integral.\noansline}",
                  [{"id": 1, "type": "manual",
                    "desc": "Uses the Fundamental Theorem to justify the "
                            "sign flip when bounds reverse"}])
    check("a theorem name in the desc does not fire", rc == 0,
          out.strip()[-160:])

    # 19. THE SILENT-PASS HOLE. AUTHORING.md prescribes `\item[(a)]` for
    #     sub-part labels, and the marker there follows a `[` — which the
    #     character class originally omitted, so a sheet following the brief's
    #     own guidance lost the lettered-sub-part half of this gate and PASSED.
    #     133 of 300 worksheets in the regeneration run use that form.
    rc, out = run(r"\problem[5cm]{Two parts. \begin{itemize}"
                  r"\item[(a)] Solve for x. \item[(b)] Explain your choice."
                  r"\end{itemize}}",
                  [entry(1), {"id": 1, "type": "manual", "desc": "the choice"}])
    check("\\item[(a)] sub-parts are counted (AUTHORING's own form)",
          rc == 0, out.strip()[-160:])
    rc, out = run(r"\problem[5cm]{Two parts. \begin{itemize}"
                  r"\item[(a)] Solve for x. \item[(b)] Solve for y."
                  r"\end{itemize}}", [entry(1)])
    check("\\item[(a)] sub-parts still FAIL when uncovered",
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
