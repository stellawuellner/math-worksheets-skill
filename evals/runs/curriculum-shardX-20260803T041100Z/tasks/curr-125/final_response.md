# Ordering Fractions and Mixed Numbers — Grades 4–5

Three PDFs, all gated green:

- **Worksheet** (`ws_orderfractions_curr125.pdf`, 5 pages) — 12 problems.
  Numbers arrive in three different forms (proper fractions, fractions greater
  than one, mixed numbers), so every problem forces a decision about *which*
  form to convert to and *which* comparison test to reach for. A value-free
  benchmark number line sits with the directions as a shared reference, labelled
  in words so it can never be mistaken for a problem's givens.
- **Answer key** (`ak_orderfractions_curr125.pdf`, 3 pages) — every problem
  worked in numbered steps. Step 1 always names the *reason* a method was
  chosen (benchmark ties, denominators share a factor, whole parts equal), not
  just the arithmetic. Problem 5 also shows the common-denominator cross-check.
- **Study guide** (`ss_orderfractions_curr125.pdf`, 2 pages) — three sections:
  equivalent forms, comparing a pair (a stop-at-the-first-test ladder:
  benchmark → gap to one → matching tops/bottoms → common denominator), and
  ordering a whole set. Each has a rule box, a worked example, and a distinct
  try-it with the answer printed upside down. A watch-out box covers the two
  classic errors (bigger denominator read as bigger number; comparing numerators
  across unlike denominators).

## What the sheet actually exercises

| Facet | Problems |
|---|---|
| `equivalent-forms` (rewrite so a comparison becomes possible) | 1, 2, 6, 9 |
| `compare-a-pair` (benchmark or common denominator) | 3, 5, 8, 11 |
| `order-a-set` (three or four numbers, mixed representations) | 4, 7, 10, 12 |

Perfectly interleaved after the two-problem warm-up: max same-facet run = 1.
Difficulty ramp `1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 5`. The method-choice design
is deliberate — problem 3 is settled by the half benchmark alone, problem 5 by
the gap-to-one argument, and problem 8 defeats both (5/9 and 4/7 are both just
above a half) so only a common denominator works. Problem 12 is the synthesis:
four numbers in three forms, with the student asked to state the common form
they converted into.

## Verification

- **12 of 12 worksheet problems machine-verified** — 4 `equiv` (the rewriting
  problems) and 8 `compare` (4 pairwise relations, 4 full orderings, checked as
  sorted lists, not just as a relation symbol). **0 manual.**
- **6 of 6 study-guide boxes machine-verified** (3 worked examples + 3 try-its).
- Prose–JSON number binding is 53/53 (100%) on the worksheet: every numeral a
  student reads is a value the verifier actually used.
- Standard tagged on every problem: `3.NF.A / 4.NF.A`. Note that
  `references/standards-map.md` writes the fraction-equivalence row as that
  combined string, so it is used verbatim rather than trimmed to the task's
  `4.NF.A`.

Nothing here is open-ended, so nothing is flagged for manual review.

**First-attempt gate failure (one):** `template-ss` rejected a `\skillheading`
of 63 characters against the 57-character budget. Shortened the section-2
heading; everything else passed on the next run.
