# Vertex, Axis, Intercepts, and Opening Direction — Algebra 1

Three PDFs are ready:

- **Worksheet** (`ws_parabola_curr281.pdf`) — 10 problems on reading a parabola's features straight
  off its rule. Four locate the axis of symmetry and the vertex (including one already in vertex
  form, $(x-4)^2 - 9$, where the vertex needs no rearranging); three find both kinds of intercept,
  including a downward parabola where the $-1$ has to come out before factoring; three work on
  opening direction and what it forces about the vertex, with problem 8 asking for a labelled
  sketch on the grid provided and problem 10 pulling all four features together. Difficulty ramps
  1 → 5.
- **Answer key** (`ak_parabola_curr281.pdf`) — the axis computed with signs shown, the vertex found
  by substituting into the axis value, the factoring written out with the sign flip made explicit,
  and rubrics for the four written or drawn responses. A "Common wrong answers" block covers the
  three declared misconceptions. Quick Answers and a Curriculum block sit at the top.
- **Study guide** (`ss_parabola_curr281.pdf`) — 2 pages: axis and vertex, both kinds of intercept
  (with the $(x+6) \Rightarrow x = -6$ sign flip called out), and what the sign of $a$ forces about
  the vertex. Rule box, worked example with a stated strategy step, and a try-it per section.

## What is verified, honestly

- **21 machine checks passed.** Every axis of symmetry, every vertex $y$-value, every $y$-intercept
  and every pair of $x$-intercepts was recomputed by SymPy — the intercepts as genuine zero-finding
  on the polynomial, not by re-checking my own factoring — and matched the printed key.
- **4 responses are instructor-judged**: 3(a) and 10(a) (opening direction with a reason), 9(c)
  (maximum or minimum, and how you can tell without graphing), and 8(d) (the labelled sketch).
  Direction, vertex type and a drawing are not things a computer algebra system grades; each
  carries a `manual` entry and a printed rubric, and the sketch rubric lists the four features that
  must appear. The key's "What is verified" note names problems 3, 8, 9 and 10 as the `---` items.
- **3 misconception traps** were machine-tested for distinguishability: dropping the minus sign in
  $-b/2a$, stopping at $-b$, and reading intercepts off the factors without flipping their signs.
- All six study-guide examples and try-its were verified.

Nothing is marked `[unchecked]`.
