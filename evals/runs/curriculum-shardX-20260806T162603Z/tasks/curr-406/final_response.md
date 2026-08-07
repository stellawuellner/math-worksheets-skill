# Using End Behavior and Multiplicity to Sketch Polynomials — three PDFs

A 10-problem precalculus set that builds the sketch from its two deciding
features, plus the worked answer key and a two-page study guide.

| File | What it is |
|---|---|
| `ss_polysketch_curr406.pdf` | Study guide (2 pages) |
| `ws_polysketch_curr406.pdf` | Student worksheet, 10 problems (6 pages) |
| `ak_polysketch_curr406.pdf` | Step-by-step answer key (3 pages) |

**How the sheet teaches it.** Three strands alternate, and the sketching
problems come only after both ingredients have been practised separately:

* **Zeros and multiplicity** (#1, #3, #6, #8) — factor, then read the exponents.
  #3 asks directly which zero the curve crosses and which it only touches, and
  why; #8 needs factoring by grouping before the zeros appear.
* **End behavior** (#2, #4, #7) — stated as limits, so the notation and the idea
  arrive together. #4 asks for both ends of an even-degree polynomial; #7 asks
  for one end of an odd-degree one and then for the rule in words.
* **Assembling the sketch** (#5, #9, #10) — each of these prints a full
  coordinate grid to draw on, with the zeros and the y-intercept computed first.
  #10 is the reverse problem: given the zeros with their multiplicities and one
  point, find the leading coefficient and then draw the curve.

**How much is machine-checked — honestly.** There are 17 responses across the 10
problems. **12 were recomputed with SymPy** — every factorisation, every zero
list, every limit, and both intercept values. **5 are instructor-judged** and
marked `---` in the Quick Answers bank: problems 3, 5, 7, 9 and 10.

Those five are the three sketches and the two written explanations. A drawing
cannot be machine-checked, so the key prints a specific rubric for each: for #5,
the curve must cross at −2, touch at 1 without crossing, pass through (0, 2),
fall to the lower left and rise to the upper right — and a sketch that crosses
at 1 should be marked down, because the squared factor is the whole point of the
item. The key's "What is verified" note names all five.

All six study-guide items are fully machine-verified.
