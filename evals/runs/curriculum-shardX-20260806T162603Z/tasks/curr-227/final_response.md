Here are the three PDFs for a Grade 8 / Pre-Algebra fluency set on **solving
systems of two linear equations by graphing**.

**Skills Summary (study guide)** — `ss_graphsys_curr227.pdf`, 2 pages.
Four sections that follow the difficulty ramp of the worksheet: reading a
crossing point off a graph that is already drawn (with a small worked grid),
graphing two lines from $y = mx + b$, graphing a line given as $Ax + By = C$
using its intercepts, and the cases where the lines never meet. Each has a rule
box, a two-step worked example whose first step says why that method applies,
and a try-it with the answer printed upside down inside the box.

**Worksheet** — `ws_graphsys_curr227.pdf`, 7 pages, 12 problems.
The ramp is built in: problems 1 and 2 arrive with both lines already drawn, so
the only job is reading and checking the point. Problems 3 onwards give a blank
grid and the student draws both lines. No two problems share a skeleton — the
set moves through slope-intercept pairs, a fractional slope, a line in standard
form, a vertical line ($x = 5$), a pair of parallel lines, an equation that has
to be rearranged before it can be graphed and then turns out to be the same
line as its partner, and two pricing contexts. Every problem carries its own
grid, and every grid is followed by 2.6 cm of writing space for plotting points
and checking the answer in both equations.

**Answer key** — `ak_graphsys_curr227.pdf`, 3 pages.
Quick Answers bank labelled by response, then a worked solution that gives both
the graphical reading and the algebraic confirmation for every problem, so a
student who mis-plots can see where the point should have been.
Curriculum block: 8.EE.C.8a and 8.EE.C.8c, difficulty 1–4.

**What is verified, honestly.** Fifteen checks were declared across the twelve
problems, and **twelve are machine-checked with SymPy**: every intersection is
solved independently and confirmed to satisfy both equations with the count
matching SymPy's full solution set, the parallel system is machine-confirmed
inconsistent, and the rearrangement in problem 10 is verified by solving the
standard-form equation for $y$ symbolically. That is exactly what the key's
generated note says: 12 of 15 answers machine-checked across 12 problems.

**Three responses are instructor-judged, not machine-checked**: part (b) of
problems 5, 10 and 12 — what parallel lines mean for the system, why two
identical equations give infinitely many solutions, and which company is
cheaper on a long trip. The "infinitely many" case genuinely cannot be checked
by the solver (an infinite solution family is not a list it can compare), so it
is flagged rather than dressed up as verified. The Quick Answers bank prints
`---` for those three, and each worked solution states what a correct
explanation must contain and what should not earn credit.
