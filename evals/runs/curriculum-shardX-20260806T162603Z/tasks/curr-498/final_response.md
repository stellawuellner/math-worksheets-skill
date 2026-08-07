# Intervals of Convergence, Endpoint by Endpoint — AP Calculus BC

Three PDFs are ready:

- **`ws_ioc_curr498.pdf`** — the student worksheet, 8 problems.
- **`ak_ioc_curr498.pdf`** — the full step-by-step answer key.
- **`ss_ioc_curr498.pdf`** — a 2-page study guide.

## What the worksheet covers

Every problem follows one representation, printed as a labelled number line in
the directions: centre $a$, radius $R$, and two endpoints that each need their
own test. The sheet then walks that picture through eight different power
series:

- **Ordinary radii** (2, 3, 5, 6) with the four possible endpoint outcomes —
  both ends open, both closed, and each of the two half-open cases. Problem 6 is
  the instructive one: the two endpoints have *identical* term sizes
  ($1/\sqrt{n}$) and opposite verdicts.
- **The two degenerate radii**: problem 1 ($R = \infty$, no endpoints exist) and
  problem 4 ($R = 0$, the series converges at one point only).
- **A coefficient on the variable** (problem 7): $(3x-6)^n$ must be factored as
  $3^n(x-2)^n$ first, or the radius comes out three times too large. That is the
  single most common error on this topic and the problem asks about it directly.
- **An application** (problem 8): a dose–response index defined by a power
  series in the dose $d$ in milligrams, where the interval of convergence is
  literally the range of doses the model is defined for.

Each problem asks for a numeric radius, a numeric series value, and then the
interval written in interval notation with the brackets justified.

## Verification — what a machine checked, what you check

The answer key's "What is verified" note reports the same split.

- **15 of the 23 checks are machine-verified with SymPy**: every radius (computed
  as the limit of the coefficient ratio, including the $\infty$ and $0$ cases and
  the $\tfrac13$ of problem 7) and every series value at a named point — $e^2$,
  $\ln\tfrac32$, $\tfrac{\pi^2}{6}$, $-\ln 2$, $\ln\tfrac52$, $\ln\tfrac53$.
- **8 are instructor-judged** — the interval statement on every problem. An
  interval with justified brackets is an argument, not a number, so it is flagged
  rather than claimed as verified. Each has a rubric in the key: which series
  each endpoint produces, which test settles it, and (for problems 7 and 8) the
  specific trap or interpretation that full credit requires.

Nothing is marked `[unchecked]`: every printed answer slot has an entry.

## Notes

- The coefficient ratios are given in each stem. That is deliberate — this sheet
  is about the *interval*, and making students re-derive eight algebraic
  simplifications first would crowd out the endpoint work that is the focus.
- Problem 8's mathematical interval is $[-1, 9)$, but a dose cannot be negative,
  so the key states the usable range as $0 < d < 9$ milligrams. Worth pointing
  out: a model's domain and a series' interval of convergence are not the same
  thing.
- The grade level and the LIM-8 tagging print on the answer key only.
