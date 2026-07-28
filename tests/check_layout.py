#!/usr/bin/env python3
"""
check_layout.py — catch the two layout faults that make a *correct* worksheet
unusable in front of a student.

Usage: python3 tests/check_layout.py <worksheet.tex>

Both faults below were found by generating a real sheet: every answer verified,
every figure label correct, and the printed page still misleading or unusable.
Neither is visible to verify.py, which only sees the JSON.

1. FIGURE SCOPE. A figure carrying numbers belongs to exactly one problem, but
   on the page it simply sits near several. If problem 6 has a triangle labelled
   a=6, b=8 and problems 7-8 have none, a student reading 7 sees a labelled
   triangle a few lines up and reasonably assumes it applies. The figure is
   correct and the worksheet is still wrong. Rule: within one problem list,
   value-bearing figures are all-or-nothing. Shared conventions belong in a
   value-free reference figure outside the list.

2. WORK SPACE. SKILL.md specifies ~5cm per problem, 8cm multi-step. Nothing
   enforced it, so a generator can emit itemsep=14pt (about half a line) and
   produce a sheet with nowhere to show work. Trig and multi-step algebra need
   three or four lines each.

Exit 0 clean, 1 on any fault. Skips answer keys and study guides, which are
read rather than written on.
"""

import re
import sys

MIN_CM_PER_PROBLEM = 2.5      # hard floor; SKILL.md recommends 5cm
UNIT_CM = {"cm": 1.0, "mm": 0.1, "in": 2.54, "pt": 0.0352778, "ex": 0.15, "em": 0.35}


def to_cm(value, unit):
    return float(value) * UNIT_CM.get(unit, 0.0)


def enumerates(tex):
    """Each enumerate environment: (options, body)."""
    out = []
    for m in re.finditer(r"\\begin\{enumerate\}(\[[^\]]*\])?(.*?)\\end\{enumerate\}",
                         tex, re.S):
        out.append((m.group(1) or "", m.group(2)))
    return out


def items(body):
    return [p for p in re.split(r"\\item\b", body)[1:]]


def has_valued_figure(item):
    """A tikzpicture whose visible node labels contain a number."""
    for fig in re.finditer(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", item, re.S):
        for node in re.finditer(r"\\node\b[^{]*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}", fig.group(0)):
            if re.search(r"\d", node.group(1)):
                return True
    # macro-style figures: \rt{...}{$b=8$}... — any braced arg holding a digit
    for mac in re.finditer(r"\\[a-zA-Z]*(?:rt|tri|fig)[a-zA-Z]*((?:\{[^{}]*\}){2,})", item):
        if re.search(r"\d", mac.group(1)):
            return True
    return False


def space_cm(opts, item):
    """Vertical space a student gets for this problem."""
    cm = 0.0
    m = re.search(r"itemsep\s*=\s*([\d.]+)\s*(cm|mm|in|pt|ex|em)", opts)
    if m:
        cm += to_cm(m.group(1), m.group(2))
    for v in re.finditer(r"\\vspace\*?\{\s*([\d.]+)\s*(cm|mm|in|pt|ex|em)\s*\}", item):
        cm += to_cm(v.group(1), v.group(2))
    return cm


def main():
    path = sys.argv[1]
    tex = open(path).read()
    name = path.rsplit("/", 1)[-1]
    if re.match(r"^(ak|ss)_", name):
        print(f"check_layout: {name} is a key/guide, not written on — skipped")
        return 0

    faults = []
    print(f"Layout report: {path}")

    for n, (opts, body) in enumerate(enumerates(tex), 1):
        its = items(body)
        if not its:
            continue
        valued = [i for i, it in enumerate(its, 1) if has_valued_figure(it)]

        # 1. figure scope
        if valued and len(valued) != len(its):
            faults.append(
                f"list {n}: {len(valued)} of {len(its)} problems carry a figure with "
                f"values (items {valued}). A student reading a neighbouring problem "
                f"will apply the nearest figure to it. Give every problem in the list "
                f"its own figure, or move the shared labelling into a value-free "
                f"reference figure outside the list.")
        else:
            print(f"  list {n}: figure scope ok "
                  f"({'all' if valued else 'no'} {len(its)} problems carry valued figures)")

        # 2. work space
        thin = [(i, round(space_cm(opts, it), 2))
                for i, it in enumerate(its, 1) if space_cm(opts, it) < MIN_CM_PER_PROBLEM]
        if thin:
            worst = min(c for _, c in thin)
            faults.append(
                f"list {n}: {len(thin)} of {len(its)} problems have under "
                f"{MIN_CM_PER_PROBLEM}cm of work space (thinnest {worst}cm). "
                f"SKILL.md specifies ~5cm per problem, 8cm multi-step. Raise itemsep "
                f"or add \\vspace after each item.")
        else:
            print(f"  list {n}: work space ok (all {len(its)} problems ≥ {MIN_CM_PER_PROBLEM}cm)")

    if faults:
        print("\n❌ layout faults:")
        for f in faults:
            print(f"  • {f}")
        return 1
    print("\n✅ layout ok — figures are unambiguous and every problem has room to work.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
