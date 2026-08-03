# Computing Distance and Midpoint from Coordinates (High School Geometry)

- **Worksheet** (`ws_coordgeo_curr326.pdf`) — 8 problems, 4 pages. It opens with a
  single value-free reference figure on a grid: the segment $AB$ with its horizontal
  and vertical legs dashed in, so the distance formula is introduced as the
  Pythagorean theorem rather than as a string to memorise, and the midpoint is named
  as an average rather than a length. The figure carries the labelling convention
  ($A(x_1,y_1)$, $B(x_2,y_2)$, $M$) and no values, so it cannot be mistaken for any
  problem's data. Then: 4 distance problems (integer answer, negative coordinate,
  exact radical $6\sqrt{2}$, and a vertical segment), 3 midpoint problems (including
  a reverse one — find the far endpoint from the midpoint), a two-part median problem
  that needs a midpoint *and* a distance, and a closing coordinate proof. 5–7.5 cm of
  work space per problem.
- **Answer key** (`ak_coordgeo_curr326.pdf`) — every solution names the two legs
  before substituting, shows the substitution line separately from the simplification,
  and adds a check where one exists (recomputing the midpoint to confirm the recovered
  endpoint). The quick-answer bank under the title block prints the three declared
  traps, so "17" or "7" on a paper is immediately readable as adding the legs.
- **Study guide** (`ss_coordgeo_curr326.pdf`) — 2 pages, three sections matching the
  worksheet skills: distance formula · midpoint formula · using midpoints in a
  coordinate proof. Each has a rule box that explains *why* (subtract-then-square
  versus add-then-halve), a two-step worked example, and a distinct try-it with the
  answer upside down; the watch-out box contrasts the two formulas directly, which is
  the confusion this topic actually produces.

## Verification

10 of the 11 verify entries are machine-verified with SymPy — 4 `distance` checks
(including the exact radical form $6\sqrt{2}$, verified symbolically rather than as a
rounded decimal) and 6 `midpoint` checks. Problems 7 and 8 carry multiple entries
against one problem id, which is how the multi-part items are encoded.

**One entry is flagged `manual`, correctly:** the written proof in problem 8. The two
diagonal midpoints it rests on *are* both machine-verified — the sheet proves
$(4, 3.5)$ twice — but the argument that a shared midpoint means the diagonals bisect
each other is prose, so it is encoded `{"type": "manual", ...}` and the key supplies a
model proof plus an explicit look-for list. The build ends at exit 2 for that reason,
which is the right outcome, not a failure. Every other gate is green, first attempt.

Standard `HSG-GPE.B.4–B.7` is taken verbatim from `references/standards-map.md`
("Coordinate geometry proofs"). Three misconception traps (adding the legs instead of
using the Pythagorean form) are declared and confirmed distinguishable. Difficulty
ramps 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4 across the entries.

Gate-log note: two prose flags on worksheet problem 7 (1.2 and 2.6) are the
`leftmargin`/`itemsep` dimensions of that problem's part-list, i.e. layout markup, not
printed values. The study-guide flags are intermediate arithmetic printed inside the
worked examples (legs 8 and 6, their squares 64 and 36, the second diagonal's
endpoints) — deliberate teaching detail.
