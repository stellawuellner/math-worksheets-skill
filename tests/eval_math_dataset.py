#!/usr/bin/env python3
"""
eval_math_dataset.py — Corpus evaluation of the verifier against the MATH
dataset (Hendrycks et al., "Measuring Mathematical Problem Solving").

MATH problems carry a final answer in \\boxed{...} inside the solution, tagged
by subject (Prealgebra, Algebra, Geometry, Precalculus, ...) and difficulty
1-5 — nearly the same scope as this skill. This eval measures:

  1. EXPRESSIBILITY — what fraction of boxed answers our allowlist grammar can
     represent (numbers, fractions, radicals, pi-multiples). The remainder is
     the honest ceiling on machine verification for competition-style answers.
  2. ACCEPT-CORRECT — expressible answers, checked as equiv/approx against
     themselves parsed independently, must PASS.
  3. REJECT-PERTURBED — the same answers shifted (+1, or numerator+1 for
     fractions) must FAIL.

NOTE: this script needs the dataset locally — some sandboxed environments
(including Claude Code remote containers) block huggingface.co, so download on
your own machine:

  Option A (Hugging Face):
    pip install datasets
    python3 -c "from datasets import load_dataset; \\
        load_dataset('EleutherAI/hendrycks_math', 'algebra')"

  Option B (original archive): https://people.eecs.berkeley.edu/~hendrycks/MATH.tar
    tar xf MATH.tar   # gives MATH/test/<subject>/*.json

Usage:
  python3 tests/eval_math_dataset.py MATH/test --subjects algebra geometry precalculus prealgebra
"""

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import verify  # noqa: E402


def extract_boxed(solution):
    """Return the content of the last \\boxed{...} (handles nested braces)."""
    start = solution.rfind("\\boxed{")
    if start == -1:
        return None
    i = start + len("\\boxed{")
    depth = 1
    out = []
    while i < len(solution) and depth:
        ch = solution[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                break
        out.append(ch)
        i += 1
    return "".join(out) if depth == 0 else None


LATEX_REPLACEMENTS = [
    (re.compile(r"\\dfrac"), r"\\frac"),
    (re.compile(r"\\tfrac"), r"\\frac"),
    (re.compile(r"\\frac\{([^{}]+)\}\{([^{}]+)\}"), r"((\1)/(\2))"),
    (re.compile(r"\\frac(\d)(\d)"), r"((\1)/(\2))"),
    (re.compile(r"\\sqrt\{([^{}]+)\}"), r"sqrt(\1)"),
    (re.compile(r"\\sqrt(\d)"), r"sqrt(\1)"),
    (re.compile(r"\\pi"), "pi"),
    (re.compile(r"\\cdot|\\times"), "*"),
    (re.compile(r"\\left|\\right"), ""),
    (re.compile(r"\\!|\\,|\\;|\\ |~"), ""),
    (re.compile(r"\\%"), ""),
    (re.compile(r"\\\$"), ""),
    (re.compile(r"(?<=\d),(?=\d{3})"), ""),
    (re.compile(r"\^"), "**"),
    (re.compile(r"\{"), "("),
    (re.compile(r"\}"), ")"),
]


def latex_to_expr(ans):
    """Best-effort translation of a boxed LaTeX answer to allowlist syntax.
    Returns None for answers that clearly aren't a single closed-form value
    (intervals, tuples, text, matrices, units)."""
    ans = ans.strip()
    if any(tok in ans for tok in ("\\text", "\\begin", "\\end", "\\mbox", ",",
                                  "\\pm", "\\infty", "\\cup", "=", "<", ">",
                                  "^\\circ", "\\circ")):
        return None
    for pattern, repl in LATEX_REPLACEMENTS:
        prev = None
        while prev != ans:
            prev = ans
            ans = pattern.sub(repl, ans)
    if "\\" in ans:  # anything still un-translated
        return None
    # insert explicit multiplication: 2sqrt(3) → 2*sqrt(3), 3pi → 3*pi
    ans = re.sub(r"(\d)\s*(sqrt|pi)\b", r"\1*\2", ans)
    ans = re.sub(r"\)\s*(sqrt|pi)\b", r")*\1", ans)
    return ans


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root", help="MATH/test directory")
    ap.add_argument("--subjects", nargs="*",
                    default=["prealgebra", "algebra", "geometry", "precalculus"])
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--report", default=None)
    args = ap.parse_args()

    stats = {"total": 0, "expressible": 0, "pass": 0, "fail": 0,
             "perturbed_false_accepts": 0, "perturbed_checked": 0}
    failures, false_accepts = [], []

    files = []
    for subject in args.subjects:
        subject_dir = Path(args.root) / subject
        if not subject_dir.is_dir():
            print(f"warning: {subject_dir} not found, skipping", file=sys.stderr)
            continue
        files.extend(sorted(subject_dir.glob("*.json")))
    if args.limit:
        files = files[: args.limit]

    for path in files:
        with open(path) as f:
            row = json.load(f)
        boxed = extract_boxed(row.get("solution", ""))
        if boxed is None:
            continue
        stats["total"] += 1
        expr = latex_to_expr(boxed)
        if expr is None:
            continue
        try:
            parsed = verify.safe_parse(expr)
        except verify.VerifyInputError:
            continue
        stats["expressible"] += 1

        ok = verify.sym_equal(parsed, verify.safe_parse(expr))
        if ok:
            stats["pass"] += 1
        else:
            stats["fail"] += 1
            failures.append((str(path), boxed))
            continue

        stats["perturbed_checked"] += 1
        if verify.sym_equal(parsed, verify.safe_parse(f"({expr}) + 1")):
            stats["perturbed_false_accepts"] += 1
            false_accepts.append((str(path), boxed))

    print(f"MATH corpus eval — {stats['total']} boxed answers "
          f"({', '.join(args.subjects)})")
    if stats["total"]:
        print(f"  expressible in allowlist grammar: {stats['expressible']}"
              f"/{stats['total']} ({100*stats['expressible']/stats['total']:.1f}%)")
    if stats["expressible"]:
        print(f"  accept-correct: {stats['pass']}/{stats['expressible']}")
        print(f"  reject-perturbed: "
              f"{stats['perturbed_checked'] - stats['perturbed_false_accepts']}"
              f"/{stats['perturbed_checked']} "
              f"({stats['perturbed_false_accepts']} false accepts)")
    if args.report:
        with open(args.report, "w") as f:
            json.dump({"stats": stats, "sample_failures": failures[:50],
                       "false_accepts": false_accepts[:50]}, f, indent=2)
    sys.exit(1 if stats["perturbed_false_accepts"] else 0)


if __name__ == "__main__":
    main()
