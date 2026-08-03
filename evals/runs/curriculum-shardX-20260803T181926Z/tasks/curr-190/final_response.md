# Proportional Relationships — Grades 6–7

Three PDFs are ready:

- **`ws_proportion_curr190.pdf`** — the student worksheet, 12 problems, 5 pages.
- **`ak_proportion_curr190.pdf`** — the step-by-step answer key, 3 pages.
- **`ss_proportion_curr190.pdf`** — a 2-page study guide.

## What the worksheet covers

The focus is **moving between representations** — table, graph, equation, context —
and every problem crosses at least one of those boundaries. Four kinds are
interleaved after a short warm-up so the student has to notice which representation
they are starting from:

1. **Table → equation** (problems 1, 2, 7) — read a value, divide to find the
   constant of proportionality, write $y = kx$, and check a second column.
2. **Graph → unit rate** (3, 5, 10) — read a lattice point off a line through the
   origin and turn it into a rate.
3. **Equation → value** (4, 8, 11) — substitute when $x$ is known, and *solve* when
   $y$ is known. Telling those two apart is the whole skill.
4. **Context → model** (6, 9, 12) — build the relationship from a story and use it.

Every problem is laid out with a work column on the left and a coordinate grid on the
right, so the student is always asked to produce the graph as well as read one.
That closes the loop: table → equation → graph, in one place.

Problem 9 is the one that is deliberately *not* proportional: Plan B charges a
monthly fee plus a per-minute rate, so the cost per minute changes from 0.4 to 0.275
depending on how much you talk. Working out both figures is what shows the student
that a straight-line graph is not enough — it has to pass through the origin.

## What was verified

28 of the 29 checks were recomputed by SymPy before the PDFs were built, and all 28
passed. The checks cover every part of every problem separately: the value read out
of a table, the constant of proportionality, the substitution, and the equation that
has to be solved are four different checks, not one.

- The two table problems are verified against the *same* data that prints in the
  table, so the printed table and the answer key cannot disagree.
- The graph problems are verified as slopes through the two points the graph actually
  marks.
- Problem 10's comparison ("which runner is faster") is machine-checked as a relation,
  not just asserted.
- Units are bound in both directions on the two problems that carry them (litres,
  kilometres).

**Flagged for manual review (1 item):** problem 9(c) asks for a sentence explaining
what the two cost-per-minute figures show. That is an open response — the numbers
behind it are checked, the sentence is for a human to read — and the answer key
carries a model answer.

## The study guide

Four sections, one per representation move, each with the rule, a worked example whose
first line says which move is being made and why, and a try-it with the answer printed
upside down. The graph section carries a small worked graph so the "read a lattice
point, divide" method is shown on a real picture rather than described.
