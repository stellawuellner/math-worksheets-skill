#!/usr/bin/env python3
r"""
check_layout.py — catch the layout faults that make a *correct* worksheet
unusable in front of a student.

Usage: python3 tests/check_layout.py <worksheet.tex> [--figs <figs.tex>]

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

4. ANSWER LOCATION. Bare workspace gives the grader nowhere to look and the
   student nothing to commit to — the final answer drowns in scratch work.
   Every enumerate \item must therefore contain one answer-location macro:
   \ansline (right-aligned blank), \ansblank (inline drill blank),
   \answerline{unit} (blank + measurement unit), or \noansline (explicit
   opt-out for problems whose worked product IS the answer — sketch, proof,
   construction). \problem regions are exempt BY DESIGN: the shipped
   preamble's \problem macro emits the answer line itself whenever its
   workspace argument is positive, so the document body shows nothing to
   count — construction, not linting, is the guarantee there. Rules run on
   comment-stripped text, so a commented-out marker can never satisfy this.

Both the enumerate/\item and the \problem{...} macro shapes are parsed — the
skill's first-taught template style is \problem, and a checker that only sees
enumerate lists passes a zero-workspace \problem sheet vacuously (the same
zero-parse failure class fixed in check_prose_consistency.py). Enumerate
parsing is DEPTH-AWARE via _tex_segments.enumerate_lists: every nested
part-list is checked as its own list against its own [itemsep=..], and a
naive regex that truncated the outer list at the first nested \end{enumerate}
(dropping every item after the multi-part problem) is gone.

Exit 0 clean, 1 on any fault, 2 when nothing parsed (no list and no \problem
block means nothing was checked — that is NOT a pass). Skips answer keys and
study guides, which are read rather than written on.
"""

import re
import sys

from _probfig import expand_probfigs, probfig_bodies
from _tex_segments import enumerate_lists

MIN_CM_PER_PROBLEM = 2.5      # hard floor; SKILL.md recommends 5cm
UNIT_CM = {"cm": 1.0, "mm": 0.1, "in": 2.54, "pt": 0.0352778, "ex": 0.15, "em": 0.35}
# \bigskip/\medskip/\smallskip at their conventional sizes — coarse, but they
# are real writing room and ignoring them under-credits a legitimate sheet
SKIP_CM = {"bigskip": 0.42, "medskip": 0.28, "smallskip": 0.14}

# matches a \problem use site — \problem{...} or \problem[5cm]{...} (the macro
# takes the workspace as an optional first argument). Does NOT match the
# preamble's \newcommand{\problem}... definition: there the next char is `}`.
PROBLEM_RE = re.compile(r"\\problem(\[[^\]]*\])?\{")

# the answer-location macros the shipped preamble defines (rule 4). \b so a
# hypothetical \anslinesque never satisfies the rule.
ANSWER_RE = re.compile(r"\\(?:ansline|ansblank|answerline|noansline)\b")


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


def blank_spans(text, spans, base=0):
    """Overwrite the given absolute spans with spaces inside text[base:...].

    Blanking (not deleting) keeps every remaining offset true to the source,
    the same discipline strip_comments follows."""
    chars = list(text)
    for a, b in spans:
        for i in range(max(a - base, 0), min(b - base, len(chars))):
            chars[i] = " "
    return "".join(chars)


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
    # depth-aware env spans: a naive .*? strip ends at the FIRST nested
    # \end{enumerate}, leaving the tail of a multi-part region in place —
    # the same truncation class enumerate_lists exists to kill
    env_spans = [span for _, span, _, _ in enumerate_lists(tex)]
    out = []
    for m, nxt in zip(matches, matches[1:] + [None]):
        start = m.start()
        end = nxt.start() if nxt else len(tex)
        region = tex[start:end]
        opt_cm = 0.0
        if m.group(1):
            o = re.search(r"(-?[\d.]+)\s*(cm|mm|in|pt|ex|em)", m.group(1))
            if o:
                opt_cm = to_cm(o.group(1), o.group(2))
        inner = [(a, b) for a, b in env_spans if a < end and b > start]
        stripped = blank_spans(region, inner, base=start)
        out.append((opt_cm, stripped, stripped != region))
    return out


def has_valued_figure(item):
    """A figure whose visible labels contain a number: tikz \\node text, pic
    "..." quotes, figure-macro args, \\probfig{N}, or any \\includegraphics."""
    for fig in re.finditer(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", item, re.S):
        for node in re.finditer(r"\\node\b[^{]*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}", fig.group(0)):
            if re.search(r"\d", node.group(1)):
                return True
        # pic-quote labels ("$34^\circ$") are printed values too — the taught
        # circle-angle template carries its ONLY numbers there. Same
        # extraction as check_prose_consistency.figure_label_numbers' pic
        # branch, so the two detectors cannot disagree about what counts as a
        # figure value. Accepted edge (fix both branches together if it ever
        # bites): a digit-subscripted label like $\theta_1$ counts as valued —
        # nothing in the repo emits one, and the failure direction is a loud
        # false FAIL, never a silent false PASS. Confined to the tikzpicture
        # body: straight-quoted prose digits elsewhere in the item must not
        # trip the figure rule.
        for q in re.finditer(r'"\s*\$?([^"$]*)\$?\s*"', fig.group(0)):
            if re.search(r"\d", q.group(1)):
                return True
    # \includegraphics is an opaque image: no checker can read the values it
    # almost certainly shows (a figure worth including carries labels), so it
    # must be ASSUMED valued and the all-or-nothing scope rule applies
    # unconditionally. check_prose_consistency additionally hard-fails it.
    if re.search(r"\\includegraphics\b", item):
        return True
    # macro-style figures: \rtfig{...}{$b=8$}... — any braced arg holding a
    # digit. The optional [..] arg (scale/styling, e.g. \rtfig[scale=1.2])
    # must neither defeat detection nor have its digits counted as values —
    # a macro the detector silently stops seeing is a false PASS on the
    # all-or-nothing figure rule, the dangerous direction.
    for mac in re.finditer(r"\\[a-zA-Z]*(?:rt|tri|fig)[a-zA-Z]*"
                           r"(?:\[[^\]]*\])?((?:\{[^{}]*\}){2,})", item):
        if re.search(r"\d", mac.group(1)):
            return True
    # \probfig{N} is generated by scripts/render_figures.py from the problem's
    # verified givens, so it ALWAYS carries values — but its single braced arg
    # is a problem index, which the two-args-with-a-digit test above cannot
    # see. Recognize the call itself, or a mixed \probfig/bare list would slip
    # past the all-or-nothing scope rule.
    if re.search(r"\\probfig\{\d+\}", item):
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
    argv = sys.argv[1:]
    figs_path = None
    if "--figs" in argv:
        i = argv.index("--figs")
        figs_path = argv[i + 1] if i + 1 < len(argv) else ""
        del argv[i:i + 2]
    if len(argv) != 1 or figs_path == "":
        print("Usage: check_layout.py <worksheet.tex> [--figs <figs.tex>]",
              file=sys.stderr)
        return 1
    path = argv[0]
    tex = open(path).read()
    # Expand rendered \probfig{N} figures in place so both rules run on what
    # actually prints. Unresolved calls (stale figs, no --figs) stay in the
    # text — has_valued_figure counts them as valued, so the scope rule holds
    # either way.
    if figs_path:
        tex, _ = expand_probfigs(tex, probfig_bodies(open(figs_path).read()))
    # blank comments AFTER expansion so rendered figure bodies are cleaned too
    tex = strip_comments(tex)
    name = path.rsplit("/", 1)[-1]
    if re.match(r"^(ak|ss)_", name):
        print(f"check_layout: {name} is a key/guide, not written on — skipped")
        return 0

    faults = []
    print(f"Layout report: {path}")

    # Depth-aware: every enumerate at any depth is its own list, judged
    # against its own [itemsep=..] — a naive .*? regex ended the outer list at
    # the FIRST nested \end{enumerate}, so nested parts were counted as
    # top-level problems and every real item after them silently escaped both
    # rules (the false-PASS direction).
    lists = enumerate_lists(tex)
    for n, (opts, _env_span, item_spans, child_idxs) in enumerate(lists, 1):
        if not item_spans:
            continue
        # a nested part-list is checked as its own list (with its own opts),
        # so its items are blanked out of the parent item — otherwise a
        # part's figure would false-fail the parent's all-or-nothing rule
        child_item_spans = [sp for k in child_idxs for sp in lists[k][2]]
        its, had_nested = [], []
        for (s, e) in item_spans:
            inner = [(a, b) for a, b in child_item_spans if a >= s and b <= e]
            its.append(blank_spans(tex[s:e], inner, base=s))
            had_nested.append(bool(inner))
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

        # 2. work space — items holding a nested part-list are skipped: their
        # workspace lives in the child's itemsep, which the child's own pass
        # enforces (mirrors problem_regions' had_list)
        thin = [(i, round(space_cm(opts, it), 2))
                for i, (it, nested) in enumerate(zip(its, had_nested), 1)
                if not nested and space_cm(opts, it) < MIN_CM_PER_PROBLEM]
        if thin:
            worst = min(c for _, c in thin)
            faults.append(
                f"list {n}: {len(thin)} of {len(its)} problems have under "
                f"{MIN_CM_PER_PROBLEM}cm of work space (thinnest {worst}cm). "
                f"SKILL.md specifies ~5cm per problem, 8cm multi-step. Raise itemsep "
                f"or add \\vspace after each item.")
        else:
            print(f"  list {n}: work space ok (all {len(its)} problems ≥ {MIN_CM_PER_PROBLEM}cm)")

        # 4. answer location (\problem regions are exempt — see the docstring)
        noans = [i for i, it in enumerate(its, 1) if not ANSWER_RE.search(it)]
        if noans:
            faults.append(
                f"list {n}: items {noans} have no designated answer location. "
                f"End each item with \\ansline (right-aligned answer blank) or "
                f"an inline \\ansblank; mark \\noansline only where the worked "
                f"product IS the answer (sketch, proof, construction). A grader "
                f"should never hunt through scratch work for the final answer.")
        else:
            print(f"  list {n}: answer location ok "
                  f"(all {len(its)} items carry an answer-location macro)")

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
