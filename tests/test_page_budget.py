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

print()
if FAILS:
    print(f"❌ {len(FAILS)} page-budget test(s) failed:")
    for failure in FAILS:
        print(f"   {failure}")
    sys.exit(1)
print("✅ Page-budget behavior and CLI contract passed")
