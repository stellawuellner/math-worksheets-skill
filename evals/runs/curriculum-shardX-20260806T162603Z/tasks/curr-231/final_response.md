Here are the three PDFs for a Grade 8 / Pre-Algebra guided-concept set on
**function concepts, focused on deciding whether a relation is a function**.

**Skills Summary (study guide)** — `ss_isfunction_curr231.pdf`, 2 pages.
An opening box states the definition and the part students get wrong: the rule
restricts *inputs*, so repeated outputs are always fine and only a repeated
input with two different outputs breaks it. Four sections follow, one per
representation — table, list of pairs, graph (with a small plotted example and
the vertical-line test), and a relation given by a rule. Each has a rule box, a
two-step worked example whose first step says why that method applies, and a
try-it with the answer printed upside down inside the box.

**Worksheet** — `ws_isfunction_curr231.pdf`, 6 pages, 10 problems.
A **Graph Bank** at the top plots two relations as sets of points, one that
passes the vertical-line test and one that fails it; the caption says only the
problems naming graph P or graph Q use it. The four representations rotate so
no method repeats twice in a row. Two problems are deliberately built around
the misconception: problem 8 has the output 4 under every input (still a
function), and problem 9 puts a clean table beside a list of pairs that repeats
an input while also repeating an output, so both traps appear at once. Every
part has its own answer blank.

**Answer key** — `ak_isfunction_curr231.pdf`, 3 pages.
Quick Answers bank labelled by response, then a worked solution per problem
that gives the decision *and* the reason, and explicitly flags the
repeated-output cases as allowed. Curriculum block: 8.F.A.1, difficulty 1–4.

**What is verified, honestly.** Twenty-two checks were declared across the ten
problems, and **fourteen are machine-checked with SymPy**. "Is it a function?"
is a yes/no judgement no solver can grade, so the sheet routes the *evidence*
through checkable work instead: every table and graph reading is verified
against the same data the printed table or plot is drawn from, every rule
evaluation is computed, and each "the repeated input has two different outputs"
claim is verified as a comparison — so the key cannot print `<` where `>`
belongs, and the two outputs are machine-confirmed to differ. Worksheet prose
numbers match the verification data 43 out of 43.

**Eight responses are instructor-judged, not machine-checked**: the "is this a
function? explain" part of problems 1, 2, 3, 5, 7, 8, 9 and 10. Because eight
of the ten problems carry one, the key's generated note reads "14 of 22 answers
machine-checked across 10 problems" and names those eight — only problems 4 and
6, the two pure rule evaluations, are fully machine-checked. That is the honest
picture for this topic: the arithmetic and the readings are checked, and the
reasoning that defines a function is yours to read. Each worked solution states
what a correct justification must contain, and problem 8's rubric names the
misconception ("no, because the outputs repeat") that must not earn credit.
