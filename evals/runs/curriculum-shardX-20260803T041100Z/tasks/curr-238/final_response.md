# Using Dilations to Reason About Similarity — three PDFs

**Worksheet** (`ws_dilations_curr238.pdf`, 10 problems, ~4 pages). Every problem
uses a dilation to reason about similarity (10 of 10 on the requested focus).
Five planned facets, declared in the JSON and interleaved after the warm-up
(longest same-facet run: 3):

1. image of $P(3,5)$ under $k=2$ about the origin — each coordinate separately
2. image of $Q(8,-6)$ under $k=0.5$, and enlargement vs reduction
3. three parts: $AB$ and $A'B'$ by the distance formula (10 and 15 units), then $k$ from the two lengths
4. slope of a ramp segment and of its image under $k=3$ — the equal-slope evidence
5. **open justification** (manual): why the dilated triangle must be similar — what happens to the three side lengths and the three angle measures
6. photo enlargement: 4 cm by 6 cm, the 6 cm side becomes 15 cm
7. dilation centred at $(1,1)$, not the origin, using $(h+k(x-h),\ m+k(y-m))$
8. similar sails: $k$ from 6 cm → 9 cm, then the side matching 8 cm
9. three parts: areas of a rectangle and its image under $k=2$, then the area ratio and its link to $k^2$
10. scale drawing of a school yard: $k = 21/6$, then the real flagpole height

Difficulty ramps 1 → 5. Multi-part problems carry a separate answer blank per
part, and seven blanks are unit-tagged (units, cm, square units, m) against the
JSON's `answer_unit`.

**Answer key** (`ak_dilations_curr238.pdf`). Each solution states the reason
before the arithmetic (measure from the centre; image over original, in that
order; both dimensions scale so area scales twice), and checks the result by a
second route — ratio reduction ($9{:}12 = 6{:}8$) or back-substitution. Problem
5's entry is a model argument with explicit grading guidance. The generated
quick-answer bank prints the three declared traps: 0.67 (ratio inverted), 9
(dilated about the origin when the centre was $(1,1)$), 2.29 (upside-down
ratio on the scale drawing).

**Study guide** (`ss_dilations_curr238.pdf`, 2 pages). Four skill sections —
coordinates of a dilated point, scale factor from two lengths, slope under a
dilation, similar figures (sides and area) — with five worked example/try-it
pairs, so the area-ratio facet gets its own worked example inside the similarity
section.

## Verification

Of the 21 worksheet verification entries, **20 are machine-verified** with SymPy
(eval, distance, slope, polygon_area) and **1 is `manual`** — problem 5 is an
open "explain why" justification, which is not CAS-checkable and is labelled as
such; the build exits 2 with that item listed, which is the correct outcome, not
a failure. All 10 study-guide results are machine-verified. The three declared
traps were proved distinguishably wrong. Every other gate is green, including
facet coverage, subtitle binding, per-problem answer binding, and unit binding.

Standard: `8.G.A` from `references/standards-map.md`, exactly the code the task's
`standard_refs` names.
