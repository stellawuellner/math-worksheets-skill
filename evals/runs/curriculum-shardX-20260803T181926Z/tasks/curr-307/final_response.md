# Angle Measures on Parallel Lines — High-School Geometry

Three PDFs are ready: the student worksheet, a full step-by-step answer key,
and a two-page study guide.

## What's in the worksheet (10 problems)

All ten problems solve for angle measures on two parallel lines cut by a
transversal, the skill in CCSS **HSG-CO.C.9**. Every problem names its angles
from one shared, labelled diagram printed with the directions — angles *a*
through *h*, no measures marked, captioned so nothing can be read off the
picture. The set ramps from difficulty 1 to 5 across three strands:

- **Find an angle from one you know (4 problems)** — each gives one measure
  and asks for two more, deliberately one congruent partner and one
  supplementary partner, so the student has to make the distinction rather
  than apply one habit. Problem 6 needs two relationships chained together.
- **Solve for x when the pair is congruent (3 problems)** — corresponding,
  alternate interior and alternate exterior pairs, each finishing by
  substituting x back to get the angle.
- **Solve for x when the pair is supplementary (3 problems)** — same-side
  interior pairs, where the expressions add to 180 rather than being set equal.

Problem 10 gives no hint about which rule applies. The two named angles are
not one of the standard pairs, so the student has to chain two relationships
to discover that they are supplementary, then justify the choice in writing.

## What was verified

All 20 machine-checkable answers were recomputed independently with SymPy —
every value of x solved from its own equation, and every angle measure
re-evaluated from that x. Each boxed answer in the key matches its own
problem's verified value.

Three misconception traps were machine-checked as distinguishably wrong: twice
the classic "stopped at x and wrote that as the angle", and once the error of
setting a same-side interior pair equal instead of adding it to 180. They
print in the answer key as common wrong answers.

**One item is flagged for manual review** — problem 10's written
justification. No computer can grade a sentence of geometric reasoning, so the
answer key states what to accept: any valid chain of reasons reaching
"supplementary" (corresponding then linear pair, or vertical then same-side
interior), and explicitly *not* "they looked supplementary". The key also
notes that a student who assumed congruent gets a non-integer x, which is
itself a useful signal.

## The study guide

Two pages carrying the same labelled diagram, so the guide and the worksheet
speak one language. The opening box sorts every parallel-line pair into just
two buckets — congruent or supplementary — because that single decision is
what the topic actually turns on. Three sections follow, each with a rule box,
a worked example whose first step names the pair and why it is that pair, and
a separate try-it with the answer upside down.

The watch-out box targets the two habits that cost the most: treating every
parallel-line pair as congruent, and answering with x when the question asked
for an angle.
