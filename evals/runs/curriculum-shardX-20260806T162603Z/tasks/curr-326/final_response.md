Here are the three PDFs for the distance-and-midpoint set:

- **Worksheet** — `ws_coordinate_curr326.pdf` (4 pages)
- **Answer key** — `ak_coordinate_curr326.pdf` (3 pages)
- **Study guide** — `ss_coordinate_curr326.pdf` (2 pages)

**What the worksheet covers.** Eight problems, every one of them computing a
distance or a midpoint from coordinates. The sheet is built to develop the two
models behind the formulas rather than just drill them: distance as the
hypotenuse of the gap triangle, midpoint as a pair of averages. Two problems
include a blank grid so the student can plot and sanity-check; plotting is
optional and the grids carry no data.

The ramp runs from a whole-number distance and midpoint, through a
work-backwards item (given the midpoint and one endpoint, find the other), a
city-map application, and a conceptual "why does averaging land on the segment",
to a closing problem where the midpoints of both diagonals of a quadrilateral
come out equal and the student says what that means.

**What is verified, honestly.** The verification file holds 13 entries, one per
response.

- **11 entries are machine-checked** with SymPy: 10 units, (1, 4), 13 units, the
  two coordinates 7 and 8 of the missing endpoint, 15 blocks, (−2, −1), 13 units
  with midpoint (3, 1.5), and both diagonal midpoints (1, 0). **6 of the 8
  problems are fully machine-checked end to end.**
- **2 entries are instructor-judged**: problem 6(b) (why averaging gives a point
  on the segment) and problem 8(c) (what two equal diagonal midpoints tell you).
  Both are written reasoning; the key prints a grading rubric for each, and the
  "What is verified" note names problems 6 and 8.

One design point worth flagging: problem 4 gives the midpoint and one endpoint
and asks for the other. Its check **computes the missing endpoint** — both
coordinates, as 2M − A — rather than feeding the answer back in to reproduce the
given midpoint. A check of that second kind cannot fail and would print the
given as the answer; this one genuinely verifies (7, 8). The bank row reads
`x-coordinate of B = 7, y-coordinate of B = 8`.

Nothing is marked `[unchecked]`. Four problems carry declared misconception
traps, so the key's "Common wrong answers" block identifies a student who added
the two gaps instead of using the theorem (14 units, 21 blocks, 17 units) or
subtracted the squares instead of adding them (10.91 units).

**Study guide.** Three sections: the distance formula with the right-triangle
picture it comes from, the midpoint formula as a pair of averages, and working
backwards from a midpoint to a missing endpoint. Each has a rule box, a worked
example that opens with the reasoning, and a try-it printed with its answer
upside down. The watch-out box separates walking distance along the grid from
straight-line distance — the error the first trap is built from.
