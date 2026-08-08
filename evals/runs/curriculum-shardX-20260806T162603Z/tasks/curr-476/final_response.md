# Substitution in Integrals — three PDFs

**Course:** AP Calculus AB/BC · **Topic:** substitution, parts, partial
fractions and improper integrals, focused on using u-substitution in indefinite
and definite integrals · **8 problems**

## What you get

- **`ws_usub_curr476.pdf` — the student worksheet.**
  The model is a **three-row substitution table** — inner function,
  differential, integral rewritten in $u$ — and problem 1 shows it filled in as
  scaffolding before the student builds their own. Every problem after that is
  the same table with more of it left blank, which is what most substitution
  errors turn out to be: bookkeeping, not calculus. The definite-integral
  problems (3, 5, 7) ask for the converted $u$-limits as their own answers
  before the value, so limit conversion becomes a visible step rather than a
  silent one. Problem 8 finishes with an improper integral, where the
  substitution is followed by a limit.
- **`ak_usub_curr476.pdf` — the full answer key.**
  Every problem restated and worked, with the substitution table's three moves
  written out. It opens with a generated Quick Answers bank, a "What is
  verified" note, and a Curriculum block listing the AP codes.
- **`ss_usub_curr476.pdf` — the study guide (2 pages).**
  Three sections: spotting the inner function, finishing an *indefinite*
  integral (convert back to $x$, add $+C$), and finishing a *definite* one
  (convert the limits, then stop). Each has a rule box, a worked example whose
  first step says why substitution is the tool here, and a try-it with its
  answer printed upside down.

## Verification, stated honestly

The eight problems ask for **15 responses**.

- **13 of 15 are machine-checked** with SymPy. Antiderivatives are checked by
  differentiating them back to the integrand — so a missing $\tfrac{1}{2}$ or a
  wrong power cannot pass — and every definite integral, every converted
  $u$-limit, and the improper integral's limit are recomputed exactly.
- **2 of 15 are instructor-judged**: 6(b), why the $1/x$ in the integrand is
  what makes $u = \ln x$ work, and 8(c), what the limit says about the area
  under an unbounded region. They print as `---` in the Quick Answers bank, and
  the key states what a correct answer must contain — for 6(b) the
  $du = dx/x$ step, for 8(c) the word *converges* or an equivalent.

The study guide's six results are all machine-checked.

## Suggested order

Study guide first, then the worksheet, then the answer key.
