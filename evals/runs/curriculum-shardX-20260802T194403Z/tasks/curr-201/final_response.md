# Rational and Irrational Numbers — Grade 8 / Pre-Algebra

Three PDFs are ready:

- **Study guide** — `ss_irrational_curr201.pdf` (2 pages) — read this first.
- **Worksheet** — `ws_irrational_curr201.pdf` (4 pages, **10 problems**).
- **Answer key** — `ak_irrational_curr201.pdf` (3 pages), full reasoning per problem.

## What the worksheet does

All ten problems ask one underlying question — *can this number be written as a
ratio of two integers?* — approached four ways, rotating between them so the
student has to choose the right test rather than repeat one procedure:

- **perfect-square roots** (1, 4, 9): the root is exact, so the number is
  rational — including $\sqrt{25/36}$, where the rule applies to numerator and
  denominator separately.
- **non-perfect roots** (3, 7, 10): trap the root between two perfect squares,
  then round. Problem 10 is the closer: $\sqrt{12}\cdot\sqrt{3}=6$, a
  counterexample to "the product of two irrationals is always irrational".
- **decimals and fractions** (2, 6): a terminating decimal and a repeating one,
  each converted to a fraction to *prove* rationality rather than assert it.
- **comparing and ordering** (5, 8): ordering a root against a decimal and a
  fraction, and deciding whether $\sqrt3 = 1.73$ (it does not).

Two models tie notation to something concrete: a perfect-square table (to
$15^2$) printed with the directions and referenced by every root problem, and a
decimal / fraction / lowest-terms conversion table the student completes in
problem 2. Difficulty ramps 1 to 4; the facet plan is declared in the verify JSON
and bound to the sheet's subtitle.

## What was verified

**All 10 problems machine-verified with SymPy** — nothing is flagged manual, and
every printed answer in the key binds back to its own problem's recomputed value
at the printed precision. Two misconception traps are declared and machine-checked
(halving the radicand instead of taking its root: 10 for $\sqrt{20}$, 20 for
$\sqrt{40}$); both were proved distinguishably wrong and print in the key's
"Common wrong answers" block. All 8 study-guide boxes are verified as well.

## Standards

**Every one of the 10 problems is tagged `8.NS.A`**, taken verbatim from
`references/standards-map.md` ("Rational vs irrational numbers, roots"). The
study-guide entries carry the same code. Nothing was invented and nothing is
untagged.

## Study guide

Opens with the single definition and a two-column "always rational / irrational"
summary, then four sections matching the worksheet's four facets. Each has a rule
box, a worked example whose first step says *why* that method applies, and a
try-it with the answer printed upside down inside the box. It closes with the two
warnings that cost the most marks: a radical sign does not make a number
irrational, and a calculator display is not proof.

## Gate chain

`build.sh` finished **BUILD PASSED — all gates green** (exit 0). The answer key
`\input`s the generated quick-answer bank directly under `\aktitleblock` with **no
`\raggedright` and no `\emergencystretch`**; both trap lines set cleanly and the
key compiles at 3 pages with no overfull box.

One gate failed on the first attempt, and it is worth flagging: `answer-key-ak`
(then `answer-key-ss`) rejected boxed ordering answers written as
`\dfrac{\,16}{5}`, `\dfrac{\,11}{4}`, `\dfrac{\,7}{4}` — the number normalizer
did not recover 3.2 / 2.75 / 1.75 from that form. `evals/AUTHORING.md` currently
recommends exactly that form ("`\dfrac` with a leading `\,` is safe") as the way
to avoid a two-digit-numerator `\tfrac`. In this build the opposite held:
`\tfrac{16}{5}` and `\tfrac{11}{4}` bound correctly and the `\dfrac{\,...}` form
did not. Nothing else changed.
