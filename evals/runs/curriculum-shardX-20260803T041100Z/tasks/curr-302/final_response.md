# Postulates, Theorems, Converses and Biconditionals — High School Geometry

Three PDFs are ready:

- **Study guide** (`ss_prooflogic_curr302.pdf`, 2 pages) — read this first.
- **Worksheet** (`ws_prooflogic_curr302.pdf`, 5 pages, 10 problems).
- **Answer key** (`ak_prooflogic_curr302.pdf`, 4 pages) — worked algebra plus model wording for every explanation.

## What the worksheet does

This is a logic topic, so the design problem is keeping it *checkable* instead of
letting it drift into vocabulary recitation. Every problem makes the student
name which kind of statement is in play, and six of the ten attach that naming
to algebra that can be recomputed:

- **Applying a postulate** (1, 3, 8): Segment Addition, Angle Addition, and the
  perpendicular-bisector biconditional. Each asks for the postulate *by name*
  before the equation, then solves it. Problem 8 finishes by asking which half
  of the biconditional was used.
- **Postulate, theorem, or definition?** (2, 7): a five-row classification table
  where the reason column carries the learning, and then the sharpest version of
  the question — why "through any two points there is exactly one line" is a
  postulate while "two distinct lines meet in exactly one point" is a theorem,
  even though both sound obvious.
- **Testing a converse** (4, 6, 9): the algebraic converse ("if $x = 6$ then
  $x^2 = 36$") where solving *completely* produces the counterexample $x = -6$;
  the converse of the Vertical Angles Theorem, disproved by two congruent but
  adjacent $67^\circ$ angles; and the square/right-angles converse, disproved
  with a labelled non-square rectangle.
- **When a biconditional is valid** (5, 10): why a solution set of exactly one
  value validates "$2x - 7 = 9$ iff $x = 8$", and then a definition rewritten as
  a biconditional next to a statement (complementary $\rightarrow$ adjacent)
  where *both* directions fail.

The algebraic converse device is the spine of the sheet: it turns "is the
converse true?" into "solve completely and look at the solution set", which is
the same reasoning move the geometric counterexamples use. Difficulty ramps
1 → 5 and the four facets are fully interleaved.

## What was verified, and what is flagged manual

**Six of the ten problems were machine-verified with SymPy** (1, 3, 4, 5, 6, 8);
every boxed value in the key was bound back to the recomputed answer, including
problem 4's full two-element solution set.

**Four problems are flagged `manual` on purpose** (2, 7, 9, 10). Classifying a
statement, explaining why one obvious claim is assumed and another is proved,
producing a counterexample figure, and judging whether a biconditional can be
formed are genuinely open reasoning — no CAS can check them, and marking them
verified would be a false claim. The build exits 2 and says so, which is the
correct outcome rather than a defect. For each of the four, the key gives a full
model answer plus an explicit *grading note* saying what to accept, so a parent
or teacher can mark them without being a geometry specialist.

## Standards

`HSG-CO.A–HSG-CO.D` on all ten problems, taken verbatim from
`references/standards-map.md` ("Congruence: transformations, triangle
congruence, proofs"), which is the row that covers this unit's definitions and
proof logic. Every problem also carries a difficulty, a Bloom level, a skill and
a facet, and the declared subtitle is bound to the worksheet title block.

## Study guide

Two pages, four sections matching the four facets. Sections 1, 3 and 4 have
machine-verified worked examples and try-its; section 2 (classification) is
honestly marked manual in both its example and its try-it, since there is no
value to compute — its try-it still prints the expected classification and
reason upside down so the student can self-check. The opening box gives the four
labels and the one sentence students most need: swapping a statement into its
converse is free, but truth is not carried along.

## Gate chain

`build.sh` finished **BUILD PASSED — 2 verification run(s) flagged
manual-review items (exit 2)**: template shells, both verification files, skill
and facet coverage, subtitle binding, layout and work space, three compiles
inside their page budgets (5 / 4 / 2 pages), per-problem answer-key binding,
study-guide structure, and prose consistency.

One gate failed on the first attempt: `compile-ws` rejected the worksheet at 6
pages against a computed budget of 5. The cause was stem prose, not work space —
a three-column explanatory table in the header plus long multi-sentence stems.
The fix kept every problem, every sub-part and every centimetre of work space,
and compressed the header table into a short paragraph and the stems into their
essential wording. Worth flagging for the skill: the page budget is computed
from the JSON (problem type plus declared `workspace_cm`) and cannot see stem
length, so a reasoning-heavy sheet with long prompts will overrun a budget that
looked generous, and the only lever the author has is prose.
