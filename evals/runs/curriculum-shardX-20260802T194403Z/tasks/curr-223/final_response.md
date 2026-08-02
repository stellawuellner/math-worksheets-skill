# Converting Between Standard Form and Slope-Intercept Form — Grade 8 / Pre-Algebra

Three PDFs are ready:

- **Worksheet** (`ws_linearforms_curr223.pdf`, 5 pages) — 10 problems, five of them
  multi-part, with full room to show the algebra.
- **Answer key** (`ak_linearforms_curr223.pdf`, 2 pages) — quick-answer bank first, then every
  conversion worked line by line, each with the substitution check that proves the rewritten
  equation is the same line.
- **Study guide** (`ss_linearforms_curr223.pdf`, 2 pages) — four rules, four worked examples,
  four try-it items.

## What the worksheet practices

The focus is the conversion itself; all ten problems require it. The four interleaved
subskills are:

1. **Standard $\rightarrow$ slope-intercept** (problems 1, 3, 6, 9) — including a fractional
   slope, a negative $B$, and a ticket-sales context.
2. **Slope-intercept $\rightarrow$ standard** (2, 5, 8) — clear fractions, collect terms,
   make $A > 0$.
3. **Building the equation from a representation** (4, 7) — a drained-pool table with units
   (hours, centimetres) and a two-point problem; each ends by converting to the other form.
4. **Converting inside a context** (10) — a synthesis problem where the slope $-\frac{3}{5}$
   has to be read as a trade-off rate ($5$ more lawns = $3$ fewer driveways).

Difficulty ramps 1 → 5, no facet repeats twice in a row after problem 3, and every context
states its units and its variables explicitly.

## Verification

Every answer on the sheet is machine-checked with SymPy: **23 checks over the 10 problems**,
all PASS, nothing flagged for manual review (`BUILD PASSED — all gates green`, exit 0).

How each kind of conversion is checked:

- Standard $\rightarrow$ slope-intercept: a `slope` check on two points of the line plus an
  `eval` check of the $y$-intercept, so both $m$ and $b$ in the printed answer are verified.
- Slope-intercept $\rightarrow$ standard: substituting $y = mx + b$ into the claimed
  $Ax + By$ must give the constant $C$ — checked at **two different $x$-values**, which for a
  linear form pins the equation exactly. This is why the key's worked solutions end with a
  numeric check: it is the same check the verifier runs.
- The table problem also carries a `read_data` check whose data array is the table printed on
  the sheet, and the two-point problem uses a `solve` check for the intercept $b$.

The answer key and the study guide were each bound back to their verification files problem
by problem, so no printed answer can differ from the verified value.
