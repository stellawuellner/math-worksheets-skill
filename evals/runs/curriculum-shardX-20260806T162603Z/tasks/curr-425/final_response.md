# Identities, multiple angles and exact solution sets (Precalculus)

Three PDFs are ready.

**Study guide (`ss_identities_curr425.pdf`, 2 pages)** — four sections, each a
rule box, a worked example whose first step names why that tool is the right one,
and a try-it with the answer upside down inside the box: Pythagorean identities,
sum and difference formulas (with the sign flip on cosine called out), the three
forms of $\cos 2\theta$ and how to choose between them, and exact solution sets —
including the count check that a value strictly inside $[-1,1]$ gives two angles
per turn while $\pm 1$ gives one.

**Worksheet (`ws_identities_curr425.pdf`, 6 pages)** — 12 problems. The first two
are a warm-up; after that the four subskills interleave with no run longer than
one, so the student must decide which identity the problem needs before starting.
All answers are exact — radicals and fractions, never decimals. The set ends with
a synthesis challenge: rewrite $\cos 2\theta + 3\sin\theta = 2$ with a
double-angle formula, factor the resulting quadratic, solve it, and account for
why the solution set has three members rather than four.

**Answer key (`ak_identities_curr425.pdf`, 4 pages)** — worked solutions with the
choice of formula justified (for instance, *which* form of $\cos 2\theta$ and
why), a Quick Answers bank, and a Curriculum section for HSF-TF.C.8.

## What is verified, honestly

The sheet asks for **15 responses across the 12 problems**.

- **13 are machine-checked** by SymPy. The four simplification problems are
  checked as **identities in $\theta$** — equivalence as functions, not agreement
  at a sample angle — which is the only check that means anything for an identity.
  The exact values ($\cos 15^\circ$, $\tan 15^\circ$, $\cos 105^\circ$,
  $\sin 2\theta$) are checked as exact symbolic values, so a decimal
  approximation would not satisfy them. Every solution set is checked for
  *completeness* on its interval.
- **2 are instructor-judged** and marked `---` in the Quick Answers bank:
  problem 11(b), the written proof of the identity, and problem 12(c), the
  explanation of the solution count. A proof is prose and a computer algebra
  system cannot grade its structure — notably, it cannot tell a one-sided proof
  from a both-sides manipulation, which is the thing worth grading here. The key
  prints a step-by-step rubric for 11(b) that names each move a full-credit proof
  must contain, and says explicitly that a check at one angle is not a proof.

That is the split the key's own "What is verified" note reports. Nothing is
marked `[unchecked]`.
