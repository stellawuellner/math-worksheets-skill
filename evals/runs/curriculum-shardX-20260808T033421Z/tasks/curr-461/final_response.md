Three PDFs — study guide, worksheet, answer key.

**Study guide (`ss_implicit_curr461.pdf`, 2 pages).** Three sections with a rule
box, a worked example, and a try-it whose answer is printed upside down inside
the box: the basic move (every $y$ differentiated picks up a $dy/dx$ factor, then
collect and divide), products and powers of $y$ (why $xy$ needs the product rule
*and* the chain rule, and why missing the first term leaves a suspiciously simple
answer), and checking an implicit result against the explicit branch when the
relation can be solved for $y$.

**Worksheet (`ws_implicit_curr461.pdf`, 4 pages).** Eight problems, all on
differentiating implicit relations. **Figure A** at the top draws the circle
$x^2+y^2=25$ with its tangent at $(3,4)$, and problems 1 and 2 find that same
slope two ways — first by solving for the upper branch and differentiating
directly, then implicitly — so the picture, the explicit derivative and the
implicit derivative all land on $-3/4$ together. From there the relations get
harder: an $xy$ cross term, cubes, $x^2y$, $x^2y^3$, and finally the folium
$x^3+y^3=6xy$ at $(3,3)$. Every problem states a point and asks the student to
check it satisfies the relation first. Difficulty ramps 1 → 4.

**Answer key (`ak_implicit_curr461.pdf`, 4 pages).** Full derivations with the
$dy/dx$ terms collected explicitly, each opening with the point-check, and each
closing with the reason the answer is believable. Quick Answers bank at the top,
plus a generated Curriculum block (FUN-3.D, difficulty 1–4).

**What is verified.** The sheet asks for 11 graded responses. **Ten are
machine-checked** with SymPy — both explicit-branch derivatives were
differentiated symbolically, and every tangent slope was recomputed from the
implicit derivative formula at the stated point. **One is instructor-judged:
problem 8(b)**, where the student argues from the folium's symmetry in $x$ and
$y$ that the slope at $(3,3)$ must be its own reciprocal, and therefore $-1$. It
prints as `---` in the Quick Answers bank and the key carries the full argument
as a rubric.

One thing to be plain about: for the implicit problems the machine check confirms
that the stated derivative formula produces the printed slope at the given point.
The step from the relation to that formula is shown in full in the answer key and
was checked by hand — no verification type in this pipeline differentiates a
relation implicitly. Problems 1 and 5 are the guard against that gap: each pairs
an implicit answer with an independently differentiated explicit branch that must
agree, and both do.

Three misconception traps are declared and were machine-checked as
distinguishable: substituting the coordinates the wrong way round on problem 2
(gives $-4/3$ instead of $-3/4$), dropping the squares on problem 4 (gives $-1/2$
instead of $-1/4$), and skipping the product rule on problem 6 (gives a slope of
0, a horizontal tangent that is visibly wrong).
