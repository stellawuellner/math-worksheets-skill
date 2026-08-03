Three PDFs are ready for a high-school geometry student on triangle similarity and
proportional reasoning, focused on diagnosing **reversed correspondence** (pairing
a side with the wrong partner) and **reversed scale factors** (using large-over-
small where small-over-large belongs, or scaling an area by the side ratio).

- **Worksheet** (6 problems, `ws_similarity_curr319.pdf`) — a value-free reference
  figure with the directions shows how a similar pair is named, then: a warm-up
  that asks for the matching pairs before the proportion; Kai's proportion whose
  two ratios run in opposite directions; a deliberately scrambled statement
  (△ABC ~ △FED) where Rho pairs correctly but multiplies by the reciprocal factor;
  Rae scaling an area by 8/5 instead of (8/5)²; Ines pairing the flagpole's shadow
  with the person's height in a shadow problem; and a challenge in which Tomas's
  33.33 must be rejected on size grounds before any arithmetic is checked. Four of
  the six are explicit find-and-fix items. Work space is 5–7 cm, declared with
  `workspace_cm`.
- **Answer key** (`ak_similarity_curr319.pdf`) — four to six numbered steps per
  problem. Every solution states the correspondence, then *decides which triangle
  is larger and predicts the direction of the answer*, then computes, then checks
  the proportion and the predicted direction. The diagnosis sections say exactly
  which two lengths the student paired and why the resulting number was impossible
  (Kai's 9.33 shrinks a side of the larger triangle; Ines's 17.6 ft is three times
  the person's height while the shadow is 5.5 times as long). It carries the
  generated quick-answer bank and a "Common wrong answers" block (9.33, 13.5, 80,
  17.6, 33.33), plus a full-credit checklist for the open parts.
- **Study guide** (2 pages, `ss_similarity_curr319.pdf`) — three skills matching
  the worksheet tags: reading the correspondence from the statement, pointing the
  scale factor the right way (going-to over coming-from, with a prediction), and
  scaling an area by k². Each has a rule box, a two-step worked example and an
  upside-down try-it, plus a watch-out box on why re-doing the arithmetic can
  never catch either error.

**Verification.** Problems 1–5 and part (c) of problem 6 are machine-checked with
SymPy (one `solve` proportion and five `approx` computations); all 6 study-guide
results are machine-checked. Parts (a) and (b) of problem 6 ask for explanations,
so a second entry on problem 6 is declared `{"type": "manual"}` and the build
correctly exits 2 with one manual-review item — the explanation is nowhere
described as machine-verified. Five planted wrong answers (9.33, 13.5, 80, 17.6,
33.33) are declared misconception traps; the verifier proved each is
distinguishably wrong and really is what the reversed method computes. Givens were
chosen so a reversed factor lands far from the truth (33.33 vs 12) rather than on
a near miss.

**No numbered figures, on purpose.** The skill requires triangle figures to come
from `scripts/render_figures.py`, which covers right triangles and `triangle`-type
problems; these are general similar pairs verified as `solve`/`approx`, which the
renderer does not draw, and hand-built TikZ carrying values is explicitly banned.
The sheet therefore uses one **value-free** reference figure with the directions
(allowed, and placed before the first problem), and states every length in the
problem text.

Standards: every problem is tagged `HSG-SRT.A.1–A.3, HSG-SRT.B.4–B.5`, copied
verbatim from `references/standards-map.md`.

**Build note.** The first build failed one gate — `compile-ak`, an overfull hbox
of 19.6 pt caused by an inline `\dfrac` whose numerator and denominator were
sentences ("side of the triangle you are going TO" over "matching side ... coming
FROM"). Rewritten as a displayed equation with short labels; the rerun is fully
green.
