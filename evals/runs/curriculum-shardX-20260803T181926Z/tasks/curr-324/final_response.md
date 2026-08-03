Three PDFs are ready for a high-school geometry student on right triangles,
focused on the three errors that actually cost marks in this unit: the **wrong
ratio**, an **inverse taken upside down**, and a calculator left in **radian
mode**.

- **Worksheet** (6 problems, `ws_righttri_curr324.pdf`) — all six problems turn
  on one of those three errors. Problem 1 asks for the side opposite a given
  angle from the hypotenuse (sine, where cosine is the tempting wrong choice);
  problem 4 asks for the *adjacent* leg from the hypotenuse and says outright
  that a classmate reached for sine; problem 6 is a 30-60-90 triangle where the
  student must find the short leg and then identify whose side Sasha's $8.66$
  actually is. Problems 2, 3 and 5 are find-and-fix items: Dana's correct
  tangent setup returning $-84.75$ (radian mode), Eli's
  $\tan^{-1}(24/7)=73.74^\circ$ (sides inverted), and Ravi's flagpole height of
  $12.41$ ft that is too small for a $38^\circ$ elevation. That is three
  find-and-fix items, above the two the request asked for.
  Every triangle figure is rendered by `scripts/render_figures.py` from the same
  `given`/`expr` values the verifier checks, so no figure can disagree with its
  answer; a value-free reference figure at the top fixes the $a/b/c$ labelling
  convention. Work space is 4.5–5 cm of writing room under each figure, declared
  as `workspace_cm: 9` per problem so the page budget charges for the figure too.
- **Answer key** (`ak_righttri_curr324.pdf`) — four to five numbered steps per
  problem: name the two sides involved, choose and justify the ratio, compute in
  degree mode, box the answer, and sanity-check it. Each find-and-fix solution
  separates the *setup* from the *execution* (Dana's and Ravi's setups are
  correct; only the mode is wrong) and says what the wrong number actually is —
  Eli's $73.74^\circ$ is the complementary angle of the same triangle, Sasha's
  $8.66$ is the other leg, the classmate's $13.12$ is the opposite side. It
  carries the generated quick-answer bank and the generated "Common wrong
  answers" block.
- **Study guide** (2 pages, `ss_righttri_curr324.pdf`) — three sections matching
  the worksheet's skill tags: pick the ratio that fits your two sides
  (SOH-CAH-TOA plus the special-triangle ratios), inverse trig for a missing
  angle (including the inverse-versus-reciprocal distinction and the
  bigger-side-faces-the-bigger-angle check), and degree mode with the two checks
  that catch a mode error instantly ($\sin 30^\circ$ must read $0.5$; a leg must
  be shorter than the hypotenuse). Each has a rule box, a two-step worked
  example, and an upside-down try-it, plus a watch-out box on the asymmetry that
  makes wrong ratios so hard to catch: a mode error usually produces an absurd
  number, a wrong ratio produces a believable one.

**Verification.** All 6 worksheet answers and all 6 study-guide answers are
machine-verified with SymPy — four `approx` trigonometric computations, two
`triangle` solves from raw givens, and no `manual` items, so the build finished
all-green (exit 0) rather than with manual-review flags. **Six planted wrong
answers are declared as misconception traps** ($9.83$, $-84.75$, $73.74$,
$13.12$, $12.41$, $8.66$): the verifier recomputed each wrong method and proved
both that the printed wrong number really is what that method produces and that
the problem's own check rejects it.

**Standards.** Every problem is tagged `HSG-SRT.C.8` (right-triangle trig:
solving for sides and angles, elevation and depression), taken verbatim from
`references/standards-map.md`. The grade level prints on the answer key only,
in the generated Curriculum section.

**Gate log.** All 22 gates green. Worksheet prose matched 94.7% of its numbers
against the JSON givens — the single flag is the $45^\circ$ used in a
sanity-check sentence, which is a reference angle rather than a given. The study
guide reports 87.0%: the flags are unrounded intermediate values
($7.0420\ldots$, $22.6198\ldots$) shown inside worked examples.
