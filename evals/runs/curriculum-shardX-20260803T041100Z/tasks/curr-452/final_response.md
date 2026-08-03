# One-Sided, Infinite, and End-Behavior Limits (AP Calculus AB / BC)

Three PDFs are ready.

- **Worksheet** (`ws_limits_curr452.pdf`, 4 pages) — 10 problems in a
  procedural-fluency format. The directions box separates the three situations
  the notation hides (pick a side / find a sign / compare degrees) and asks for
  the reasoning line that decides the answer, not just the answer. Problems 1–4
  are the warm-up, one of each kind; after that the four methods are
  interleaved. No skeleton repeats: problem 5 is a piecewise jump, problem 6 is
  an infinite limit whose sign depends entirely on the chosen side, problem 7
  is a radical end-behavior limit where $\sqrt{x^2}$ has to be handled
  explicitly, problem 8 is an $\infty-\infty$ form that must be combined
  before it means anything, problem 9 solves for a constant that makes a
  piecewise function continuous, and the closing challenge asks for three
  limits on one rational function and then a description of its asymptotes.
- **Answer key** (`ak_limits_curr452.pdf`, 3 pages) — a quick-answer bank, then
  a full solution per problem: which side is in force, what sign the small
  factor carries, the division-by-the-highest-power line, and the boxed answer.
  Four problems carry a grading note naming the specific wrong answer a common
  error produces (answering "does not exist" to a one-sided question; getting
  $3/2$ at both ends of problem 7 because the $\sqrt{x^2}=-x$ step was skipped).
- **Study guide** (`ss_limits_curr452.pdf`, 2 pages) — four sections (one-sided,
  infinite, end behavior, piecewise continuity), each with a rule box, a worked
  example whose first line says *why* that method applies, and a try-it with the
  answer printed upside down inside the box. The end-behavior box gives the
  three degree cases and the one safe method underneath all three.

## Verification

13 of the 15 checks are machine-verified with SymPy: 11 `limit` checks (each
carrying its own `dir` for the one-sided ones, and `to: "oo"` / `to: "-oo"` for
the end-behavior ones, so the checker is evaluating the exact limit the stem
asks for, including the $\pm\infty$ results) and 2 `solve` checks for the
continuity constants. Several problems have more than one part and therefore
carry more than one verify entry under the same problem id.

Two items are labelled for manual review, and the key says so at the point of
use:

- problem 5(c) — "explain why the two-sided limit does not exist". The two
  one-sided values it rests on (5 and 7) are machine-checked; the written
  justification is not.
- problem 10(d) — "describe every vertical and horizontal asymptote in words".
  The three limits it rests on are machine-checked; the description is prose.

Both are encoded as `{"type": "manual", ...}` rather than claimed as verified,
which is why the build exits 2. All 8 study-guide items (4 worked examples +
4 try-its) are fully machine-verified, and each of the four worksheet facets
has a matching worked example.

**Standards used:** `LIM-1` for limit evaluation and `LIM-2` for the
continuity and asymptote reasoning, both taken verbatim from
`references/standards-map.md` (row "Limits & continuity").

## Build

Green on the first build — all 21 gates pass, including the per-problem
answer-key binding (13 boxed answers across 10 problem segments) and the page
budget (worksheet 4 pages, key 3, guide 2 against its hard 2-page cap).
