# Derivative Applications and Modeling — AP Calculus AB/BC

Three PDFs are ready: the student worksheet, a full step-by-step answer key,
and a two-page study guide.

## What is on the worksheet (10 problems, 6 pages)

The whole set is derivative *applications*, deliberately shuffled so the first
decision on every problem is which kind of question is being asked. The three
strands rotate rather than sitting in blocks:

- **Curve analysis** (Problems 1, 2, 5, 8) — differentiate a cubic, find its
  critical numbers and increasing intervals, decide which zeros of $f''$ are
  genuine inflection points, and find absolute extrema on a closed interval.
- **Related rates** (Problems 3, 6, 9) — an inflating spherical balloon, the
  classic sliding 13-foot ladder, and an inverted cone filling with water where
  the $r = h/2$ substitution has to happen before differentiating.
- **Optimization** (Problems 4, 7, 10) — a three-sided fenced garden, an
  open-top box cut from a 12-inch square, and a closing synthesis on a
  rectangle inscribed under a parabola.

Problems 7 and 10 both hinge on the step students skip: rejecting a root that
the physical domain forbids, and justifying that a critical point is the
*absolute* extreme. Difficulty ramps from 1 to 5.

## What was machine-verified

Fourteen of the fifteen checks were recomputed independently with SymPy and all
passed — the derivative in Problem 1, every critical-number solve, both
related-rates evaluations (exact, in terms of $\pi$), and both maximum values.
The answer key's quick-answer bank is regenerated from that same verified data
each build, so the printed answers cannot drift.

Two misconception traps are declared and machine-checked to be
*distinguishably* wrong, and both are printed in the key as common wrong
answers:

- dropping the $dr/dt$ factor on the balloon, which computes surface area
  ($\approx 314$) rather than a rate;
- skipping the $r = h/2$ substitution on the cone, which makes the cross-section
  four times too large ($\approx 0.08$ instead of $1/\pi$).

The answer key also flags $x = 6$ on the box problem: the algebra is right and
the model is wrong, which is exactly what that problem is testing.

## What is flagged for manual review

**Problem 10(b)** is genuinely open reasoning and is labelled as such rather
than claimed verified: justifying that $x = \sqrt{3}$ gives the absolute
maximum on $[0, 3]$, and explaining why a table of sampled values could never
settle it. The key gives a three-point grading rubric (Extreme Value Theorem
statement, candidate comparison or sign chart, and the argument about
unsampled inputs) and names the answer to push back on.

## The study guide (2 pages)

Three sections — curve analysis, related rates, optimization — each with a rule
box, a short worked example whose first step names *why* that tool applies, and
a try-it with the answer printed upside down inside the box. The opening box is
a triage panel: how to tell the three problem types apart before starting. All
six study-guide answers were verified by the same gate as the worksheet.

## One note on tagging

`references/standards-map.md` has AP CED rows for related rates (CHA-3.D),
optimization (FUN-4.B–FUN-4.C) and the derivative rules (FUN-3.A–FUN-3.C), but
no row for the analytical-applications unit that covers increasing/decreasing,
concavity and inflection (FUN-4.A). The curve-analysis problems are tagged
FUN-4.B–FUN-4.C, matching the codes this task supplied, rather than inventing a
code.
