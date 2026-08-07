Here are the three PDFs for a Grade 8 / Pre-Algebra set on **linear equations
in one variable, focused on deciding whether an equation has one solution, no
solution, or infinitely many solutions**.

**Skills Summary (study guide)** — `ss_linsolutions_curr213.pdf`, 2 pages.
One overview box gives the whole decision rule ("simplify, collect the variable
terms, and look at what is left"), then three sections — exactly one solution,
no solution, and true for every value — each with a rule box, a two-step worked
example, and a try-it whose answer is printed upside down inside the box so the
student attempts it first. Two watch-out boxes flag the errors that actually
happen: reading "no solution" as "$x = 0$", and distributing to only the first
term inside parentheses.

**Worksheet** — `ws_linsolutions_curr213.pdf`, 4 pages, 10 problems.
Every problem is a short realistic situation with its units stated (rental
hours, gigabytes, weeks of saving, metres and seconds, litres per minute), and
every problem ends by asking for the classification, so the focus is exercised
10 times out of 10. The set starts with two one-solution warm-ups, then rotates
the three cases so the student has to decide which one they are looking at
rather than repeating a pattern. The last two problems are two-part: one asks
which constant makes an equation true for every value, the other asks what a
"no solution" result means about two water tanks over time. Work space is
4.4–5 cm per problem with a printed answer blank on every response.

**Answer key** — `ak_linsolutions_curr213.pdf`, 2 pages.
A Quick Answers bank at the top for fast grading, then a full worked solution
for each problem showing the step where the variable terms cancel or combine,
which is the step that decides the classification. It also carries the
curriculum block: standard 8.EE.C.7 on all ten problems, difficulty 1–4.

**What is verified, honestly.** Twelve checks were declared across the ten
problems. Ten are machine-checked with SymPy: each one-solution equation is
solved symbolically, each "infinitely many" equation is proved to be an
identity (both sides are literally the same expression), and each "no solution"
equation is proved to simplify to a non-zero constant, which is what makes it
unsolvable. Eight of the ten problems are therefore fully machine-checked.

Two responses are **instructor-judged, not machine-checked**: problem 9(b) and
problem 10(b), both written explanations. They cannot be verified by a computer
algebra system, and the key does not pretend otherwise — the Quick Answers bank
prints `---` for them, the "What is verified" note names them, and the worked
solution for each states exactly what a correct explanation must contain and
what should not earn credit. That matches the key's own generated note: 8 of 10
problems fully machine-checked, problems 9 and 10 carrying an instructor-judged
part.
