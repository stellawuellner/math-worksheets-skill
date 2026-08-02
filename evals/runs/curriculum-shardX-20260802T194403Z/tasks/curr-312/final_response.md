# Completing Two-Column Triangle-Congruence Proofs — High School Geometry

Three PDFs are ready.

**Worksheet (`ws_tricong_curr312.pdf`, 6 pages, 10 problems).** A fluency ramp that never repeats
a skeleton. Problem 1 is the worked pattern: a complete SSS proof with only two reasons missing.
Problem 2 supplies the statements and asks for every reason; problem 3 leaves gaps in both
columns; problem 6 inverts it — the reasons are printed and the student writes the statements;
problems 7, 9 and 10 are written from scratch. The congruence tests rotate rather than block:
SSS, SAS (vertical angles), SAS (angle bisector), ASA (parallel lines), AAS (shared side),
AAS (bisector), HL (right triangles), and a final overlapping-triangle SAS proof that ends in a
CPCTC conclusion. Problems 4 and 8 turn CPCTC into equations to solve. Problem 9 also asks why
SSA is not a test while HL is. Every figure is drawn to scale with tick marks and letters only —
no numbers appear in any diagram, so no figure can be read as belonging to a neighbouring
problem — and every proof table has blank rows sized for handwriting.

**Answer key (`ak_tricong_curr312.pdf`, 4 pages).** A complete model two-column proof for each
of the eight proof problems, plus a short note under each explaining the decision the problem
turns on: why SSS rather than SAS, why the vertical angle is the *included* angle, why the shared
side makes problem 6 AAS and not ASA, and why HL is the one safe form of SSA. The two CPCTC
problems are solved line by line with a substitution check. Grading guidance at the top tells the
marker to accept any logically complete proof with equivalent reasons.

**Study guide (`ss_tricong_curr312.pdf`, 2 pages).** Three sections — side-based tests (SSS/SAS),
angle-based tests (ASA/AAS/HL), and CPCTC equations. Each has a rule box listing the tests and
the "free facts" a figure hands you (reflexive side, midpoint, vertical angles, parallel-line
angles), a fully worked two-column proof with the strategy sentence stated before the table, and
a try-it whose answer is printed upside down inside the box. The watch-out box covers the two
habits that cost the most credit: mismatching vertex order, and omitting the reflexive line.

## Verification

The 2 CPCTC problems (4 and 8) are machine-checked with SymPy as `solve` on the equation CPCTC
produces: $3x-4 = 2x+5 \Rightarrow x = 9$ and $5x+12 = 7x-8 \Rightarrow x = 10$.
**The 8 proof problems are flagged `manual`** and the build reports them as manual-review items,
which is the correct outcome: a two-column proof has no single value a CAS can check, and no
verification is claimed for one. Each manual entry records in the verification file exactly what
the model proof must contain, and the answer key prints that proof in full. In the study guide,
the two worked proofs are likewise `manual` and the two CPCTC examples are machine-verified.
All other gates are green: skill and facet coverage, layout and work space, page budgets,
per-problem answer-key binding, worked-example structure, and prose consistency.

One note on tagging: the skill's standards map has no HSG-CO entry, and codes may not be
invented, so the proof problems carry the map's geometry-proof code and the two CPCTC equation
problems carry its one/two-step-equation code — both verbatim from `references/standards-map.md`.
