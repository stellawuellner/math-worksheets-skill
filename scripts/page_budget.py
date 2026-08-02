#!/usr/bin/env python3
r"""
page_budget.py — derive a worksheet's page budget from what it actually asks
of the student, instead of a flat cap.

Usage: python3 scripts/page_budget.py <verify.json> [--doc ws|ak]
                [--paper letter|a4|legal] [--max-pages]

WHY THIS EXISTS
A single number ("worksheets may not exceed 8 pages") is wrong in both
directions at once. Fifty linear-graphing problems each need their own
coordinate plane and legitimately run past twenty pages; a flat cap fails that
sheet, and the only way to pass is to shrink the planes or drop the workspace,
which is exactly the compression this system exists to prevent. Meanwhile ten
arithmetic drills that somehow filled eight pages sail through the same cap
while wasting seven sheets of a school's paper budget.

So the budget is COMPUTED from the problem set: how many problems, and how much
room each kind of problem deserves. The gate then asks the only question worth
asking — did this sheet land where its own content says it should? — and it is
two-sided:

  too many pages  -> bloat: paper spent on layout accident, not on work space
  too few pages   -> compression: the work space was squeezed to fit

Space is never the thing that gives. If a sheet needs more pages, it gets them;
the budget moves. What the gate refuses is a page count that does not match the
work the sheet contains.

COST MODEL (cm of column height, worksheet geometry: 24.1cm usable per page)
Each problem costs a fixed overhead plus the workspace its kind deserves. The
workspace figures are SKILL.md's own guidance (~5cm standard, 8cm multi-step,
10cm+ for graphs), and the overheads are measured from the shipped preamble.

Per problem:
  0.4cm  \problem lead-in
  0.6cm  stem (1.2cm when the stem is a word problem: longer prose wraps)
  0.3cm  answer line
  + workspace by class (below)
  + 5.0cm when the problem carries a figure (a coordinate plane or geometric
    figure is ~9cm tall and partly overlaps the workspace the student would
    otherwise use)

Two-column drill sheets pack two problems per row, so a sheet whose problems are
ALL compact is charged half the per-problem height.

Exit 0 always when the JSON parses (this computes a budget, it does not judge a
document). --max-pages prints just the ceiling, for build.sh to pass to
compile.sh. Exit 2 on unreadable/oversized input.
"""
import json
import math
import os
import sys

# Usable column height per page at the worksheet's margins (top/bottom 0.75in
# = 1.905cm each). US Letter is the default because that is what the schools
# this was built for use; A4 is 1.8cm taller per page, which is a real
# difference over a long set (about one page saved every fourteen), so the
# budget must know which one it is sizing for rather than assume.
PAPER_CM = {
    "letter": 27.94 - 2 * 1.905,   # 8.5 x 11in
    "a4":     29.70 - 2 * 1.905,   # 210 x 297mm
    "legal":  35.56 - 2 * 1.905,   # 8.5 x 14in
}
DEFAULT_PAPER = "letter"

# A worksheet is a practice set, not a workbook. Beyond this the request is
# better served as several worksheets, which also print and grade better.
MAX_PROBLEMS = 100

OVERHEAD_CM = 0.4 + 0.3          # lead-in + answer line
STEM_CM = 0.6
WORD_PROBLEM_STEM_CM = 1.2
FIGURE_CM = 5.0

COMPACT, STANDARD, MULTISTEP = 3.0, 5.0, 8.0

# verify type -> workspace class. Unknown types fall back to STANDARD, which is
# the middle of the range: a new check type can never silently make the budget
# absurdly tight or absurdly loose.
WORKSPACE = {
    "compare": COMPACT, "estimate": COMPACT, "read_data": COMPACT,
    "probability": COMPACT,

    "solve": STANDARD, "zeros": STANDARD, "factor": STANDARD,
    "expand": STANDARD, "eval": STANDARD, "slope": STANDARD,
    "distance": STANDARD, "midpoint": STANDARD, "stats": STANDARD,
    "equiv": STANDARD, "approx": STANDARD,

    "system": MULTISTEP, "inequality": MULTISTEP, "series": MULTISTEP,
    "limit": MULTISTEP, "diff": MULTISTEP, "integrate": MULTISTEP,
    "definite_integral": MULTISTEP, "triangle": MULTISTEP,
    "solve_interval": MULTISTEP, "polygon_area": MULTISTEP,

    # open reasoning: a proof, sketch or explanation needs room to write prose
    "manual": MULTISTEP,
}

# How far the actual page count may sit from the computed ideal before the gate
# objects. Pagination is lumpy — a problem that will not fit at the foot of a
# page moves whole to the next one — so the ideal is a target, not an identity.
SLACK_OVER = 2      # pages of pagination slop allowed above the ideal
SLACK_UNDER = 0.30  # fraction below the ideal that counts as compression


def problem_cost(p):
    """Column height one problem deserves, in cm."""
    ptype = p.get("type", "manual")
    ws = p.get("workspace_cm")
    # verify.py runs first and rejects a non-numeric workspace_cm, but this
    # module is also called directly, so it degrades to the type default rather
    # than dying on input it did not validate.
    try:
        ws = float(ws) if ws is not None else WORKSPACE.get(ptype, STANDARD)
    except (TypeError, ValueError):
        ws = WORKSPACE.get(ptype, STANDARD)
    stem = WORD_PROBLEM_STEM_CM if p.get("word_problem") else STEM_CM
    cost = OVERHEAD_CM + stem + ws
    if isinstance(p.get("figure"), dict):
        cost += FIGURE_CM
    return cost


def budget(spec, paper=DEFAULT_PAPER):
    """Return the budget dict for a parsed verify JSON."""
    page_cm = PAPER_CM.get(paper, PAPER_CM[DEFAULT_PAPER])
    problems = spec.get("problems", [])
    # one entry per problem id: several checks may bind to the same problem,
    # and charging a problem twice would inflate the budget
    by_id, order = {}, []
    for p in problems:
        pid = p.get("id")
        if pid not in by_id:
            by_id[pid] = p
            order.append(pid)
        elif isinstance(p.get("figure"), dict):
            by_id[pid] = p          # prefer the entry that carries the figure
    unique = [by_id[i] for i in order]

    declared = spec.get("problem_count", len(unique))
    costs = [problem_cost(p) for p in unique]
    total = sum(costs)

    # an all-compact sheet is the two-column drill format: two per row
    all_compact = bool(unique) and all(
        WORKSPACE.get(p.get("type", "manual"), STANDARD) == COMPACT
        and not isinstance(p.get("figure"), dict) for p in unique)
    if all_compact:
        total /= 2.0

    title_block_cm = 2.0                      # title + rule + instruction line
    ideal = max(1, math.ceil((total + title_block_cm) / page_cm))
    return {
        "problems": len(unique),
        "declared_count": declared,
        "content_cm": round(total, 1),
        "ideal_pages": ideal,
        "max_pages": ideal + SLACK_OVER,
        "min_pages": max(1, math.floor(ideal * (1 - SLACK_UNDER))),
        "two_column": all_compact,
        "paper": paper,
        "sheets_duplex": math.ceil(ideal / 2),
    }


def render(b, doc="ws"):
    lines = [
        f"Page budget ({doc}, {b['paper']}): {b['problems']} problems, "
        f"{b['content_cm']}cm of content"
        + (" (two-column drill: charged at half height)" if b["two_column"] else ""),
        f"  ideal {b['ideal_pages']} page(s) · accepted range "
        f"{b['min_pages']}-{b['max_pages']} · "
        f"{b['sheets_duplex']} sheet(s) of paper double-sided",
    ]
    if b["max_pages"] > 12:
        lines.append(
            f"  NOTE: this set needs {b['ideal_pages']} pages of paper. If that is "
            f"more than intended, ask for fewer problems — do NOT shrink the work "
            f"space to fit, which is what makes a sheet unusable.")
    return "\n".join(lines)


def main():
    argv = sys.argv[1:]
    doc = "ws"
    if "--doc" in argv:
        i = argv.index("--doc")
        doc = argv[i + 1] if i + 1 < len(argv) else "ws"
        del argv[i:i + 2]
    paper = DEFAULT_PAPER
    if "--paper" in argv:
        i = argv.index("--paper")
        paper = (argv[i + 1] if i + 1 < len(argv) else DEFAULT_PAPER).lower()
        del argv[i:i + 2]
        if paper not in PAPER_CM:
            print(f"page_budget: unknown paper {paper!r}; known: "
                  f"{', '.join(sorted(PAPER_CM))}", file=sys.stderr)
            return 2
    only_max = "--max-pages" in argv
    if only_max:
        argv.remove("--max-pages")
    if len(argv) != 1:
        usage = next(line for line in __doc__.splitlines()
                     if line.startswith("Usage:"))
        print(usage, file=sys.stderr)
        return 2
    path = argv[0]
    if not os.path.exists(path):
        print(f"page_budget: no such file: {path}", file=sys.stderr)
        return 2
    try:
        spec = json.load(open(path))
    except Exception as e:                                  # noqa: BLE001
        print(f"page_budget: cannot parse {path}: {e}", file=sys.stderr)
        return 2

    b = budget(spec, paper)
    if b["problems"] > MAX_PROBLEMS:
        print(f"page_budget: {b['problems']} problems exceeds the {MAX_PROBLEMS}-problem "
              f"ceiling. Split this into several worksheets: past ~100 problems a "
              f"single sheet is a workbook, and it prints and grades worse than "
              f"two focused sets.", file=sys.stderr)
        return 2

    # the answer key holds worked solutions, not work space: it runs shorter
    # than the worksheet but never shorter than the problem list itself
    if doc == "ak":
        b["max_pages"] = max(2, math.ceil(b["ideal_pages"] * 0.9) + SLACK_OVER)
        b["min_pages"] = 1

    if only_max:
        print(b["max_pages"])
    else:
        print(render(b, doc))
    return 0


if __name__ == "__main__":
    sys.exit(main())
