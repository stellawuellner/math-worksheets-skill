# Exponential Growth and Decay — Algebra 1 (12 problems)

Three PDFs are ready:

- **Worksheet** (`ws_expgrowth_curr277.pdf`, 6 pages) — 12 problems on evaluating
  and graphing exponential functions, with four printed coordinate grids and two
  tables of values to fill in.
- **Answer key** (`ak_expgrowth_curr277.pdf`, 3 pages) — full worked reasoning for
  every problem, plus a generated quick-answer bank, a curriculum section, and
  "common wrong answer" notes for the three misconception traps.
- **Study guide** (`ss_expgrowth_curr277.pdf`, 2 pages) — three skill sections, each
  with a rule box, a worked example, and a separate try-it whose answer is printed
  upside down.

## What the worksheet covers

The sheet ramps from difficulty 1 to 5 without repeating a skeleton:

1–2. Evaluate $f(x)=3\cdot2^x$ and a decaying $g(x)=100(0.8)^x$ directly.
3. Build a table for $h(x)=2^x$ (including $x=-1$) and plot the curve on a grid.
4. A negative exponent with an exact fractional answer, $p(-2)=\tfrac{2}{9}$.
5. A doubling bacteria model evaluated at $t=5$.
6. Graph a decay model from a table, then read the graph backwards to find when 2 litres remain.
7. Car depreciation at 0.85 per year, to the nearest cent.
8. Two evaluations of the same function on opposite sides of zero.
9. Graph $2^x$ and $(1/2)^x$ together and find the single crossing point.
10. A 3%-per-year town population after 12 years.
11. Recover the starting value $a$ from the point $(3,40)$, then sketch.
12. Challenge: compare two compound-growth accounts after 10 years.

## Verification

All 18 machine checks (some problems carry several — the table problem alone has
five) passed under SymPy: 5 direct evaluations, the full table, 3 solved
equations, and 4 rounded model values. Nothing on this sheet is flagged for
manual review — every answer, including the graphing problems, resolves to a
value the checker recomputed independently.

Three misconception traps are declared and machine-confirmed as distinguishable
from the correct answer, and they print in the key so a wrong answer tells you
which mistake produced it:

- multiplying by the base and then by the exponent (gives 160 instead of 64),
- using the 15% lost rather than the 0.85 kept (gives 12.15 instead of 12528.15),
- adding 3% twelve times rather than compounding (gives 11560 instead of 12119).

## Notes for the adult

The grade level prints on the answer key only, never on the pages the student
holds. Graphing problems ask for a sketch *and* a stated value, so each one still
has a single answer to grade. The answer key tells you to accept any smooth curve
through the correct plotted points.
