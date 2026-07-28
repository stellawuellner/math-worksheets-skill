#!/usr/bin/env python3
"""
_tex_segments.py — split a LaTeX document into per-problem segments.

Shared segmentation for the binding checkers (check_answer_key.py today; the
sibling checkers parse the same shapes and can adopt it). Why a helper: the
shipped templates emit THREE document shapes, and a checker that parses only
one silently skips the others — the exact parser gap that let a fully swapped
enumerate-style answer key pass green (audit B1) after c2608b9 had fixed the
mirror-image gap in check_prose_consistency.py only.

Shapes, tried in order:

  1. \\problem{...} macros (answer-key template): a segment runs from each
     \\problem to the next, so the worked steps and \\boxed answers that
     FOLLOW the statement stay attached to their problem. Tolerates the
     optional-argument form \\problem[8cm]{...}.
  2. enumerate/\\item lists (worksheet template): DEPTH-AWARE — only \\item
     tokens belonging directly to an outermost enumerate start a segment.
     A naive regex split truncates at the first nested \\end{enumerate} and
     over-splits multi-part problems whose parts are their own nested list.
  3. examplebox environments (study-guide template): one worked example per
     box (SKILL.md: "one entry per worked example"), so ss_ documents bind
     per example exactly like answer keys bind per problem.

segment_spans(tex) -> list of (start, end) offsets into tex, or None when
none of the three shapes appears — callers decide how loudly to fail.
"""
import re

# \begin{enumerate} / \end{enumerate} never false-match the option text
# ([itemsep=4cm] carries no backslash) and \b keeps \itemsep from matching
# \item. itemize is tracked too: an \item of a bullet list nested inside a
# problem must not start a new problem segment.
_LIST_TOKEN = re.compile(
    r"\\begin\{(enumerate|itemize)\}|\\end\{(enumerate|itemize)\}|\\item\b")

_COMMENT = re.compile(r"(?<!\\)%[^\n]*")


def blank_comments(tex):
    """Overwrite LaTeX comments with spaces, PRESERVING length and offsets.

    A commented-out \\item or a '% \\problem{...}' remark would otherwise
    start a phantom segment and shift every answer after it. Blanking (not
    deleting) keeps every span valid against the original text. \\% escapes
    are kept — they are printed percent signs, not comments.
    """
    return _COMMENT.sub(lambda m: " " * len(m.group(0)), tex)


def _problem_spans(tex):
    """One span per \\problem{...} use, running to the next \\problem or EOF.
    The regex skips the preamble definition (\\newcommand{\\problem}... has no
    '{' directly after the name) and accepts an optional [length] argument."""
    starts = [m.start() for m in re.finditer(r"\\problem(?:\[[^\]]*\])?\{", tex)]
    if not starts:
        return None
    return list(zip(starts, starts[1:] + [len(tex)]))


def _item_spans(tex):
    """One span per top-level \\item across every outermost enumerate.

    Walks list tokens with an environment stack instead of a regex over the
    whole environment: nested part-lists (multi-part template) and itemize
    bullets inside an item must extend the current segment, not split it."""
    spans, stack, item_start = [], [], None
    for m in _LIST_TOKEN.finditer(tex):
        opened, closed = m.group(1), m.group(2)
        if opened:
            stack.append(opened)
        elif closed:
            if stack == ["enumerate"] and item_start is not None:
                spans.append((item_start, m.start()))
                item_start = None
            if stack:
                stack.pop()
        else:  # \item
            if stack == ["enumerate"]:
                if item_start is not None:
                    spans.append((item_start, m.start()))
                item_start = m.start()
    return spans or None


def _examplebox_spans(tex):
    """One span per examplebox body — the study-guide worked-example unit."""
    spans = [(m.start(1), m.end(1)) for m in re.finditer(
        r"\\begin\{examplebox\}(.*?)\\end\{examplebox\}", tex, re.S)]
    return spans or None


def segment_spans(tex):
    """Per-problem (start, end) spans, or None if no known shape parses."""
    tex = blank_comments(tex)
    return _problem_spans(tex) or _item_spans(tex) or _examplebox_spans(tex)
