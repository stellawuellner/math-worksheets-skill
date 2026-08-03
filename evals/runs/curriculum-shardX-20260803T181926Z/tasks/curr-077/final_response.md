# Multiplication Fact Strategies — Grades 2–3 practice set

Three PDFs are ready:

- **`ss_factstrategies_curr077.pdf` — Skills Summary (2 pages).** The reference card
  to keep beside the worksheet. Three sections, each with a rule, a worked example,
  and a "try it" whose answer is printed upside down inside the box:
  (1) **turnaround facts** — swapping the factors does not change the product, shown
  with the array-turning picture; (2) **breaking a factor apart** — splitting by
  adding (`6 × 8 = 6×5 + 6×3`) and by subtracting (`9 × 7 = 10×7 − 7`); and
  (3) **missing-factor facts** for division. A watch-out box flags the classic slip
  in the nines strategy: taking away *one* instead of one whole group.
- **`ws_factstrategies_curr077.pdf` — Student worksheet (4 pages), 10 problems.**
  Eight of the ten problems directly exercise the commutative and distributive
  strategies; the other two use the related missing-factor fact for division, which
  is the same fact family seen from the other side. The set opens with two
  turnaround warm-ups where the partner fact is handed to the student, then moves to
  guided break-aparts with the split written in, then to problem 8 where the student
  chooses their own split, and finishes with Malik's nines strategy and a sharing
  story. Difficulty ramps 1 → 4; each problem has 3.5–5 cm of work space and its own
  answer line.
- **`ak_factstrategies_curr077.pdf` — Answer key (3 pages).** Every problem is
  restated with the strategy explained in words a second- or third-grader's adult can
  read aloud, plus the arithmetic of each part-product. It opens with a quick-answer
  bank and a generated Curriculum section (3.OA.C.7, with 3.OA.A.3 on the sharing
  story) and the difficulty range. Problem 8 accepts any correct split, and the key
  says so; a second valid split is shown.

**Verification.** All 16 machine checks were recomputed independently with SymPy and
passed. Where a problem hands the student a break-apart strategy, both halves are
checked: the strategy expression (`6 × (5+2)`) *and* the plain fact (`6 × 7`) are
verified to give the same product, so the printed strategy cannot quietly disagree
with the answer. The declared misconception trap on problem 9 was confirmed
distinguishable — subtracting 1 instead of a group of 7 gives 69, which the check
rejects. **Nothing is flagged for manual review.**
