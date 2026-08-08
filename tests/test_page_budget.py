#!/usr/bin/env python3
"""Behavioral and CLI coverage for scripts/page_budget.py."""
import contextlib
import io
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import page_budget  # noqa: E402


FAILS = []


def check(name, condition, detail=""):
    print(f"  {'✅' if condition else '❌'} {name}")
    if not condition:
        FAILS.append(f"{name}{': ' + detail if detail else ''}")


def run_main(args):
    """Call main with isolated argv/stdout/stderr and return all three."""
    old_argv = sys.argv
    out, err = io.StringIO(), io.StringIO()
    try:
        sys.argv = ["page_budget.py", *args]
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = page_budget.main()
    finally:
        sys.argv = old_argv
    return rc, out.getvalue(), err.getvalue()


def json_file(data):
    f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
    json.dump(data, f)
    f.close()
    return f.name


print("Problem cost model:")
check("manual default uses multi-step workspace",
      page_budget.problem_cost({}) == 9.3)
check("unknown types use standard workspace",
      page_budget.problem_cost({"type": "future_check"}) == 6.3)
check("word problems get the longer stem allowance",
      page_budget.problem_cost({"type": "solve", "word_problem": True}) == 6.9)
check("explicit workspace and figures are additive",
      page_budget.problem_cost({"type": "solve", "workspace_cm": "4.5",
                                "figure": {"kind": "plane"}}) == 10.8)

print("Budget calculation:")
compact = {"problem_count": 2, "problems": [
    {"id": 1, "type": "compare"}, {"id": 2, "type": "estimate"}]}
b = page_budget.budget(compact)
check("all-compact sheets use two columns", b["two_column"] is True)
check("compact height is halved", b["content_cm"] == 4.3)
check("small sets still receive a one-page ideal", b["ideal_pages"] == 1)
check("worksheet slack is reported", (b["min_pages"], b["max_pages"]) == (1, 3))
check("duplex sheet count rounds up", b["sheets_duplex"] == 1)

duplicate = {"problem_count": 9, "problems": [
    {"id": 1, "type": "solve"},
    {"id": 1, "type": "solve", "figure": {"kind": "plane"}},
    {"id": 2, "type": "compare"}]}
b = page_budget.budget(duplicate)
check("duplicate verifier entries count as one printed problem", b["problems"] == 2)
check("declared count is preserved for diagnostics", b["declared_count"] == 9)
check("a duplicate carrying a figure wins", b["content_cm"] == 15.6)
check("a figure prevents compact two-column mode", b["two_column"] is False)

empty = page_budget.budget({"problems": []}, paper="not-a-cli-paper")
check("empty specs use the unique-count default", empty["declared_count"] == 0)
check("library callers fall back to Letter geometry", empty["ideal_pages"] == 1)
check("the requested paper label remains observable", empty["paper"] == "not-a-cli-paper")

many = {"problems": [
    {"id": i, "type": "manual", "word_problem": True,
     "figure": {"kind": "diagram"}} for i in range(30)]}
letter = page_budget.budget(many, "letter")
a4 = page_budget.budget(many, "a4")
legal = page_budget.budget(many, "legal")
check("larger paper never increases the ideal",
      letter["ideal_pages"] >= a4["ideal_pages"] >= legal["ideal_pages"])
check("long budgets report the no-compression note",
      "do NOT shrink" in page_budget.render(letter))
check("short budgets omit the long-set note",
      "do NOT shrink" not in page_budget.render(b))
check("render identifies answer-key documents",
      "Page budget (ak," in page_budget.render(b, "ak"))

print("Command-line contract:")
path = json_file(compact)
try:
    rc, out, err = run_main([path, "--max-pages"])
    check("--max-pages prints only the ceiling", rc == 0 and out.strip() == "3" and not err)

    rc, out, err = run_main([path, "--doc", "ak", "--max-pages"])
    check("answer-key ceiling has its own formula", rc == 0 and out.strip() == "3")

    rc, out, err = run_main([path, "--paper", "A4"])
    check("paper names are case-insensitive", rc == 0 and "(ws, a4)" in out)

    rc, out, err = run_main([path, "--doc"])
    check("a missing --doc value safely defaults", rc == 0 and "Page budget (ws," in out)

    rc, out, err = run_main([path, "--paper"])
    check("a missing --paper value safely defaults", rc == 0 and "(ws, letter)" in out)
finally:
    os.unlink(path)

rc, _, err = run_main([])
check("missing positional input prints usage", rc == 2 and "Usage:" in err)
rc, _, err = run_main(["/definitely/not/a/worksheet.json"])
check("missing input is rejected", rc == 2 and "no such file" in err)
rc, _, err = run_main(["irrelevant", "--paper", "tabloid"])
check("unknown paper is rejected before file access", rc == 2 and "unknown paper" in err)

bad = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
bad.write("{not json")
bad.close()
try:
    rc, _, err = run_main([bad.name])
    check("malformed JSON is rejected", rc == 2 and "cannot parse" in err)
finally:
    os.unlink(bad.name)

too_many = json_file({"problem_count": 101, "problems": [
    {"id": i, "type": "solve"} for i in range(101)]})
try:
    rc, _, err = run_main([too_many])
    check("workbook-sized requests are rejected", rc == 2 and "101 problems exceeds" in err)
finally:
    os.unlink(too_many)

# ── A picture in the stem the JSON cannot see ───────────────────────────────
# The stem charge is a flat 0.6cm, right for a sentence and badly wrong for a
# stem holding a coordinate grid or a ten-frame. Three authors in one run hit
# it the same way: every pre-compile gate green, then compile-ws failing by a
# page, fixed by declaring workspace_cm. Now that --from-tex exists the budget
# can say so BEFORE three compiles run. Deliberately a note, not a charge — a
# tikzpicture's height is whatever its author drew.
print()
print("pictures the JSON cannot see")
_ws_tex = tempfile.NamedTemporaryFile("w", suffix=".tex", delete=False)
_ws_tex.write(r"""\documentclass[12pt]{article}
\begin{document}
\problem[3cm]{Plot the points.
\begin{tikzpicture}\begin{axis}[height=6.4cm]\end{axis}\end{tikzpicture}}
\problem[3cm]{Fill in the table.
\begin{tabular}{|c|c|}\hline a & b \\ \hline\end{tabular}}
\problem[3cm]{This one declares its own workspace.
\begin{tikzpicture}\begin{axis}[height=9cm]\addplot {x};\end{axis}\end{tikzpicture}}
\end{document}
""")
_ws_tex.close()
_probe = json_file({"problem_count": 3, "problems": [
    {"id": 1, "type": "eval"}, {"id": 2, "type": "eval"},
    {"id": 3, "type": "eval", "workspace_cm": 9.0}]})
try:
    rc, out, _ = run_main([_probe, "--from-tex", _ws_tex.name])
    check("a gridded stem with no workspace_cm is named", "problem 1's stem" in out)
    check("and its own declared height is quoted", "height=6.4cm" in out)
    check("a table counts too", "problem 2's stem" in out and "tabular" in out)
    # Declaring workspace_cm IS how an author takes responsibility for the
    # block; repeating the warning afterwards trains people to ignore it.
    check("a problem that declared workspace_cm is not nagged",
          "problem 3's stem" not in out)
    rc2, out2, _ = run_main([_probe])
    check("without --from-tex there is nothing to see and nothing is claimed",
          "stem holds" not in out2 and rc2 == 0)
finally:
    os.unlink(_probe)
    os.unlink(_ws_tex.name)

# ── Pagination is quantised and the sum is not ──────────────────────────────
# \problem wraps stem and workspace in ONE unbreakable minipage, so a block
# taller than half the column packs one per page and strands the rest of it.
# Four authors in one run hit the same wall: a 12-problem sheet where every
# problem carried a figure ran to 10 real pages against a ceiling of 7, and
# declaring workspace_cm honestly moved the ceiling to 9 — still short, because
# an additive model never sees the stranded space. The gate then reads as
# "declare more workspace_cm", and an author who follows it literally keeps
# inflating a number that is supposed to be a measurement.
print()
print("blocks that cannot share a page")
_tall = json_file({"problem_count": 12, "problems": [
    {"id": i, "type": "triangle", "workspace_cm": 11.0} for i in range(1, 13)]})
_short = json_file({"problem_count": 12, "problems": [
    {"id": i, "type": "eval", "workspace_cm": 5.0} for i in range(1, 13)]})
try:
    _, tall_out, _ = run_main([_tall])
    _, tall_max, _ = run_main([_tall, "--max-pages"])
    _, short_out, _ = run_main([_short])
    _, short_max, _ = run_main([_short, "--max-pages"])
    check("a one-per-page sheet is charged for the stranded space",
          int(tall_max.strip()) >= 12,
          f"ceiling {tall_max.strip()} for 12 blocks that pack one per page")
    check("and is told the fix is a shorter block, not a bigger number",
          "SHORTER BLOCK" in tall_out and "not a larger workspace_cm" in tall_out)
    # The change may only ever RAISE a ceiling: a sheet whose blocks do pack is
    # untouched, or this would newly fail work that was passing.
    check("a sheet whose blocks pack two per page is unaffected",
          int(short_max.strip()) <= 6, f"ceiling {short_max.strip()}")
    check("and gets no stranded-space note", "SHORTER BLOCK" not in short_out)
finally:
    os.unlink(_tall)
    os.unlink(_short)

# ── One problem, several verifier entries ───────────────────────────────────
# A problem's checks are separate JSON entries sharing one id, and the PAGE
# gets one block for all of them. The budget used to keep the FIRST entry and
# throw the rest away, so a workspace_cm declared on any later entry was
# invisible — while the advisory pass in the same file merged across entries.
# The two halves disagreed, and the disagreement had a direction: the budget
# under-measured, the ceiling came out short, and compile-ws then failed the
# sheet telling the author to declare the very field they had declared.
#
# Reproduced in the run: moving identical numbers from the last entry of each
# id to the first moved a sheet from 65cm/ideal 3 to 129cm/ideal 6 against a
# real 7 pages. Same JSON, same mathematics, same page — different budget.
print()
print("one problem, several verifier entries")
_first = {"problem_count": 8, "problems": [
    e for i in range(1, 9) for e in (
        {"id": i, "type": "eval", "workspace_cm": 8.0},
        {"id": i, "type": "manual"})]}
_last = {"problem_count": 8, "problems": [
    e for i in range(1, 9) for e in (
        {"id": i, "type": "eval"},
        {"id": i, "type": "manual", "workspace_cm": 8.0})]}
_bf, _bl = page_budget.budget(_first), page_budget.budget(_last)
check("workspace_cm counts wherever in the id it was declared",
      _bf["content_cm"] == _bl["content_cm"],
      f"first-entry {_bf['content_cm']}cm vs last-entry {_bl['content_cm']}cm")
check("and the declared number is what gets charged",
      _bl["content_cm"] == 74.4, f"{_bl['content_cm']}cm for 8 x (1.3 + 8.0)")
check("so the two orderings agree on the ceiling",
      _bf["max_pages"] == _bl["max_pages"] == 6,
      f"{_bf['max_pages']} vs {_bl['max_pages']}")
# The entry carrying the figure used to REPLACE the representative outright,
# which discarded a workspace_cm declared on the entry it replaced. Both are
# facts about the same block; both are charged.
_figlate = page_budget.budget({"problems": [
    {"id": 1, "type": "eval", "workspace_cm": 5.5},
    {"id": 1, "type": "eval", "figure": {"kind": "plane"}}]})
check("a figure on a later entry does not discard an earlier workspace_cm",
      _figlate["content_cm"] == 11.8, f"{_figlate['content_cm']}cm")

# Each entry claims the room it needs — declared, or its type's default — and
# the block holds all of them, so it is charged the TALLEST claim. A problem
# that computes a value and also asks for the reasoning is an `eval` entry plus
# a `manual` one, and the writing still needs prose room whether or not the
# arithmetic half put a number on itself. Taking only the declared numbers
# would let 5.5cm written on one check silently shrink the 8cm the other was
# asking for, resizing a part the author never touched.
_sibling = page_budget.budget({"problems": [
    {"id": 1, "type": "manual"},
    {"id": 1, "type": "eval", "workspace_cm": 5.5}]})
check("a declaration on one check does not shrink a sibling's larger default",
      _sibling["content_cm"] == 9.3, f"{_sibling['content_cm']}cm, want 1.3 + 8.0")
_sibling_up = page_budget.budget({"problems": [
    {"id": 1, "type": "eval"},
    {"id": 1, "type": "eval", "workspace_cm": 9.0}]})
check("but a declaration above every default still raises the block",
      _sibling_up["content_cm"] == 10.3, f"{_sibling_up['content_cm']}cm")
# Types differing across one id is the same fact spread over entries: the
# block is sized for the part that needs the most room, not for whichever
# entry the JSON happened to list first.
_typemix = page_budget.budget({"problems": [
    {"id": 1, "type": "eval"}, {"id": 1, "type": "manual"}]})
_typemix_rev = page_budget.budget({"problems": [
    {"id": 1, "type": "manual"}, {"id": 1, "type": "eval"}]})
check("entry order does not decide which type sizes the block",
      _typemix["content_cm"] == _typemix_rev["content_cm"] == 9.3,
      f"{_typemix['content_cm']} vs {_typemix_rev['content_cm']}")
# word_problem is the same class of fact and was read off the first entry too.
_wplate = page_budget.budget({"problems": [
    {"id": 1, "type": "solve"},
    {"id": 1, "type": "solve", "word_problem": True}]})
check("a word_problem flag on a later entry is not lost",
      _wplate["content_cm"] == 6.9, f"{_wplate['content_cm']}cm")

# The budget and the advisory pass must read the same JSON the same way. This
# is the exact shape that failed in the run: a gridded stem whose workspace_cm
# sits on the second entry of the id.
_agree_tex = tempfile.NamedTemporaryFile("w", suffix=".tex", delete=False)
_agree_tex.write(r"""\documentclass[12pt]{article}
\begin{document}
\problem[9cm]{Plot the points.
\begin{tikzpicture}\begin{axis}[height=9cm]\addplot {x};\end{axis}\end{tikzpicture}}
\end{document}
""")
_agree_tex.close()
_agree = json_file({"problem_count": 1, "problems": [
    {"id": 1, "type": "eval"},
    {"id": 1, "type": "manual", "workspace_cm": 9.0}]})
try:
    _, _ag_out, _ = run_main([_agree, "--from-tex", _agree_tex.name])
    check("a stem whose workspace_cm sits on a later entry is not nagged",
          "declares no workspace_cm" not in _ag_out, _ag_out)
    check("and the same declaration is what the budget charged",
          "10.3cm of content" in _ag_out, _ag_out)
finally:
    os.unlink(_agree)
    os.unlink(_agree_tex.name)

# ── Two-column halving keys off the EFFECTIVE workspace ─────────────────────
# An all-compact sheet is charged half height because a compact drill sets two
# problems per row. The test for "compact" used to read the TYPE DEFAULT and
# ignore what the problems actually declared, so a sheet of `compare` or
# `estimate` items — exactly the elementary comparison and estimation bands —
# was halved even when every problem declared a large workspace_cm and the
# .tex was ordinary single-column \problem with no multicols anywhere.
#
# The damage runs through the ceiling, which is derived from the ideal: those
# sheets got a ceiling one to two pages tighter than their content needed, and
# raising workspace_cm — the fix the budget's own message prints — bought half
# of what it declared.
print()
print("two-column halving follows the declared workspace")
_declared_compact = {"problem_count": 8, "problems": [
    {"id": i, "type": "compare", "workspace_cm": 6.0} for i in range(1, 9)]}
b = page_budget.budget(_declared_compact)
check("a compare sheet declaring real workspace is not a two-column drill",
      b["two_column"] is False)
check("and is charged its full declared height",
      b["content_cm"] == 58.4, f"{b['content_cm']}cm for 8 x (1.3 + 6.0)")
check("so its ceiling covers the content",
      b["ideal_pages"] == 3, f"ideal {b['ideal_pages']}")
# Raising workspace_cm must buy what it declares, not half of it. This is the
# property the run's authors were denied: they followed the printed advice and
# the ceiling moved by half their number.
_low = page_budget.budget({"problems": [
    {"id": i, "type": "estimate", "workspace_cm": 4.0} for i in range(1, 11)]})
_high = page_budget.budget({"problems": [
    {"id": i, "type": "estimate", "workspace_cm": 8.0} for i in range(1, 11)]})
check("declaring 4cm more workspace on 10 problems buys all 40cm",
      round(_high["content_cm"] - _low["content_cm"], 1) == 40.0,
      f"{_low['content_cm']} -> {_high['content_cm']}")
# The halving is real for real drill sheets and must survive.
_true_drill = page_budget.budget({"problem_count": 20, "problems": [
    {"id": i, "type": "compare"} for i in range(1, 21)]})
check("an undeclared compact sheet is still a two-column drill",
      _true_drill["two_column"] is True)
check("and is still charged half height",
      _true_drill["content_cm"] == 43.0, f"{_true_drill['content_cm']}cm")
_tight = page_budget.budget({"problems": [
    {"id": i, "type": "compare", "workspace_cm": 2.0} for i in range(1, 21)]})
check("declaring LESS than the compact default stays two-column",
      _tight["two_column"] is True)
# A mixed sheet where one problem declares room is not a drill sheet.
_mixed = page_budget.budget({"problems": [
    {"id": 1, "type": "compare", "workspace_cm": 9.0},
    {"id": 2, "type": "compare"}, {"id": 3, "type": "estimate"}]})
check("one problem that needs room ends the two-column assumption",
      _mixed["two_column"] is False)
# ...and the declaration is read across entries here too, or the two fixes
# would disagree on the same sheet.
_late_decl_drill = page_budget.budget({"problems": [
    {"id": 1, "type": "compare"},
    {"id": 1, "type": "manual", "workspace_cm": 9.0},
    {"id": 2, "type": "compare"}]})
check("a late-entry declaration also ends the two-column assumption",
      _late_decl_drill["two_column"] is False)

print()
if FAILS:
    print(f"❌ {len(FAILS)} page-budget test(s) failed:")
    for failure in FAILS:
        print(f"   {failure}")
    sys.exit(1)
print("✅ Page-budget behavior and CLI contract passed")
