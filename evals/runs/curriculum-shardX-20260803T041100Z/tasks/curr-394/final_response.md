Three PDFs are ready for an Algebra 2 student on sequences, series and the
binomial theorem, focused on diagnosing index, common-ratio and convergence
errors.

- **Worksheet** (8 problems, `ws_seqseries_curr394.pdf`, 5 pages) — six of the
  eight problems are find-and-fix items, each carrying one of the three named
  errors. Index: Dev writes a₁₂ = 7 + 12(4) = 55 (one step too many); Ines sums
  ten terms but computes the last term as a₁ + nd and gets 280 instead of 255;
  a student solves 7 + 4n = 91 and lands on a *plausible whole number*, which is
  why that error survives. Ratio: Kai subtracts consecutive terms of 5, 10, 20
  and calls the result the common ratio, and part (b) makes the student confirm
  the ratio on a second pair — one pair is consistent with both an arithmetic and
  a geometric rule. Convergence: Nia divides by r instead of 1 − r and gets 8
  instead of 24, after first being made to state *why* the series converges at
  all. Problem 7 is the binomial index trap: Vic sets k to the exponent on x, and
  because C(5,2) = C(5,3) = 10 the binomial coefficient does not reveal his error
  — only the power of 3 does. Problem 8 is an open explanation of the |r| < 1
  condition. Work space runs 5–7 cm.
- **Answer key** (`ak_seqseries_curr394.pdf`) — three to five numbered steps per
  problem, each opening by naming the slip in words, then the corrected work, then
  the boxed answer, then an independent check: the n = 1 test that exposes an
  index error in one line, the second sum formula for the series, partial sums
  climbing toward 24, and the exponent-pair check on every binomial term. It
  carries the generated quick-answer bank and the generated "Common wrong
  answers" block (55, 5, 280, 8, 90), plus a full model answer and a full-credit
  checklist for the open item.
- **Study guide** (2 pages, `ss_seqseries_curr394.pdf`) — three skills matching
  the worksheet tags: count steps rather than terms (with the n = 1 test as the
  self-check), ratios divide and only some sums exist, and which k a binomial term
  wants. Each has a rule box, a two-step worked example and an upside-down try-it,
  plus a watch-out box on why an off-by-one index produces a plausible number.

**Verification.** 7 of the 8 worksheet problems are machine-checked with SymPy —
two `eval` term computations, a finite `series` sum, an `expand` of (x+2)⁴, an
infinite `series` sum, a `solve` for the index, and an `eval` binomial
coefficient. Problem 2 carries *two* entries under one id so both ratio checks
(10/5 and 20/10) are verified, which is the point the problem is making. All 6
study-guide results are machine-checked. Problem 8 is a genuinely open
explanation and is declared `{"type": "manual"}`; the build correctly exits 2 with
one manual-review item and the problem is nowhere described as machine-verified.

Five planted wrong results are declared misconception traps (55, 5, 280, 8, 90);
the verifier proved each one distinguishably wrong and derived from the stated
wrong method rather than typed by hand.

**Standards.** Sequence and series problems are tagged
`HSF-BF.A.2, HSF-LE.A.2` and the two binomial problems `HSA-APR.C.5`, both copied
verbatim from `references/standards-map.md` ("Sequences & series
(explicit/recursive)" and "Binomial theorem & Pascal's triangle"). Together they
cover the task's `HSF-BF / HSA-APR.C` reference; no code was invented.

**Gate-log note.** Worksheet prose matches 25 of 27 numbers; the two flags are the
"1" and "2" in problem 8's *hypothetical* series (|r| < 1, ratio 2), which is
prose about a scenario with no computation attached. The study guide's flags
(57, 14, 34, 4, 10) are all intermediate values written inside worked examples.
No computed value or figure label is unbound.
