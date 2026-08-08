# Locating Zeros and Turning-Point Constraints — three PDFs

A 12-problem precalculus fluency set, plus the worked answer key and a two-page
study guide.

| File | What it is |
|---|---|
| `ss_polyzeros_curr407.pdf` | Study guide (2 pages) |
| `ws_polyzeros_curr407.pdf` | Student worksheet, 12 problems (6 pages) |
| `ak_polyzeros_curr407.pdf` | Step-by-step answer key (3 pages) |

**The ramp.** Problem 1 is a factorable quadratic; problem 12 reconstructs a
degree-4 polynomial from its zeros and one point and then argues how many
turning points its graph actually has. No two problems use the same factoring
route — common factor, difference of squares, quadratic in x², grouping, and
finally division by a known factor to expose a fractional zero.

Three strands alternate throughout:

* **Factoring to locate zeros** (#1, #4, #6, #8, #10). #10 is the important one:
  its zeros are 3, ½ and −2, and the ½ is exactly the zero an integer-guessing
  search never finds.
* **Multiplicity against degree** (#3, #7, #11). #11 is the deliberate trap —
  `x⁵ − 4x³` has a repeated factor at 0, but the multiplicity is 3, which is
  odd, so the curve crosses rather than touching.
* **Turning-point bounds** (#2, #5, #9, #12) — the n−1 bound, and then #9 and
  #12 push from the other side: how *few* turning points the graph can have,
  given where the zeros are.

**How much is machine-checked — honestly.** There are 20 responses across the 12
problems. **16 were recomputed with SymPy** — every zero list, every
factorisation, the limit, both turning-point counts, and the leading
coefficient. **4 are instructor-judged** and marked `---` in the Quick Answers
bank: the written halves of #3, #9, #11 and #12, which ask for multiplicities
with their crossing behaviour or for an argument about how many turning points
must occur. The key's "What is verified" note names those four.

Each carries a grading note. On #9, for example, an answer that simply asserts
"at least two" gets no credit — the gap argument between consecutive zeros is
what is being taught, and the note says so.

All six study-guide items are fully machine-verified.
