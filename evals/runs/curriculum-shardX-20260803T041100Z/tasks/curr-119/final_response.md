Three PDFs are ready for a Grade 4–5 learner on factors, multiples, primes and
patterns, focused on diagnosing a rule that was generalized from too few terms.

- **Worksheet** (8 problems, `ws_patternrules_curr119.pdf`) — every problem
  presents a stated rule *together with the evidence its author checked*, and asks
  the student to test it where the author stopped looking. Kip's "double the term
  before" on 3, 6, 9, 12; Dee's "add 3" on the square numbers 1, 4, 9, 16; Nia's
  "every multiple of 4 is a multiple of 8" (find-and-fix, defeated by the
  remainder of 12 ÷ 8); Tam's half-right "multiples of 5, so every term ends in 5"
  (find-and-fix, cross out the wrong half, then use the surviving half);
  a comparison of the 6th terms produced by a correct add-4 rule and Bea's
  doubling rule that agrees with it for two terms; Ollie's "every odd number is
  prime" (find-and-fix, smallest counterexample written as a product); Pattern E
  where a doubling rule survives two steps and breaks at the fourth term; and a
  closing open-response item on why three supporting examples never prove a rule.
  Work space runs 5–7 cm and is declared per problem with `workspace_cm`.
- **Answer key** (`ak_patternrules_curr119.pdf`) — three to four numbered steps per
  problem: test the rule on an unchecked term, name the real step or structure,
  compute, and check. Each find-and-fix solution also says *why* the author's
  evidence could not have caught the error (Nia sampled only multiples of 8; Tam
  generalized from the first term). It carries the generated quick-answer bank and
  a generated "Common wrong answers" block (192, 19, 115, 128), and gives a full
  model answer plus a full-credit checklist for the open item.
- **Study guide** (2 pages, `ss_patternrules_curr119.pdf`) — three skills matching
  the worksheet tags: test the rule on terms nobody checked, beat a rule with one
  counterexample (divide and read the remainder), and repair a rule by testing it
  one half at a time. Each has a rule box, a two-step worked example, and an
  upside-down try-it, plus a watch-out box on "it worked three times".

**Verification.** 7 of the 8 worksheet problems are machine-checked with SymPy
(six `eval` term/remainder/product computations and one `compare` relation), and
all 6 study-guide results are machine-checked. Problem 8 is genuinely open — it
asks for an explanation and a self-chosen counterexample — so it is declared
`{"type": "manual"}` and the build correctly exits 2 with one manual-review item;
it is not described anywhere as machine-verified. Four planted wrong answers
(192, 19, 115, 128) are declared misconception traps, so the verifier proved each
is distinguishably wrong and really is what the overgeneralized rule computes.

**Standard tags.** The focus here is grade 4–5 number patterns and
factor/multiple reasoning, so every worksheet problem and every study-guide entry
is tagged **`4.OA.B.4 / 4.OA.C.5`**, verbatim from the "Factors, multiples,
primes, number patterns" row of `references/standards-map.md`. That row covers
both halves of the sheet: generating and analysing a number or shape pattern and
identifying features the stated rule did not name (4.OA.C.5), and the
factor/multiple/prime reasoning the counterexamples run on — a multiple of 4 that
is not a multiple of 8, an odd number that is composite (4.OA.B.4). The earlier
build left `"standard"` off every problem because that row did not yet exist in
the map and the nearest available code (3.OA.A.3 / 4.OA.A.2, multiplication and
division word problems) does not describe this content.

**Gate-log note.** The prose-consistency reports show a match rate near 60% on
both documents. Every flagged number is a printed *pattern term* (the 9, 12 of
3, 6, 9, 12; Rosa's 20, 40, 60) — story numbers the check does not compute with,
which that checker documents as the expected false-flag case. No figure labels and
no computed values are unbound.
