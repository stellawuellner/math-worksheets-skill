# Complex numbers — sign and conjugate errors (Algebra 2)

Three PDFs are ready:

- **Worksheet** (`ws_complexsigns_curr354.pdf`, 4 pages) — 8 problems, all on
  diagnosing sign and conjugate errors: subtracting a complex number (distributing
  the minus to both parts), multiplying with $i^2 = -1$, the conjugate product,
  two "find the mistake" items, a division by the conjugate, a quadratic with a
  conjugate pair of solutions, and all four zeros of $x^4 - 16$.
- **Answer key** (`ak_complexsigns_curr354.pdf`, 2 pages) — full step-by-step
  reasoning for every problem, a quick-answer bank at the top for fast grading, a
  generated Curriculum section (standards HSN-CN.A.1–A.3 and HSN-CN.C.7–C.9,
  difficulty 1–5), and a "common wrong answers" line for each declared trap so you
  can tell at a glance which misconception a wrong answer came from.
- **Study guide** (`ss_complexsigns_curr354.pdf`, 2 pages) — three sections
  (sign rules for $+,-,\times$; dividing with the conjugate; non-real solutions
  come in conjugate pairs). Each has a rule box, a worked example that starts by
  saying *why* that tool applies, and a separate try-it with the answer printed
  upside down inside the box.

**Find-and-fix items (2, as requested).** Problem 4 plants "$(7-3i)(7-3i)=58$" —
the value of the *conjugate* product, used where the same factor was squared;
problem 6 plants a denominator of 8 for $(3+i)(3-i)$, the classic "$i^2=+1$"
subtraction. Both planted numbers are declared as machine-checked misconception
traps, so SymPy confirmed each wrong number really is what the wrong method
produces AND that the problem's own check rejects it. A third trap (21 for
$(5+2i)(5-2i)$) is declared on problem 3.

**What was verified.** Every numeric answer was recomputed by SymPy: 9 of the 10
checks passed automatically (8 problems, two of which carry two checks). The one
item flagged for **manual review** is problem 4(a) — "explain which factor she
should have multiplied by" — a written explanation, which no CAS can grade. The
key gives the model answer and says what earns credit. Problem 6(a) also asks for
an explanation, but its numeric half (the correct denominator, 10) is machine-checked.

Layout, work space, answer blanks, page budget, the study guide's structure, and
the binding of every boxed answer to the verified value all passed the build gates.
