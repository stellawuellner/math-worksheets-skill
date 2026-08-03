# Sigma Notation: Index Shifts and Convergence Conditions — Precalculus

Three PDFs are ready:

- **Worksheet** (`ws_seqindex_curr444.pdf`, 4 pages) — 8 problems, every one aimed at the
  two errors named in the brief: an index shifted in the summand but not in the limits,
  and the geometric sum formula used without its convergence condition (or with the wrong
  first term). The directions state both habits explicitly — shift the limits by the same
  amount, and name $a$ and $r$ before dividing.
- **Answer key** (`ak_seqindex_curr444.pdf`, 3 pages) — generated quick-answer bank with a
  "common wrong answers" line for each declared trap, then reasoning that models the fix:
  every solution counts terms before and after a shift, and every geometric problem states
  the condition before applying the formula.
- **Study guide** (`ss_seqindex_curr444.pdf`, 2 pages) — three sections (shifting a finite
  sum, checking the ratio before the sum formula, reading a sequence limit), each with a
  rule box, a worked example whose first step names the tool, and a distinct try-it with
  the answer upside down inside the box.

## What was verified

8 machine-checked results across the 8 problems, plus 2 flagged manual
(`verify_seqindex_curr444.json` carries 10 entries because problems 5 and 6 are two-part —
multiple entries sharing one problem id):

| # | Check | Answer |
|---|---|---|
| 1 | $\sum_{n=1}^{5}(2n+1)$ | 35 |
| 2 | number of terms in $\sum_{k=4}^{19}$ | 16 terms |
| 3 | find-and-fix: $\sum_{n=2}^{7}(n-1)^2$ shifted correctly | 91 |
| 4 | $\sum_{n=0}^{\infty}3(2/5)^n$ | 5 |
| 5b | the first four terms of Tess's divergent series | 48.75 |
| 6a | $\lim_{n\to\infty} 1/n$ | 0 |
| 7 | $\sum_{n=2}^{\infty}(2/3)^n$ (first term is $(2/3)^2$, not 1) | 4/3 |
| 8 | $\sum_{n=4}^{12}(n-3)^3$ rewritten from $m=1$ | 2025 |

**Two items are flagged `manual`, both deliberately:**

- **5a/5c** — the answer to "what is true about $\sum 4(3/2)^n$" is *it diverges*, a
  statement about a condition, not a number. No CAS check can stand in for "state the
  condition and show it fails", so it is manual. I kept a verified companion part (5b, the
  first four partial terms = 48.75) so the student has concrete evidence that the partial
  sums are growing rather than a bare assertion.
- **6b** — explaining why $a_n \to 0$ does not prove $\sum a_n$ converges, and naming the
  harmonic series as the counterexample. Open reasoning; the key states what a full-credit
  answer must contain and what the $n$th-term test can and cannot conclude.

**Six misconception traps are declared and machine-checked** as distinguishable, printing
in the key's common-wrong-answers block:

- problem 1 — 36, the index started at 0;
- problem 2 — 15, the fencepost error (limits subtracted without adding one);
- problem 3 — 140, the summand shifted while the upper limit stayed put (the planted
  result the student must diagnose);
- problem 4 — 2, the $n=1$ term used as $a$ although the sum starts at $n=0$;
- problem 7 — 3, the sum of the series that starts at $n=0$ rather than $n=2$;
- problem 8 — 6084, the same unshifted-limit error as problem 3 at larger scale.

Problems 3 and 5 are the two requested explicit find-and-fix items; problem 6 is a third
in critique form.

Standards: sums and series are tagged `HSF-BF.A.2, HSF-LE.A.2` and the sequence-limit
problem `LIM-1, LIM-2`, both taken verbatim from `references/standards-map.md`.

## Gate chain

`BUILD PASSED` (exit 2 — two manual-review items, which is the correct encoding for a
divergence argument and a "why doesn't this prove it" explanation). One gate failed on the
first attempt and was fixed: `template-ss` rejected a `\skillheading` of 59 characters
against its 57-character budget; the heading was shortened and everything after it ran
green.

Final run: all 21 gates green, three compiles inside budget (worksheet 4, key 3, guide 2).
Prose consistency reports 22/26 on the worksheet and 29/33 on the study guide; every flag
is an *original* index bound that legitimately disappears under the shift (the 7 in
$\sum_{n=2}^{7}$, the 4 and 12 in $\sum_{n=4}^{12}$) or a printed exponent — exactly the
"story numbers unused by the computation" the checker documents as expected flags, and on
this topic they are the point of the problem rather than drift.
