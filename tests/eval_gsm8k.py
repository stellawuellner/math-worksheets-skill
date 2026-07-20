#!/usr/bin/env python3
"""
eval_gsm8k.py — Corpus evaluation of the worksheet verifier against GSM8K.

GSM8K (openai/grade-school-math) solutions embed calculator annotations of
the form <<expr=result>>. Each is a ground-truth arithmetic fact, which makes
the corpus a natural test bed for scripts/verify.py:

  1. PARSE COVERAGE — what fraction of real-world arithmetic expressions does
     the strict token allowlist accept? (Rejections here are coverage gaps,
     not bugs — but we want the number.)
  2. ACCEPT-CORRECT — of parseable checks, how many ground-truth results PASS
     (type "approx", tol 0.01 to absorb the dataset's own rounding)?
  3. REJECT-PERTURBED — same checks with the expected value shifted by +1;
     every one must FAIL. Any PASS is a real false-accept bug.

Usage:
  python3 tests/eval_gsm8k.py <path/to/test.jsonl> [--limit N] [--report out.json]

Dataset:
  https://raw.githubusercontent.com/openai/grade-school-math/master/grade_school_math/data/test.jsonl
"""

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import verify  # noqa: E402  (the skill's fixed verifier)

ANNOTATION_RE = re.compile(r"<<([^<>=]+)=([^<>]+)>>")


def normalize(expr):
    """Light cleanup of GSM8K notation before the allowlist sees it."""
    expr = expr.replace("$", "")
    expr = re.sub(r"(?<=\d),(?=\d{3})", "", expr)   # 1,000 → 1000
    expr = re.sub(r"(\d+(?:\.\d+)?)%", r"(\1/100)", expr)  # 25% → (25/100)
    return expr.strip()


def check(expr, expected, tol=0.01):
    """Returns 'PASS', 'FAIL', or 'REJECTED' using the verifier's approx path."""
    problem = {"id": 0, "type": "approx", "expr": expr, "expected": expected,
               "tol": tol}
    try:
        status, _ = verify.check_problem(problem, "approx")
        return status
    except verify.VerifyInputError:
        return "REJECTED"
    except Exception:
        return "REJECTED"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("jsonl", help="GSM8K test.jsonl path")
    ap.add_argument("--limit", type=int, default=None,
                    help="max annotations to evaluate")
    ap.add_argument("--report", default=None, help="write JSON report here")
    args = ap.parse_args()

    annotations = []
    with open(args.jsonl) as f:
        for line in f:
            row = json.loads(line)
            for m in ANNOTATION_RE.finditer(row["answer"]):
                annotations.append((m.group(1), m.group(2)))
    if args.limit:
        annotations = annotations[: args.limit]

    stats = {"total": len(annotations), "pass": 0, "fail": 0, "rejected": 0,
             "perturbed_false_accepts": 0, "perturbed_checked": 0}
    failures, rejections, false_accepts = [], [], []

    for raw_expr, raw_expected in annotations:
        expr = normalize(raw_expr)
        expected_str = normalize(raw_expected)
        try:
            expected = float(expected_str)
        except ValueError:
            try:  # a few annotations state the result as a fraction like 3/4
                import sympy
                expected = float(sympy.N(verify.safe_parse(expected_str)))
            except Exception:
                stats["rejected"] += 1
                rejections.append((raw_expr, raw_expected, "non-numeric result"))
                continue

        status = check(expr, expected)
        if status == "PASS":
            stats["pass"] += 1
        elif status == "FAIL":
            stats["fail"] += 1
            failures.append((raw_expr, raw_expected))
        else:
            stats["rejected"] += 1
            rejections.append((raw_expr, raw_expected, "allowlist/parse"))
            continue

        # Perturbation: shifting the expected answer must never pass.
        stats["perturbed_checked"] += 1
        if check(expr, expected + 1) == "PASS":
            stats["perturbed_false_accepts"] += 1
            false_accepts.append((raw_expr, raw_expected))

    parseable = stats["pass"] + stats["fail"]
    print(f"GSM8K verifier corpus eval — {stats['total']} calculator annotations")
    print(f"  parse coverage:      {parseable}/{stats['total']} "
          f"({100*parseable/max(1,stats['total']):.1f}%) "
          f"— {stats['rejected']} rejected by allowlist/format")
    print(f"  accept-correct:      {stats['pass']}/{parseable} "
          f"({100*stats['pass']/max(1,parseable):.2f}%) ground-truth checks PASS")
    print(f"  reject-perturbed:    "
          f"{stats['perturbed_checked'] - stats['perturbed_false_accepts']}"
          f"/{stats['perturbed_checked']} perturbed checks correctly FAIL "
          f"({stats['perturbed_false_accepts']} false accepts)")

    if failures[:10]:
        print("\n  sample ground-truth FAILs (dataset rounding or verifier gap):")
        for e, x in failures[:10]:
            print(f"    {e!r} = {x!r}")
    if rejections[:10]:
        print("\n  sample rejections:")
        for e, x, why in rejections[:10]:
            print(f"    [{why}] {e!r} = {x!r}")

    if args.report:
        with open(args.report, "w") as f:
            json.dump({"stats": stats,
                       "sample_failures": failures[:50],
                       "sample_rejections": rejections[:50],
                       "false_accepts": false_accepts}, f, indent=2)
        print(f"\n  report written: {args.report}")

    # Exit nonzero only on genuine verifier bugs (false accepts).
    sys.exit(1 if stats["perturbed_false_accepts"] else 0)


if __name__ == "__main__":
    main()
