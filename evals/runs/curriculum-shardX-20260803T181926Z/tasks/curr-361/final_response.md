# Factoring Cubes and Higher-Degree Expressions — three PDFs

- `ws_polyfactor_curr361.pdf` — student worksheet (6 pages, 10 problems)
- `ak_polyfactor_curr361.pdf` — full step-by-step answer key (3 pages)
- `ss_polyfactor_curr361.pdf` — 2-page study guide / skills summary

## What the worksheet asks

Ten problems, all of them on cubes or on expressions of degree three and above.
A short perfect-cubes table sits with the directions so recognition, not recall
of a list, is what the problems test.

1. $x^3 - 8$ — the plain difference of cubes; name $a$ and $b$ first.
2. $27x^3 + 64$ — both terms are cubes even though neither is a bare power of $x$.
3. $2x^3 - 54$ — GCF first; neither term is a cube as written.
4. $x^3 + 3x^2 - 4x - 12$ — grouping, then a difference of squares.
5. $x^4 - 13x^2 + 36$ — quadratic form via $u = x^2$, then split both brackets.
6. $P(x) = x^3 + 2x^2 - 9x - 18$ — factor, list the zeros, and complete a sign
   table for the four intervals they create.
7. $x^4 - 5x^2 + 4 = 0$ — solve a quartic by factoring into four linear factors.
8. Find the mistake: a factorisation of $8x^6 - 27$ with the trinomial's middle
   sign flipped. Name the broken rule, then give the correct factorisation.
9. $Q(x) = x^3 - 4x^2 - 4x + 16$ — factor, list the zeros, and sketch the cubic on
   the blank grid provided.
10. $R(x) = 3x^5 - 24x^2$ — GCF then a cube pattern, the real zeros with the factor
    each comes from, and which quadratic factor contributes no real zero and why.

Difficulty runs 1 → 5. The four methods (cube patterns, grouping, quadratic form,
factors-to-zeros) are blocked for the first three problems and interleaved after
that, so from problem 4 on the student has to decide which pattern applies before
touching the algebra. Standards tags are HSA-SSE.B.3 and HSA-APR.B.3; those
generate the Curriculum section on the answer key, and the course level prints
there rather than on the student's pages.

## What was verified, and what is not

Eleven machine checks ran before anything compiled: every factorisation was
re-expanded and compared by SymPy, and every zero-set and solution-set was
recomputed independently. The answer key's boxed answers were then bound back to
those verified values problem by problem.

**One item is flagged for manual review, correctly:** the graph sketch in problem
9. A hand-drawn curve cannot be machine-checked, so it is declared open, and the
build reports it as a manual-review item rather than claiming verification. The
answer key gives a full model answer for it — end behaviour, three simple
crossings, the sign on each of the four intervals, and two check values
($Q(0) = 16$, $Q(3) = -5$) — so a grader has something concrete to compare
against. The sign table in problem 6 and the written explanations in problems 8
and 10 all have determinate answers that follow from checked algebra, and the key
works each one through.

## The study guide

Four sections, each a rule box, a worked example whose first step says why that
pattern was chosen, and a try-it with the answer upside down inside the box:
sum and difference of cubes (with the SOAP sign mnemonic and the cubes list);
factoring by grouping; quadratic in disguise; and turning factors into zeros and
graph shape (including touch-versus-cross for a repeated factor). All eight
study-guide answers are verified the same way the worksheet's are.
