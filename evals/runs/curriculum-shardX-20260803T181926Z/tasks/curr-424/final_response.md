Three PDFs are ready for a precalculus student on trigonometric identities and
equations, focused on diagnosing illegal cancellation and lost-solution errors.

- **Worksheet** (8 problems, `ws_trigcancel_curr424.pdf`, 5 pages) — seven of the
  eight problems are find-and-fix items, covering both halves of the focus.
  *Lost solutions from dividing:* Rafi divides $2\sin\theta\cos\theta = \sin\theta$
  by $\sin\theta$ and reports only $60^\circ, 300^\circ$ when the full set is
  $0^\circ, 60^\circ, 180^\circ, 300^\circ$; Nils does the same with $\cos\theta$
  on $2\cos^2\theta = \cos\theta$ and loses $90^\circ$ and $270^\circ$; Yuki
  "cancels the cosine" from $\cos 2\theta = \cos\theta$ to get $2\theta = \theta$
  and reports $0^\circ$ alone, losing $120^\circ$ and $240^\circ$. *Illegal
  cancellation:* Bea cancels $\dfrac{\cos^2 x - 1}{\cos x - 1}$ term by term to
  $\cos x$ (the truth is $\cos x + 1$, and a single test at $\cos x = 0.5$ gives
  1.5 against her 0.5); another student cancels the $\cos x$ out of
  $\dfrac{\sin^2 x + \cos x}{\cos x}$, which is a term of a sum, not a factor
  (2.5 against 1.75). *Signs and extraneous roots:* Tam roots $4\sin^2\theta = 1$
  and keeps only the positive branch, losing $210^\circ$ and $330^\circ$; Ola
  squares $\sin\theta - \cos\theta = 1$, gets four candidates and keeps all of
  them, when only $90^\circ$ and $180^\circ$ survive a check. Problem 8 is an open
  explanation that asks the student to state which operation adds solutions and
  which removes them. Work space runs 5.5–7.5 cm per problem.
- **Answer key** (`ak_trigcancel_curr424.pdf`, 4 pages) — four to six numbered
  steps per problem: name the slip, redo the work by factoring, box the full
  solution set, then verify the specific solutions the student lost by
  substituting them into the original equation. Two teaching points recur and are
  stated explicitly: the lost solutions are always the zeros of whatever was
  divided by, and a solution set that is a strict subset of the true one is the
  signature of a division. It carries the generated quick-answer bank and the
  generated "Common wrong answers" block (0.5 and 1.75), plus a model answer and a
  full-credit checklist for the open item.
- **Study guide** (2 pages, `ss_trigcancel_curr424.pdf`) — three skills matching
  the worksheet tags: factor, never divide (zero-product property, and the
  diagnostic that the lost roots are the zeros of the divisor); only factors
  cancel (with the numerical-test habit); and keep both signs, check every
  candidate ($\sqrt{u^2} = |u|$, squaring adds, dividing removes). Each has a rule
  box, a two-step worked example and an upside-down try-it, plus a watch-out box
  on diagnosing a subset solution set.

**Verification.** 7 of the 8 worksheet problems are machine-checked with SymPy:
five `solve_interval` runs over $[0^\circ, 360^\circ)$ in degree mode — each
expression stated in factored form, as the skill requires — one `equiv` check that
$\dfrac{\cos^2 x - 1}{\cos x - 1}$ really is $\cos x + 1$, and two `eval` checks
that carry the numerical counterexamples. Problem 2 carries two entries under one
id so both the symbolic simplification and its numeric test are bound. The
$\sin\theta - \cos\theta = 1$ problem is the interesting one: the verifier
confirmed root *completeness* numerically, which is exactly the property Ola's
squared equation destroys. All 6 study-guide results are machine-checked.
Problem 8 is a genuinely open explanation and is declared `{"type": "manual"}`;
the build exits 2 with one manual-review item, and it is nowhere described as
machine-verified.

Two planted wrong results are declared as machine-checked misconception traps
(0.5 and 1.75), both proved distinguishably wrong and derived from the stated
wrong method. The other five planted errors are **lost-solution** errors, where
the wrong answer is a solution *set* that is a strict subset of the correct one
rather than a single number. The `traps` field is scalar-only by design (it is
allowed on `approx`, `eval`, `triangle`, `slope`, … but not on `solve_interval`),
so those five could not be declared as traps. They are instead bound the other
way round: every angle in each student's wrong list is one of the verified roots,
so the printed wrong answers cannot drift from the verification data, and each
lost angle is re-checked by substitution in the answer key.

**Standards.** Identity and equation problems are tagged `HSF-TF.C.8` ("Trig
identities") and the $\sin\theta - \cos\theta = 1$ problem
`HSF-TF.A.2, HSF-TF.B.5` ("Trig functions & unit circle"), both copied verbatim
from `references/standards-map.md`. This covers the task's `HSF-TF.C.8`
reference; no code was invented.

**Gate-log note.** Worksheet prose matched 31 of 34 numbers. The flags are the
"$2$" in "$2\theta$", the "$4$" in "$4\sin^2\theta$" (a coefficient absorbed into
the factored form the checker verifies), and $270^\circ$ — which is one of Ola's
*extraneous* candidates and therefore correctly absent from the verified solution
set. Study-guide flags are intermediate decimals inside the worked example (0.36,
0.4, 0.64) and the same coefficient $4$. No computed final value is unbound.
