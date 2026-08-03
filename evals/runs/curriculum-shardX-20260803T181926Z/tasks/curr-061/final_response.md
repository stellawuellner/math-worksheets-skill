# Two-Digit Subtraction with Place-Value Models — three PDFs

All three documents are built and gated. Files:

- `ws_subtraction_curr061.pdf` — the student worksheet (3 pages, 8 problems)
- `ak_subtraction_curr061.pdf` — the full step-by-step answer key (2 pages)
- `ss_subtraction_curr061.pdf` — the 2-page study guide / skills summary

## What the worksheet asks

Eight problems on subtracting two-digit numbers, every one of them tied to a
place-value model (ten rods and ones cubes, or expanded form):

1–2. Base-ten block pictures: cross out the rods and cubes being taken away
     ($47-23$, $68-35$). No ten needs breaking yet, so the model is learned
     on the easy case first.
3.   Round each number to the nearest ten and subtract the rounded numbers
     ($61-28$) — the estimate that tells you whether an answer is sensible.
4–5. Expanded form with a broken ten ($52-27$, $83-46$): $52 = 50+2$ becomes
     $52 = 40+12$ so there are enough ones.
6.   Estimate first, then compute exactly ($85-47$), and compare the two.
7.   A sticker story ($74-58$) answered with a unit.
8.   Find-the-mistake: a worked solution that flips the ones column
     ($9-3$ instead of $3-9$) and lands on 46. The student names the error and
     gives the correct difference.

Difficulty ramps 1 → 4 across the set, and each problem is tagged with a
CCSS code (2.NBT.B.5 / 3.NBT.A.2), a Bloom level, and a skill name. Those tags
generate the Curriculum section on the answer key — the grade level is printed
there for you and deliberately nowhere on the student's pages.

## What was verified

Every one of the eight problems is machine-checked by SymPy before anything
compiled — six exact differences and two rounding estimates — and the printed
answer key is bound back to those verified values problem by problem, so a
boxed answer cannot drift from what was checked. **Nothing on this sheet is
left to manual review.**

Three problems (4, 5, 8) also declare the classic "subtract the smaller digit
from the larger one" misconception. The verifier proves each wrong method
produces a visibly different number (35, 43, 46), and those wrong answers are
printed in the key's "Common wrong answers" notes so you can tell at a glance
which mistake a student made.

## The study guide

Three sections, each with a rule box, a worked example whose first step says
*why* that method applies, and a try-it problem with the answer printed upside
down inside the box: subtract tens then ones; break a ten when there are not
enough ones; estimate by rounding to the nearest ten. A watch-out box flags the
one error the worksheet targets — never turning a column around.
