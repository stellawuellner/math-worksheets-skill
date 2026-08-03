# Evaluating Perfect Square Roots and Cube Roots — Grade 8 / Pre-Algebra

Three PDFs are ready:

- **Study guide** (`ss_roots_curr202.pdf`, 2 pages) — read this first.
- **Worksheet** (`ws_roots_curr202.pdf`, 6 pages, 12 problems).
- **Answer key** (`ak_roots_curr202.pdf`, 3 pages) — every root worked, with the factor pair or triple shown.

## What the worksheet does

The sheet holds one question steady — *what number, used two (or three) times as
a factor, gives this?* — and rotates through four ways of asking it, so the
student picks the method each time rather than repeating one procedure:

- **Perfect square roots** (1, 3, 7): $\sqrt{144}$ straight from the table, then
  $\sqrt{225}$, which is past most memorised tables and wants factoring
  ($225 = 9 \times 25$), then a square patio of area 169 sq ft where the root
  carries a unit.
- **Perfect cube roots** (2, 6, 11): $\sqrt[3]{27}$, $\sqrt[3]{343}$, and a cube
  of volume 216 cm³. Each one asks the student to say why the *index* picks the
  table — problem 2 explicitly asks why the answer is not 9.
- **Roots of fractions and decimals** (4, 8, 10): the root distributes over a
  quotient, so $\sqrt{49/64}$, $\sqrt[3]{8/125}$, and $\sqrt{0.36}$ (rewritten
  as $36/100$) are all exact, no calculator and no rounding.
- **Estimating a root that is not perfect** (5, 9, 12): bracketing $\sqrt{60}$
  between 7 and 8, deciding whether $\sqrt{50}$ or $7.1$ is larger by squaring
  both, and finally $\sqrt[3]{100}$ — which also breaks the belief that a cube
  root should be bigger than a square root.

A value-free table of squares and cubes prints with the directions as the shared
reference; no problem carries its own figure. Difficulty ramps 1 → 5 and the
four facets are fully interleaved.

## What was verified

**All 12 problems were machine-verified with SymPy** — nothing is flagged for
manual review, and every boxed answer in the key was bound back to the
recomputed value at its printed precision. The two problems whose answers carry
units (13 ft, 6 cm) were checked in both directions: the declared unit has a
matching answer line on the sheet, and the key prints the same unit inside the
box.

Eight misconception traps were declared and machine-checked as distinguishably
wrong. They print in the key's "Common wrong answers" block, so a wrong paper
names its own error:

- halving the radicand instead of rooting it (72 for $\sqrt{144}$, 30 for $\sqrt{60}$),
- dividing by 3 instead of cube-rooting (9 for $\sqrt[3]{27}$, 33.3 for $\sqrt[3]{100}$),
- using the square root where the cube root was asked (18.5 for $\sqrt[3]{343}$, 14.7 for the 216 cm³ cube),
- rooting the numerator only ($0.016$ for $\sqrt[3]{8/125}$),
- shifting the decimal point instead of rooting ($0.06$ for $\sqrt{0.36}$).

Three problems also ask for a sentence of reasoning (why a rounded root is not
equal to the root, why volume calls for a cube root, whether $\sqrt[3]{100} >
\sqrt{100}$). Those are teaching prose, not separate answers — the key gives a
model response and says what to accept, and every answer line carries a
machine-checked value.

## Standards

Codes come verbatim from `references/standards-map.md`: `8.EE.A` (exponents,
scientific notation, square/cube roots) on the nine evaluation problems, and
`8.NS.A` (rational vs irrational numbers, roots) on the three that estimate or
compare a non-perfect root. Every problem also carries a difficulty, a Bloom
level, a skill, and a facet, and the declared subtitle is bound to the
worksheet's title block.

## Study guide

Two pages, four sections matching the four facets, opening with both reference
lists and the statement that the index counts equal factors. Each section has a
rule box, a worked example whose first step says *why* that method applies, and
a try-it with the answer printed upside down inside the box. The closing
watch-out names the two errors that produce most lost marks: treating a root as
a division, and reading the radicand before the index (64 is in both lists —
$\sqrt{64} = 8$, $\sqrt[3]{64} = 4$).

## Gate chain

`build.sh` finished **BUILD PASSED — all gates green** (exit 0) on the first
build: template shells, both verification files, skill and facet coverage,
subtitle binding, layout and work space, answer-unit binding, three compiles
inside their page budgets (6 / 3 / 2 pages), per-problem answer-key binding,
study-guide structure, and prose consistency. No gate failed. The worksheet sits
at 6 pages because each problem is given 4.5–6 cm of work space; that was not
compressed to save paper.
