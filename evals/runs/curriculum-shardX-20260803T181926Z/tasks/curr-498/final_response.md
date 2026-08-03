# Intervals of Convergence with Endpoint Checks — AP Calculus BC

Three PDFs are ready: the student worksheet, a full step-by-step answer key, and
a two-page study guide.

**Worksheet (6 pages, 8 problems).** Every problem is an interval-of-convergence
problem, and the sheet is built as four short chains rather than eight unrelated
series, so the student sees the whole procedure end to end twice. Problems 1–4
work one model all the way through: ratio test on a pressure-sensor series,
endpoints from center and radius, then each endpoint substituted and settled
separately — the left one converges (alternating harmonic), the right one
diverges (harmonic), giving the asymmetric interval $[2, 6)$. Problems 5–6 do
the same for a control-loop gain model where both endpoints converge. Problem 7
is the case with no endpoints at all ($L = 0$, infinite radius) and asks the
student to say why. Problem 8 closes with an energy model whose terms grow, so
both endpoints fail the $n$th-term test.

Each series is stated with its input variable and unit (bars, volts, kelvins
above a reference, dimensionless), and the directions block spells out the
four-move procedure the sheet drills. Difficulty ramps 1 → 5.

**What was machine-verified.** Eleven separate checks were recomputed with
SymPy and the build was blocked until all agreed with the answer key: the four
ratio-test limits ($\tfrac{1}{2}$, $\tfrac{1}{5}$, $0$, $\tfrac{1}{3}$), the two
endpoint arithmetic results ($x = 2$ and $x = 6$ bars), and every endpoint sum
evaluated exactly — $\sum (-1)^n/n = -\ln 2$, $\sum 1/n = \infty$ (divergence
confirmed, not assumed), $\sum 1/n^2 = \pi^2/6$, $\sum (-1)^n/n^2 = -\pi^2/12$,
and $\sum 1/n! = e$. The answer key's boxed values were bound problem by problem
against those results, so no printed answer can drift from what was verified.

**Flagged for manual review.** Problem 8(b)–(c) asks the student to test both
endpoints in words, name the test that settles each, and justify the bracket
given to each. That is open reasoning and is not machine-checkable, so it is
labelled manual. The answer key gives a full model answer plus a grading note
naming the specific error to watch for: reaching for the alternating series test
at $x = -2$, where the terms increase without bound and only the $n$th-term test
applies.

**Study guide (2 pages).** One section per move — ratio test and radius,
endpoints from center and radius, substituting an endpoint, deciding at each
endpoint — each with a rule box, a worked example whose first line says why that
tool applies, and a try-it with the answer printed upside down inside the box.
The watch-out box names the two classic errors: treating $a_n \to 0$ as proof of
convergence, and copying one endpoint's bracket to the other. All four worked
examples and all four try-it answers were verified by the same gate as the
worksheet.
