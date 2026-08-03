# Function Notation — When $f(x)$ Is Not Multiplication

Three PDFs for an Algebra 1 student, all pointed at one misreading: treating the
parentheses in $f(x)$ as a multiplication sign instead of an input slot.

- **Worksheet** (`ws_functionnotation_curr269.pdf`) — 8 problems. 1–2 evaluate
  $f(3)$ and $g(5)$ with rules chosen so that the "times the rule" misreading
  lands far off ($21$ instead of $7$; $115$ instead of $23$). Problem 3 separates
  $2f(3)$ from $f(2 \cdot 3)$, which is the same slide-the-factor-inside move in
  its subtler form. 4–5 are find-and-fix items: Leo distributes a factor of $3$
  over the rule and reports $33$; Sam borrows the distributive property across
  the input slot and reports $28$. 6–7 reverse the direction — given an output,
  solve for the input — because "divide by $f$" is where the multiplication
  reading does its real damage; problem 7 is built so the misreading loses a root
  ($x = 4$) rather than merely changing a number. Problem 8 is an open
  explanation with `\noansline` (the written paragraph *is* the answer).
  Work space is 3.5–5 cm.
- **Answer key** (`ak_functionnotation_curr269.pdf`) — full reasoning. Every
  solution writes the substitution step before any arithmetic, and each
  find-and-fix solution names the *signature* of the error, not just the right
  number ("his $33$ is $3 \cdot 11$, the correct output times the input"; "the
  gap of $12$ is the cross-term squaring a sum creates"). Problem 8 carries a
  complete model answer plus an explicit note on what a reviewer should look for.
  The generated quick-answer bank under the title block prints all five declared
  traps.
- **Study guide** (`ss_functionnotation_curr269.pdf`) — two pages, three sections
  matching the three worksheet skills (evaluating function notation · fix a
  notation-as-multiplication error · solving for the input). Each has a rule box,
  a two-step worked example, and a distinct try-it with the answer upside down.
  The middle section's rule box lists the three visible signatures of the
  misreading, so it works as a self-check rather than a restatement.

## Verification

7 of 8 worksheet problems are machine-verified with SymPy (5 `eval`, 2 `solve`);
all 6 study-guide answers are verified (4 `eval`, 2 `solve`).

**Problem 8 is `manual` by construction** — it is an "explain in your own words"
task with no computable answer, so it is declared
`{"type": "manual", "desc": ...}` with reviewer criteria in the `desc`, and the
build correctly ends at exit 2 with a manual-review item. That is the right
encoding, not a gap: claiming verification for a paragraph would be a false
claim.

Five misconception traps are declared and machine-checked as distinguishable on
the worksheet (two more on the study guide's error-analysis boxes):

| Problem | Planted wrong result | Error it targets |
|---|---|---|
| 1 | $21$ | read $f(3)$ as $f \cdot 3$, multiplying the rule by 3 |
| 2 | $115$ | same misreading, $5(x^2-2)$ at $x=5$ |
| 3 | $37$ | slid the outside factor inside, computing $f(6)$ |
| 4 | $33$ | distributed a factor of 3 over the rule |
| 5 | $28$ | split the input: $f(2)+f(3)$ instead of $f(5)$ |

`bash scripts/build.sh` ends **BUILD PASSED** with exit 2 (manual-review item),
all 21 gates green. Worksheet prose consistency is 100%.

Standard code `HSF-IF.A–HSF-IF.C` is copied verbatim from
`references/standards-map.md` (the "Function behaviour, notation, graphs" row),
which covers the task's `standard_refs` of `HSF-IF.A`. Difficulty ramps
1, 2, 2, 3, 3, 3, 4, 4; bloom mix is 1 recall / 2 apply / 4 analyze / 1 justify.

## Build notes

No gate failed. The build was green on the first attempt. The study-guide prose
report sits at 89%: the three flagged numbers ($10$, $12$, $12$) are intermediate
products shown inside worked examples (`2(5) + 7 = 10 + 7`), the documented
false-flag class for that heuristic.
