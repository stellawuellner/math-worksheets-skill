# Authoring brief for eval-run generation

You are producing one eval artifact set per task: a worksheet, a step-by-step
answer key, and a study guide, all three gated and recorded. This is the brief
every generating agent works from, so runs stay comparable across agents.

Read `SKILL.md` first — it is the authoring contract. This file only adds the
things that have actually gone wrong, plus the exact commands for logging.

## Per task

```bash
TASK=curr-123                      # your assigned id
STEM=<short_topic>_${TASK//-/}     # e.g. limits_curr451
D=/tmp/evalbuild/$TASK && mkdir -p $D
python3 evals/run_eval.py next --run "$RUN"   # or read the prompt from task.json
```

Write four files in `$D`:

| File | Contents |
| --- | --- |
| `verify_$STEM.json` | one entry per worksheet problem, `problem_count` = the task's expected count |
| `ws_$STEM.tex` | the worksheet |
| `ak_$STEM.tex` | the answer key |
| `ss_$STEM.tex` | the study guide |
| `verify_ss_$STEM.json` | one entry per study-guide box, in document order |

Then:

```bash
bash scripts/build.sh $D/verify_$STEM.json --outdir $D 2>&1 | tee $D/gate_log.txt
```

Fix whatever it names and re-run until it prints `BUILD PASSED`. Keep the LAST
run's `gate_log.txt` — the judge is entitled to see the chain that passed.

Write a short `$D/response.md` (what you would tell a parent: what the three
documents contain, what was verified, what is flagged manual). Then record:

```bash
python3 evals/run_eval.py record $TASK --run "$RUN" --from $D \
  --response-file $D/response.md \
  --generator-model <your exact model id> --latency-seconds <elapsed>
```

`--generator-model` must be your real model identifier, not the agent name. The
run is designed so acceptance can later be broken down by the model that drove
the skill; a wrong or missing label silently pools two models into one number.

## Fixed since the earlier waves — do NOT work around these any more

The first 150 tasks hit forty real faults. All are fixed. If you find yourself
reaching for one of these workarounds, stop: the bug is gone, and the workaround
now degrades the artifact.

- **Do not print a grade level on the worksheet or the study guide.** Pass it to
  `\wstitleblock` as usual — the macro accepts it and deliberately does not
  print it. It appears on the answer key, in a Curriculum section generated from
  your verify JSON's `standard` and `difficulty` tags. Do not hand-write that
  section, and do not put "Grade 5" in a title, subtitle or running head where a
  student sees it.
- **Blank grids are fine beside graphed problems.** A `\begin{axis}` with
  nothing plotted in it is a plotting workspace, not a valued figure. A sheet of
  graphing problems where some show data and others are empty grids to draw on
  passes the scope gate. Do not delete a grid a problem needs in order to make
  a figure rule go quiet.
- **A mixed number is one value on both sides.** Write it in the JSON as
  `"2 + 3/4"` (sympy has no mixed-number syntax) and print it as
  `\ans{2\,\tfrac{3}{4}}`; the binding gate reads both as 2.75. You do not
  need to box the whole part and the fraction separately.
- **Traps work.** `\commonerror` used to overflow the answer key, so agents
  deleted their declared traps or wrapped the bank in `\raggedright` /
  `\emergencystretch`. Do neither. Declare traps freely — a misconception task
  without them is a worse worksheet.
- **Trap descriptions may contain any character.** `^`, `%`, `&`, `_` are
  escaped for you now. Write the description in plain English.
- **Stem length no longer breaks the page gate.** `check_log.py` reads a wrapped
  log. Name files for clarity, not brevity.
- **`word_problem: true` is a legal field now.** It tells the page budget the
  stem is prose that wraps, charging 1.2cm instead of 0.6cm. It had always been
  read by the budget and rejected by the schema, so the one lever built for
  prose-heavy stems was unreachable — use it before reaching for `workspace_cm`
  when the extra height is stem rather than writing room.
- **`workspace_cm` is a legal field** (0 < cm ≤ 24). If a problem genuinely
  needs more room than its type's default — displayed student work, a
  hand-built figure, a table to fill in — declare it and the page budget will
  charge for it. Do not compress a sheet to hit a ceiling; that is the trade
  this project explicitly rejects.
- **`\skillheading` is gated at 57 characters** before compile. Name the skill
  in plain words; leave the slug to the JSON, which is what the coverage gate
  actually reads.
- **A RANGE row is a range, not a tag.** `HSG-CO.A–HSG-CO.D` and
  `HSF-IF.A–HSF-IF.C` name a span of clusters; copying the whole string into a
  problem's `standard` tags it with something meaningless. Tag the specific
  cluster inside the range that the problem exercises (`HSG-CO.B`), which is
  usually what the task's own `standard_refs` already names. Slash rows
  (`3.OA.A.3 / 4.OA.A.2`) split the same way — pick the on-grade one, and never
  print a grade-2 code on a kindergarten key.
- **Nothing machine-compares your `standard` against the task's
  `standard_refs`.** Curriculum alignment is judged by reading, so a code from
  the map that differs textually from the task's phrasing is fine. Checked
  directly in `evals/score_eval.py` and the rubric — neither mentions the field.
- **`standards-map.md` gained 26 rows** (grades 6–8 geometry/ratio/statistics,
  grade-8 number system, HS congruence, similarity, complex numbers, vectors,
  matrices, statistics, sequences, binomial theorem, radicals). Check it again
  before concluding a code is missing. If it still is, say so in `response.md`
  and leave `standard` off rather than tagging an off-grade code — but a
  genuinely missing row is now rare.

## Traps that remain, and how to avoid them

- **Any inline expression wider than about half a box line needs display math.**
  Inline math has no break point, so the surrounding prose cannot absorb it —
  and a `formulabox`'s mdframed inset makes the study guide bite at widths the
  worksheet survives. It is not only `\dfrac`: an inline `\sqrt` over
  subscripted binomials overflowed by 22pt, and a row of three inline formulas
  separated by `\quad` by 11pt. Put them in `\[ ... \]`.
- **Draw grid lines you can actually see.** `[gray!30, very thin]` at a 0.33cm
  unit renders as effectively blank paper at reading size; `[gray!55, thin]` at
  0.38cm is legible. No gate catches this — `check_overprint` and `check_log`
  both pass an unreadable grid — and visual/print quality is a scored dimension.
  Render a page and look at it.

- **In a STUDY GUIDE, `\ans{}` must sit inside `$...$`.** The preamble defines
  it as `\boldsymbol`, which is math-only; `\akheader` renews it to a text-mode
  boxed form, so the same markup that is correct in an answer key is a fatal
  `! Missing $ inserted` in a study guide. Every ss exemplar in
  `references/latex-templates.md` happens to write `$\ans{...}$` and none says
  why. (Checked: `\ans{2}` in ss prose gives four errors, `$\ans{2}$` gives
  none.)
- **A claim that did NOT reproduce, recorded so nobody re-derives it.** One
  author reported that `\ans{}` starting a paragraph in an ANSWER KEY is a fatal
  `\unskip` in vertical mode, and edited 13 call sites. The `\unskip` is real —
  it is the first token of the text-mode branch — but six probes (top-level,
  inside `\problem`, after a display, after an itemize, after a center, with
  `\meaning` confirming the text-mode branch was active) all compiled clean and
  printed the box. Whatever failed in that build, this was not it. Put `\ans{}`
  where it reads best.

- **A presentation-only misconception can never be a distinguishable trap.**
  "Left the fraction improper instead of regrouping" is `3 + 9/6` against a
  correct `4 + 1/2` — the same number, so the problem's own check accepts it and
  the trap gate rejects the declaration, correctly. Unsimplified, unreduced and
  improper-vs-mixed all have this shape. Declare an error that changes the
  VALUE ("added the denominators too"), and handle presentation in the prose.
  (Checked by running both.)
- **`at` accepts expression strings, exactly like `expected`.**
  `"at": {"a": "2 + 3/8"}` goes through the same parser, so a mixed-number sheet
  verifies as exact rational arithmetic and the stem's 2, 3 and 8 all count as
  givens for the prose checker. The docs stated this only for `expected`.
- **A study-guide box may carry SEVERAL entries under one id.** The rule is box
  count = `problem_count` = number of distinct ids — not one entry per box. Two
  authors read the older wording as a prohibition. Use it when an example needs
  a distance AND the perimeter built from it: the extra entries make the
  example's givens machine-checked instead of unexplained prose numbers.
- **tikz `scale=` does not scale node text.** Captions under scaled shapes
  collide; the overprint gate catches it, but put the labels in a `tabular` row
  instead and it cannot happen.

- **`\ans{}` MUST NOT start a paragraph in an answer key — that is a fatal
  error, and it is the opposite of the study-guide rule.** `\akheader`
  redefines `\ans` to a compact end-of-proof form beginning with `\unskip`,
  which needs horizontal mode; a blank line before it gives
  `! You can't use '\unskip' in vertical mode` and no PDF at all. Attach it to
  the end of the preceding line. In a STUDY GUIDE `\ans` is `\boldsymbol`,
  used inside math, and there a blank line before it is correct. One author had
  to edit 13 call sites in a single key after following the study-guide rule.
- **Every distinct `answer_unit` on a problem needs its own `\answerline`.**
  A problem answering in both m and s must print both lines; declaring two and
  printing one used to pass, because only the first declaration was read.

- **Thousands separators are safe on both sides.** `4{,}187` and `4,187` are
  normalised by the prose checker and the answer-key binder alike. Do not strip
  them from a grade 2–5 place-value sheet; one author did, on an inference from
  an incomplete grep, before testing and finding both forms report 100%.
- **An `at` binding the expression never uses donates nothing.** Listing a
  problem's other givens under `at` to quiet the prose report no longer works —
  only keys the `expr` actually references count as verified givens. If a number
  is printed in the stem and nothing checks it, the report is right to say so.
- **`equiv` on a rational expression is the clean encoding for polynomial long
  division**: `"expr": "(P)/(D)", "expected": "Q + R/(D)"` verifies the division
  as an identity AND makes the `expected` string literally the boxed answer, so
  the key binds by construction.
- **`estimate` needs every operand to survive its place.** `4187*6 @ thousand`
  rounds the 6 away; so does `632/8 @ hundred`. Both now say so by name. For a
  compatible-numbers estimate write two entries — an `estimate` that rounds the
  large number, then an `eval` that combines it with the exact small one, which
  is the two steps the key shows anyway.
- **Inline math longer than a few tokens inside a bulleted item will overfull.**
  Inline math has no break point, so the surrounding prose cannot absorb it.
  Put it in `\[...\]` inside the item. Same class as the `\dfrac` width hazard
  below, and it bit a distance-formula bullet by 53pt.

- **Sub-part labels: `\item[(a)]`, never `[label=(\alph*)]`.** The brief says to
  use `itemize` and not `enumerate` for directions and sub-parts, and `\alph*`
  is an enumerate counter — inside an `itemize` it raises
  `! Missing number, treated as zero`, which `check_log` fails, and the error is
  reported at the `\end{itemize}` rather than at the option that caused it.
  Write the labels out. (Checked directly: `[label=(\alph*)]` produces the
  errors, `\item[(a)]` compiles clean.)
- **A trap on a complex-valued problem works now.** It used to crash the whole
  run with "error evaluating problem N: Cannot convert complex to float" — a
  message naming the problem rather than the trap, so it read like a bad `expr`.
  Two authors designed every complex-number misconception around a real-valued
  wrong result because of it. Declare the trap that belongs to the error.
- **En-dashed standards codes are safe.** `HSN-CN.A.1–A.3` with a literal U+2013
  compiles clean through the generated Curriculum block under the pdflatex
  fallback, despite the "ASCII only in templates" rule elsewhere. Copy the map's
  string exactly; do not invent an ASCII-fied code.

Not bugs — real constraints the checkers enforce. Every one cost an earlier
agent a rebuild.

- **No `enumerate` anywhere in a study guide.** The answer-key segmenter prefers
  enumerate lists over boxes, so a numbered list inside a `formulabox` makes the
  guide segment as N "problems" and the binding gate fails with a confusing
  count mismatch. Use `itemize`.
- **The grade level prints on the answer key only.** Keep passing it as
  `\wstitleblock`'s second argument — the macro accepts it and does not typeset
  it, and the answer key's generated Curriculum section reads the level from
  there. Do not put a level in a worksheet or study-guide title either.
- **`\ans{}` ends its paragraph.** A following `\\` is a fatal error. Put
  `\ans{}` last in a problem block, or start a new paragraph after it. The
  mirror case bites too: a standalone `$\ans{...}$` on the line after a
  `\step{...}` joins that step's paragraph and overfulls — put a blank line
  BEFORE it as well as after.
- **`\frac12` unbraced tokenises as the number 12** in the prose checker.
  Write `\frac{1}{2}`.
- **`definite_integral` accepts string `from`/`to`** (`"-pi/6"`), and
  `solve_interval` takes a float radian interval with exact-string `expected`.
  Both save an ugly degree-mode workaround on polar problems.
- **Put a `\par` before any `tabular` or `\ans` that follows prose**, or the
  table joins the text line and overfulls.
- **Directions blocks use `itemize`, never `enumerate`** — the layout checker
  treats an enumerate in a worksheet as a problem list and applies work-space
  rules to it.
- **A reference figure must sit before the first `\problem`.** Problem regions
  run from one `\problem` to the next, so a figure after the last one is scoped
  into that problem.
- **Variables `d f g j l p q` are now legal** alongside the originals, so a
  common difference can be `d` and a function value `f`. `e`, `i` and `o` stay
  reserved — they read as Euler's number, the imaginary unit, and zero.
- **A trap's `expr` now sees the problem's `at` bindings**, so lifting literals
  into named variables no longer makes the problem's traps illegal. A symbol the
  problem never binds is still refused.
- **`eval` needs a non-empty `at`.** Lift literals into named variables
  (`"expr": "a/b", "at": {"a": 45, "b": 99}`), which also exposes the givens to
  the prose checker.
- **`solve_interval` on an expanded trig quadratic returns MANUAL**, because the
  CAS is genuinely incomplete on that form and the verifier now says so instead
  of passing a short root list. State the expression factored.
- **Multiple verify entries may share one problem `id`** — the right encoding
  for a multi-part problem. Every entry for that id must repeat an identical
  `difficulty`.
- **Spacing around a SUBTRACTION does not matter** — `"t**4 - 3*t**2"` and
  `"t**4-3*t**2"` extract identically. **Spacing around a SIGN does.** A
  negative answer must print its minus against the digit: `\ans{-2}`, never
  `\ans{- 2}`, because a detached minus is indistinguishable from the
  subtraction in `3|x-5| - 2` without parsing the expression, and the checker
  reads `- 2` as $+2$. If you hit it the message now names it as a detached
  sign rather than a wrong value, but printing the sign against the digit is
  better typography anyway.
  (Both halves of this were checked directly. An earlier version of this brief
  claimed spacing never mattered, from an agent report nobody had tested; that
  claim was right about subtraction and wrong about signs.)
- **Fractions in boxed answers now normalize correctly** — `\frac`, `\dfrac`
  and `\tfrac` all work, with or without a leading `\,`, and a two-digit
  numerator is safe. (Earlier guidance here said the opposite and was wrong: the
  normalizer was matching a prefix and rewriting `\tfrac{11\pi}{6}` to `1/1`.
  Fixed. A fraction whose parts are not plain numbers is now left alone rather
  than mangled.)
- **A declared `subtitle` must contain no LaTeX markup.** `check_facet_coverage`
  matches it as a whitespace-normalised verbatim substring, so a `$i$` in the
  printed copy breaks a plain-text `i` in the JSON. Name symbols in words
  ("powers of the imaginary unit").
- **`\rule{\linewidth}` after prose needs a blank line**, not just a `\vspace`
  — `\vspace` does not end a paragraph, so the rule is typeset into the last
  prose line and overfulls by ~200pt. Same class as the `tabular`/`\ans` rule.
- **Prefer `\underline{\hspace{1.2cm}}` and `\\[0.9cm]`** over bare `\rule{}{}`
  in stems — raw dimensions leak into the prose checker as phantom numbers.
- **The 57-char `\skillheading` budget includes the `"Skill N --- "` prefix**,
  which eats about 12. Do not echo the JSON slug in the heading — six agents
  overflowed it that way, and the coverage gate reads the tag, not the title.
- **A trap `value` is compared at the DECIMAL PLACES you write it with**
  (`rounds_to`), not at a fixed significant-figure count — `1.667` and `1.66667`
  both bind, and `37.70` binds at 1 dp. (An earlier version of this line said
  six significant figures; an agent tested it and it is wrong.) Simpler still:
  omit `value` when the wrong number does not need printing — the
  distinguishability check runs either way.
- **For `estimate` traps, check the two rounding places actually disagree**
  before declaring one. Rounding to the nearest hundred and the nearest thousand
  agree far more often than sin-for-cos does, and an indistinguishable trap is a
  hard failure.
- **A prose-filled `\dfrac` is a width hazard.** Put wide `\text{}` fractions in
  display math. If a rebuild returns the *identical* overfull measurement, your
  edit hit the wrong line — the log names the paragraph, not the fraction.
- **Multi-entry ids work in the STUDY GUIDE too**, with the same positional
  binding (entry *i* ↔ box *i*), and all of that id's expected values must sit
  in that one box. This is the clean way to verify a matrix entry-by-entry:
  four `eval` entries under ss id 1, printed as
  `\begin{bmatrix}\ans{7} & \ans{1}\\ \ans{1} & \ans{4}\end{bmatrix}`.
  Beats faking a scalar.
- **A trap may omit `value` entirely.** The distinguishability check still runs.
  Drop `value` when you do not need the wrong number printed, and the sig-fig
  rounding hazard goes away with it.
- **`tikzpicture` bodies are stripped from the prose scan**, so pgfplots tick
  labels do not leak — a sheet with ten numbered coordinate grids reported 100%
  prose match. (Confirmed by observation, not inference.)
- **A `\begin{axis}` that DRAWS something counts as a valued figure** unless both
  `xtick=\empty` and `ytick=\empty`; an axis with nothing plotted in it is a
  blank grid for the student and counts as value-free. The scope rule then asks
  only that no problem be left with no figure at all beside one whose figure
  carries data — so a sheet of ten graphing problems where three are empty
  grids to plot on is fine, and does NOT need those grids deleted.
- **Confirmed against the source:** `\problem[Ncm]{stem}` typesets the stem,
  THEN the workspace, so an
  `\answerline` inside the stem prints above the blank space — use
  `\problem{stem \par\vspace*{Ncm}\answerline{unit}}` when you need a unit.
- **A rational coefficient may be written either way.** `\dfrac{2}{9}(x^3+1)^{3/2}`
  and `\dfrac{2(x^3+1)^{3/2}}{9}` both bind now — the checker offers the
  collapsed value and its parts as alternatives for symbolic answers.
- **`solve` needs `"domain": "real"` whenever the equation has complex roots** —
  cubics AND exponentials both. `2**(x+1) - 2**(3*x-5)` and `2**x - (1/2)**x`
  each fail without it, because `b**u = b**v` always carries complex branches.
  Four problems on one sheet failed this way at once.
- **`integrate` wants the `Abs` form of a log antiderivative.** `x*tan(x) +
  ln(cos(x))` is rejected as undefined where the integrand is real;
  `ln(Abs(cos(x)))` passes, and it is also the form a key should print.
- **A `system` with `"expected": []` machine-verifies "no solution".** Parallel
  lines PASS as inconsistent; a DEPENDENT pair with `[]` fails, because that
  system has infinitely many. The `--schema` output shows only the
  `{var: value}` shapes, so this is easy to miss and turns a planned `manual`
  into a real check.
- **An absolute-value equation verifies directly now** — `Abs(x-3)+2-6` with
  `expected: [-1, 7]`. No need to square both sides to get it past the checker.
- **A mixed `manual` + verified pair under one id is the clean way to write
  "part (a) explain, part (b) compute"** — one answer-key segment, one box, the
  verified half checked and the open half honestly flagged.
- **Aim a `\skillheading` at about 40 characters of your own words.** The cap is
  57 visible characters and a plain-English heading with no slug can still pass
  it ("Skill 1 --- Naming a shape by counting how many straight sides it has" is
  69).
- **Count problems per page BEFORE deciding how to fix a page overrun.** The two
  remedies are opposite and both gates recommend one of them. `pdftotext` the
  failing PDF and look: **≥2 problems per page** means the blocks pack fine and
  the budget is simply under-measured — declare `workspace_cm` covering the real
  block height, which is the honest move. **≤1 per page** means the block cannot
  share a page and no declaration will help; shorten the block.
- **`minipage[t]` beside a `tikzpicture` silently doubles the block.** The
  documented "figure beside the workspace" layout can produce a block twice its
  visible height, because a tikzpicture's baseline sits at the BOTTOM of its
  bounding box — in a `[t]`-aligned minipage the picture becomes all height and
  the neighbouring column all depth, so the two columns stack instead of sitting
  side by side. Put `\vspace{0pt}` immediately after `\begin{minipage}[t]{...}`
  on BOTH columns. The tell is that shrinking the figure changes the page count
  by exactly zero. One author measured a block at 311.8pt whose visible content
  was about 8cm, and the fix let them *enlarge* the grid and still fit two per
  page.
- **When every problem carries a figure, aim the whole block at ≤ 11.5cm so two
  fit per page.** `\problem` makes the block unbreakable, so a 12.3cm block
  packs one per page and strands half of every sheet. The page budget now
  charges for that, and it will tell you — but the fix is a shorter block (a
  smaller figure, or workspace beside the figure rather than under it), NOT a
  larger `workspace_cm`. Inflating the declaration raises the ceiling without
  recovering the stranded space, and the declaration is supposed to be a
  measurement.
- **`distance` compares exactly unless you give `tol`.** A rounded irrational
  (7.07 for 5·sqrt2) hard-fails without `"tol": 0.01`. Unlike `approx`, there is
  no scale-aware default.
- **Long prose does not belong inside `\ans{}`.** The box is unbreakable, so a
  sentence in it always overflows. Box the short answer; put the grading note
  outside.
- **A shared display placed before problem 1 is invisible to the page budget.**
  Charge it to the problems that consume it via `workspace_cm`.
- **Declare stem furniture in `workspace_cm` BEFORE the first compile.** The
  budget charges a flat 0.6 cm of stem per problem, so a stem holding a table, a
  drawing, or displayed math costs 1.5–2 cm the model cannot see. Note the
  leverage: raising the printed `\problem[Ncm]` argument moves the budget and
  the real page count together and can never close the gap — only
  `workspace_cm` raises the ceiling without also raising the content.
- **Displayed math inside a `formulabox` costs about as much as a whole extra
  section.** Four sections whose formula boxes all carry displayed math will
  overflow the 2-page cap. Inline the formulas, or drop to three sections.
- **Budget four study-guide sections, not five,** when any section carries a
  figure or displayed math. Section cost is quantised: a section that will not
  fit in the page remainder moves entirely to the next page.

## What has actually failed here

These are real gate failures from earlier tasks in this suite, not hypotheticals.

- **The answer key must `\input{qa_$STEM}`** directly under `\aktitleblock`.
  `build.sh` generates the quick-answer bank and then fails if the key never
  shows it.
- **`\wsheader` has a 36-character budget** (`\akheader` and `\ssheader` get 60).
  Use a short running title — `\wsheader{Algebraic Limits}` — and put the full
  topic in the title block, which has its own space.
- **Standards codes come from `references/standards-map.md` only.** Never invent
  one. Use the code string exactly as that file writes it.
- **Skill tags are all-or-nothing and gating.** Every worksheet problem carries a
  `"skill"`, and the study guide needs a `\skillheading` section for each
  distinct one. Three or four skills is the working range; five is the ceiling.
- **The study guide is capped at 2 pages, mechanically.** Three sections of
  formula box + example + try-it fits. If you overflow, cut the watch-out box
  first, never the try-it.
- **Each `examplebox` needs at least two `\step` lines and a boxed answer**, and
  each `tryitbox` needs its result in `\ans{}`. `verify_ss` entries are bound
  positionally, so they must be listed example, try-it, example, try-it, …, with
  every try-it tagged `"role": "tryit"`.
- **Never claim verification you do not have.** A proof, sketch, or "explain
  why" is `{"type": "manual", "desc": ...}`. The build exits 2 and says so; that
  is the correct outcome, not a failure to fix.
- **Difficulty must ramp**: start at 1–2, majority 2–3, finish with one or two
  4–5. `verify.py` reports the ramp and flags drops.

- **A bulleted overview box before section 1 costs about as much as a whole
  skill section.** With four sections it is the first thing to cut, ahead of the
  watch-out box that SKILL.md's drop order names first — two authors landed on a
  3-page guide this way and both fixed it by deleting the intro box. The section
  cost table in `references/latex-templates.md` also understates a `formulabox`
  carrying a 4-5 item `itemize`.

## Quality bar

These artifacts are going to an independent judge that recomputes every answer
and inspects every page. It rejects a task outright for a wrong or ambiguous
problem, a missing artifact, a problem count that differs from the task, a
severe layout defect, or a focus that appears in under 70% of the problems.

So: match the requested problem count exactly, keep every problem inside the
named focus, give real work space (the page budget is computed from content —
do not compress to save a page), and make the study guide something a student
could actually learn the skill from rather than a formula dump.

## Do not

- Do not commit to git. Artifacts are committed centrally after each wave.
- Do not edit anything outside `/tmp/evalbuild/$TASK` and the run folder.
- Do not hand-roll the LaTeX preamble; `\input{worksheet-preamble}` always.
- Do not re-record a task another agent already recorded.
