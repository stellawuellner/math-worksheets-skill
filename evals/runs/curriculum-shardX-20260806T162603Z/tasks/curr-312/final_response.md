# Completing Two-Column Triangle-Congruence Proofs — high-school geometry (10 problems)

Three PDFs are ready:

- **Worksheet** (`ws_congruence_proofs_curr312.pdf`, 10 pages) — 10 two-column proofs on a
  clean fluency ramp. It starts with the statement column printed and the reason column
  blank, moves to the reverse (reasons printed, statements blank — which forces the student
  to read a criterion backwards), and finishes with proofs the student completes and then
  uses CPCTC to compute from. No two problems share a skeleton: the set covers SSS with a
  shared diagonal, SAS from vertical angles, ASA, HL, SSS from a midpoint, AAS from
  parallel segments, and a final proof written from scratch. Each problem has its own marked
  figure, its own proof table, and room to work; that is why it runs to a page per problem.
- **Answer key** (`ak_congruence_proofs_curr312.pdf`, 3 pages) — every reason and every
  statement supplied, with a note on each proof explaining *why* that criterion and not a
  neighbouring one (why SAS and not SSA, why AAS and not ASA, why the right-triangle line
  is not optional before citing HL). Each computation is worked with a substitution check.
- **Study guide** (`ss_congruence_proofs_curr312.pdf`, 2 pages) — three sections: supplying
  the reason for a line (including the two reasons no tick mark ever shows), supplying the
  statement for a reason (read the criterion backwards to get the pattern), and finishing
  with CPCTC. Rule box, worked example, and try-it in each.

## What is verified, and what is not

**8 of the 18 responses are machine-checked with SymPy** — every computation the proofs
lead to: $x = 5$ and $BC = 17$ cm, $x = 12$ and $m\angle C = 39^\circ$, $x = 11$ and
$m\angle B = 59^\circ$, $x = 10$ and $BC = 27$ cm. All six study-guide answers are verified
the same way. The key's "What is verified" note reports that no problem is fully
machine-checked, and that is correct: every one of the ten carries a written proof
component as well.

**10 responses are flagged for your judgement** — the proof content of all ten problems: the
reason columns of 1, 2, 6 and 9, the statement columns of 4 and 7, the criterion-naming
parts of 3, 5 and 8, and the full proof in 10(a). A two-column proof is a chain of
justifications, which is exactly what a computer algebra system cannot grade. The answer
key gives every reason and statement, plus a grading note naming the element that must be
present — the reflexive property named rather than "it's the same side"; the criterion named
rather than the conclusion restated; the included-side condition checked before ASA is
claimed. The Quick Answers bank marks these `---`. No `[unchecked]` marks appear.

## Notes

Standards: HSG-CO.B (the congruence criteria) on eight problems, HSG-CO.C on the two that
lean on the vertical-angle and alternate-interior-angle theorems. Difficulty ramps 1 to 5.
The worksheet is long because each block holds a figure, a five-row proof table and writing
room, and those cannot share a page — the alternative would be shrinking the space the
student writes in, which is the one thing worth spending paper to avoid.
