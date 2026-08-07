Here are the three PDFs for the coordinate perimeter-and-area set:

- **Worksheet** — `ws_polygons_curr328.pdf` (6 pages)
- **Answer key** — `ak_polygons_curr328.pdf` (3 pages)
- **Study guide** — `ss_polygons_curr328.pdf` (2 pages)

**What the worksheet covers.** Eight problems, all on finding the perimeter or
the area of a polygon given its vertices. The applications are concrete and the
units are stated every time: a city park, an L-shaped patio, two triangular
plots to compare, and a pentagonal community garden. Two problems come with a
blank grid so the student can sketch the figure and sanity-check the answer; the
grids carry no data of their own.

The ramp goes from a right triangle's area, through a four-part perimeter
computation and a shoelace quadrilateral, to a rhombus where equal side lengths
tempt a wrong area, a two-plot comparison, and a five-vertex garden that also
asks why the shoelace method does not care which vertex you start from.

**What is verified, honestly.** The verification file holds 19 entries, one per
response the sheet asks for.

- **17 entries are machine-checked** with SymPy: every side length, perimeter and
  area (54, 10/6/8/24, 24, 72 m², 44 m², 5/5/20/15, 30/36/6, 84 m², 7.21 m).
  **6 of the 8 problems are fully machine-checked end to end.**
- **2 entries are instructor-judged**: problem 5(b), checking the patio area by
  splitting it into two rectangles and showing the pieces add up, and problem
  8(c), explaining why the shoelace total is independent of the starting vertex.
  Both are written work; the key prints a grading rubric for each, and the "What
  is verified" note names problems 5 and 8.

Nothing is marked `[unchecked]`. Two problems carry declared misconception traps,
so the key's "Common wrong answers" block flags a student who forgot to halve a
right triangle's leg product (108 square units) or multiplied two adjacent sides
of the rhombus as though it were a rectangle (25 square units).

**Study guide.** Three sections: perimeter from coordinates (with the shortcut
that horizontal and vertical sides need no square root), area by the shoelace
method, and area by splitting a grid-aligned shape into rectangles — presented
as the independent check on a shoelace answer, since the two methods share no
arithmetic. Each has a rule box, a worked example that opens with the reasoning,
and a try-it with its answer printed upside down. The watch-out box is the
rhombus trap: four equal sides do not make a square.
