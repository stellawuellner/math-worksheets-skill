#!/usr/bin/env python3
r"""test_dependency_versions.py — the version contract, pinned in one place.

WHY THIS EXISTS. "0 false accepts on 6,993 checks" is a statement about a
computer algebra system, not about verify.py. It was measured on sympy 1.14.0.
Nothing in the repo enforced or even agreed on that: CI installed `sympy>=1.12`,
the README's dev setup said `sympy==1.14.0`, its prose said "baselines were
established on SymPy 1.14", and a changelog line claimed SymPy was "pinned"
when no code anywhere checked a version. Four statements, three numbers, zero
enforcement.

THE TWO CONTROLS ARE NOT EQUALLY USEFUL, and the asymmetry is the point.

  MIN_SYMPY is a floor against the genuinely ancient. It buys less than it
  looks like it should. verify.py's sympy surface is small and old — Symbol,
  simplify, trigsimp, nsimplify, solve/integrate/limit by attribute access,
  lambdify with the mpmath backend — so an out-of-range CAS does not raise
  AttributeError and halt. It computes, and answers differently. A floor
  catches the loud failure. The silent one is the one that ships a wrong
  answer key.

  MEASURED_SYMPY is therefore load-bearing: a run under a different CAS says
  so, in the header line, instead of inheriting a guarantee nobody measured it
  under. That is the same rule the rest of this project runs on — a check that
  did not run must not read like one that passed.

There is deliberately no upper bound. Refusing to run on a newer sympy would
age the skill into uselessness, and an author who cannot run the gate at all
ships unverified answers instead of imperfectly verified ones.

The pgfplots floor is a different shape and a real one: `compat=1.18` is
required by the shipped figure styles, older distributions ship less (Ubuntu
20.04 has 1.16), and pgfplots' own error tells the user to LOWER the compat
level — which silently changes axis scaling under every style rather than
fixing anything.

No LaTeX needed: this reads source and configuration.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []


def check(label, cond, detail=""):
    print(f"  {'✅' if cond else '❌'} {label}")
    if not cond:
        FAILS.append(f"{label}{': ' + detail if detail else ''}")


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8", errors="replace") as fh:
        return fh.read()


def main():
    print("the sympy contract is stated once and enforced:")
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "verify_under_test", os.path.join(ROOT, "scripts", "verify.py"))
    v = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(v)

    check("verify.py declares a floor and the measured baseline",
          hasattr(v, "MIN_SYMPY") and hasattr(v, "MEASURED_SYMPY"))
    check("the baseline is at or above the floor",
          v._version_tuple(v.MEASURED_SYMPY)[:2] >= v.MIN_SYMPY,
          f"{v.MEASURED_SYMPY} vs floor {v.MIN_SYMPY}")

    # Version parsing, including the shape that was wrong on the first pass:
    # stripping non-digits reads '0rc1' as 1, sorting a release candidate ABOVE
    # the release it precedes. Harmless against a two-component floor and wrong
    # everywhere else, which is how it survives.
    for text, want in [("1.14.0", (1, 14, 0)), ("1.12", (1, 12)),
                       ("1.14.0rc1", (1, 14, 0)), ("1.9", (1, 9)),
                       ("2.0.0", (2, 0, 0)), ("1.14.0.dev", (1, 14, 0)),
                       ("", ())]:
        check(f"_version_tuple({text!r}) == {want}",
              v._version_tuple(text) == want, str(v._version_tuple(text)))

    check("a pre-floor version really does compare below the floor",
          v._version_tuple("1.9")[:2] < v.MIN_SYMPY and
          v._version_tuple("1.11.1")[:2] < v.MIN_SYMPY)
    check("the floor version itself is allowed",
          not v._version_tuple(".".join(map(str, v.MIN_SYMPY)))[:2] < v.MIN_SYMPY)

    print("\nthe stamp names the drift rather than hiding it:")
    real = v.sympy.__version__
    try:
        v.sympy.__version__ = v.MEASURED_SYMPY
        on_baseline = v.sympy_stamp()
        v.sympy.__version__ = "1.13.3"
        off_baseline = v.sympy_stamp()
    finally:
        v.sympy.__version__ = real
    check("on the measured version the stamp is quiet",
          on_baseline == f"SymPy {v.MEASURED_SYMPY}", on_baseline)
    check("off it, the stamp says the baselines do not cover this run",
          v.MEASURED_SYMPY in off_baseline and "1.13.3" in off_baseline
          and "not covered" in off_baseline, off_baseline)

    print("\nevery place that states a version agrees with verify.py:")
    floor = ".".join(map(str, v.MIN_SYMPY))
    readme = read("README.md")
    # CI must not install something the verifier would refuse to run under.
    wf = read(".github", "workflows", "tests.yml")
    ci_pins = re.findall(r'sympy>=([0-9.]+)', wf)
    check("CI installs sympy with a lower bound", bool(ci_pins), wf.count("sympy"))
    check(f"every CI lower bound is at or above the {floor} floor",
          all(v._version_tuple(p)[:2] >= v.MIN_SYMPY for p in ci_pins),
          f"found {ci_pins}")
    check("the README quotes the same floor",
          f"sympy>={floor}" in readme or f"sympy {floor}" in readme.lower())
    check("the README quotes the measured baseline exactly",
          v.MEASURED_SYMPY in readme,
          f"expected {v.MEASURED_SYMPY} to appear in README.md")
    # The claim that started this: nothing pinned anything.
    check("the README no longer claims SymPy is 'pinned' without qualifying it",
          "SymPy pinned and version-stamped" not in readme)

    print("\nthe pgfplots floor is guarded, not just assumed:")
    pre = read("templates", "worksheet-preamble.tex")
    check("the preamble still sets compat=1.18", "compat=1.18}" in pre)
    check("and checks the package is new enough BEFORE setting it",
          "@ifpackagelater{pgfplots}" in pre and
          pre.index("@ifpackagelater{pgfplots}") < pre.index("compat=1.18}"),
          "an unguarded compat= line fails with pgfplots' own message, which "
          "tells the user to LOWER the level")
    check("the guard raises a package error rather than a warning",
          "PackageError{worksheet-preamble}" in pre)
    check("and the message names the fix, not just the fault",
          "tectonic" in pre.split("@ifpackagelater{pgfplots}")[1][:900] and
          "texlive" in pre.split("@ifpackagelater{pgfplots}")[1][:900].lower())

    print()
    if FAILS:
        print(f"❌ {len(FAILS)} dependency-version check(s) failed:")
        for x in FAILS:
            print(f"   {x}")
        return 1
    print("✅ the version contract is stated once and agrees everywhere")
    return 0


if __name__ == "__main__":
    sys.exit(main())
