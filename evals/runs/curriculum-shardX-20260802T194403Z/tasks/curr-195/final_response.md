# Surface Area and Scale Design Workshop — Grade 6–7

Three PDFs are ready.

**Worksheet (`ws_sadesign_curr195.pdf`, 6 pages, 12 problems).** An interleaved review: after a
short warm-up (closed-prism surface area, a scale-drawing perimeter, a closed cylinder), the
four methods rotate so the student has to pick the tool rather than repeat one — prism surface
area, cylinder surface area, composite plan areas, and scale factors. Every problem takes at
least two steps, and several are design decisions rather than formula drills: paint a shed but
not its floor (problem 5), a label with a glued overlap (7), two identical L-shaped panels (8),
a 1:5 model whose surface area must be scaled by 25 (9), and a box whose height must be
recovered from a given surface area (10). Problem 11 asks for a written design justification,
and problem 12 is the synthesis: read a tank's dimensions off a 1 cm = 2.5 m drawing, then find
the painted area of the curved wall plus the top only. Diagrams carry letters ($\ell$, $w$, $h$,
$r$) rather than numbers, so no figure can be misread as belonging to a neighbouring problem.
Every answer line is printed with its unit (m, m$^2$, cm, cm$^2$).

**Answer key (`ak_sadesign_curr195.pdf`, 3 pages).** Quick-answer bank at the top, then a worked
solution for each problem that names the formula, substitutes, and keeps units on every line.
Each solution also names the wrong answer the common misconception produces (196 for an
undoubled prism, 150.80 for a cylinder missing its ends, 60 for a length factor applied to an
area, 740 for the same error at 1:5, 125.66 for painting both circles), so a grader can read the
error from the student's number.

**Study guide (`ss_sadesign_curr195.pdf`, 2 pages).** Four sections — prism, cylinder, composite
plan area, scale factors — each with a rule box, a two-step worked example, and a separate try-it
whose answer is printed upside down inside the box. The scale section states the $k$, $k^2$, $k^3$
rule explicitly, since that is the error this topic is built around.

## Verification

11 of the 12 worksheet answers are machine-checked with SymPy: 9 `approx` (surface areas, scaled
areas, the synthesis tank), 1 `polygon_area` (the six-corner floor plan, checked by shoelace from
its raw coordinates), and 1 `solve` (the height recovered from a 448 cm$^2$ surface area).
**Problem 11 is flagged `manual`** — it asks the student to justify a packaging choice, which is
open reasoning and cannot be CAS-checked; the key carries a full model answer with both surface
areas (216 vs 252 cm$^2$) and grading guidance. Eight problems additionally declare a
machine-checked misconception trap: SymPy computes the wrong method's value and the build fails
if the problem's own check would accept it, which proves each problem can actually discriminate
the error it targets. All 8 study-guide boxes are verified too. Units are gated in both
directions — every declared unit appears on the worksheet's answer line and inside the key's
boxed answer.

Standards codes are taken verbatim from the skill's standards map (no codes were invented);
where that map has no middle-grades surface-area entry, the closest listed codes are used —
area/perimeter for the surface-area work and the ratio/proportional-relationship codes for the
scale problems.
