# Rational and Irrational Numbers — Grade 8 / Pre-Algebra

Three PDFs are ready:

- **Study guide** (`ss_irrational_curr201.pdf`, 2 pages) — read this first.
- **Worksheet** (`ws_irrational_curr201.pdf`, 4 pages, 10 problems).
- **Answer key** (`ak_irrational_curr201.pdf`, 3 pages) — full reasoning for every problem.

## What the worksheet does

All ten problems ask the same underlying question — *can this number be written
as a ratio of two integers?* — approached four ways, and the sheet rotates
between them so the student has to pick the right test each time rather than
repeating one procedure:

- **perfect-square roots** (problems 1, 2, 9): the root is exact, so the number
  is rational — including $\sqrt{9/16}$, where the rule applies to numerator and
  denominator separately.
- **non-perfect roots** (4, 7, 10): trap the root between two perfect squares,
  then round. Problem 10 is the closer: $\sqrt 8 \cdot \sqrt 2 = 4$, a
  counterexample to "the product of two irrationals is always irrational".
- **decimals and fractions** (3, 6): a terminating decimal and a repeating one,
  each converted to a fraction to *prove* rationality rather than assert it.
- **comparing and ordering** (5, 8): ordering a root against a decimal and a
  fraction, and deciding whether $\sqrt2 = 1.41$ (it does not — problem 8 makes
  the difference between a number and its rounded stand-in explicit).

Two models tie the notation to something concrete: a perfect-square table printed
with the directions, which every root problem refers back to, and a decimal /
fraction / lowest-terms conversion table the student completes in problem 3.
Difficulty ramps 1 to 4; the facet plan is declared in the verify JSON and bound
to the sheet's subtitle.

## What was verified

**All 10 problems were machine-verified with SymPy** — nothing on this sheet is
flagged for manual review, and every printed answer in the key was bound back to
the recomputed value at its printed precision. Two misconception traps were
declared and machine-checked (dividing the radicand by 2 instead of taking its
root); both were proved distinguishably wrong, and they print in the key's
"Common wrong answers" block so a wrong paper tells you which error was made.

The short written explanations the sheet also asks for (why a repeating decimal
is still rational, what $1.41$ really is, what problem 10 shows) are teaching
prose, not separate answers — the key gives a model response for each, and the
value on every answer line is the machine-checked one.

## One deliberate omission

No Common Core code is tagged on these problems. The repository's
`references/standards-map.md` has no entry covering grade-8 irrational numbers
and roots, and the rule is to use that file verbatim and never invent a code, so
the field was left off rather than filled with an unrelated or made-up one.
Everything else — difficulty, Bloom level, skill and facet — is tagged.

## Study guide

Opens with the single definition and a two-column "always rational / irrational"
summary, then four sections matching the worksheet's four facets. Each has a rule
box, a worked example whose first step says *why* that method is the right one,
and a try-it with the answer printed upside down inside the box. It closes with
the two warnings that cause most of the lost marks: a radical sign does not make
a number irrational, and a calculator display is not proof.

## Gate chain

`build.sh` finished **BUILD PASSED — all gates green** (exit 0): template shells,
both verification files, skill and facet coverage, subtitle binding, layout and
work space, three compiles inside their page budgets, per-problem answer-key
binding, study-guide structure, and prose consistency.

One gate failed on the first attempt: the answer key overran a line
(`Overfull \hbox`) where the generated quick-answer bank's "common wrong answers"
text met the rule below it. It was fixed by letting that generated block set
ragged-right; nothing about the answers changed.
