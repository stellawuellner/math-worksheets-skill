# Graphing Proportional Relationships — Grades 6–7

Three PDFs are ready:

- **Study guide** (`ss_prop_graphs_curr188.pdf`, 2 pages) — the rule, three worked examples, three try-its.
- **Worksheet** (`ws_prop_graphs_curr188.pdf`, 6 pages, 10 problems) — every problem has its own coordinate grid.
- **Answer key** (`ak_prop_graphs_curr188.pdf`, 3 pages) — worked reasoning, a quick-answer bank, and what to check on the graphs the student draws.

## What the worksheet does

Every one of the ten problems works on a graph of a proportional relationship
through the origin — either the student draws it, or reads it, or converts it to
the equation $y = kx$. Each problem carries its own grid, so no figure can be
misread as belonging to a neighbouring problem.

- **From a table to a graph** (1, 2, 6): plot the rows, rule the line, then read
  the unit rate. Problem 6 is the counter-example on purpose — a straight line
  whose $y \div x$ quotients are 5, 4 and 3.5, so it misses the origin and is
  *not* proportional. That contrast is what makes the "through the origin"
  condition mean something.
- **Unit rate from a drawn graph** (3, 7, 8): one line, then two lines compared
  (two runners), then a tank graph read at two times.
- **Equation from a graph** (4, 5, 9, 10): write $y = kx$; solve $1.5x = 12$;
  predict at $x = 12$ where the drawn axis stops at 6; and finally build the
  graph from a verbal rate (5 pages every 2 minutes) and solve for the time to
  print 45 pages.

Difficulty ramps 1 → 4 and no method is used more than twice in a row, so after
the warm-up the student has to decide which move the problem is asking for.

## What was verified

**Seventeen machine checks passed** across the ten problems (several problems
carry more than one check — for instance problem 1 verifies the unit rate from
the origin *and* between two non-origin points, which is the whole idea of a
constant of proportionality). The checks use the repository's `slope`, `eval`,
`solve` and `read_data` verifiers, and the tank problem's numbers come from the
same data array the check reads.

**Three items are flagged for manual review**, all of them graphs the student
draws by hand (problems 1, 2 and 10). A drawn line cannot be machine-checked, so
it is declared `manual` rather than claimed as verified; the answer key says
exactly what to look for on each. The build therefore ends at exit 2 with those
three items named, which is the correct outcome.

One misconception trap is declared and machine-checked as distinguishably
wrong: 0.33 on problem 3, from dividing hours by kilometres instead of
kilometres by hours. It prints in the key's "Common wrong answers" block.

## Standards and tagging

`7.RP.A.2` ("Proportional relationships") from `references/standards-map.md`,
verbatim, on every problem. Each problem also carries a difficulty (ramp 1→4), a
Bloom level (10 apply, 9 analyze across the checks) and one of three skill tags;
the three-facet plan is declared in the verify JSON and its subtitle is bound
verbatim into the worksheet title block.

## Study guide

Two pages, three sections matching the three skills: table to graph, unit rate
from a drawn graph, and using the equation to predict. Each has a rule box, a
worked example whose first step says *why* that method applies, and a try-it
with the answer printed upside down inside the box. The watch-out box carries
the two errors this topic actually produces: calling any straight line
proportional, and dividing $x$ by $y$ instead of $y$ by $x$.

## Gate chain

`build.sh` finished **BUILD PASSED** (exit 2 — green with three manual-review
items): template shells, both verification files, skill and facet coverage,
subtitle binding, figure scope and work space, three compiles inside their page
budgets (6 / 3 / 2 pages against 7 / 7 / 2), per-problem answer-key binding,
study-guide structure, and prose consistency at 100% on both documents. No gate
failed on the first attempt.
