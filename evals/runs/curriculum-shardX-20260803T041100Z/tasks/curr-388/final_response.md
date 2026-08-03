# Basic Matrix Operations — Algebra 2

Three PDFs are ready:

- **Study guide** (`ss_matrix_ops_curr388.pdf`, 2 pages) — size rules, three worked examples, three try-its.
- **Worksheet** (`ws_matrix_ops_curr388.pdf`, 4 pages, 10 problems).
- **Answer key** (`ak_matrix_ops_curr388.pdf`, 3 pages) — every entry computed, plus a quick-answer bank.

## What the worksheet does

Ten problems, all of them matrix operations, arranged so the student has to
check sizes before choosing a method:

- **Add, subtract, scale** (1, 2, 4, 5): a $2 \times 2$ sum, a scalar multiple,
  a $2 \times 3$ difference (with two subtract-a-negative entries), and the
  linear combination $2A + 3B$.
- **Multiply** (3, 6, 8): a $2 \times 2$ product with the row-by-column pairing
  shown; a two-store inventory model where a $2 \times 3$ stock matrix times a
  $3 \times 1$ price column produces each store's stock value in dollars; and a
  $2 \times 3$ times $3 \times 2$ product where the size of the answer is part
  of the question.
- **Determinant and matrix equations** (7, 9, 10): $ad - bc$; then equal
  matrices solved entry by entry for $x$ and $y$; then a system written as
  $AX = B$ and solved.

The inventory problem is the "application" the format asks for and it is not
decoration — it is the standard reason matrix multiplication is defined the way
it is. Difficulty ramps 1 → 4, and no facet runs more than twice in a row.

## What was verified

**Thirty-two machine checks passed.** A matrix answer is not a single scalar, so
each problem's result is verified *entry by entry*: problem 1 carries four
checks (one per entry of $A + B$), problem 4 carries six, problem 8's four
entries are each verified as a three-term row-column sum, and problem 10 is
checked with the `system` verifier against both equations. This is the honest
encoding — every number the student is asked to produce is independently
recomputed, not just one representative entry.

**Two items are flagged for manual review**, both genuinely open:

- problem 8's written argument that $AB$ is defined and is $2 \times 2$
  (a dimension argument, not a computed value), and
- problem 10's matrix equation $AX = B$ — the student's own representation.

Both are declared `manual` rather than claimed as verified, so the build ends at
exit 2 with them named. The key states what to accept for each.

Two misconception traps are declared and machine-checked as distinguishably
wrong: 150 on problem 6 (adding stock counts to prices instead of multiplying)
and 41 on problem 7 (adding the two diagonal products instead of subtracting).
They print in the key's "Common wrong answers" block.

## Standards and tagging

The task's own `standard_refs` names `HSA-REI.C.7`, which is the
linear-and-quadratic *systems* code — it does not describe matrix arithmetic.
`references/standards-map.md` has a Matrices row, so every problem is tagged
`HSN-VM.C.6–C.12` from that row, verbatim. Nothing was invented, and no
off-topic code was used to fill the slot. Each problem also carries a difficulty
(ramp 1→4), a Bloom level and one of three skill tags; the three-facet plan is
declared in the verify JSON and its subtitle is bound verbatim into the
worksheet title block.

## Study guide

Two pages, three sections matching the three skills. The opening box puts *size*
first, because almost every error on this topic is a size error. Each section
has a rule box, a worked example whose first step justifies the method from the
dimensions, and a try-it with the answer printed upside down inside the box —
with the matrix answers printed as matrices, each entry boxed, rather than
flattened to a list. The watch-out box carries non-commutativity, the
scale-every-entry slip, and the sign in $ad - bc$.

## Gate chain

`build.sh` finished **BUILD PASSED** (exit 2 — green with two manual-review
items): template shells, both verification files, skill and facet coverage,
subtitle binding, layout and work space, three compiles inside their page
budgets (4 / 3 / 2 pages), per-problem answer-key binding (all 32 verified
entry values bound to their own problem's boxed answer), study-guide structure,
and prose consistency at 96% on the worksheet. No gate failed on the first
attempt.
