# Composite Solids, Surface Area, and Density Design — High School Geometry

Three PDFs are ready:

- **Worksheet** (`ws_composite_curr345.pdf`, 4 pages) — 10 problems, each with its own
  labelled figure and work space beside it.
- **Answer key** (`ak_composite_curr345.pdf`, 3 pages) — quick-answer bank, then each solid
  decomposed piece by piece with the exact multiple of $\pi$ carried to the last line.
- **Study guide** (`ss_composite_curr345.pdf`, 2 pages) — four rules, four worked examples,
  four try-it items.

## What the worksheet practices

An interleaved review: after two warm-up problems the four methods rotate, so the student has
to decide *which* one a problem needs rather than repeat a procedure.

1. **Composite volume** (1, 5, 9) — cylinder + hemisphere, cone + hemisphere, and a
   cylinder + cone hopper whose volume then feeds a density calculation.
2. **Composite surface area** (2, 7) — a drilled plate (two circles removed, one inner wall
   added) and a cone-on-cylinder where the hidden joint circle must *not* be counted.
3. **Density and mass** (3, 6) — steel roller, brass ball.
4. **Reverse design** (4, 8, 10) — solve for a height from a target volume, for a radius from
   a target mass, and a synthesis bollard problem.

Problem 10 is the synthesis challenge: solve the composite-volume equation for the cylinder
height, find the mass, then argue about a second design. Difficulty ramps 2 → 5. Every figure
is labelled only with the values that problem gives, and every answer line prints the unit
the answer must be in (m$^3$, cm$^2$, g, kg, cm).

## Verification

12 checks over the 10 problems. **11 are machine-verified with SymPy** (`approx` checks that
recompute each composite expression exactly and compare at the printed precision, plus one
`solve` check for the box-height design problem); every printed value in the answer key was
then bound back to its own problem's verified value, including its unit.

**One item is flagged for manual review, and it is correctly flagged**: problem 10(c) asks
the student to explain what a fixed volume forces about the two designs' masses and to give a
practical reason for preferring the wider bollard. That is open reasoning — no CAS can grade
it — so it is declared `{"type": "manual"}` in the verification file and the build reports
`BUILD PASSED — 1 verification run(s) flagged manual-review items (exit 2)`. The answer key
gives a full model response for it (both required moves, plus the wrong answer to watch for)
so a parent or teacher can grade it confidently.

## One note on standards tagging

`references/standards-map.md` — the only source the skill permits for standards codes — has
no HSG-GMD or HSG-MG entry. Rather than invent a code, every problem is tagged with the map's
volume code `8.G.C.9` verbatim. The content itself is high-school geometry (composite solids,
density modelling); only the tag is coarser than the topic deserves.
