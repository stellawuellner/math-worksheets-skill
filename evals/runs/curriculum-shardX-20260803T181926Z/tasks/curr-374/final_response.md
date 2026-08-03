Three PDFs are ready for an Algebra 2 student on radical expressions and
rational exponents, focused on the one error that drives the whole sheet:
distributing a radical (or a $1/2$ power) across a **sum**.

- **Worksheet** (8 problems, `ws_radicals_curr374.pdf`) — every problem turns on
  $\sqrt{a+b} \ne \sqrt{a}+\sqrt{b}$. It opens with two perfect-square tests
  where the split is easy to catch ($\sqrt{9+16}$, and Priya's
  $\sqrt{36+64}=14$), then hides the same split in decimals (Bo's $4.88$ for
  $\sqrt{5+7}$), runs it backwards (Dana merging $\sqrt{50}+\sqrt{18}$ into
  $\sqrt{68}$), rewrites it in rational-exponent notation (Kofi's
  $25^{1/2}+144^{1/2}=17$), puts it inside a radical equation (Jamal's
  $\sqrt{x}+\sqrt{9}=5 \Rightarrow x=4$), and inside a geometry story (Sam
  calling the patio diagonal $20+21$). The closing problem asks the student to
  square $\sqrt{a}+\sqrt{b}$, find the dropped cross term $2\sqrt{ab}$, and then
  use it to find the only $x \ge 0$ with $\sqrt{x+25}=\sqrt{x}+5$.
  Four problems are explicit find-and-fix items (2, 4, 6, and Sam's diagonal in
  7), which is above the "at least two" the request asked for. Work space runs
  5–8 cm and is declared per problem with `workspace_cm`.
- **Answer key** (`ak_radicals_curr374.pdf`) — three to five numbered steps per
  problem: name the illegal step, redo the work correctly, box the answer, and
  check. Each find-and-fix solution also explains *why* the wrong method looked
  safe (perfect squares hide it; a rational exponent disguises it; merging two
  radicals is the same split reversed). It carries the generated quick-answer
  bank and a generated "Common wrong answers" block, and gives a full model
  answer plus a full-credit checklist for the open part of problem 8.
- **Study guide** (2 pages, `ss_radicals_curr374.pdf`) — three sections matching
  the worksheet's skill tags: test a split claim with numbers (with the
  $a+b+2\sqrt{ab}$ reason it always fails), simplify each radical with the
  product rule and combine like radicals, and solve a radical equation by
  squaring one whole side and checking. Each has a rule box, a two-step worked
  example, and an upside-down try-it, plus a watch-out box on perfect squares
  making the split look harmless.

**Verification.** 10 of the 11 checks are machine-verified with SymPy: six
`eval` computations, two `approx` decimals, three `solve` root sets and one
`equiv` simplification (problems 4, 6 and 8 each carry two entries, so the exact
form and the decimal, or the equation and the arithmetic, are both checked). All
six study-guide results are machine-verified too. **Seven planted wrong answers
are declared as misconception traps** (7, 14, 4.88, 8.25, 17, 4, 41), so the
verifier proved each is really what the split produces *and* that the problem's
own check rejects it — a trap that the correct answer could not distinguish
would have failed the build.

Part (a) of problem 8 is genuinely open — it asks for an explanation in the
student's own words — so it is declared `{"type": "manual"}`, the build exits 2
with exactly one manual-review item, and nothing describes it as
machine-verified. Part (b) of the same problem is machine-checked.

**Standards.** Problems tagged `HSN-RN.A.1, HSN-RN.A.2` (radicals and rational
exponents) and, for the two equation problems, `HSA-REI.A.2` (radical equations
and extraneous roots) — both taken verbatim from `references/standards-map.md`.
The grade level prints on the answer key only.

**Gate-log note.** The worksheet prose matched 96.6% of its numbers against the
JSON givens; the single flag is $\sqrt{68}$, Dana's wrong merged radical, which
is quoted in the stem but is not itself a computed given (its decimal value
$8.25$ is the declared trap). The study guide reports 72.4%: every flag there is
an intermediate value inside a worked example ($625$, $7+24$, $\sqrt{25\cdot 3}$)
rather than an unbound answer.
