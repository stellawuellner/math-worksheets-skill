# Composing Functions from Symbolic Rules — Algebra 2

Three PDFs are ready:

- **Worksheet** (`ws_compose_curr381.pdf`) — 10 problems on composing functions
  from their symbolic rules.
- **Answer key** (`ak_compose_curr381.pdf`) — quick-answer bank, then a worked
  solution per problem that shows the substitution before the simplification.
- **Study guide** (`ss_compose_curr381.pdf`, 2 pages) — four sections: composing
  at a number; composing into a new rule; why the two orders differ; and solving
  an equation built from a composition. Each has a rule, a worked example that
  names its strategy first, and a try-it.

## The model

The worksheet opens with a "two machines in a row" model: an input goes through
$g$, its output goes into $f$, and a three-row table follows one input at a time
through both columns for $f(x)=2x+5$, $g(x)=x^2-3$. Problem 1 then uses exactly
those machines, so the notation $(f\circ g)(4)$ is attached to a picture the
student has already traced by hand before any algebra begins. Problems 2–5 move
from a number to a rule; problems 3 and 8 put the two orders side by side;
problems 6, 9 and 10 use a composition inside an equation.

## Verification — the honest split

**17 verified responses across the 10 problems**:

- **14 are machine-checked** with SymPy. Composed rules are checked as
  *identities*, so an answer written in a different but equivalent form still
  passes and a botched substitution cannot. The numeric compositions are
  recomputed from the original input through both rules, not from an
  intermediate value fed back in.
- **3 are instructor-judged**, marked `---` in the quick-answer bank:
  **3(b)**, **8(c)** and **10(c)**. These are the reasoning parts — why the two
  orders give different functions, and why the composition is defined everywhere
  although the outer function is not. The key prints a grading rubric for each.

The key's "What is verified" note reports the same 14 of 17, naming problems 3, 8
and 10. No `[unchecked]` marks.
