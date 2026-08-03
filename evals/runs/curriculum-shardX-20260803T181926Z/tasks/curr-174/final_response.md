Three PDFs are ready for a sixth- or seventh-grade learner on numerical and
algebraic expressions, focused on the two errors named in the request: **invalid
distribution** (multiplying only the first term, or dropping the sign) and
**unlike-term combination** ($5x+3y$ forced into one term).

- **Worksheet** (8 problems, `ws_expressions_curr174.pdf`) — it opens with a
  clean distribution ($4(x+7)$), then runs three find-and-fix items built on the
  substitution test: Kim's $3(x+5)=3x+5$ (checked at $x=4$: $27$ against her
  $17$), Devon's $5x+3y=8xy$ (checked at $x=2$, $y=3$: $19$ against his $48$),
  and Nadia's $8-2(x-3)=8-2x-6$ (checked at $x=1$: $12$ against her $0$). In
  between are the corresponding correct procedures — combining $7a+4-2a+9$,
  simplifying $5(2x-3)+4x$, and factoring $6x+15$ with a distribute-back check,
  which is the same rule read right to left. The closing problem asks the student
  to explain why unlike terms cannot combine and then to simplify
  $3(2x-4)-2(x-5)$ and test it at $x=3$. Work space runs 5–8 cm, declared per
  problem with `workspace_cm`.
- **Answer key** (`ak_expressions_curr174.pdf`) — four numbered steps per
  problem: do the legal move, name the illegal one, compute, and check by
  substitution. Each error is given a *size*, not just a label (Kim's gap of $10$
  is exactly the $15-5$ she never multiplied; Nadia's $12$ is the whole amount
  lost to the sign), and the pens-and-notebooks model explains why no single term
  can hold $5x+3y$. It carries the generated quick-answer bank and the generated
  "Common wrong answers" block, plus a model answer and a full-credit checklist
  for the open part of problem 8.
- **Study guide** (2 pages, `ss_expressions_curr174.pdf`) — three sections
  matching the worksheet's skill tags: distribute to every term with the sign
  included, combine only like terms (and let unlike terms stay put), and factor
  out then distribute back to check. Each has a rule box, a two-step worked
  example, and an upside-down try-it, plus a watch-out box on the fact that the
  two errors are opposites — one does too little, the other does too much — and
  that a single substitution catches either.

**Verification.** 8 of the 9 checks are machine-verified with SymPy: four `eval`
substitution tests, two `equiv` simplifications, one `expand` and one `factor`.
All six study-guide results are machine-verified too. **Four planted wrong
answers are declared as misconception traps** ($17$, $48$, $0$, $-10$), each
written as the wrong *method* (`3*x + 5`, `8*x*y`, `8 - 2*x - 6`,
`6*x - 12 - 2*x - 10`) so the verifier could confirm both that the printed wrong
number is really what that method produces and that the problem's own check
rejects it. The substitution values were chosen so the wrong and right versions
disagree — at $x=0$, for instance, Nadia's error would have been invisible.

Part (a) of problem 8 is genuinely open — it asks for an explanation in the
student's own words — so it is declared `{"type": "manual"}`, the build exits 2
with exactly one manual-review item, and it is not claimed as verified. Part (b)
of the same problem is machine-checked.

**Standards.** Every problem is tagged `6.EE.A / 7.EE.A` (write, read, evaluate
and identify equivalent expressions), taken verbatim from
`references/standards-map.md`. The grade level prints on the answer key only.

**Gate log.** All 22 gates green. The worksheet's prose-consistency check matched
100% of printed numbers against the verified givens; the study guide matched
96.2%, the one flag being a substitution value used inside a worked example's
check.
