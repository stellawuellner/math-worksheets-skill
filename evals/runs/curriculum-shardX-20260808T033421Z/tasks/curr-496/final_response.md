# Geometric Series, p-Series, and the nth-Term Test — AP Calculus BC

Three PDFs are ready:

- **`ws_series_curr496.pdf`** — the student worksheet, 8 problems.
- **`ak_series_curr496.pdf`** — the full step-by-step answer key.
- **`ss_series_curr496.pdf`** — a 2-page study guide.

## What the worksheet covers

Every problem is about recognising which of three tools applies, and each idea
is introduced through something concrete before the notation is asked for:

- **A table of partial sums** opens problems 1 and 5, so the student can *see*
  the sums climbing and flattening before writing the closed form. Problem 1
  then asks what the table can and cannot prove — a distinction worth making
  early.
- **A bouncing ball** (problem 4) is the geometric series as a physical
  quantity: the first drop plus an infinite up-and-down sequence, total 8 m.
- **A repeating decimal** (problem 7): $0.\overline{45}$ written as a series and
  summed to $\tfrac{5}{11}$, then generalised to every repeating decimal.
- Problems 3, 6 and 8 drill the nth-term test, including the case students most
  often mishandle — $n\sin(1/n)$, where the terms *look* like they shrink and
  do not.

Problem 8 puts all three tools side by side: one series converges, one fails on
the exponent, one fails on the terms.

## Verification — what a machine checked, what you check

The answer key's "What is verified" note reports the same split.

- **10 of the 16 checks are machine-verified with SymPy**: every series sum
  (evaluated to closed form, including $\tfrac{\pi^2}{6}$, $\tfrac{\pi^4}{90}$
  and $\tfrac{5}{11}$) and every limit of terms.
- **6 are instructor-judged** — the written half of problems 1, 3, 5, 6, 7 and
  8. These are the parts that carry the concept: what a table of partial sums is
  and is not evidence for; why the nth-term test only proves divergence; why
  $n\sin(1/n)$ does not shrink; why every repeating decimal is rational. Each
  has a rubric in the answer key stating what full credit requires.

That is a high proportion of open response, and it is deliberate — this is a
classification sheet, and classification is an argument, not a number.
Nothing is marked `[unchecked]`: every printed answer slot has an entry.

## Notes

- Problem 2 assumes the student knows $\sum 1/n^2 = \pi^2/6$; the stem says so
  explicitly rather than expecting them to derive it.
- The study guide's three sections match the three tools, and each formula box
  leads with the *test* (how you recognise the type) before the value formula,
  which is the order the worksheet asks for.
- The grade level and the LIM-7 tagging print on the answer key only.
