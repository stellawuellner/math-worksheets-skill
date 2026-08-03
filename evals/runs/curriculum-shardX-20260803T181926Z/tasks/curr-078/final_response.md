# Finding the Missing Factor — Grades 2–3

Three PDFs are ready:

- **Worksheet** (`ws_missingfactor_curr078.pdf`, 5 pages) — 10 problems on solving
  missing-factor equations within 100, all under 3.OA.C.7 / 3.OA.A.3.
- **Answer key** (`ak_missingfactor_curr078.pdf`, 3 pages) — a full three-step
  solution for every problem, plus a quick-answer bank and a generated Curriculum
  section (grade level, standards, difficulty range) at the top.
- **Study guide** (`ss_missingfactor_curr078.pdf`, 2 pages) — three skill sections,
  each with a rule box, a worked example, and a separate try-it.

## What is on the worksheet

The sheet moves through three ways the same idea shows up:

1. **From a picture** (problems 1–3): an array of tiles, three equal bags of
   marbles, and a seating chart. The student counts one group, writes the
   multiplication sentence, and fills the box.
2. **In a number sentence** (4, 5, 8, 9): bare sentences such as
   `__ × 8 = 56`, `9 × __ = 63` and the division form `72 ÷ __ = 8`, each solved
   with the matching division fact. Problem 9 is an error-analysis item — a
   student subtracted instead of dividing, and your child has to say what went
   wrong before giving the right factor.
3. **In a story** (6, 7, 10): chairs in equal rows, stickers packed 9 to a pack,
   and a two-part challenge where 56 counters are laid out first in 7 rows and
   then in 8. Answers for the story problems are written on a labelled blank so
   the unit (chairs, packs) is part of the answer.

Difficulty ramps 1 → 4, and after the warm-up the three types are mixed so the
student has to decide which move to make rather than repeating one.

## What was verified

Every one of the 10 problems was checked by the SymPy gate — the missing-factor
equations as `solve` checks, the division-fact problems as `eval` checks — and
the answer key's boxed answers were machine-bound to those verified values, so
no printed answer can drift from the checked one. The units (`chairs`, `packs`)
are bound in both directions: the sheet's answer line and the key's boxed answer
must carry the same unit.

Three misconception traps are declared and machine-tested to be distinguishable
from the right answer (subtracting instead of dividing, in the three places a
child most often does it). They print in the answer key as "common wrong
answers", so if you see 54, 64 or 32 on the page you know exactly what happened.

The study guide's six items (three worked examples, three try-its) were verified
the same way.

**Nothing is flagged for manual review** — the build finished all green with no
unverified items.
