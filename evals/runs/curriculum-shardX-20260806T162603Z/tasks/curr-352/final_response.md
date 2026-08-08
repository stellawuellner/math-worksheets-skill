# Complex Number Operations — Algebra 2 practice set

Three PDFs are ready:

- **`ss_complexops_curr352.pdf` — Skills Summary (2 pages).** Start here. Four
  sections, each with a rule box, a worked mini-example, and a "try it" whose
  answer is printed upside down inside the box so your student attempts it
  before checking: adding/subtracting, multiplying two complex numbers,
  conjugate pairs, and squaring. A watch-out box flags the two errors this
  topic produces most — losing the middle term of a square, and treating
  $i^2$ as $+1$.
- **`ws_complexops_curr352.pdf` — Student worksheet (5 pages), 12 problems.**
  The ramp runs from two one-step sums (difficulty 1) through binomial
  products and conjugate pairs to a two-part synthesis problem at difficulty 5.
  No two problems share a skeleton, and the four methods are interleaved after
  the first three so your student has to *choose* the method rather than repeat
  one. Every problem has real writing room (4.5–6 cm) and its own answer line.
- **`ak_complexops_curr352.pdf` — Answer key (4 pages).** Every solution is
  worked step by step, including the $i^2 \to -1$ substitution, not just a
  final value. A "Quick Answers" bank at the top gives the whole column at a
  glance for fast grading, followed by a curriculum block (standard
  HSN-CN.A.2, difficulty range) and a "Common wrong answers" note: a student
  who writes 21 on problem 7 treated $i^2$ as $+1$, and that is a different
  conversation from "wrong".

## What is verified, and what is not

The set carries **14 declared responses across 12 problems. 12 are machine
checked** — each expression was recomputed independently with SymPy and the
build refuses to produce a PDF if a printed answer disagrees with the
recomputed one. The study guide's four worked examples and four try-it answers
were verified the same way.

**2 responses are instructor-judged**, and the answer key marks them with
`---` rather than a value:

- **Problem 7, second part** — "describe what kind of number the product is and
  why the $i$ terms cancelled". The key states what a full-credit answer must
  contain: that the product is real, and that the two middle terms are
  opposites so they add to zero.
- **Problem 12(b)** — "explain why a product of two numbers that each carry an
  imaginary part can end up with a real part neither factor had". The key
  requires two moves to be named: the $i^2$ term appearing, and $i^2 = -1$
  turning it into a real contribution.

Those are genuinely open written responses; no computer algebra system can
grade them, so the sheet does not claim to. Everything else on the page carries
a machine guarantee.

## Notes

- Grade level is printed on the answer key only — the worksheet and study guide
  a student holds carry no level label.
- Three misconception traps are declared and machine-checked to be
  distinguishably wrong (they cannot be confused with the correct answer):
  incomplete distribution of a subtraction, $i^2 = +1$, and squaring each term
  of a binomial separately.
