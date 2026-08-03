# Groups, arrays, and products — three PDFs

Here is a 12-problem practice set on the foundations of multiplication, built
around moving between the three ways the same amount gets shown: repeated
addition, an array, and a product.

**What is in each document**

- **Worksheet** (`ws_multgroups_curr070.pdf`, 5 pages). Twelve problems that
  rotate between four moves: *repeated addition to a multiplication*
  ($5+5+5+5$), *reading an array* (rows and row size), *writing a product back
  as repeated addition* ($6 \times 3$ is six threes), and *finding a missing
  factor* ($4 \times \_\_ = 24$). The first two problems are a gentle warm-up;
  after that the four moves are mixed, so the child has to decide what kind of
  question is being asked instead of repeating one procedure. Problem 10 shows
  a wrong answer ("Ben wrote $4 \times 6 = 4 + 6 = 10$") and asks what he mixed
  up; problem 12 is a challenge that reshapes 32 tiles from rows of 8 into rows
  of 4. Numbers stay inside the usual grade 2–3 range, and every problem has
  room to draw or count. Nothing on the worksheet or study guide prints a grade
  level.
- **Answer key** (`ak_multgroups_curr070.pdf`, 3 pages). Answers at a glance at
  the top, then a worked solution for each problem in the words a child would
  use ("count by fours: 4, 8, 12, 16, 20, 24"), with the final answer boxed and
  a short *listen for* note naming the mistake that answer usually hides.
- **Study guide** (`ss_multgroups_curr070.pdf`, 2 pages). One page-half per
  skill: the rule in plain language, a worked example that starts by saying
  *why* that method fits, and a try-it whose answer is printed upside down in
  the box so the child can check without turning the page. It ends with the
  watch-out that matters most here: $4 \times 6$ is not $4 + 6$.

**What was verified**

All 14 checks behind the 12 problems were recomputed with SymPy before
anything was compiled — every product, both readings of the 4-by-7 array, and
all three missing-factor equations. The printed answer key was then bound
problem-by-problem to those verified values, so a boxed answer cannot disagree
with the checked one. The wrong answer planted in problem 10 was machine-checked
to be distinguishably wrong (adding gives 10; the product is 24).

**Nothing is flagged for manual review** — every problem on this sheet has a
machine-checkable answer, which is what the "machine first" setting asks for.
Problem 10 and problem 12(b) also ask the child to *write* an explanation or a
repeated addition; the key shows a model for each, and those sentences are the
part a grown-up should read.

One note on standards: the map this generator uses has rows for multiplication
situations (3.OA.A.3 / 4.OA.A.2) and for fact fluency (3.OA.C.7), which is how
the problems here are tagged; it has no separate row for 3.OA.A.1, the
"interpret products as equal groups" standard that the array problems most
directly serve.

Suggested order: study guide first, then the worksheet, then the answer key.
