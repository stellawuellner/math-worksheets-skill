# Integer Exponent Laws: Product and Quotient (Grade 8 / Pre-Algebra)

Three PDFs: the student worksheet (10 problems, 4 pages), a step-by-step answer
key, and a two-page study guide.

## The model the sheet runs on

A power is a *count of equal factors*. The worksheet opens with an
expanded-form table ($2^3 \cdot 2^4$ shown as three factors set beside four),
and every law on the page is then bookkeeping on that count rather than a rule
to memorise. Problems 1, 3 and 7 explicitly ask for the expansion before the
law.

## What the worksheet asks

- **1, 2, 5, 10** — product of powers. Problem 1 expands and counts; problem 5
  simplifies $a^3 \cdot a^2$ then evaluates at $a=2$; problem 10 is error
  analysis on the classic multiply-the-exponents mistake.
- **3, 4, 6, 9** — quotient of powers. Problem 6 adds a coefficient
  ($12x^5 / 4x^2$) so the student separates coefficient division from exponent
  subtraction. Problem 9 asks which of $3^4 \cdot 3^2$ and $3^7/3^1$ is larger —
  they are equal, which only shows up if both sides are simplified first.
- **7, 8** — where zero and negative exponents come from. Problem 7 reads
  $6^4/6^4$ two ways and forces $6^0 = 1$; problem 8 subtracts to a negative
  exponent and rewrites it as a fraction.

Difficulty ramps 1, 2, 2, 2, 3, 3, 3, 3, 4, 4; facets interleave after the
warm-up (longest same-facet run is 2).

## Verification

All 10 problems machine-checked — **10 verified, 0 manual**. `equiv` proves the
simplified form is the same function as the original (so $4^2/4^5$ really is
$4^{-3}$), `eval` recomputes the two numerical answers, and `compare` checks the
relation symbol in problem 9 — a relation answer is bound explicitly, so a key
printing $>$ against a verified $=$ could not pass.

**Two misconception traps are declared and verified distinguishable:**

- P5: multiplying the exponents gives $2^6 = 64$ instead of $2^5 = 32$
- P10: multiplying the exponents gives $2^{15} = 32768$ instead of $2^8 = 256$
  (the number printed in the stem is derived from the trap expression)

Both are printed in the answer key's common-wrong-answers block, so a grader
seeing 64 or 32768 knows immediately which law the student mis-applied.

`BUILD PASSED — all gates green`.

## Study guide (2 pages)

An opening box stating the counting idea, then one section per skill — product
of powers, quotient of powers, zero and negative exponents — each with the rule
plus a one-line reason, a worked example that opens with a strategy sentence,
and a try-it whose answer is printed upside down inside the box. The watch-out
box flags the two errors this topic reliably produces.

## Notes

- Standard `8.EE.A.1, 8.EE.A.4` used verbatim from
  `references/standards-map.md` (row "Exponents & scientific notation"); it is
  also exactly the code pair the curriculum task names.
- The two remaining prose flags are the literal $0$ in "$6^0$" and the value
  $1/25$ shown as a check in a study-guide example — both derived, neither a
  drift between the sheet and the verified data.
