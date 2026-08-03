# Zeros, Multiplicity, and Graph Behavior — Algebra 2

Three PDFs were generated. The build is green; it exits 2 because one graph
sketch is correctly encoded as a manual-review item.

- **Worksheet** (`ws_zeros_multiplicity_curr363.pdf`) — 10 problems. It opens
  with a value-free reference figure showing the three local shapes at a zero
  (crosses · touches · flattens), captioned so it cannot be read as any one
  problem's data. The ten problems cover the whole chain the focus names: three
  factor a polynomial completely and read its zeros, three read multiplicity out
  of factored form and say whether the curve crosses or touches, two describe
  end behavior from degree and leading coefficient, and two run the reading
  backwards to build a least-degree polynomial from stated intercept behavior.
  The last problem is a full sketch on a blank grid, tying all four together.
  Difficulty ramps 1 → 5.
- **Answer key** (`ak_zeros_multiplicity_curr363.pdf`) — every solution shows the
  factoring path (GCF first, then the pattern), states each zero *with* its
  multiplicity and the resulting behavior, and closes with a degree or
  substitution check. The sketch problem gets a model description plus explicit
  credit criteria. The generated quick-answer bank sits under the title block.
- **Study guide** (`ss_zeros_multiplicity_curr363.pdf`) — 2 pages, four sections
  (factor first · multiplicity as shape · end behavior · building from zeros),
  each with a rule box, a worked example whose first step names the strategy,
  and a distinct try-it with the answer inverted inside the box.

## Verification

Twelve entries across 10 problems are machine-checked by SymPy: `factor` (2),
`zeros` (3), `expand` (2), `solve` (1), and `limit` (4 — end behavior is verified
as the actual limit at $\pm\infty$ rather than left as prose, so both directions
of each end-behavior problem are checked). The study guide's eight boxes are
verified the same way.

**One item is flagged manual and should stay that way:** problem 10's graph
sketch. A hand-drawn curve cannot be CAS-verified, so it is
`{"type": "manual", ...}` with a description of exactly what the correct sketch
shows; its zeros are separately machine-verified by a `zeros` entry sharing the
same problem id, so the numeric part of the problem is still gated.

Standard `HSA-APR.B.3` (from `references/standards-map.md`, row "Polynomial zeros
& graphs") is tagged on all entries. `workspace_cm` is declared per problem
(6–11 cm), with 11 cm on the sketch so the grid and its labelling are paid for
in the page budget rather than compressed.

## Notes for the reviewer

No gate failed on this task. Two visual defects were caught by inspecting the
rendered pages and fixed before recording: the three reference-figure panels
overlapped because a `xshift` inside a scaled `tikzpicture` is scaled too, and
the sketching grid was rendered too small to draw on. Both are cosmetic, and
neither is detectable by the gate chain.
