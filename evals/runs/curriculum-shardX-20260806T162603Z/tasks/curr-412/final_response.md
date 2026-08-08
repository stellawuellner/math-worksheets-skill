# Solving Logarithmic Equations with Domain Checks — three PDFs

A 12-problem precalculus fluency set, plus the worked answer key and a two-page
study guide.

| File | What it is |
|---|---|
| `ss_logdomain_curr412.pdf` | Study guide (2 pages) |
| `ws_logdomain_curr412.pdf` | Student worksheet, 12 problems (5 pages) |
| `ak_logdomain_curr412.pdf` | Step-by-step answer key (3 pages) |

**How the sheet is built.** It ramps from a one-step conversion (#1) to a
condensed natural-log equation with an extraneous root (#12), and no two
problems share a skeleton. Three methods rotate through the set:

* **Convert to exponential form** (#1, #4, #7, #10) — including a reciprocal
  base and a fractional exponent.
* **Equate arguments** (#2, #5, #8) — #8 is the deliberate twist: its argument
  is a quadratic, so the negative candidate `x = -8` is a genuine solution.
  Students trained to discard negatives on reflex will lose it.
* **Condense, then solve** (#3, #6, #9, #11, #12) — the four hardest are written
  as two parts: **(a)** state the domain the arguments force, **(b)** solve and
  keep only what (a) allows. Writing the domain first is the whole point;
  problems 6, 11 and 12 each produce a candidate the domain rejects.

**How much is machine-checked.** All 16 answers — the 12 solutions plus the four
domain inequalities — were recomputed with SymPy and matched against the key
before the PDFs were produced, as were all six study-guide items. **Nothing is
flagged for instructor judgement on this sheet**; every question asks for a
value or an interval, so every printed answer carries a machine guarantee, and
the key's "What is verified" note says so.

Three misconception traps are declared and machine-tested: on #6, #11 and #12
the verifier confirmed that keeping the extraneous root produces an answer the
problem's own check rejects. The key prints these under "Common wrong answers",
so if your student hands back `x = 5, -2` on #6 you know immediately that they
solved the quadratic correctly and skipped the domain test — a different
conversation from an arithmetic slip.

Standards on the key: HSF-LE.A.4 (definition of a logarithm) and HSF-BF.B.5
(log properties), with the problems each covers listed.
