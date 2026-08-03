# Place value to 1,000 — the zero that holds a place (Grades 2–3)

Three PDFs are ready:

- **Worksheet** (`ws_placevalue_curr054.pdf`, 4 pages) — 8 problems, every one of
  them about the zero placeholder in expanded form: reading a place-value chart with
  0 tens, turning $600 + 0 + 5$ back into a number, comparing 406 and 460, two
  "find the mistake" items, a base-ten block story, ordering 308/380/830, and a
  challenge comparing 7 hundreds with 7 tens. Plenty of open space per problem and
  an answer line on each.
- **Answer key** (`ak_placevalue_curr054.pdf`, 2 pages) — each solution reads the
  number one place at a time and says *why* the zero matters, not just the answer.
  It opens with a quick-answer bank for fast checking, plus a generated Curriculum
  section (2.NBT.A, difficulty 1–4) and a "common wrong answers" line for each
  declared trap.
- **Study guide** (`ss_placevalue_curr054.pdf`, 2 pages) — three short sections:
  what a zero does in a number, how to catch and fix a missing zero (add your
  pieces back up), and comparing numbers made of the same digits. Each has a rule
  or model, a worked example, and a separate try-it with the answer upside down.

**Find-and-fix items (2, as requested).** Problem 4 plants Jamal's
"$308 = 300 + 80$" (pieces add to 380) and problem 5 plants Ruby's
"$720 = 700 + 2$" (pieces add to 702). Both planted totals are declared as
machine-checked misconception traps: SymPy confirmed each wrong number is exactly
what the wrong method produces and that the problem's own check rejects it. The
study guide carries a third trap of the same family (600 + 40 for 604).

**What was verified.** All 10 numeric checks across the 8 problems were recomputed
by SymPy and passed — every expanded-form total, both comparisons, and the
ordering. Two items are flagged for **manual review**: the "tell what Jamal did
wrong" and "tell what Ruby did wrong" parts, which are written explanations no
computer can grade. The key gives a model explanation and states what earns credit
for each. Layout, work space, answer blanks, page budget, and the binding of every
boxed answer to its verified value all passed the build gates.
