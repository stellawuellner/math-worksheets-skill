# Second and Higher Derivatives — AP Calculus AB/BC

Three PDFs were generated. The build is green; it exits 2 because one
sign-reasoning part is correctly encoded as a manual-review item.

- **Worksheet** (`ws_higher_derivatives_curr463.pdf`) — 8 problems, the count the
  task asks for. It opens with a value-free "derivative ladder" table
  (function → first → second → third and up) fixing the notation and the meaning
  of each rung. All eight problems are about second or higher derivatives: two
  repeated power-rule problems (including a third derivative), three that need
  the product, chain, or log rule on *both* rungs, one implicit second
  derivative on a circle with an evaluation at a point, and two motion problems
  where the second derivative is acceleration and its sign is concavity.
  Difficulty ramps 1 → 5, and every problem states its units and domain.
- **Answer key** (`ak_higher_derivatives_curr463.pdf`) — shows every rung, not
  just the last: $f'$ simplified, then $f''$, with the reason a rung is factored
  before the next differentiation. Each solution ends with a check, an
  interpretation, or the specific error to watch for (the dropped inner
  derivative on the second chain-rule rung, the sign lost differentiating
  $x^{-1}$). The generated quick-answer bank sits under the title block.
- **Study guide** (`ss_higher_derivatives_curr463.pdf`) — 2 pages, four sections
  (climbing the ladder · product and chain rules on the second rung · implicit
  second derivatives · what the second derivative means), each with a rule box, a
  worked example whose first step names the strategy, and a distinct try-it with
  its answer inverted inside the box.

## Verification

Twelve entries across the 8 problems are machine-checked by SymPy: `diff` with
`order` 2 and 3 (7 entries), `solve` for the times when acceleration vanishes
(2), and `eval` for the two point evaluations. The implicit problem is verified
twice over — the closed form $d^2y/dx^2 = -25/(25-x^2)^{3/2}$ is checked as an
actual second derivative of the upper arc $\sqrt{25-x^2}$, and its value at
$(3,4)$ is checked as $-25/64$ — so the implicit derivation is bound to a
genuinely computed result rather than to arithmetic I supplied. The study
guide's eight boxes are verified the same way.

**One item is flagged manual and should stay that way:** problem 8(c), reading
the interval of concave-down behavior off the sign of $a(t) = 12t(t-2)$. That is
a sign argument a student can reach several correct ways (sign chart, factored
form, test values), so it is `{"type": "manual", ...}` with the expected answer
and the credit criterion stated. Parts (a) and (b) of the same problem are
machine-verified.

Standard `FUN-3.D–FUN-3.E` (from `references/standards-map.md`, row
"Implicit/inverse differentiation") is tagged on all entries, written exactly as
that file spells it. `workspace_cm` is declared per problem (6–9 cm) so the
multi-rung work and the implicit derivation are paid for in the page budget.

## Notes for the reviewer

No gate failed on this task. One authoring detail worth recording for the next
agent: the answer-key binder extracts a leading minus into the expected value,
so a verified `-1/x**2+6*x` is satisfied by a box printed as
`-1/x^2 + 6x` but **not** by the algebraically identical `6x - 1/x^2`, whose
tokens read `+1`. Boxes here were written to lead with the negative term. The
remaining prose-checker flags are domain endpoints and story constants that the
computation does not use.
