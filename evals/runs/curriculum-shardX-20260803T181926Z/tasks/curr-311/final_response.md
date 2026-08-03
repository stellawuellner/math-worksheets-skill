# Triangle Congruence: SSS, SAS, ASA, AAS and HL — three PDFs

- `ws_congruence_curr311.pdf` — student worksheet (5 pages, 8 problems)
- `ak_congruence_curr311.pdf` — full step-by-step answer key (3 pages)
- `ss_congruence_curr311.pdf` — 2-page study guide / skills summary

## What the worksheet asks

Every problem is about deciding *which* evidence a figure or a list of givens
actually supplies — the position of the parts, not just their count.

1. A six-row table of given-lists; write the criterion for each. Rows (a)–(e)
   are SSS, ASA, SAS, AAS and HL; row (f) is the same three letters as (c) with
   the angle moved outside the sides, and is not a criterion at all.
2. A marked kite with a shared diagonal: solve $5x-3 = 2x+9$, then name the
   criterion and say where the unmarked third pair comes from (reflexive).
3. Crossing segments: solve $4x+10 = 6x-20$, then name the criterion and the pair
   the vertical-angle theorem supplies.
4. Two triangles marked with two arcs and a non-included side: find the third
   angle ($180 - 52 - 61$), name the arrangement (AAS), then explain why the same
   figure also gives ASA once the third angle is known.
5. Two right triangles: compute the third side from the hypotenuse 13 and leg 5,
   and use that computation to explain why HL is enough.
6. The SSA counterexample, drawn: one angle, one fixed side, and a swinging side
   that reaches the far ray at two different points. Explain why SSA fails and
   what extra condition rescues it.
7. A two-column proof that a parallelogram's diagonal splits it into congruent
   triangles (blank statement/reason table on the sheet).
8. Judge a claim: "$PQ \cong ST$, $QR \cong TU$, $\angle R \cong \angle U$,
   therefore SAS." Solve $3x+8 = 5x-16$, name the arrangement correctly (SSA),
   and give one extra given that would make it valid.

Difficulty ramps 1 → 5. Figures carry only tick marks, arcs and right-angle
squares — no numbers — so no diagram can be misread as another problem's data.

## What was verified, and what is not — please read this part

This is a topic where honesty about verification matters, because most of what a
congruence worksheet asks for is a *name and a justification*, and no computer
algebra system can check those.

**Machine-verified (5 checks):** every algebraic value on the sheet — $x = 4$
(problem 2), $x = 15$ (3), $m\angle C = 67^\circ$ (4), $BC = 12$ (5), and
$x = 12$ (8). Each was recomputed by SymPy and the answer key's boxed values are
bound back to those verified results.

**Flagged for manual review (8 items):** every criterion name, every
justification, the SSA explanation, and the two-column proof. These are declared
open in the verification data rather than dressed up as verified, so the build
reports them as manual-review items. The answer key gives a complete model answer
for each one — including a full five-step two-column proof for problem 7 and an
explicit "accept any answer that…" note where more than one response is correct —
so an adult marking the sheet has something concrete to compare against.

**One note on standards tags:** `references/standards-map.md` lists congruence as
the range `HSG-CO.A–HSG-CO.D`. I tagged the criterion problems `HSG-CO.B` and the
proof `HSG-CO.C`, the specific clusters inside that range, matching the codes the
task itself names.

## The study guide

Four sections, each a rule box, a worked example whose first step says why that
move applies, and a try-it with the answer upside down inside the box:

1. The five criteria, with the position rule that separates SAS from SSA and ASA
   from AAS, plus the two arrangements that are not criteria.
2. Finding the third pair the figure hides — shared parts, vertical angles,
   alternate interior angles.
3. HL, and the swinging-side picture that shows why plain SSA fails.
4. Writing the two-column proof, with a worked model and a matching try-it.

Sections 1–3 carry machine-verified worked answers; section 4's proof example and
its try-it are declared manual, for the same reason the worksheet's proof is.
