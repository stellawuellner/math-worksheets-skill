Three PDFs are ready for a Grade 8 / pre-algebra student on **solving linear
equations that combine the distributive property with fractions**:

- **Worksheet — 12 problems, no two with the same skeleton.** It opens with a
  fully worked pattern (clear fractions → distribute → collect → isolate →
  check) and then ramps 1 → 5: single distribution (1, 2), a negative in front
  of the brackets (4), one LCD clear (3), a fractional coefficient distributing
  over brackets (8), variables on both sides (6), fractions on both sides
  (10), a fraction bar covering a whole numerator (11), and a challenge that
  needs all four moves plus a substitution check (12). Two problems isolate the
  rewriting sub-skill itself — multiply by the LCD (5) and expand a subtracted
  bracket (9) — because those are the two steps students actually lose marks on.
- **Answer key — every step shown, plus the error each problem targets.** Each
  solution names the move before doing it, and most carry either a substitution
  check or a "common error" line with the wrong answer that mistake produces
  (e.g. $x = -12$ from not distributing the negative in problem 2, $x = 19$ from
  a minus sign that only reaches the first term in problem 11).
- **Study guide — 2 pages, four sections**: distribute-then-solve, clear the
  fractions with the LCD, variables on both sides, and rewriting into an
  equivalent form. Each has a rule box, a worked example whose first step says
  *why* that tool is the right one, and a try-it with the answer upside down
  inside the box. It ends with the sign/whole-number-term watch-out.

**Verification:** all 12 worksheet answers and all 8 study-guide answers were
recomputed by SymPy through the build gate — ten worksheet problems as `solve`
(exact root sets) and two as `equiv` (the rewritten expression proved equal to
the original as a function). Nothing is flagged manual: there is no open
response on this sheet. The prose gate also confirmed that every number printed
in a problem is a given in the verification data (48/48). Final verdict:
**BUILD PASSED — all gates green** (worksheet 5 pages, key 3, guide 2).
