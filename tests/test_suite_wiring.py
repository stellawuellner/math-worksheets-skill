#!/usr/bin/env python3
r"""test_suite_wiring.py — a suite that never runs is indistinguishable from a
suite that passes, so the wiring is a contract and this checks it.

TWO THINGS WENT WRONG, both found by auditing rather than by a red build, which
is the whole problem with this class of fault.

1. `coverage.sh` carried a hand-maintained list of suites and it drifted: eleven
   wired suites stopped being measured, and the reported percentage described a
   shrinking fraction of the tests while reading like a whole-project number.
   Fixed by globbing `tests/test_*.py`. This file keeps the glob honest from the
   other side — every suite on disk must actually be reachable from CI.

2. Six suites render a real document and read the PDF back, so they open with
   `shutil.which("pdflatex") or shutil.which("tectonic")` and skip cleanly when
   no engine is present. CI's `verify` job does not install TeX. Four of the six
   were invoked ONLY there, so on every push they printed "skipped" and exited 0
   — including the SSA label-collision measurement and the probe that compiles
   every figure snippet the docs print. A clean skip is the right behaviour on a
   contributor's laptop and the wrong result in CI, and nothing distinguished
   the two. They now run in the `visual` job, which is the one that installs TeX.

The check is deliberately textual: it reads the shell drivers and the workflow
as text rather than importing them, because what it is testing is whether a name
appears in the file that CI executes.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS = os.path.join(ROOT, "tests")
WORKFLOW = os.path.join(ROOT, ".github", "workflows", "tests.yml")
FAILS = []

# The engine probe every render-and-read-back suite opens with. A suite matching
# this skips silently without TeX, which is why it may not live in a TeX-less job.
ENGINE_PROBE = re.compile(r"which\(\s*['\"](?:pdflatex|tectonic)['\"]\s*\)")


def check(label, cond, detail=""):
    print(f"  {'✅' if cond else '❌'} {label}")
    if not cond:
        FAILS.append(f"{label}{': ' + detail if detail else ''}")


def read(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def suites():
    """Every executable suite on disk, by basename."""
    names = sorted(f for f in os.listdir(TESTS)
                   if f.startswith("test_") and f.endswith(".py"))
    return names + ["visual_regression.py"]


def code_only(src):
    """Source with comments and docstrings removed, string literals kept.

    A plain grep for the engine probe matches this very file, which quotes the
    probe in its own docstring to explain it — and would then report itself as
    an unwired rendering suite. Stripping every string instead would go too far
    the other way: the probe IS a call with a string argument, so dropping
    string tokens makes it undetectable everywhere. What has to go is exactly
    the prose: comments, and strings standing alone as a statement.
    """
    import io
    import token as tk
    import tokenize
    try:
        toks = list(tokenize.generate_tokens(io.StringIO(src).readline))
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return src  # unparseable: fall back to matching everything
    kept, at_stmt_start = [], True
    for t in toks:
        if t.type == tk.COMMENT:
            continue
        if t.type == tk.STRING and at_stmt_start:
            continue                      # a docstring: prose, not behaviour
        if t.type in (tk.NEWLINE, tk.NL, tk.INDENT, tk.DEDENT, tk.ENCODING):
            at_stmt_start = True
            continue
        kept.append(t.string)
        at_stmt_start = False
    return "".join(kept)


def needs_engine(name):
    return bool(ENGINE_PROBE.search(code_only(read(os.path.join(TESTS, name)))))


def strip_yaml_comments(text):
    """Drop `#` comments, keeping line structure.

    Every membership test below asks "does this job RUN x", and a comment is
    not a step. This matters more than it sounds: the comment explaining why
    the TeX job installs sympy contains the word "sympy" and names two of the
    suites it guards, so matching against raw text made three assertions
    unfalsifiable — deleting the step they check left them green. Caught by
    mutation-testing the assertions rather than by trusting them.

    A `#` inside a quoted string is not a comment; the workflow has none today,
    but tracking quote state costs three lines and removes the caveat.
    """
    out = []
    for line in text.split("\n"):
        q = None
        for i, ch in enumerate(line):
            if q:
                if ch == q:
                    q = None
            elif ch in "\"'":
                q = ch
            elif ch == "#":
                line = line[:i]
                break
        out.append(line)
    return "\n".join(out)


def workflow_jobs(text):
    """Split tests.yml into {job-name: body}. Jobs are the 2-space keys under
    `jobs:`; a body runs to the next such key. Enough structure for "which job
    RUNS this file", and no YAML dependency to install in CI."""
    text = strip_yaml_comments(text)
    body = text.split("\njobs:", 1)[1] if "\njobs:" in text else text
    starts = [(m.group(1), m.start()) for m in
              re.finditer(r"^  ([a-zA-Z0-9_-]+):\s*$", body, re.M)]
    out = {}
    for i, (name, pos) in enumerate(starts):
        end = starts[i + 1][1] if i + 1 < len(starts) else len(body)
        out[name] = body[pos:end]
    return out


def main():
    print("Suite wiring:")

    on_disk = suites()
    driver = read(os.path.join(TESTS, "run_tests.sh"))
    cov = read(os.path.join(TESTS, "coverage.sh"))
    wf = read(WORKFLOW)
    jobs = workflow_jobs(wf)

    check("tests.yml parses into named jobs", bool(jobs), str(list(jobs)))
    check("the workflow still has a `verify` and a `visual` job",
          "verify" in jobs and "visual" in jobs, str(sorted(jobs)))
    if FAILS:
        return report()

    # ── 1. Every suite on disk is reachable from CI ──────────────────────────
    # coverage.sh globs tests/test_*.py, so membership there is automatic for
    # anything matching that pattern; assert the glob is still what it uses,
    # rather than trusting a list that could have been reintroduced.
    globbed = "tests/test_*.py" in cov
    check("coverage.sh still GLOBS the suite list rather than listing it",
          globbed,
          "a hand-maintained list is what let eleven suites stop being measured")

    unreachable = [n for n in on_disk
                   if n not in driver and n not in cov
                   and not (globbed and n.startswith("test_"))]
    check("every suite on disk is reachable from a CI entry point",
          not unreachable, ", ".join(unreachable))

    # ── 2. No engine-dependent suite runs ONLY where there is no engine ──────
    # The `verify` job installs poppler but not TeX. A suite that probes for an
    # engine exits 0 there without asserting anything, so it has to also appear
    # in `visual`, which installs texlive.
    tex_job = jobs["visual"]
    check("the visual job is the one that installs TeX",
          "texlive-latex-base" in tex_job,
          "if TeX moved jobs, this file is pinning the wrong one")

    engine_suites = [n for n in on_disk if needs_engine(n)]
    check("the engine-dependent suites are still detectable by their probe",
          len(engine_suites) >= 5, f"found {len(engine_suites)}: {engine_suites}")

    silent = [n for n in engine_suites if n not in tex_job]
    check("every engine-dependent suite runs in the job that has TeX",
          not silent,
          f"{', '.join(silent)} — these skip cleanly and report green wherever "
          "no engine exists, so running them only in `verify` tests nothing")

    # TeX alone is not the whole environment. These suites render figures via
    # scripts/render_figures.py, which imports verify.py's triangle solver, so
    # sympy is a hard requirement in this job too. Missing it is worse than a
    # skip: test_ssa_figure_labels exits 1, and test_overprint quietly drops
    # three renderer checks and still exits 0. Both happened on the first CI run
    # that executed this step.
    check("the TeX job also installs sympy, which the figure renderer needs",
          "sympy" in tex_job,
          "test_ssa_figure_labels exits 1 without it and test_overprint "
          "degrades to 'renderer unavailable' while still passing")

    # ── 3. The README's count matches what is on disk ────────────────────────
    # Not a wiring fact, but it is the number a reader trusts, and it is the
    # same drift in a different file.
    readme = read(os.path.join(ROOT, "README.md"))
    n_suites = len([n for n in on_disk if n.startswith("test_")])
    claimed = re.search(r"\*\*(\d+) Python suites", readme)
    check("README states a Python-suite count", bool(claimed))
    if claimed:
        check(f"the README's suite count matches the {n_suites} on disk",
              int(claimed.group(1)) == n_suites,
              f"README says {claimed.group(1)}")

    return report()


def report():
    print()
    if FAILS:
        print(f"❌ {len(FAILS)} wiring check(s) failed:")
        for x in FAILS:
            print(f"   {x}")
        return 1
    print("✅ every suite runs somewhere it can actually assert something")
    return 0


if __name__ == "__main__":
    sys.exit(main())
