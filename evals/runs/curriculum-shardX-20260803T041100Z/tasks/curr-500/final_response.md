# Taylor Polynomials and Remainder Bounds (AP Calculus BC)

Three PDFs are ready.

- **Worksheet** (`ws_taylor_curr500.pdf`, 6 pages) — 10 problems in an
  interleaved-synthesis format. The directions box states the four things the
  sheet asks the student to discriminate between: building $T_n$ from
  derivative values, building it by substituting into a memorised Maclaurin
  series, bounding the remainder (Lagrange or alternating), and using a
  polynomial to settle a value or a limit. Every answer is required exact, so
  no problem can be finished with a calculator. Problems 1–3 are the warm-up
  (a derivative table, the degree-4 polynomial for $e^x$, the degree-5
  polynomial for $\sin x$); after that the four methods rotate. The set covers
  the composition case ($e^{-x^2}$ by substituting $u = -x^2$ rather than
  differentiating six times), a Lagrange bound where the student must also
  *justify* the choice of $M$, a series evaluation of
  $\lim_{x\to0}(e^x-1-x)/x^2$ with L'Hôpital explicitly ruled out, an
  alternating-series bound for $\cos(2/5)$, a supplied-$M$ Lagrange bound, and a
  three-part synthesis on $\ln(1.1)$ that asks for the estimate, the error
  bound, and the *direction* of the error.
- **Answer key** (`ak_taylor_curr500.pdf`, 6 pages) — the generated
  quick-answer bank, then a full solution per problem with the common-denominator
  arithmetic written out so every exact fraction can be traced. Six problems
  carry a named common wrong answer, and they target the errors that actually
  cost BC points: using the raw derivative values as coefficients (5 instead of
  3.25), using $n$ instead of $n+1$ in the Lagrange bound (1/24 instead of
  1/192, and 0.104 instead of 1/96 — ten times too large), bounding an
  alternating-series error with the last *included* term instead of the first
  *omitted* one, and truncating $e^x$ at $1+x$ so the limit collapses to 0.
  Several solutions add the sanity check a grader wants: $65/24$ against $e$,
  $1367/7500$ against $\ln(1.2)$ with the next term shown to cover the gap, and
  a grader-only confirmation on problem 10 that the true value really does sit
  below the estimate and inside the bound.
- **Study guide** (`ss_taylor_curr500.pdf`, 2 pages) — four sections matching
  the four worksheet skills. Section 2 lists the four Maclaurin series worth
  memorising and warns that substitution changes which *degree* each term
  reaches ($n = 3$ of $e^u$ is already degree 6 when $u = -x^2$). Section 3
  puts both remainder theorems side by side and says where $M$ comes from.
  Every worked example opens with a step naming why that tool applies, and each
  try-it prints its verified answer upside down inside the box.

## Verification

11 of the 13 checks are machine-verified with SymPy: 5 `eval` checks (the
Taylor construction written with explicit `factorial(k)` denominators, and three
Lagrange bounds written as $M|x-c|^{n+1}/(n+1)!$ with $n$ itself bound as a
given, so the checker is exercising the $n+1$ rule rather than a pre-simplified
number), 4 `series` checks (partial sums of $e^x$, $\sin x$ at $1/2$,
$e^{-x^2}$ at $1/2$, and $\ln(1+x)$ at $1/5$ and $1/10$), 1 `limit` check, and
one more `eval` for the alternating bound. Problems 5 and 10 carry more than one
verify entry under one problem id.

Two items are labelled for manual review, and the key says so at the point of
use:

- problem 5(b) — justify that $M = 2$ bounds $\left|f^{(4)}\right|$ on
  $[0, 0.5]$. The bound it feeds (1/192) is machine-checked; the argument is
  written work, and the key notes that $M = e$ or $M = 1.65$ would also earn
  full credit.
- problem 10(c) — decide whether the estimate is an over- or underestimate and
  justify it from the sign of the first omitted term. Parts (a) and (b) are
  machine-checked; the reasoning is prose, and the stem forbids settling it with
  a calculator.

Both are encoded as `{"type": "manual", ...}` rather than claimed as verified,
which is why the build exits 2. All 8 study-guide items (4 worked examples +
4 try-its) are fully machine-verified, and each of the four worksheet facets has
a matching worked example.

Six misconception traps are declared and machine-proved distinguishable from the
correct answers.

**Standards used:** `LIM-7` for constructing polynomials and series and `LIM-8`
for the remainder bounds, both taken verbatim from the "Series (BC) | LIM-7,
LIM-8" row of `references/standards-map.md`.

## Build

All 21 gates green on the fourth attempt (exit 2 for the two declared manual
items). Three failures, all real:

1. `verify-ws` rejected `M` as a variable name. The allowlist is
   **lowercase only** (`a b c d f g h j k l m n p phi q r s t theta u v w x y z`),
   so the conventional Lagrange bound `M` has to be written `m` in the JSON —
   the printed documents still say $M$, which is what the student reads.
2. `verify-ws` rejected a trap whose declared `value` was `0.00000416667`, with
   a message saying the printed number "does not match" an expr that computes to
   exactly the same thing. I traced it: `rounds_to()` derives the comparison
   precision from `repr(value)`, and for magnitudes below $10^{-4}$ Python's
   repr switches to scientific notation (`4.16667e-06`), so the decimal count is
   read off `"16667e-06"` and the comparison is made at the wrong place. **This
   is a checker bug, tested directly, not inferred** — the same trap with a
   value above $10^{-4}$ (`0.00106667` on problem 7) passes. Workaround: omit
   the optional `value` on a trap whose result is smaller than $10^{-4}$; the
   trap is still machine-proved distinguishable.
3. `compile-ss` ran the study guide to 3 pages twice. Only the final try-it box
   spilled, so roughly 60pt had to come out of page 2; it came from tightening
   the intro line and three formula-box paragraphs, with no box dropped. Worth
   recording for the brief: this guide has **no** watch-out boxes at all — the
   "(!)" warnings live inside the formula boxes — and four sections still
   overran, because two of the four formula boxes carry displayed math (the
   Taylor sum and the Lagrange fraction) and the four memorised series in
   section 2 run three lines on their own.

Page counts: worksheet 6 (budget 7), answer key 6 (budget 7), study guide 2
against its hard 2-page cap.
