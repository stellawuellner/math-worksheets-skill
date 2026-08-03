# Composing Piecewise and Nonlinear Functions — Precalculus

Three PDFs are ready:

- **Study guide** (`ss_composition_curr402.pdf`, 2 pages) — read this first.
- **Worksheet** (`ws_composition_curr402.pdf`, 6 pages, 12 problems).
- **Answer key** (`ak_composition_curr402.pdf`, 3 pages) — every composition worked inside out, with the domain reasoning spelled out.

## What the worksheet does

One function library is defined once at the top — $f(x)=x^2-3$, $g(x)=2x+1$,
$h(x)=\sqrt{x-4}$, and two piecewise functions $p$ and $q$ — and all twelve
problems compose from it. That lets later problems reuse earlier results (and
lets a wrong rule in problem 2 surface again in problem 4), which is how a real
unit builds:

- **Evaluating a composition** (1, 5, 8): $(f\circ g)(2) = 22$ and then
  $(g\circ f)(3) = 13$ — the same two functions in the other order, which is the
  cheapest possible demonstration that composition is not commutative. Problem 8
  sends a *negative* inner value into a piecewise function.
- **Simplifying into one rule** (2, 6, 10): $f(g(x)) = 4x^2+4x-2$ against
  $g(f(x)) = 2x^2-5$, and then the important one — $f(h(x))$ simplifies to
  $x-7$, but the composition is only defined on $[4,\infty)$. Simplification
  threw the restriction away; the problem asks the student to notice.
- **Choosing the piece / finding the domain** (3, 7, 11): the recurring error
  this topic produces is testing $x$ against the break point instead of testing
  the *inner output*. Problem 3 punishes it directly, problem 7 asks where
  $(p\circ g)$ switches pieces (at $x=\frac12$, not at 2 — the inner function
  moves the break), and problem 11 derives the two-piece domain of
  $\sqrt{x^2-7}$.
- **Solving composition equations** (4, 9, 12): a quadratic composition with two
  solutions, a second with $x=\pm5$, and the closer — solving
  $(q\circ g)(x)=5$ piece by piece, where one algebraically correct candidate
  ($x=-\frac32$) must be rejected because it falls outside the region where that
  piece is in force.

Difficulty ramps 1 → 5 and the four facets are interleaved throughout.

## What was verified

**All 12 problems were machine-verified with SymPy — 13 checks in total**, since
problem 12 carries one check per piece of the piecewise equation (the
multi-entry encoding for a multi-part problem). Nothing is flagged for manual
review. Every boxed answer in the key was bound back to its recomputed value,
including the symbolic ones ($x-7$, $\pm\sqrt{7}$, $-\frac52$ and $\frac32$).

Four misconception traps were declared and machine-checked as distinguishably
wrong; they print in the key's "Common wrong answers" block:

- computing $g(f(2)) = 3$ where $f(g(2)) = 22$ was asked (and $f(g(3)) = 46$ where $g(f(3)) = 13$ was asked) — composition order,
- choosing the piece of $p$ by testing $x = -2$ instead of the inner output $g(-2) = -3$ (giving 8 instead of 9),
- choosing the $u^2+1$ piece of $q$ because $x = 1$ is positive, when the value reaching $q$ is $f(1) = -2$ (giving 5 instead of 2).

Several problems also ask for a sentence — what the order comparison shows, what
the simplification of $f\circ h$ discarded, why the domain of $h\circ f$ comes in
two pieces, why a candidate had to be thrown out. Those are teaching prose, not
separate answers: the key gives a model response for each, and the value on
every answer line is machine-checked.

## Standards

Codes verbatim from `references/standards-map.md`: `HSF-BF.A.1c, HSF-BF.B.4`
(function composition/inverse) on the eight problems that build or solve a
composition, and `HSF-IF.A–HSF-IF.C` (function behaviour, notation, graphs) on
the five that turn on branch selection and domain. Every problem carries a
difficulty, a Bloom level, a skill and a facet, and the declared subtitle is
bound to the worksheet's title block.

## Study guide

Two pages, four sections matching the four facets, with its **own** function
library ($a$, $b$, $w$) so the worked examples teach the method without handing
over any worksheet answer. Each section has a rule box, a worked example whose
first step says *why* that move comes first, and a try-it with the answer printed
upside down inside the box. The opening box states the two rules that cause most
of the lost marks: order matters, and the domain must be read off the
composition before simplifying.

## Gate chain

`build.sh` finished **BUILD PASSED — all gates green** (exit 0) on the first
build: template shells, both verification files, skill and facet coverage,
subtitle binding, layout and work space, three compiles inside their page budgets
(6 / 3 / 2 pages), per-problem answer-key binding (including the two-check
problem 12), study-guide structure, and prose consistency. No gate failed.
