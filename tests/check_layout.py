#!/usr/bin/env python3
r"""
check_layout.py — catch the layout faults that make a *correct* worksheet
unusable in front of a student.

Usage: python3 tests/check_layout.py <worksheet.tex>

Each fault below was found by generating a real sheet: every answer verified,
every figure label correct, and the printed page still misleading or unusable.
None is visible to verify.py, which only sees the JSON.

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
   three or four lines each. Space is credited from itemsep, signed \vspace
   (deliberate reclaiming with \vspace{-2.9cm} is charged, not ignored),
   \\[5cm] line skips, and the three standard skips — all of which put real
   ink-to-ink distance on the page.

3. PAGE-BREAK GLUE. LaTeX discards \vspace glue that falls at a page or column
   break, so workspace left outside a minipage silently vanishes exactly when
   its problem lands at a page bottom — a multi-page sheet loses the workspace
   of roughly one problem per page. The fix is structural: keep the workspace
   inside the problem's unbreakable minipage (\par\vspace*{5cm} before
   \end{minipage}, see references/latex-templates.md). A workspace-sized
   unstarred \vspace outside any minipage is therefore a fault. Starred
   \vspace* at least survives the break, so it is tolerated as a minimal fix.

Both the enumerate/\item and the \problem{...} macro shapes are parsed — the
skill's first-taught template style is \problem, and a checker that only sees
enumerate lists passes a zero-workspace \problem sheet vacuously (the same
zero-parse failure class fixed in check_prose_consistency.py).

Exit 0 clean, 1 on any fault, 2 when nothing parsed (no list and no \problem
block means nothing was checked — that is NOT a pass). Skips answer keys and
study guides, which are read rather than written on.
"""

import re
import sys

MIN_CM_PER_PROBLEM = 2.5      # hard floor; SKILL.md recommends 5cm
UNIT_CM = {"cm": 1.0, "mm": 0.1, "in": 2.54, "pt": 0.0352778, "ex": 0.15, "em": 0.35}
# \bigskip/\medskip/\smallskip at their conventional sizes — coarse, but they
# are real writing room and ignoring them under-credits a legitimate sheet
SKIP_CM = {"bigskip": 0.42, "medskip": 0.28, "smallskip": 0.14}

# matches a \problem use site — \problem{...} or \problem[5cm]{...} (the macro
# takes the workspace as an optional first argument). Does NOT match the
# preamble's \newcommand{\problem}... definition: there the next char is `}`.
PROBLEM_RE = re.compile(r"\\problem(\[[^\]]*\])?\{")


def to_cm(value, unit):
    return float(value) * UNIT_CM.get(unit, 0.0)


def strip_comments(tex):
    """Blank TeX comments (unescaped % to end of line), preserving offsets.

    Commented-out material must neither satisfy a rule (a dead \\vspace{5cm}
    is not workspace) nor trip one (a comment MENTIONING \\vspace{5cm} is not
    stranded glue). Blanking instead of deleting keeps every reported line
    number true to the file the author is editing.
    """
    return re.sub(r"(?<!\\)%[^\n]*", lambda m: " " * len(m.group(0)), tex)


def enumerates(tex):
    """Each enumerate environment: (options, body)."""
    out = []
    for m in re.finditer(r"\\begin\{enumerate\}(\[[^\]]*\])?(.*?)\\end\{enumerate\}",
                         tex, re.S):
        out.append((m.group(1) or "", m.group(2)))
    return out


def items(body):
    return [p for p in re.split(r"\\item\b", body)[1:]]


def problem_regions(tex):
    """Each \\problem block as (workspace_cm_from_optional_arg, region, had_list).

    A region runs from one \\problem use to the next (or EOF): the workspace
    \\vspace and any figure live AFTER the macro call, so the trailing text —
    not just the braced stem — is what layout must see. Nested enumerate
    bodies are stripped (had_list=True): the multi-part template carries its
    workspace in the nested list's itemsep, which the enumerate pass already
    validates — counting the region's own \\vspace there would false-fail the
    skill's own template.
    """
    matches = list(PROBLEM_RE.finditer(tex))
    out = []
    for m, nxt in zip(matches, matches[1:] + [None]):
        region = tex[m.start():nxt.start() if nxt else len(tex)]
        opt_cm = 0.0
        if m.group(1):
            o = re.search(r"(-?[\d.]+)\s*(cm|mm|in|pt|ex|em)", m.group(1))
            if o:
                opt_cm = to_cm(o.group(1), o.group(2))
        stripped = re.sub(r"\\begin\{enumerate\}.*?\\end\{enumerate\}", "",
                          region, flags=re.S)
        out.append((opt_cm, stripped, stripped != region))
    return out


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
    # signed: \vspace{-2.9cm} after a 3cm itemsep leaves ~0.1cm of real room —
    # an unsigned sum credits space the student never gets
    for v in re.finditer(r"\\vspace\*?\{\s*(-?[\d.]+)\s*(cm|mm|in|pt|ex|em)\s*\}", item):
        cm += to_cm(v.group(1), v.group(2))
    # \\[5cm] line skips are workspace too — a sheet built on them is usable
    # and must not be rejected (that trains generators to route around the gate)
    for v in re.finditer(r"\\\\\*?\s*\[\s*(-?[\d.]+)\s*(cm|mm|in|pt|ex|em)\s*\]", item):
        cm += to_cm(v.group(1), v.group(2))
    for s in re.finditer(r"\\(bigskip|medskip|smallskip)\b", item):
        cm += SKIP_CM[s.group(1)]
    return cm


def minipage_depth_fn(tex):
    """Return a pos -> minipage-nesting-depth function for this document."""
    events = sorted([(m.start(), 1) for m in re.finditer(r"\\begin\{minipage\}", tex)] +
                    [(m.start(), -1) for m in re.finditer(r"\\end\{minipage\}", tex)])

    def depth_at(pos):
        d = 0
        for p, delta in events:
            if p >= pos:
                break
            d += delta
        return d
    return depth_at


def stranded_workspace(tex):
    """Workspace-sized unstarred \\vspace outside any minipage (fault 3).

    Only unstarred \\vspace is flagged: \\vspace* survives a page break, so
    the space is never lost (though the templates' minipage form is still
    preferred, since it also keeps stem and workspace on the same page).
    Returns [(line_number, cm), ...].
    """
    depth_at = minipage_depth_fn(tex)
    found = []
    for m in re.finditer(r"\\vspace\{\s*(-?[\d.]+)\s*(cm|mm|in|pt|ex|em)\s*\}", tex):
        cm = to_cm(m.group(1), m.group(2))
        if cm >= MIN_CM_PER_PROBLEM and depth_at(m.start()) == 0:
            found.append((tex.count("\n", 0, m.start()) + 1, round(cm, 2)))
    return found


def main():
    path = sys.argv[1]
    tex = strip_comments(open(path).read())
    name = path.rsplit("/", 1)[-1]
    if re.match(r"^(ak|ss)_", name):
        print(f"check_layout: {name} is a key/guide, not written on — skipped")
        return 0

    faults = []
    print(f"Layout report: {path}")

    lists = enumerates(tex)
    for n, (opts, body) in enumerate(lists, 1):
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

    # \problem-macro sheets: same two rules over the regions, treated as one
    # pseudo-list (a figure sits just as ambiguously between \problem blocks
    # as between \item entries)
    regions = problem_regions(tex)
    if regions:
        valued = [i for i, (_, r, _) in enumerate(regions, 1) if has_valued_figure(r)]
        if valued and len(valued) != len(regions):
            faults.append(
                f"problem blocks: {len(valued)} of {len(regions)} problems carry a "
                f"figure with values (problems {valued}). A student reading a "
                f"neighbouring problem will apply the nearest figure to it. Give "
                f"every problem its own valued figure, or move shared labelling "
                f"into a value-free reference figure.")
        else:
            print(f"  problem blocks: figure scope ok "
                  f"({'all' if valued else 'no'} {len(regions)} problems carry valued figures)")

        # regions whose workspace lives in a nested list (multi-part template)
        # are governed by the enumerate pass above — skip the floor here
        thin = [(i, round(opt + space_cm("", r), 2))
                for i, (opt, r, had_list) in enumerate(regions, 1)
                if not had_list and opt + space_cm("", r) < MIN_CM_PER_PROBLEM]
        if thin:
            worst = min(c for _, c in thin)
            faults.append(
                f"problem blocks: {len(thin)} of {len(regions)} problems have under "
                f"{MIN_CM_PER_PROBLEM}cm of work space (thinnest {worst}cm). "
                f"SKILL.md specifies ~5cm per problem, 8cm multi-step. Pass the "
                f"workspace as the macro's optional argument — \\problem[5cm]{{...}} "
                f"— so it lives inside the problem's unbreakable minipage.")
        else:
            print(f"  problem blocks: work space ok "
                  f"(all {len(regions)} problems ≥ {MIN_CM_PER_PROBLEM}cm)")

    if not lists and not regions:
        print("\n  ⚠ PARSED ZERO PROBLEMS from this file.")
        print("    Nothing was checked, so this is NOT a pass. The worksheet")
        print("    must use \\problem{...}/\\problem[5cm]{...} or an")
        print("    enumerate/\\item list.")
        return 2

    # 3. page-break glue
    for line, cm in stranded_workspace(tex):
        faults.append(
            f"line {line}: workspace \\vspace{{{cm}cm}} sits outside any minipage. "
            f"LaTeX discards \\vspace glue at a page or column break, so this space "
            f"vanishes exactly when its problem lands at a page bottom — the student "
            f"gets a stem with zero cm to work in. Put the workspace inside the "
            f"problem's unbreakable minipage (\\par\\vspace*{{{cm}cm}} before "
            f"\\end{{minipage}}, or \\problem[{cm}cm]{{...}} — see "
            f"references/latex-templates.md), or at minimum star it (\\vspace*).")

    if faults:
        print("\n❌ layout faults:")
        for f in faults:
            print(f"  • {f}")
        return 1
    print("\n✅ layout ok — figures are unambiguous and every problem has room to work.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
