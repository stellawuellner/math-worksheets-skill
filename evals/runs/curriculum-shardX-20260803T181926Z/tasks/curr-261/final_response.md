# Systems on the Graph — three documents

Here are the three PDFs on interpreting the solution of a linear system
graphically (Algebra 1, CCSS HSA-REI.C.6).

**Study guide** (`ss_graphsys_curr261.pdf`, 2 pages) — three sections, each with
a rule box, a worked example whose first step is the reasoning rather than the
arithmetic, and a try-it with the answer printed upside down:

1. *Reading the solution point off a graph* — why the crossing point is the
   solution, how to write it (across, then up), and why substituting into both
   equations is not optional.
2. *Solving a system by graphing* — intercept, slope step, draw, read; plus the
   honest limit of the method when the crossing is not on a lattice point.
3. *One solution, none, or infinitely many* — the slope/intercept test, and how
   the algebra (a leftover true or false sentence) matches the picture.

**Worksheet** (`ws_graphsys_curr261.pdf`, 6 pages) — 10 problems, every one of
them about reading or interpreting a system on a graph. Four give a finished
graph to read (1, 2, 4, 9); three give a blank grid to graph on and then read
(3, 6, 8); three ask for the classification (5 parallel, 7 the same line drawn
twice, 10 the explanation). Problem 6 is a kayak-rental break-even and asks what
the crossing point means for a customer; problem 9 is an error-analysis item
where a student has reported a point that lies on only one of the two lines.
Each problem has its grid on the left and lined space on the right for the
ordered pair and the substitution check.

**Answer key** (`ak_graphsys_curr261.pdf`, 3 pages) — quick-answer bank at the
top, then per problem: how the graph is read, the substitution check in both
original equations, and for the special cases what the picture and the algebra
each show. Grading notes are included for the three items with a written
component. The curriculum section (level, standard, difficulty range) prints
here only, not on the student's copy.

**What was machine-verified:** eight of the ten worksheet answers were recomputed
with SymPy, which re-solved each system from the equations and confirmed both
that the listed point satisfies both equations and that it is the *only* one.
Problem 5's "no solution" was verified by showing the equation
$2x + 1 = 2x - 3$ has an empty solution set. All six study-guide answers were
verified the same way.

**Two items are flagged for manual review, correctly:**

- Problem 7 (the two equations that describe one line) has infinitely many
  solutions. The checker confirmed the sample point $(1, 4)$ lies on both lines
  and reported the system as an infinite family — a solution set with infinitely
  many members cannot be enumerated by machine, so the completeness claim is
  yours to accept.
- Problem 10 is an open justification ("why never exactly two solutions?"). The
  key gives the expected argument and what earns partial credit.
