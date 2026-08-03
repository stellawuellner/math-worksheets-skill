Three PDFs are ready for a fourth- or fifth-grade learner on fraction
equivalence and comparison, focused on the error the request names: deciding
which fraction is bigger by looking at the **tops only** or the **bottoms
only**.

- **Worksheet** (8 problems, `ws_fractions_curr124.pdf`) — it is built so the
  child meets the shortcut where it works before meeting it where it fails.
  Problem 1 has matching bottoms (counting tops is safe, and the child says why);
  problem 2 has matching tops, where the bigger bottom is the *smaller* fraction.
  Then come the find-and-fix items: Ben's $\frac{2}{9} > \frac{2}{4}$ "because
  nine is bigger than four", and Cara rewriting $\frac{3}{5}$ as $\frac{3}{40}$
  by changing only the bottom. Problems 5, 7 and 8 need real rewriting —
  $\frac{3}{4}$ against $\frac{5}{7}$ over $28$, three fractions ordered over
  $30$, and $\frac{5}{6}$ against $\frac{7}{9}$ over $18$ — each chosen so the
  numerator-only shortcut points at the wrong fraction. Problem 6 simplifies
  $\frac{6}{8}$, the same rule run backwards. Work space runs 5–8 cm, declared
  per problem with `workspace_cm`.
- **Answer key** (`ak_fractions_curr124.pdf`) — four to five numbered steps per
  problem: check what matches, reason about piece size, rewrite, compare, and
  then a closing line saying what the shortcut *would* have answered. Several
  solutions include the picture argument a child can hold on to (two slices of a
  pizza cut into nine against two slices of the same pizza cut into four). It
  carries the generated quick-answer bank and the generated "Common wrong
  answers" block, plus a model answer and a full-credit checklist for the open
  part of problem 8.
- **Study guide** (2 pages, `ss_fractions_curr124.pdf`) — three sections matching
  the worksheet's skill tags: when the tops or the bottoms match (with the rule
  for each case, and "neither matches: no shortcut"), build an equal fraction by
  doing the same thing to both numbers, and rewrite both fractions then compare.
  Each has a rule box, a two-step worked example, and an upside-down try-it, plus
  a watch-out box on the belief that drives the whole error: "bigger bottom
  number, bigger fraction" is backwards.

**Verification.** 10 of the 11 checks are machine-verified with SymPy: six
`compare` checks (five relations and one ascending ordering), three `eval`
computations of a missing numerator, and one `equiv` simplification. All six
study-guide results are machine-verified too. Problems 5 and 8 each carry two or
three entries under one id, so the comparison AND the rewriting arithmetic are
both checked.

**Traps.** Three planted wrong results are declared as machine-checked
misconception traps — Cara's $3$, and the $3$ and $5$ that a child writes when
only the bottom has been multiplied up. In each case the trap expression is the
original numerator itself, which is exactly the "changed only one number" error,
and the verifier proved the problem's own check rejects it.

One honest limitation, worth flagging: `verify.py` allows `"traps"` only on types
with a single comparable answer, and **`compare` is not one of them**. The
planted wrong results in problems 3, 5 and 8 that are *relations* ($\frac{2}{9} >
\frac{2}{4}$) therefore cannot be declared as machine-checked traps — they are
stated in the worksheet prose and answered in the key, but the distinguishability
proof the trap machinery gives is not available for them. That is why three traps
are declared rather than six.

Problem 8(a) is genuinely open — it asks the child to explain the error and
supply their own counterexample — so it is declared `{"type": "manual"}`, the
build exits 2 with exactly one manual-review item, and it is not described as
verified. Parts (b) of that problem are machine-checked.

**Standards.** Every problem is tagged `3.NF.A / 4.NF.A` (understanding fractions
and equivalence), taken verbatim from `references/standards-map.md`. The grade
level prints on the answer key only.

**Gate log.** All 22 gates green. Worksheet prose matched 96.7% of its numbers
against the verified givens (the one flag is the common denominator $30$
suggested in problem 7's hint); the study guide matched 81.5%, all flags being
the intermediate rewritten numerators inside worked examples.
