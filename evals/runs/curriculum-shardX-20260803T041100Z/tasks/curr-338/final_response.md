# Writing and Interpreting Circle Equations — three PDFs

**Worksheet** (`ws_circleeq_curr338.pdf`, 8 problems, ~3 pages). All 8 problems
are about writing or interpreting a circle equation, each set in a situation with
stated units. Four planned facets, declared in the JSON, interleaved (longest
same-facet run: 2):

1. radar range $(x-4)^2+(y+3)^2=49$ in miles — center, radius, and a distance check that the plane at $(11,-3)$ is exactly on the edge
2. sprinkler at $(-2,5)$ reaching 6 m — write the standard-form equation
3. cell tower at $(3,-2)$ reaching a town at $(8,-2)$ — radius by distance, then the equation
4. pond ripple $x^2+(y-6)^2=20$ — center exactly, radius to two decimals (4.47 m)
5. running track $x^2+y^2-6x+8y-11=0$ — complete the square, center and radius
6. circular fence meets the path $y=4$ — solve for both $x$-coordinates ($-2$ and $6$)
7. $x^2+y^2+10x-4y+20=0$ — complete the square (center $(-5,2)$, radius 3)
8. a classmate's claim about $x^2+y^2+4x+6y+20=0$: part (a) computes the right-hand side ($-7$), part (b) is an **open explanation** of what a negative $r^2$ means

Difficulty ramps 1 → 5. Five answer blanks are unit-tagged (mi, km, m, units)
and bound to the JSON's `answer_unit`.

**Answer key** (`ak_circleeq_curr338.pdf`). Each solution explains the move
before making it — why the sign flips when reading $h$ and $k$, why the added
completing constants must go on both sides, why the right-hand side is $r^2$ —
and verifies the result (the town lands on the boundary; both crossing points sit
5 m from the center). Problem 8(b) gives a model argument plus explicit grading
guidance. The quick-answer bank prints the three declared traps: 10 (halved 20
instead of taking a square root), 3.32 ($\sqrt{11}$ from the original constant),
33 (added the constant instead of subtracting).

**Study guide** (`ss_circleeq_curr338.pdf`, 2 pages). Four sections matching the
four facets — read center and radius, write the equation, complete the square,
use the equation — each with a rule box, a two-step worked example and a
try-it, plus a watch-out box on $r^2$ versus $r$.

## Verification

Of the 13 worksheet verification entries, **12 are machine-verified** with SymPy
(`eval`, `distance`, `approx`, `equiv` for both completing-the-square problems,
`solve` for the intersection) and **1 is `manual`** — problem 8(b) is a genuinely
open explanation and is labelled as such, so the build exits 2 with that item
listed rather than claiming verification it does not have. All 8 study-guide
results are machine-verified. The three declared traps were proved
distinguishably wrong; all other gates are green, including facet coverage,
subtitle binding, per-problem answer binding and unit binding.

Standard: `HSG-C.B.5` from `references/standards-map.md` (row "Circles (arcs,
sectors)"), the exact code the task's `standard_refs` names. Note for the record:
the map has no row for `HSG-GPE.A.1` (derive the equation of a circle), which is
the closer CCSS code for this focus; rather than invent it I used the code the
task supplied and the map contains.
