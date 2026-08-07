# Boundary Conditions and Open or Closed Endpoints — three PDFs

- **Study guide (`ss_boundaryerrors_curr299.pdf`, 2 pages)** — three sections: who owns the
  boundary value (the branch written with $\le$ or $\ge$, and why only one branch may own it);
  testing each answer against its branch's condition after solving, and why a discarded value
  is *not* an arithmetic mistake; and making the two rules meet at the boundary by setting the
  formulas equal there. Rule box, worked example with an explicit strategy step, and a try-it
  in each, plus a watch-out box making the key point: at a boundary the arithmetic is almost
  never what went wrong.
- **Worksheet (`ws_boundaryerrors_curr299.pdf`, 5 pages)** — 8 problems ramped 1 to 5. Two are
  find-and-fix items: Leo uses the $x>4$ rule at $x=4$ itself, and Sofia copies a condition as
  $t \ge 2$ instead of $t > 2$ and then gets two different prices for the same stay. The rest
  work the same idea directly — evaluating at and around a boundary, filtering solutions by
  domain, and choosing the constant that removes a jump. It ends with a synthesis item that
  ties the endpoint convention to the definition of a function.
- **Answer key (`ak_boundaryerrors_curr299.pdf`, 3 pages)** — Quick Answers bank, a "What is
  verified" note, a **Common wrong answers** block, a generated Curriculum section, and worked
  solutions that read the conditions before the formulas every time.

## What is verified

The sheet asks for **13 responses** across 8 problems.

- **9 are machine-checked.** Every evaluation, both domain-filtered solution sets, and all
  three "find the constant" equations were recomputed with SymPy, and each printed boxed
  answer in the key was separately confirmed against the verified value. Four problems (1, 2,
  5, 7) are fully machine-checked.
- **4 are instructor-judged: 3(a), 4(b), 6(a) and 8(c)** — the written diagnoses. These are
  marked `---` in the Quick Answers bank, named in the key's "What is verified" note, and each
  carries a rubric. The rubrics are strict about *why*, because on this topic the right answer
  for the wrong reason is the common outcome: on 4(b), rejecting $x=5$ as "an arithmetic
  mistake" is wrong — it does satisfy the equation, and it is discarded only because the rule
  that produced it applies just to $x \le 4$.

Nothing is marked `[unchecked]`.

## Machine-checked misconception traps

**Five traps** were declared and every one proved *distinguishably wrong* before the PDFs were
allowed to compile. That includes both planted results shown on the sheet — Leo's $13$ and the
$\$8$ Sofia's version would charge — so those numbers are derived from the wrong method rather
than typed in by hand. They print in the key under "Common wrong answers", so a wrong answer
names its own cause.

## Notes for the adult

- The single most useful habit this sheet teaches: *read both conditions before looking at
  either formula.* Every error on the page follows from skipping that step.
- The grade level prints on the answer key only.
