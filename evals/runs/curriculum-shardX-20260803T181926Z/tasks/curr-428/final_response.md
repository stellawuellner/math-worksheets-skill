Here are three PDFs on the ambiguous SSA case — two sides and a non-included
angle, which may describe two triangles, one, or none.

**Worksheet (8 pages, 10 problems).** Every problem carries a to-scale figure
drawn from its own data, and where the measurement is ambiguous the figure shows
both positions of the swinging side — the second drawn dashed — so the student
can see the two triangles before computing them. The givens were chosen to walk
the whole case space, not just to give ten similar exercises:

- **Case tests** (1, 2, 6, 10): compute the height $h = b\sin A$ and decide how
  many triangles the measurement allows. Problem 1 uses $A = 30^\circ$ so the
  height is exactly 5 and the comparison $5 < 6 < 10$ needs no calculator.
  Problem 2 adds a second sighting where $a = 7$ against a height of 7.71: the
  sine comes out at 1.10 and no triangle exists — a deliberate near miss, so the
  case cannot be settled by looking at the numbers. Problem 6 is the exact
  boundary $a = h$, and it reuses problem 1's $a$ and $A$ with a longer $b$, so
  the student sees the same swinging side go from two triangles to one.
- **Both triangles solved completely** (3, 5, 8, 9): find the acute $B$, test the
  supplement, and finish *both* triangles — third angle and third side each time.
  Problem 5 is a search-and-rescue bearing where the two answers are 45.81 km and
  21.28 km along the same shoreline. Problem 8 is the tightest ambiguous
  measurement on the sheet: $h = 9$ against $a = 10$, and part (c) asks how much
  slack that leaves — one unit, which is inside the error of many real
  instruments.
- **Exactly one triangle, with the second candidate shown to fail** (4, 7): here
  $a \ge b$, and the worksheet asks for the arithmetic that rejects the obtuse
  candidate ($A + B_2 = 196.65^\circ > 180^\circ$) rather than letting it be
  forgotten.

Problem 10 is the challenge: with $A$ and $b$ fixed, state the complete rule for
which values of $a$ give none, one, or two triangles, and justify each boundary.

**Answer key (5 pages).** Each problem is worked in steps — the height test
first, then the acute angle, then the explicit supplement test, then each
triangle's remaining parts — with the boxed answers separated as $B_1/B_2$ and
$c_1/c_2$ so a partially correct answer can be marked precisely. The quick-answer
bank at the top lists the four declared traps, including the one this topic
exists to catch: reporting the acute angle only and never checking the
supplement.

**Study guide (2 pages).** Three sections — test the case first, finish both
triangles, and show the other candidate fails — each with a rule box, a worked
example, and a try-it whose answer is printed upside down inside the box. The
opening box carries the four-way case rule in full, and a closing watch-out box
names the four errors the worksheet's traps are built around.

**Verification.** All 33 machine-checkable quantities were recomputed with
SymPy: every triangle was solved independently from its givens, and each second
triangle's angle and side were checked against explicit expressions rather than
being accepted as "the other root". All 6 study-guide boxes were verified the
same way, and the figures are generated from the same verified data, so no
figure can disagree with its answer.

**Flagged for manual review:** three open-response parts — problem 8(c), which
asks what survives when the measurement is shortened to the height, problem 9(b),
which asks which of the two positions the context rules out and what one extra
observation would settle it, and problem 10(c), the full case rule with
justification. The answer key sets out what a complete answer contains and which
alternative arguments to accept.

Standards tagged: HSG-SRT.D.10, HSG-SRT.D.11. Difficulty ramps 1 to 5.
