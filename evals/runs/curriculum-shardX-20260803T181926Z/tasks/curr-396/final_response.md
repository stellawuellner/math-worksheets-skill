# Conic sections — identifying conics from equations and key features (Algebra 2)

Three PDFs are ready:

- **`ws_conics_curr396.pdf`** — the student worksheet, 10 problems, 5 pages.
- **`ak_conics_curr396.pdf`** — the full step-by-step answer key, 4 pages.
- **`ss_conics_curr396.pdf`** — the 2-page study guide / skills summary.

## What the worksheet does

It teaches one decision procedure rather than four memorised pictures. Every conic is
written in general form $Ax^2 + Bxy + Cy^2 + Dx + Ey + F = 0$, and the *indicator*
$B^2 - 4AC$ names the family before any other work starts. A boxed concept model on page 1
gives the sorting table (negative and $A = C$ → circle, negative and $A \neq C$ → ellipse,
zero → parabola, positive → hyperbola) beside a value-free sketch of the four curves, so
the notation and the picture are attached to each other from the first problem.

The ten problems, in order:

1–3. Read $A$, $B$, $C$ off an equation and compute the indicator — circle, hyperbola, and
   a parabola where the missing square makes $C = 0$. These three are the blocked warm-up.
4. Circle: complete both squares, find centre $(3,-2)$ and radius $5$.
5. Parabola: axis $x = 3$, vertex $(3,-4)$, and the $x$-intercepts $1$ and $5$.
6. Ellipse $x^2/25 + y^2/9 = 1$: $a = 5$, $b = 3$, $c = 4$, vertices, co-vertices, foci.
7. Indicator plus the extra $A \neq C$ condition — an ellipse that is not a circle.
8. The deliberate trap: $x^2+y^2+10x-4y+13=0$ gives $r^2 = 16$, and the radius is $4$.
   Reporting $16$ is the designed-for error, and the answer key flags it by name.
9. A nonlinear model: a thrown ball follows $y = -x^2 + 6x$; the maximum is the single
   solution of the system with its axis of symmetry $x = 3$, giving $(3, 9)$.
10. Open explanation — why $4x^2 + 9y^2 = 36$ and $4x^2 - 9y^2 = 36$ are different curves.

After the warm-up the problems rotate between the four methods, so the student has to
decide which tool applies rather than repeat one.

## What was verified, and what was not

Every numeric answer on the sheet was recomputed independently with SymPy before the PDFs
were compiled: **17 machine-verified checks across problems 1–9**, all passing — the
indicators, both circle centres and radii, the parabola's axis, vertex and intercepts, the
ellipse's $a$, $b$ and $c$, and the nonlinear system in problem 9 (confirmed to be the
complete solution set, not just one solution). The declared misconception trap on problem 8
was machine-checked to be *distinguishably* wrong, so the problem really can catch the
error it targets.

**Problem 10 is flagged for manual review** and is the only such item. It asks for an
explanation, which no computer algebra system can grade, so the answer key carries a model
answer plus an explicit marking guide (full credit for naming the sign difference between
the squared coefficients or computing the two indicators; partial credit for naming both
curves without saying why; not sufficient to appeal to what the graphs look like).

## The study guide

Four one-page-and-a-bit sections, each with a rule box, a worked example whose first step
says *why* that tool is the right one, and a distinct try-it whose answer is printed upside
down inside the box: naming the family from the indicator, circle centre and radius,
parabola axis and vertex, and ellipse vertices and foci. All eight worked examples and
try-its were verified by the same SymPy gate as the worksheet, so nothing the student
learns from is unchecked.

Standards covered: HSG-GPE.A.1–A.3 (conic sections from equations) and HSF-IF.A–HSF-IF.C
(function behaviour and graphs, for the parabola features). Difficulty ramps 1 → 5.
