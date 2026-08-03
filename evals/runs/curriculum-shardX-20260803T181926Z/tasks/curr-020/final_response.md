# Making Ten — Kindergarten / Grade 1

Three PDFs are ready: the student worksheet, a full step-by-step answer key,
and a two-page study guide.

## What is on the worksheet (10 problems, 4 pages)

Every problem is about the same idea — ten is made of two parts — met in three
different ways, mixed together so your child has to decide which move to make
rather than repeating the previous one:

- **Finding the missing part of ten** (Problems 1, 2, 4, 7) — a ten-frame with
  some dots showing, a story about two pockets, and a number bond.
- **Taking a part away from ten** (Problems 3, 6, 9) — cubes off a tower, eggs
  out of a carton, empty seats at story time. This is the same pair of numbers
  read backwards, and the key says so out loud.
- **Using ten to add a bigger number** (Problems 5, 8, 10) — filling the frame
  to ten first, then counting on with whatever is left over: $8 + 4$, $7 + 5$,
  and a closing two-step story.

Problems 5, 8, 9 and 10 are split into parts (a) and (b) so the "make the ten"
step is written down before the answer, which is the habit the sheet is
building. The ten-frames are printed on the page; no manipulatives are
required, though counters would help.

Difficulty ramps from a two-second warm-up to a final problem that gives some
stickers away and then adds a bigger number back.

## What was machine-verified

All fourteen checks — every missing part, every subtraction from ten, and every
sum — were recomputed independently with SymPy and all passed. Nothing on this
sheet needed to be flagged for manual review: at this level every answer is a
number, so every answer is checkable, and it was checked. The answer key's
quick-answer bank is regenerated from that same verified data each build, so
the printed answers cannot drift from the checked ones.

Three misconception traps are declared and machine-checked to be
*distinguishably* wrong, and each is printed in the key as a "common wrong
answer" so you can tell a method mix-up from a counting slip:

- answering 18 on $10 - 8$, because the two numbers were added;
- answering 10 on $8 + 4$, because the frame was filled and the counters left
  in the hand were forgotten;
- answering 4 for the empty seats, because the children sitting were counted
  instead.

The key also flags the one to listen for on Problem 2: a child who says 2, the
rest of the top row, and forgets that the bottom row is part of the ten too.

## The study guide (2 pages)

Three short sections, one per skill, each with a rule box, a worked example
whose first line says *why* that move works, and a try-it with the answer
printed upside down inside the box so your child can check without being shown
the working. The opening box lists the six partner pairs of ten — learning
those six pairs turns most of the worksheet into recall rather than counting.
All six study-guide answers were verified by the same gate as the worksheet.

## How to use it

Read the study guide together first, then let your child work the sheet. If
they get stuck, point at the ten-frame and ask "how many squares are empty?"
rather than giving the number.
