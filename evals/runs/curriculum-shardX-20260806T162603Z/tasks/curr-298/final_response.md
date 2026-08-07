# Writing Piecewise Rules for Rates and Fees — three PDFs

- **Study guide (`ss_piecewisefees_curr298.pdf`, 2 pages)** — three sections: writing the rule
  from a price list (with the point everything turns on — *the second branch starts from what
  has already been charged*, so it is $P + \text{rate}(x-B)$ and never $\text{rate}\times x$),
  using a rule to find a charge, and working backwards from a charge by picking the branch
  from the boundary value first. Rule box, worked example with an explicit strategy step, and
  a try-it in each; a watch-out box on the conditions being part of the answer.
- **Worksheet (`ws_piecewisefees_curr298.pdf`, 6 pages)** — 10 problems, every one a real
  price structure with its units stated: a taxi meter, a pool entry, a data plan, library
  fines, an electricity tariff, overtime pay, and two competing phone plans. Six ask the
  student to *write* the piecewise rule with both conditions; the rest use a supplied rule to
  compute a charge or to work back from one. It ends with a plan-comparison synthesis item.
- **Answer key (`ak_piecewisefees_curr298.pdf`, 4 pages)** — Quick Answers bank, a "What is
  verified" note, a generated Curriculum section, and full worked solutions, each of which
  prints the correct piecewise rule in proper case notation.

## What is verified, honestly

This sheet asks for **21 responses** across 10 problems, and it has an unusually high
instructor-judged share — because *writing a rule* is the requested focus, and a rule the
student writes is not a number a computer algebra system can recompute.

- **13 are machine-checked.** Every charge computed from a rule and both work-backwards
  equations were recomputed with SymPy, and each printed boxed answer in the key was
  separately confirmed against the verified value. Only **two problems (2 and 7)** are fully
  machine-checked, because they are the two that ask for nothing but numbers.
- **8 are instructor-judged**, and they are the heart of the sheet: the six
  **write-the-rule** parts (1a, 3a, 4a, 6a, 8a, 10a) and three **explain-the-branch-choice**
  parts (5b, 9b, 10c). Each is marked `---` in the Quick Answers bank, listed by number in the
  key's "What is verified" note, and carries a rubric that states the exact rule required and
  the specific error that loses credit — most often a second branch written as
  $\text{rate}\times x$, which silently forgets the money already charged at the boundary.

Nothing is marked `[unchecked]`: no printed answer lacks either a machine check or a written
rubric.

## Notes for the adult

- Grading the rule-writing parts is quick even though it is manual: the key prints the
  intended rule in full, and the rubric tells you the one thing to look for.
- The electricity problem is worth a conversation. Its two branches agree at 300 kWh
  ($0.12 \times 300 = 36$), which is why the bill never jumps — a real tariff has to be built
  that way.
- The grade level prints on the answer key only.
