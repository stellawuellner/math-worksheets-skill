Here are the three documents for the Algebra 2 conics workshop — ten problems on
reading vertices, foci, and asymptotes off a conic model.

**Worksheet (`ws_conics_curr398.pdf`, 5 pages).** Ten application problems, each
one a real object in standard position with its units stated: a whispering
gallery, radio towers, a sprinkler patch, a cooling tower, a satellite orbit,
two navigation stations, a hyperbolic mirror, a bridge arch, a tunnel, and a
skate ramp. Three methods rotate through the sheet so the student has to decide
which one applies rather than repeat one procedure:

- ellipse vertices and foci ($c^2 = a^2 - b^2$) — problems 1, 3, 5, 8
- hyperbola vertices and foci ($c^2 = a^2 + b^2$) — problems 2, 6
- hyperbola asymptotes ($\pm b/a$) — problems 4, 7, 9, 10

Difficulty ramps from 1 to 5. Problem 3 moves the centre off the origin,
problems 5 and 8 require setting up and solving a system, problem 9 is an
error-analysis problem (a reported slope of 0.57 that inverts the correct 7/4),
and problem 10 asks for the slope, a sketch on the supplied grid, and a written
explanation of asymptotic behaviour. Every problem gets 5–8 cm of work space,
and problem 10 has a full coordinate grid to draw on.

**Answer key (`ak_conics_curr398.pdf`, 3 pages).** A quick-answer bank at the
top for fast grading, then a worked solution for every problem showing why each
formula applies before the arithmetic — including the check that $c > a$ on a
hyperbola, the elimination step in both systems, and a model sketch description
and model explanation for problem 10. The grade level and the curriculum
summary (standard HSG-GPE.A.3, difficulty range, problem-by-problem coverage)
print here only, not on the sheet the student holds.

**Study guide (`ss_conics_curr398.pdf`, 2 pages).** One section per method:
rule box, worked mini-example, and a try-it with the answer printed upside down
inside the box. It ends with a watch-out box on the single most common error —
reading $a^2$ as "the number under $x^2$" instead of "the larger denominator"
(ellipse) or "the denominator under the positive term" (hyperbola), which
inverts every asymptote slope.

**Verification.** 16 of the 17 machine checks pass under SymPy: every focal
distance, vertex coordinate, asymptote slope, and both systems were recomputed
independently of the answer key, and the printed boxed answers were bound back
to those values. Problem 9's misconception trap was machine-checked as
distinguishably wrong (0.5714 versus the correct 1.75), so the problem really
does catch the error it targets. One item is flagged for manual review, as it
should be: problem 10's sketch and written explanation cannot be machine-checked
— the key shows a model answer to judge it against.
