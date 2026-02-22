#!/usr/bin/env python3
"""
Math Worksheet Verifier
=======================
Run this BEFORE compiling LaTeX. The AI writes problem-specific assertions
below. Any failure stops the compile and reports the bad problem.

Usage:
    python3 verify_TOPIC_DATE.py

Exit codes:
    0 = all checks passed (safe to compile)
    1 = one or more checks failed (fix LaTeX before compiling)
    2 = some checks skipped (manual review needed, but no failures found)
"""

from sympy import *
from sympy.parsing.sympy_parser import parse_expr
import sys
import traceback

# ── Symbols ──────────────────────────────────────────────────────────────────
x, y, z, a, b, c, n, t = symbols('x y z a b c n t')
# Add more as needed: f = Function('f')

# ── Helpers ──────────────────────────────────────────────────────────────────

results = []  # (problem_num, status, message)

def check(num, description, assertion_fn):
    """
    Run one verification check.
    assertion_fn should return True if the answer is correct.
    """
    try:
        ok = assertion_fn()
        if ok:
            results.append((num, "PASS", description))
            print(f"  ✅  Problem {num}: {description}")
        else:
            results.append((num, "FAIL", description))
            print(f"  ❌  Problem {num} FAILED: {description}")
    except Exception as e:
        results.append((num, "ERROR", f"{description} — {e}"))
        print(f"  💥  Problem {num} ERROR: {description}")
        print(f"       {e}")

def manual(num, description):
    """Mark a problem as requiring manual review (graph, word problem, proof, etc.)."""
    results.append((num, "MANUAL", description))
    print(f"  👁   Problem {num} (manual review): {description}")

# ── Verification Patterns ────────────────────────────────────────────────────
#
# SOLVING EQUATIONS
# -----------------
# check(1, "Solve 2x - 5 = 11 → x = 8",
#     lambda: solve(2*x - 5 - 11, x) == [8])
#
# check(2, "Solve x² - 5x + 6 = 0 → x = 2 or 3",
#     lambda: set(solve(x**2 - 5*x + 6, x)) == {2, 3})
#
# check(3, "Solve 2x² - 3x - 5 = 0 → x = 5/2 or -1",
#     lambda: set(solve(2*x**2 - 3*x - 5, x)) == {Rational(5,2), -1})
#
# FACTORING
# ---------
# check(4, "Factor x² - 7x + 12 → (x-3)(x-4)",
#     lambda: factor(x**2 - 7*x + 12) == (x-3)*(x-4))
#
# check(5, "Factor 6x² + 7x - 3 → (2x+3)(3x-1)",
#     lambda: factor(6*x**2 + 7*x - 3) == (2*x + 3)*(3*x - 1))
#
# check(6, "Factor x³ + 8 → (x+2)(x²-2x+4)",
#     lambda: expand(factor(x**3 + 8)) == expand((x+2)*(x**2 - 2*x + 4)))
#
# SIMPLIFYING / EVALUATING
# ------------------------
# check(7, "Simplify √72 → 6√2",
#     lambda: simplify(sqrt(72) - 6*sqrt(2)) == 0)
#
# check(8, "f(0) for f(x) = 3x² - 2x + 1 → 1",
#     lambda: (3*x**2 - 2*x + 1).subs(x, 0) == 1)
#
# check(9, "f(-2) for f(x) = 3x² - 2x + 1 → 17",
#     lambda: (3*x**2 - 2*x + 1).subs(x, -2) == 17)
#
# ZEROS / INTERCEPTS
# ------------------
# check(10, "Zeros of x²(x+2)(x-2): x = 0 (mult 2), ±2",
#     lambda: set(solve(x**2 * (x+2) * (x-2), x)) == {0, 2, -2})
#
# check(11, "y-intercept of f(x) = (x-3)(x+1)² is -3",
#     lambda: ((x-3)*(x+1)**2).subs(x, 0) == -3)
#
# POLYNOMIAL EVALUATION / END BEHAVIOR
# ------------------------------------
# check(12, "Leading term of x⁵ - 4x³ is x⁵ (positive, odd → falls left/rises right)",
#     lambda: Poly(x**5 - 4*x**3, x).nth(5) > 0 and degree(x**5 - 4*x**3, x) == 5)
#
# MANUAL REVIEW (graphs, word problems, proofs, sign charts)
# ----------------------------------------------------------
# manual(13, "Sketch graph of f(x) = (x-3)(x+1)² — visual, check shape/crossings")
# manual(14, "Word problem: verify setup and units make sense")

# ─────────────────────────────────────────────────────────────────────────────
# THE AI FILLS IN THE CHECKS ABOVE FOR EACH SPECIFIC WORKSHEET.
# Delete the examples above and replace with real checks.
# ─────────────────────────────────────────────────────────────────────────────

# ── PASTE REAL CHECKS HERE ───────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────────────────────────

# ── Summary ──────────────────────────────────────────────────────────────────

def main():
    if not results:
        print("\n⚠️  No checks written yet. Add check() and manual() calls above.")
        sys.exit(2)

    passed  = [r for r in results if r[1] == "PASS"]
    failed  = [r for r in results if r[1] in ("FAIL", "ERROR")]
    manual_ = [r for r in results if r[1] == "MANUAL"]

    print(f"\n{'='*55}")
    print(f"  RESULTS: {len(passed)} passed | {len(failed)} failed | {len(manual_)} manual review")
    print(f"{'='*55}")

    if failed:
        print("\n❌ FAILED PROBLEMS — fix before compiling:\n")
        for num, status, msg in failed:
            print(f"   Problem {num}: {msg}")
        print()
        sys.exit(1)
    elif manual_:
        print("\n👁  Manual review needed for the problems listed above.")
        print("   (No automated failures — safe to compile, but please spot-check.)\n")
        sys.exit(2)
    else:
        print("\n✅ All checks passed — safe to compile.\n")
        sys.exit(0)

if __name__ == "__main__":
    main()
