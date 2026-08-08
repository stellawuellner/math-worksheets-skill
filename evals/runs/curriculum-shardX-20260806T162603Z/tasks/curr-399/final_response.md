# Find-the-mistake set: signs and denominators in conic equations

Three PDFs for your Algebra 2 student, all on **diagnosing sign and denominator errors in
conic equations**:

- **`ws_conicerr_curr399.pdf`** — the student worksheet, 8 problems, 4 pages.
- **`ak_conicerr_curr399.pdf`** — the full step-by-step answer key, 4 pages.
- **`ss_conicerr_curr399.pdf`** — a 2-page study guide.

## The three errors the sheet is built around

Almost every conic mistake a student makes is one of three things, and each of the eight
problems quotes a real wrong answer produced by one of them:

| The error | Problems |
|---|---|
| **Sign** — reading $(x+5)$ as a centre of $+5$, or copying a linear coefficient without halving and reversing it | 1, 6, 8 |
| **Denominator** — assuming the $x$ term always carries the major axis, or reporting $r^2$ as $r$, or inverting an asymptote ratio | 2, 3, 7 |
| **Add versus subtract for the foci** — using the ellipse rule on a hyperbola and the reverse | 4, 5 |

Problems 4 and 5 are a deliberate pair: the same mistake in both directions, so the student
sees that "subtract" and "add" are not interchangeable habits but consequences of the sign
between the two terms. The key attaches the sanity check to each — an ellipse's focus must
land *inside* its vertex, a hyperbola's *beyond* it — which catches the error without any
further arithmetic.

Problems 1, 3, 6 and 8 are the full find-and-fix items: correct the value **and** write the
diagnosis. Problem 8 is the challenge, with two different students making two different
mistakes on one equation; the student has to name them separately.

## The planted wrong answers are machine-checked

Every quoted wrong value is declared as a misconception trap, recomputed by the verifier, and
confirmed to be *distinguishably* wrong. Ten traps are declared across the eight problems,
and the answer key prints them in a **Common wrong answers** block — so a wrong answer on the
page tells you which of the three error families the student is carrying, rather than just
that they missed it.

## What was verified, and what was not

The key's generated note says it exactly: **11 of the 15 answers are machine-checked with
SymPy; 4 are instructor-judged.**

- **Machine-checked (11):** every corrected centre coordinate, radius, semi-axis, focal
  distance and asymptote slope was recomputed independently from the printed equation. The
  two completing-the-square problems were checked from their original coefficients, not from
  my rearrangement.
- **Instructor-judged (4):** the written diagnoses in **1(b)**, **3(b)**, **6(c)** and
  **8(c)**. Error analysis is two responses, not one: the correction is a value and can be
  checked, the diagnosis is prose and cannot. Each is marked `---` in the Quick Answers bank
  rather than given a value, and the key states what full credit needs — for 6(c) and 8(c) in
  particular, that *two distinct faults* be named, since describing one error twice or calling
  both "careless arithmetic" is exactly the response that looks right and diagnoses nothing.

## Study guide

Three sections, each with a rule box, a worked example whose first step names the decision
being made, and a try-it with the answer upside down inside the box: the sign flip in the
centre (with the halve-then-reverse pair spelled out), comparing denominators before deciding
which axis is major, and add-versus-subtract for the foci with the inside/outside sanity check
attached. All 14 of its worked values are machine-verified.
