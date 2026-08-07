# Synthesis Review: Taylor Polynomials and Remainder Bounds — AP Calculus BC

Three PDFs are ready:

- **`ws_taylor_curr500.pdf`** — the student worksheet, 10 problems.
- **`ak_taylor_curr500.pdf`** — the full step-by-step answer key.
- **`ss_taylor_curr500.pdf`** — a 2-page study guide.

## How the sheet is built

Problems 1–3 are a warm-up, one on each of the three moves. From problem 4 on
they rotate one after another, so no two consecutive problems use the same move
and the student has to decide first *what kind of question this is*:

| | build from derivatives | reuse a known series | bound the error |
|---|---|---|---|
| warm-up | 1 | 2 | 3 |
| mixed | 4, 7 | 5, 8 | 6, 9 |

The centres vary deliberately — Maclaurin for problems 1, 2, 5, 6, 8, 10, but
$a = 1$ for $\ln x$ and $a = 4$ for $\sqrt{x}$ — so "expand about zero" cannot
become a reflex. Problem 10 is the synthesis: build the polynomial, use it, and
then decide which of the two remainder bounds is even available. (The answer is
Lagrange: $xe^x$ has all-positive terms at a positive input, so it does not
alternate.)

## Verification — what a machine checked, what you check

The answer key's "What is verified" note reports the same split.

- **15 of the 19 checks are machine-verified with SymPy**: every derivative that
  produces a coefficient (the third derivatives of $e^{2x}$, $\ln x$ and
  $xe^{x}$, and the second derivative of $\sqrt{x}$), every polynomial
  evaluation, both Lagrange bounds, both alternating bounds, and the exact sum
  $e^{-1}$.
- **4 are instructor-judged** — the written parts of problems 3, 6, 9 and 10.
  These are the ones that matter most on this topic and none of them is a
  number: why $M = e$ on $[0,1]$; what must be checked before an alternating
  bound may be used; why $|f^{(4)}|$ for $\ln(1+x)$ is largest at the left end;
  and which bound applies to a non-alternating series. Each has a rubric in the
  key.

Nothing is marked `[unchecked]`: every printed answer slot has an entry.

## Notes

- Each problem prints the polynomial it is working with, so a slip in part (a)
  does not cascade into part (b) — the two are gradeable independently.
- Problem 5 is worth a comment: the three-term estimate 0.8944 sits noticeably
  above the true 0.892857, and the key points at the next term ($-27x^6$) as the
  reason. Seeing a truncation error be *visible* is the point of that problem.
- The grade level and the LIM-8 tagging print on the answer key only.
