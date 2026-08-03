Here are the three PDFs for the parabola-features set.

**Worksheet — `ws_parabola_curr281.pdf` (6 pages, 10 problems).** Every problem
is about the same four features: the vertex, the axis of symmetry, the
intercepts, and which way the parabola opens. Each one comes with its own blank
coordinate grid so your student reads the features off the algebra first and
then draws the curve that matches — the model and the notation stay side by
side. The set moves through three ways of getting at the same picture: reading
vertex form directly (problems 1, 2, 5, 8), using the axis formula
$x = -b/2a$ on standard form (3, 6), and starting from the $x$-intercepts (4,
7, 9). Problem 10 is the challenge: two intercepts and one extra point are
given, and the student has to build the equation, find the vertex, decide the
opening direction, sketch it, and say in a sentence why the extra point forced
that direction. Difficulty ramps 1 → 5; the methods are interleaved after the
warm-up so the student has to *choose* an approach rather than repeat one.

**Answer key — `ak_parabola_curr281.pdf` (4 pages).** Full worked reasoning for
every problem, not just answers: the axis first, then the substitution, then the
vertex, then the sketch notes (intercepts, symmetric points). A quick-answer
bank sits at the top for fast grading, along with a Curriculum section listing
the standards covered and the difficulty range. Three problems carry a
"common wrong answer" note (problems 1, 3 and 6) telling you exactly which
mistake produces the wrong number you may see on the page — sign of $h$ read
straight off the parentheses, $b/2a$ used instead of $-b/2a$, and the minus
sign on $a$ dropped.

**Study guide — `ss_parabola_curr281.pdf` (2 pages).** One overview box naming
all four features and where each comes from, then three teaching sections —
vertex form, standard form, intercepts-and-direction — each with a rule box, a
worked example (including a small labelled parabola for the vertex-form case),
and a separate try-it problem with the answer printed upside down inside the
box so the student can check without seeing the work. It closes with a
watch-out box on the two sign traps.

**What was verified.** 19 of the 20 checks ran through SymPy and passed: every
vertex height, every $y$-intercept and every intercept pair on the worksheet,
plus all six study-guide examples and try-its. The three declared misconception
traps were machine-checked to be distinguishably wrong. The one item flagged for
manual review is the open part of problem 10 — the sketch and the one-sentence
explanation — which no computer algebra system can grade; the answer key spells
out what full credit looks like.
