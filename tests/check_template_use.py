#!/usr/bin/env python3
r"""
check_template_use.py — enforce SKILL.md's "\input the shipped template,
never retype it" mechanically.

Usage: python3 tests/check_template_use.py <doc.tex>
                [--template <worksheet-preamble.tex>]

The shipped shell carries \fittedtitle overflow protection, the
workspace-in-minipage \problem semantics, and the exact environment names the
downstream binding gates expect. A hand-rolled preamble drifts in precisely
the places CI (which has no LaTeX engine) cannot see: box styling, headers,
title fitting, workspace glue. Nothing enforced the rule until this gate —
one real session hand-rolled all three document shells and every other gate
stayed green.

Three rules, all on comment-blanked text:

  A. \input{worksheet-preamble} must appear before \begin{document}.
  B. Every \input target must be a shipped template (worksheet-preamble,
     figure-macros) or a rendered figs_/meta_/qa_ file: a local preamble file
     is exactly where hand-rolled redefinitions hide from a doc-only scan.
  C. No definition (\newcommand/\renewcommand/\providecommand/\def,
     \newenvironment/\renewenvironment/\newmdenv/\renewmdenv, \definecolor)
     of an identifier the template ships. The protected set is PARSED from
     templates/worksheet-preamble.tex at run time, never hardcoded — a
     hardcoded list drifts the day the template gains a macro.

Exit 0 pass, 1 fail, 2 usage / missing file.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _tex_segments import blank_comments  # noqa: E402

# \input targets that never count as hand-rolling: the two shipped templates
# and the figs files scripts/render_figures.py emits
WHITELIST = ("worksheet-preamble", "figure-macros")

DEF_CMD = re.compile(r"\\(?:newcommand|renewcommand|providecommand)\s*\*?\s*"
                     r"\{?\s*\\([a-zA-Z]+)\}?")
DEF_TEX = re.compile(r"\\def\s*\\([a-zA-Z]+)")
DEF_ENV = re.compile(r"\\(?:newenvironment|renewenvironment)\s*\*?\s*"
                     r"\{([a-zA-Z]+)\}")
DEF_MDENV = re.compile(r"\\(?:newmdenv|renewmdenv)\s*(?:\[[^\]]*\])?\s*"
                       r"\{([a-zA-Z]+)\}")
DEF_COLOR = re.compile(r"\\definecolor\s*\{([a-zA-Z]+)\}")


def protected_identifiers(template_tex):
    """{name -> kind} for everything the shipped preamble defines.

    Derived, never hardcoded: command names from \\newcommand{\\X}, environment
    names from \\newmdenv[..]{X}, color names from \\definecolor{X}. Only
    top-level \\newcommand forms are scanned — \\renewcommand inside a macro
    body (e.g. \\headrulewidth) is LaTeX plumbing, not a shipped identifier.
    """
    tpl = blank_comments(template_tex)
    names = {}
    for m in re.finditer(r"\\newcommand\s*\{\s*\\([a-zA-Z]+)\s*\}", tpl):
        names[m.group(1)] = "command"
    for m in DEF_MDENV.finditer(tpl):
        names[m.group(1)] = "environment"
    for m in DEF_COLOR.finditer(tpl):
        names[m.group(1)] = "color"
    return names


def check(doc_tex, template_tex, template_path):
    """Return a list of fault strings (empty = pass)."""
    doc = blank_comments(doc_tex)
    protected = protected_identifiers(template_tex)
    faults = []

    # A. the template must be \input BEFORE \begin{document} (preamble-only
    # macros defined mid-document would not compile anyway)
    begin_doc = doc.find(r"\begin{document}")
    preamble = doc[:begin_doc] if begin_doc != -1 else doc
    if not re.search(r"\\input\{worksheet-preamble(?:\.tex)?\}", preamble):
        faults.append(
            "missing \\input{worksheet-preamble} before \\begin{document}")

    # B. foreign \input files: a local preamble is where hand-rolled
    # redefinitions live, invisible to the rule-C scan of this file alone.
    # figs_/meta_/qa_ files are CONSTRUCTED by the shipped renderers from the
    # verify JSON (render_figures/render_meta/render_quick_answers), so they
    # are the opposite of hand-rolled — the whole point of the construction
    # pipeline is that these inputs are allowed while everything else is not.
    _RENDERED = ("figs_", "meta_", "qa_")
    for m in re.finditer(r"\\input\{([^}]*)\}", doc):
        target = m.group(1).strip()
        base = target[:-4] if target.endswith(".tex") else target
        if base in WHITELIST or os.path.basename(base).startswith(_RENDERED):
            continue
        faults.append(
            f"\\input{{{target}}} is not a shipped template — only "
            f"\\input{{worksheet-preamble}}, \\input{{figure-macros}} and "
            f"rendered figs_*/meta_*/qa_* files are allowed")

    # C. shadowed identifiers: every *definition* verb LaTeX offers, because a
    # post-template override must use \renew* to compile and a pre-template
    # stub can use any of them
    for regex in (DEF_CMD, DEF_TEX):
        for m in regex.finditer(doc):
            if m.group(1) in protected:
                faults.append(
                    f"\\{m.group(1)} is redefined here but shipped by the "
                    f"template ({template_path} defines this "
                    f"{protected[m.group(1)]})")
    for regex in (DEF_ENV, DEF_MDENV):
        for m in regex.finditer(doc):
            if m.group(1) in protected:
                faults.append(
                    f"environment '{m.group(1)}' is redefined here but "
                    f"shipped by the template ({template_path})")
    for m in DEF_COLOR.finditer(doc):
        if m.group(1) in protected:
            faults.append(
                f"color '{m.group(1)}' is redefined here but shipped by the "
                f"template ({template_path})")
    return faults


def main():
    argv = sys.argv[1:]
    template_arg = None
    if "--template" in argv:
        i = argv.index("--template")
        template_arg = argv[i + 1] if i + 1 < len(argv) else ""
        del argv[i:i + 2]
    if len(argv) != 1 or template_arg == "":
        print("Usage: check_template_use.py <doc.tex> "
              "[--template <worksheet-preamble.tex>]", file=sys.stderr)
        return 2
    doc_path = argv[0]
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_path = template_arg or os.path.join(
        repo, "templates", "worksheet-preamble.tex")

    if not os.path.isfile(doc_path):
        print(f"Error: document not found: {doc_path}", file=sys.stderr)
        return 2
    if not os.path.isfile(template_path):
        # mirror compile.sh's partial-checkout error: the template IS the
        # contract, so a missing template means nothing can be checked
        print(f"Error: shipped template not found at {template_path} "
              f"(partial checkout?). Restore the skill's templates/ "
              f"directory.", file=sys.stderr)
        return 2

    faults = check(open(doc_path).read(), open(template_path).read(),
                   template_path)
    name = os.path.basename(doc_path)
    print(f"Template-use report: {doc_path}")
    if not faults:
        print("✅ template shell ok — shipped preamble \\input, nothing shadowed.")
        return 0
    print("\n❌ hand-rolled shell:")
    for f in faults:
        print(f"  • {f}")
    print(f"""
  Start {name} with the shipped shell (SKILL.md step 3):

    \\documentclass[12pt]{{article}}
    \\usepackage[margin=1in, top=0.75in, bottom=0.75in]{{geometry}}  % ss_: margin=0.85in, top/bottom 0.7in
    \\input{{worksheet-preamble}}
    \\input{{figure-macros}}    % when using the shipped figure macros

  compile.sh stages worksheet-preamble.tex and figure-macros.tex beside your
  .tex automatically, so /tmp compiles just work. Only geometry stays in the
  document. The shipped shell carries \\fittedtitle overflow protection, the
  workspace-in-minipage \\problem semantics, and the exact environment names
  the downstream gates bind to — a hand-rolled preamble drifts where CI
  (no LaTeX engine) cannot see.""")
    return 1


if __name__ == "__main__":
    sys.exit(main())
