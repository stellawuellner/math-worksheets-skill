# Ratios in Multiple Forms (Grades 6–7)

Three PDFs are ready for a sixth- or seventh-grade learner on ratios and
equivalent ratio tables, focused on writing and interpreting ratios in multiple
forms. Every problem starts from a model and asks for notation, which is what
the "guided concept practice" format is for.

- **Worksheet (5 pages, 10 problems).** A sticker strip drives the three written
  forms (6 to 8, 6:8, 6/8) and then the part-to-whole form off the same model; a
  tape diagram turns a 4:3 bead ratio plus a box value into a total; three ratio
  tables (red/white beads, tickets/price, lemons/water) build equivalent ratios
  by scaling both rows, each with an easy divide-down column before the harder
  scale-up; a bottling machine gives the *value* of a ratio as a unit rate; a
  5:3 shelf statement is turned into a fraction of the whole; two drink mixes
  are compared by the value of their ratios; and the closing synthesis splits
  63 L of paint in the ratio 5 to 4. Work space is 5–7 cm per problem, declared
  as `workspace_cm` in the JSON so the page budget charges for the room the
  models and tables actually need rather than the type default.
- **Answer key (2 pages).** Three labelled reasoning steps per problem — read
  the model, connect it to notation, compute and check — plus the generated
  quick-answer bank and a **"Common wrong answers"** block naming the five
  designed-for errors.
- **Study guide (2 pages).** Four skills matching the worksheet's four facets:
  reading a ratio off a model, part-to-part vs. part-to-whole, equivalent ratio
  tables, and the value of a ratio. Each has a rule box, a two-step worked
  example whose first step names the decision, and an upside-down try-it, plus a
  watch-out on the `a:b` vs. `a/(a+b)` confusion.

## Verification

All 10 worksheet problems are machine-checked with SymPy — 13 checks in total,
because the three ratio tables each carry two verified cells (a scale-down and a
scale-up) under one problem id. The mix is 5 `eval` ratio computations, 6
`solve` proportions and 1 `compare` of two ratio values. All 8 study-guide boxes
(4 worked examples + 4 try-its) are verified the same way. **Nothing is flagged
manual** and no tolerance was widened.

**Five misconception traps are declared and machine-checked**: comparing the two
parts instead of part-to-whole (0.75), counting only the red boxes of the tape
diagram (24), subtracting instead of dividing to get the value of a ratio (80),
using the other part as the denominator (0.6), and halving the 63 L instead of
splitting it into 5 + 4 shares (31.5). Verification proves each is a value the
problem's own check rejects, and the key prints them for grading.

The declared facet plan is bound to the printed subtitle, every worksheet facet
has a study-guide worked example, and the 35 L answer is unit-bound in both
directions. Standards codes are `6.RP.A.2, 6.RP.A.3` verbatim from
`references/standards-map.md`; nothing was invented. Worksheet prose numbers
bind 25/25 to the JSON givens. Full gate chain green — exit 0, no manual items.
