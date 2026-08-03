# Linear Equations: One, No, or Infinitely Many Solutions — Grade 8 / Pre-Algebra

Three PDFs are ready:

- **Worksheet** (`ws_classifying_curr213.pdf`, 5 pages) — 10 problems. A boxed
  decision guide at the top states the three signs (different $x$-terms → one
  solution; same $x$-term, different constants → no solution; identical sides →
  infinitely many), and every problem asks the student to *classify*, not just to
  solve. 6–6.5 cm of work space per single-part problem and 3.5–4 cm per part on
  the three multi-part problems, because "show both sides simplified" is the work
  that matters here.
- **Answer key** (`ak_classifying_curr213.pdf`, 2 pages) — quick-answer bank, then
  each solution simplified line by line, ending with the sentence that names *why*
  the classification follows (what was left after the variable terms cancelled, or
  why they could not cancel). The two open-response items get a full model
  explanation the grader can compare against.
- **Study guide** (`ss_classifying_curr213.pdf`, 2 pages) — four sections: one
  solution, no solution, infinitely many, and building an equation to order (find
  the coefficient that forces a chosen case). Each has a rule box naming the sign
  to look for, a two-step worked example and a try-it.

## Contexts and coverage

Applications carry the ideas rather than decorating them: two saving plans (they
meet once), two printers running at the same rate (they never meet — with a table
to fill in so the constant 5-page gap is visible before the algebra), a rectangle's
perimeter written two ways (an identity), two gym memberships, and two ride
companies with equal per-mile rates. All 10 problems ask for a classification.

Facets are tagged per verification entry, so the mixed problem 9 is tagged
honestly — its three parts are `no-solution`, `infinitely-many` and `one-solution`
respectively. Facet mix: one-solution ×4, no-solution ×4, infinitely-many ×3,
classify-and-justify ×3, with a maximum same-facet run of 2. Difficulty ramps
1 → 5.

## Verification

**14 checks over 10 problems: 12 machine-verified, 2 manual.**

- One-solution equations are verified with `solve` against the exact root list.
- No-solution equations are verified with `solve` returning the **empty** root set
  — the CAS confirms there is no value that works, rather than my asserting it.
- Infinitely-many equations are verified with `equiv`: the two sides are proved to
  be the same function, which is precisely what "true for every $x$" means.
- Problem 8's expansion is verified with `expand` (`3(2x−1) = 6x−3`), which is what
  pins $a = 6$.

The 2 manual items are the genuinely open ones and are labelled as such on the
sheet and in the key: problem 8(c) "explain why matching $x$-coefficients with
different constants forces no solution" and problem 10(b) "explain what no
solution means for the two companies' prices". No CAS can grade a justification,
so they are declared `{"type": "manual"}` rather than dressed up as verified; the
build reports them and exits 2, which is the correct outcome for this sheet.

Standard `8.EE.C.7` (linear equations in one variable) on every problem, taken
verbatim from `references/standards-map.md`.

Gate verdict: **BUILD PASSED — all gates green, 2 manual-review items (exit 2)**.
