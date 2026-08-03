# Solving Systems by Graphing — Grade 8 / Pre-Algebra (12 problems)

Three PDFs are ready:

- **Worksheet** (`ws_sysgraph_curr227.pdf`, 7 pages) — 12 systems, each with its own
  printed coordinate grid ruled to every unit, plus space below for checking the
  point.
- **Answer key** (`ak_sysgraph_curr227.pdf`, 2 pages) — how each line was plotted,
  the substitution check, and the interpretation for the story problems, plus the
  generated quick-answer bank and curriculum section.
- **Study guide** (`ss_sysgraph_curr227.pdf`, 2 pages) — four sections: slope-intercept
  graphing, standard form via intercepts, the two special cases, and reading a
  crossing point in a story. Each has a rule box, a worked example, and a try-it.

## What the worksheet covers

- **1–3, 5** — both equations already in $y = mx + b$; plot the intercept, step
  off the slope. Problem 5 uses a fractional slope so rise-over-run has to be
  counted rather than guessed.
- **4, 7, 10** — standard form. Problems 4 and 7 are graphed from intercepts;
  problem 10 has to be rearranged first, which is the point of it.
- **6, 9, 12** — story problems (club fees, growing plants, burning candles).
  Each asks for the ordered pair *and* what it means; problem 12 also asks which
  candle is taller before the crossing time.
- **8 and 11** — the special cases: parallel lines (no solution) and two
  equations that are the same line (infinitely many).

Every crossing point is a lattice point inside the printed window, so a correctly
drawn graph gives an exactly readable answer.

## Verification

11 of the 12 problems are fully machine-verified with SymPy, including problem 8:
the checker independently confirms that the parallel system is *inconsistent*, so
"no solution" is a verified answer, not an assertion.

**Flagged for your review (1 problem):** problem 11, $2x + 2y = 8$ and
$y = -x + 4$. The checker confirmed that the listed point satisfies both
equations and reported that the system is a dependent one with infinitely many
solutions — that family cannot be machine-checked as a single answer, so it is
marked for human review rather than claimed as verified. The key states the
answer as the line $y = -x + 4$ and lists what to accept from a student.

## Notes for the adult

The answer key gives the substitution check for every problem, which is worth
insisting on: a graph read one square off looks convincing. Grade level prints on
the answer key only.
