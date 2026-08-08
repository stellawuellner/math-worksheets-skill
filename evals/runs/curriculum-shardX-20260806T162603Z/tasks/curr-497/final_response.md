# Choosing and Applying a Convergence Test — AP Calculus BC

Three PDFs are ready:

- **`ws_tests_curr497.pdf`** — the student worksheet, 10 problems.
- **`ak_tests_curr497.pdf`** — the full step-by-step answer key.
- **`ss_tests_curr497.pdf`** — a 2-page study guide with all four tests.

## How the sheet ramps

The four tests appear in rotation rather than in blocks, so no two consecutive
problems use the same one, and the difficulty climbs from a single clean limit
to a problem where the obvious test provably cannot work:

| | comparison | integral | ratio | alternating |
|---|---|---|---|---|
| | 1, 5, 10 | 2, 7 | 3, 6, 9 | 4, 8 |

No two problems share a skeleton. The ratio-test items run $2^n/n!$ (limit 0),
$n!/3^n$ (limit infinite), and $n^2 3^n/n!$ (a genuine cancellation to work
through). The integral-test items run an easy $u$-substitution and then the
$\ln$-substitution one. Problem 10 is the synthesis: a student starts with the
ratio test, gets 1, and has to understand *why* that was inevitable for rational
terms before switching to limit comparison.

## Verification — what a machine checked, what you check

The answer key's "What is verified" note reports the same split.

- **14 of the 22 checks are machine-verified with SymPy**: every ratio limit and
  limit-comparison limit, both improper integrals (evaluated to
  $\tfrac{1}{2e}$ and $\tfrac{1}{\ln 2}$), the two exact sums $e^2$ and
  $\tfrac{\pi}{4}$, and both alternating-series remainder bounds
  ($\tfrac{1}{101}$ and $\tfrac{1}{11}$) computed from the term formula rather
  than counted off by hand.
- **8 are instructor-judged** — the written conclusion attached to problems 1,
  2, 4, 5, 6, 7, 9 and 10. That is deliberate: on this topic the computation is
  the easy half, and the graded skill is stating *which* conclusion a test
  licenses. Each has a rubric in the key — for instance, problem 1's requires
  the student to say why the limit being *positive* matters, and problem 2's
  requires them to say the integral's value is not the series' sum.

Nothing is marked `[unchecked]`: every printed answer slot has an entry.

## Notes

- Problem 6's answer is $\infty$, which is a legitimate ratio-test verdict, not
  a failure to compute; the key says so explicitly.
- Problem 9's cancellation is written out in full in the key, since that is
  where students lose the ratio test.
- The grade level and the LIM-7 tagging print on the answer key only.
