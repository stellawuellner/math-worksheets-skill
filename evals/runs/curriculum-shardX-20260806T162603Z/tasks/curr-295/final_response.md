# Choosing a Method and Reading the Roots — three PDFs

- **Study guide (`ss_quadmethods_curr295.pdf`, 2 pages)** — four sections, one per decision:
  square roots when the squared part is already alone; factoring and the zero-product
  property; the quadratic formula when nothing factors; and a fourth section most guides skip
  — reading the roots back into the story, where a root can be perfectly correct and still not
  answer the question. Each section has a rule box, a worked example whose first step says
  *why that method was chosen*, and a try-it with the answer upside down inside the box.
- **Worksheet (`ws_quadmethods_curr295.pdf`, 6 pages)** — 12 problems. Four short warm-ups,
  then the methods are interleaved so that no two consecutive problems use the same one: the
  student has to decide before they can start. Three problems are set in context (a kicked
  ball, a garden, a drama club's ticket price), and each of those asks for both roots *and*
  what they mean. It finishes with the ticket-price synthesis challenge.
- **Answer key (`ak_quadmethods_curr295.pdf`, 4 pages)** — Quick Answers bank, a "What is
  verified" note, a "Common wrong answers" block, a generated Curriculum section, and worked
  solutions that begin by naming the method choice and saying why the alternative would have
  been slower.

## What is verified

The sheet asks for **15 responses** across 12 problems.

- **12 are machine-checked.** Every solution set and both rounded roots were recomputed with
  SymPy, and each printed boxed answer in the key was separately confirmed to be the value
  that was verified. Nine of the twelve problems (1, 2, 3, 4, 5, 7, 9, 10, 11) are fully
  machine-checked.
- **3 are instructor-judged: 6(b), 8(b) and 12(b)** — the interpretation halves of the three
  context problems ("which solution is the landing time", "why is $-9$ rejected as a width",
  "what do the two ticket prices mean"). These are written explanations, so they are marked
  `---` in the Quick Answers bank, named in the key's "What is verified" note, and the key
  spells out what full credit requires. That last part matters here: on 8(b) the common
  half-answer is to reject $-9$ as a mistake, when in fact it solves the equation and is
  rejected only because a width cannot be negative.

Nothing is marked `[unchecked]`.

## Machine-checked misconception traps

Two traps were declared and proved distinguishably wrong before the build was allowed to
compile: dividing by $2x$ on problem 5 (which loses the root $x=0$) and dividing by $x$ on
problem 11 (which loses it again in a cubic). Both are printed in the key under "Common wrong
answers", so a wrong answer identifies its own cause.

## Notes for the adult

- Problems 3 and 9 are the two where students waste the most time: both are much faster with
  square roots than by expanding, and the study guide's first section says so explicitly.
- The grade level prints on the answer key only.
