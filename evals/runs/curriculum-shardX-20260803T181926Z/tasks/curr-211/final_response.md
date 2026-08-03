# Variables on Both Sides — three documents

Here are the three PDFs for solving linear equations with variables on both
sides (grade 8 / pre-algebra, CCSS 8.EE.C.7).

**Study guide** (`ss_bothsides_curr211.pdf`, 2 pages) — three sections, each a
rule box, a worked example with the reasoning step spelled out, and a try-it with
the answer printed upside down so it can be attempted first:

1. *From a balance or table model to an equation* — bags and counters on two
   pans, and why "the same move on both sides" is the same idea as a legal step
   in algebra.
2. *Collecting the variable terms on one side* — including which side to collect
   on so the surviving coefficient stays positive, and how to check an answer.
3. *Distribute first, then collect* — plus what it means when the variable
   disappears and a true or false number sentence is left.

**Worksheet** (`ws_bothsides_curr211.pdf`) — 10 problems, all with variables on
both sides. Problems 1 and 3 come from balance-pan pictures the student reads
into an equation; 8 is a two-plan cost table solved for the break-even point; 2,
5 and 7 are straight collect-and-solve (one negative answer, one fraction
answer); 4 and 6 need distributing first. Problems 9 and 10 are the special
cases: one equation true for every number, one true for none. Every problem has
a right-aligned answer blank and at least 5 cm of work space; difficulty ramps
1 to 4.

**Answer key** (`ak_bothsides_curr211.pdf`) — a quick-answer bank at the top,
then a full solution per problem that names the move made on each line and
finishes with a substitution check into the original equation. The balance
problems are explained as pan moves first and algebra second. The key carries
the curriculum section (level, standard, difficulty range); the grade level does
not appear on the student's copy.

**What was machine-verified:** all 10 worksheet answers and all 6 study-guide
answers were recomputed with SymPy. The eight ordinary equations were re-solved
from scratch (including $x = \tfrac{11}{2}$ and $x = \tfrac{9}{4}$); for
problems 9 and 10 the checker confirmed the distribution independently —
$3(2x+5)$ really is identical to $6x+15$ (hence infinitely many solutions), and
$4(x+2)$ really is $4x+8$, which cannot equal $4x+5$ (hence none). Nothing is
flagged for manual review.

One thing to grade by hand: problem 10 asks for a one-sentence justification of
why the vanishing variable settles the question. The key says what to accept.
