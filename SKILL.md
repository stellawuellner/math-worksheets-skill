---
name: math-worksheets
description: Generate professional math practice worksheets and full answer keys as PDFs. Compiles LaTeX to PDF using tectonic (free, no account needed). Supports any math topic from elementary through AP Calculus BC (Pre-Algebra, Algebra 1/2, Geometry, Pre-Calc, Calculus AB/BC — limits, derivatives, integrals, series). Handles coordinate plane grids, geometric figures, tables, and multi-part problems. Use when a user asks for a math worksheet, practice problems, homework help sheet, or answer key for any K-12 math topic including calculus.
---

# Math Worksheet Generator

Generate a student worksheet PDF + full step-by-step answer key PDF for any math topic from elementary through AP Calculus BC. Compiles LaTeX with `tectonic` (no TeX installation required — it auto-downloads packages).

This skill is **agent-agnostic**: it works in any agent harness that can read files and run shell commands (Claude Code, Gemini, Codex, OpenClaw, etc.). It uses no harness-specific primitives; every step is plain file I/O and shell commands, and the platform-specific delivery step is optional with a portable fallback.

Throughout this document, `$SKILL_DIR` means the directory containing this SKILL.md. Resolve it once at the start (e.g. `SKILL_DIR=/path/to/math-worksheets`) — do not rely on `$0`, which is only meaningful inside a script. In Claude Code the skill's directory is already available as `${CLAUDE_SKILL_DIR}`, so `SKILL_DIR="${CLAUDE_SKILL_DIR}"` works; other agents resolve the path however they locate the skill.

## A note on accuracy

Generate the problems with whatever model your agent is already running. Correctness does not depend on the model getting the math right the first time: the SymPy verification gate (steps 4–5) independently checks every answer and blocks the build if any check fails, so a wrong answer never reaches the PDF. Stronger reasoning models simply need fewer retries to pass the gate. The skill does not detect, switch, or recommend models.

## Prerequisites

**tectonic** (LaTeX compiler — auto-downloads packages on demand). Install with whichever is available:

```bash
brew install tectonic       # macOS or Linux with Homebrew
cargo install tectonic      # any platform with Rust
sudo apt install tectonic   # Debian/Ubuntu (recent releases)
# or download a release binary: https://github.com/tectonic-typesetting/tectonic/releases
```

**python3 + sympy** for answer verification: `pip3 install sympy`. The scripts pick the first python3 that can actually `import sympy` (machines often carry several pythons); pin one with `MWS_PYTHON_CANDIDATES=/path/to/python3` if needed.

**No tectonic?** `scripts/compile.sh` falls back to `pdflatex` automatically. Unlike tectonic, pdflatex does not download packages — install the full set up front: `texlive-latex-base texlive-pictures texlive-latex-recommended texlive-latex-extra` (the last one supplies `enumitem`, `mdframed`, and friends used by the templates).

Output directory (create if needed): `~/Documents/Worksheets/`. In headless or sandboxed environments where the user won't browse `~/Documents`, use `./worksheets/` inside the workspace instead and report the paths.

## Workflow

### 1. Gather requirements

Ask (or infer from context):
- **Student**: name, grade, course (e.g. "8th grade, Pre-Algebra")
- **Topic**: e.g. "factoring trinomials", "solving two-step equations"
- **Problem count**: default 10 if not specified
- **Page use**: the page budget is COMPUTED from the problem set (`scripts/page_budget.py`), not fixed. Fifty graphing problems that each need a coordinate plane legitimately run past 20 pages and are allowed to; a flat cap could only be met by shrinking the work space, which is the one thing that must never give. `build.sh` prints the ideal page count and the double-sided sheet count before compiling, so paper cost is visible. If a set is bigger than intended, reduce the PROBLEM COUNT, never the work space. Hard ceiling: 100 problems — past that, split into several worksheets
- **Paper size**: US Letter by default. For A4 or Legal, add the paper as a documentclass option (`\documentclass[12pt,a4paper]{article}`) with metric geometry margins, and pass `--paper a4` to `page_budget.py`. See `references/latex-templates.md` → "Paper size"
- **Accessibility**: for large-print or dyslexia-friendly output use `\documentclass[17pt]{extarticle}` (or 14pt) plus `\accessiblemode{large|dyslexia|both}`. The page budget adapts automatically; larger type simply means more pages. See `references/latex-templates.md` → "Accessibility"
- **Locale**: `\mwslocale{eu}` prints decimal commas and `\times`. The verify JSON stays canonical (period decimals) — only the printed form is localised, via `\dec{}` and `\mtimes`. Pair this with A4 paper for European users
- **Format preference**: timed quiz, homework practice, mixed difficulty, or topic drill.
  For a **timed quiz**, point values are the default: place `\probpts{N}` at the end of
  each stem and `Score: \underline{\hspace{1.5cm}} / \totalpoints\ pts` in the title
  block (rendered in step 4c). Difficulty stars (`\probmeta{N}`) are opt-in for
  practice/mixed-difficulty sheets on request; skip markers for early-elementary
  drills unless asked.

**Photo input shortcut**: If the user provides a photo of homework or a textbook page, read the image with whatever vision capability your agent provides (or by reading the image file directly) to extract problem types, format, and difficulty, then mirror that style exactly.

### 2. Design problems

Design problems appropriate to the student's level. Increase difficulty gradually across the set. Every problem must be mathematically correct — verify your own solutions.

See `references/problem-library.md` for topic-specific problem type menus.

**The grade level never prints on the worksheet or the study guide.** `\wstitleblock` takes a course argument and does not typeset it: a child working a grade below or above reads the label before the mathematics, and it tells the student nothing they need. The level is the adult's information, so it prints on the ANSWER KEY — in the title block and again in a generated **Curriculum** section beside the standards codes and the difficulty range, which is where a parent or teacher actually looks. Keep passing the course argument: it is the one place the level is declared, and the answer key's curriculum section reads it from there.

**Tag every problem** with `"standard"` (a code from `references/standards-map.md` — never invent codes, and **grep that file before concluding it lacks a row**: 11 reviewed cases asserted a missing row that was there, two of them naming the exact code they called absent, and then tagged a high-school sheet with a grade-8 standard), `"difficulty"` (1–5 per that file's ladders), `"bloom"` (recall/apply/analyze/justify, same file), and `"skill"` (a short stable name for the skill the problem exercises, e.g. `"right-triangle-trig"` — reuse the same name across problems of the same Part). Skill tags are all-or-nothing and GATING: the study guide must contain an entry tagged with each distinct worksheet skill, enforced by `build.sh`'s `coverage-ss` gate; a partially tagged sheet fails it. Ramp difficulty: start at 1–2, majority 2–3, end with one or two 4–5 challenges. Verification reports standards coverage, the bloom mix, the skill mix (the set the study guide must cover), and flags ramp drops, so a parent can see exactly which standards the sheet exercises and at what cognitive level.

**Facets (skill coverage):** a facet is a distinct method the sheet tests (e.g. `side-from-angle` vs `angle-from-sides` vs `pythagorean`) — standards codes are usually one constant per sheet and cannot show this. For sheets of 10+ problems, declare top-level `"facets": [...]` in the verify JSON and tag **every** problem with a `"facet"` from that list; consult `references/problem-library.md` → "Facet checklists" (topics without a table use your own lowercase-kebab names). The gate is strict: an unlisted facet, a planned facet with zero problems, or an untagged problem is a build failure. Tag TRUTH is your responsibility — the gate verifies plan/tag consistency, not that a tag describes its problem. Tag the `verify_ss_` entries' `"facet"` too: the facet-coverage gate (step 5) requires every worksheet facet to have a study-guide worked example.

**Interleave after the warm-up:** a blocked warm-up over the first third of the sheet is fine; after that, keep same-facet runs to 3 or fewer so the student must *choose* the method — unless the sheet is genuinely a drill, declared with top-level `"format": "drill"`. `verify.py` flags longer runs (exit 2, manual review) with a concrete swap suggestion. See `references/problem-library.md` → "How to interleave".

**Misconception traps:** consult the misconception table (`references/problem-library.md` → "Misconception traps & error analysis") when choosing givens — pick numbers so the canonical wrong method lands visibly off the correct answer — and declare `"traps"` on the 2–3 problems you designed that way. Traps are optional, but declared ones are machine-checked (step 4) AND printed in the answer key as a "Common wrong answers" block (`scripts/render_quick_answers.py` emits one `\commonerror` line per trap, so the grader sees "If they got 7.37: used cos instead of tan"). Declaring traps therefore pays twice: it hardens the problem design and it turns grading into teaching.

**Tiered worksheets (differentiation, on request):** when asked for tiers (support/on-level/challenge), build ONE set of problem skeletons, then re-parameterize per tier — same structure and standards, different givens and difficulty band (support: 1–2 with a hints box and a worked first step; core: 2–3; challenge: 3–5). Each tier gets its OWN verify JSON (the gate re-checks every tier) and file prefix: `wsS_`/`wsC_`/`wsX_` + matching keys. Because construction is JSON-first, a tier is a data change, not a rewrite.

**Tier naming for the build driver:** give each tier its own *stem* — `verify_factoring_S_2026-07-27.json` with `wsS_factoring_S_2026-07-27.tex` (or plain `ws_factoring_S_...`; both are discovered). What matters is that two tiers never share a stem in one directory: `scripts/build.sh` derives the document names from the verify JSON's stem, and two candidates for one role is a hard discovery error, not a guess.

### 3. Write LaTeX source

Write **three** `.tex` files to `/tmp/`:
- `ws_TOPIC_DATE.tex` — student worksheet (blank work areas)
- `ak_TOPIC_DATE.tex` — answer key (full step-by-step solutions)
- `ss_TOPIC_DATE.tex` — skills summary / study guide (cheat sheet)

The **skills summary** is a 1–2 page reference card the student can use while working through the worksheet or when studying. Per skill section: **formulabox → examplebox → tryitbox**. It contains:
- One section per distinct skill tested, matching the worksheet's `"skill"` names. **The slug belongs in the JSON, not in the heading** — `\skillheading` is gated at 57 characters (the budget includes the `"Skill N --- "` prefix, which eats about 12), and the coverage gate reads the JSON tag, never the printed title. Six eval-run agents overflowed this heading by echoing the slug in parentheses to make the tagging visible to a reader; it does not need to be visible there. Sections are — `build.sh`'s `coverage-ss` gate fails the build if any worksheet skill lacks a tagged study-guide entry. **Five full sections is the hard ceiling** for the 2-page cap (a full section costs ~234pt against a 1382pt two-page budget); aim for 3–4. When over budget, drop the watch-out box first, then merge two thin skills, then shorten worked examples — never drop the try-it. Add no `\vspace` between boxes; they carry their own spacing. See `references/latex-templates.md` → "Page budget"
- A **formula/rule box** (blue) per skill — the key facts and formulas
- A **mini worked example** (green) per skill — a `\step` strategy line naming why this tool applies, then the computation — fewer steps than worksheet problems, never a bare answer chain (see the exemplars in `references/latex-templates.md`)
- A **try-it** (violet) per worked example — a re-parameterization of that section's example (same skeleton, new givens), printing ONLY the stem plus the verified answer upside down INSIDE the box via `\rotatebox{180}{\footnotesize check: $\ans{...}$}` — no worked steps; solving it is the student's job. Formula-only sections (no example) are legal and need no try-it
- An optional **watch-out box** (orange) — common mistakes worth flagging
- Optional **key vocabulary** section at the bottom

See `references/latex-templates.md` → "Skills Summary / Study Guide Template" for the full shell and box macros.

**Verify the study guide too.** Its worked mini-examples are math the student learns from first, so they must not be exempt from the gate (audit 3c). Write a second verification file `/tmp/verify_ss_TOPIC_DATE.json` — one entry per worked example's computation AND one per try-it. Entries MUST be listed in document order (example, try-it, example, try-it, …) because binding is positional; tag each try-it entry `"role": "tryit"` and each entry with the `"skill"` it demonstrates. The build driver (step 5) verifies it and binds its printed answers automatically; a missing `ss_` document or `verify_ss_` JSON is a **build failure**, not a skip. Formula boxes (no computed answer) need no entry; every *worked example or try-it with a printed result* does. `check_answer_key.py` segments ss documents **by box** (`examplebox`/`tryitbox`) — keep one worked example or try-it per box, and one **id** per box — so box count = `problem_count` = the number of distinct ids. A box whose example needs more than one check (a distance AND the perimeter built from it) may carry several entries under that one id; what must not happen is two boxes sharing an id, or one box holding two, and print each result with `\ans{...}` (defined in the study-guide shell); a result set in bare `\boldsymbol` is invisible to the gate. A try-it may be type `manual` only when its paired example is also `manual` (exit-2 visibility, never silent). The structure gate (`tests/check_study_guide.py`) additionally requires ≥2 `\step` lines and a boxed final answer per examplebox — the first step is the strategy sentence, capped at ONE sentence (page 1 fills fast and the guide is hard-capped at 2 pages — enforced mechanically: the `compile-ss` gate reads the page count from the engine's log and fails a 3-page guide).

**Subtitle from facets:** when `"facets"` is declared, write a top-level `"subtitle"` in the verify JSON composed from that facet list *first*, then copy it verbatim into the worksheet's title block. The facet-coverage gate (step 5) binds the two, so the title can never promise a skill the sheet doesn't plan.

See `references/latex-templates.md` for document templates, coordinate planes, tables, geometric figures, and answer key patterns.

**Answer-key shell:** the `ak_` document starts exactly like the worksheet
(`\input{worksheet-preamble}`), then `\akheader{TOPIC}` + `\aktitleblock{...}`, and ONE
`\input{qa_TOPIC_DATE}` line directly under the title block — the build driver's
quick-answers gate regenerates that bank from the verify JSON every build and **fails a
key that hand-rolls its preamble or never `\input`s the bank** (both messages teach the
fix). `\akheader` switches `\ans{...}` to a compact same-line box, so end each worked
solution's last step with `\ans{x = 5.00}`; keep the display `\[ \boxed{...} \]` form
for long or multi-value answers. See `references/latex-templates.md` → "Answer Key
Patterns".

**Preamble — \input the shipped template, never retype it.** Start every document with:
```latex
\documentclass[12pt]{article}
\usepackage[margin=1in, top=0.75in, bottom=0.75in]{geometry}  % ss_: margin=0.85in, top/bottom 0.7in
\input{worksheet-preamble}
\input{figure-macros}    % when using the shipped figure macros (\rtfig, \trifig, \refrt)
```
`$SKILL_DIR/templates/worksheet-preamble.tex` carries the packages, `\problem`, `\fittedtitle`, the `\wsheader`/`\akheader`/`\ssheader` + title-block macros, and the study-guide box environments; `templates/figure-macros.tex` carries the figure macros. `compile.sh` (and therefore `build.sh`) stages both files beside your `.tex` automatically, so `/tmp` compiles just work — but only when you compile through the scripts, never by invoking the engine directly. Only `geometry` stays in the document (margins differ between worksheets and study guides). `build.sh` enforces this mechanically — the `template-ws`/`template-ak`/`template-ss` gates (`tests/check_template_use.py`) fail any document that hand-rolls its shell, `\input`s a non-shipped preamble file, or redefines a shipped macro/environment/color.

**Work space defaults**: `\problem[5cm]{...}` per problem; `8cm` for multi-step; `10cm+` for graphs.
The workspace must live **inside the problem's unbreakable block** (the `\problem` macro's
minipage, or a per-item minipage in lists — see the templates): `\vspace` glue outside it
is silently discarded when it falls at a page or column break, leaving a bottom-of-page
problem with zero room to work. These are a floor, not a suggestion: `tests/check_layout.py`
fails a worksheet whose problems get under 2.5cm and flags workspace `\vspace` left outside
a minipage. A sheet with correct answers and nowhere to write them is a sheet the student
cannot use.

**Answer location (every problem gets one):** `\problem` sheets emit the right-aligned
answer blank automatically whenever the workspace argument is positive — write nothing
extra. On enumerate/`\item` sheets, end every item with `\ansline` (or an inline
`\ansblank` for drill formats: `$7 + 5 =$~\ansblank`). Mark `\noansline` only where the
worked product IS the answer — graph sketches, proofs, constructions (typically the
`manual`-type set). `tests/check_layout.py` enforces one answer-location macro per item;
answer keys and study guides are unaffected.

**Units are verified data, not decoration:** any problem whose final answer carries a
measurement unit declares `"answer_unit"` in its JSON entry (`"ft"`, `"m"`, `"cm^2"`,
`"square units"` — distinct from the deg/rad angle-mode field `"unit"`) and ends with
`\answerline{<unit>}` on the sheet (write exponents math-wrapped: `\answerline{cm$^2$}`;
`\answerline` replaces `\ansline` there and suppresses `\problem`'s automatic blank).
The key must print the same unit inside `\ans{}`/`\boxed{}` (`\text{ft}`).
Both directions are gated: `tests/check_answer_line.py` fails a declared unit with no
matching `\answerline` and an `\answerline` unit the JSON never declared;
`tests/check_answer_key.py` fails a key whose box omits the declared unit or prints a
unit the JSON never declared — a metres problem answered in feet no longer passes any
gate. Prefix currency symbols are out of scope: write "in dollars" in the stem.

**Figure scope**: a figure carrying numbers belongs to one problem, but on the page it
merely sits *near* several. If problem 6 shows a triangle labelled `a=6, b=8` and
problems 7-8 show none, a student reading 7 will apply the nearest figure to it — the
figure is correct and the worksheet is still wrong. So within one problem list, **no
problem may be left with no figure at all while another problem's figure carries
values**. A problem holding its own *value-free* figure — a blank coordinate grid to
plot on, an unlabelled diagram to mark up — is fine, and mixes freely with graphed
problems beside it: the picture inside its block is visibly the one it means, and a
grid's axis numbers are its own scale, not another problem's data.
Shared labelling conventions go in a single value-free reference figure placed with the
directions, captioned so it cannot be mistaken for a problem's givens, e.g. "How every
triangle here is labelled. No values shown: use the numbers given in each problem."
Use the shipped `\refrt` macro for it. Its convention is the renderer's: sides `a/b/c`
opposite vertices `A/B/C`, right angle at `C`, hypotenuse `c` — the reference figure and
the renderer-built `\probfig` figures share one page, so
`tests/test_figure_convention.py` fails the build if the macro and
`render_figures.py` ever mark the right angle at different vertices.
`tests/check_layout.py` enforces the scope rule.

**Triangle figures MUST come from the renderer, never hand-drawn TikZ with values.**
Step 4b generates `\probfig{N}` macros from the verify JSON — every `triangle` problem
automatically, plus `approx` and `eval` problems that declare a `"figure"` object. A
write-the-ratio problem ("write $\tan A$ as a fraction") is verified as `eval` and is
renderer-figured like any other right triangle — the renderer covers it, so the
hand-macro escape hatch never applies to it. Reference the macros
in the worksheet instead of writing TikZ: hand-computed figure coordinates are exactly
the retyping drift the JSON-first pipeline exists to prevent (the reference SSA swing
figure itself shipped with wrong hand-computed constants until the renderer replaced
them). Leave a `\probfig{N}` placeholder while writing the `.tex`; the macro exists
once step 4b's figs file is `\input`. Hand-built TikZ per `references/latex-templates.md`
remains the path only for figure kinds the renderer doesn't cover — circles, sectors,
solids, transversals, coordinate grids. `\includegraphics` in worksheet problems is
rejected as unverifiable (`check_prose_consistency.py` exits 2 — no checker can bind an
external image's values to the JSON): figures come from `scripts/render_figures.py` or
the TikZ templates, never from image files.

### 4. Write and run the verification file

Before compiling, write `/tmp/verify_TOPIC_DATE.json` — a structured data file describing each problem and its expected answer. The bundled `scripts/verify.py` evaluates this using SymPy. No generated code is ever executed. The build driver (step 5) runs it first and fail-fast; to iterate on verification alone, see "Debugging individual gates" below.

**Field reference that cannot go stale:** `python3 "$SKILL_DIR/scripts/verify.py" --schema` prints every type's required/optional fields, the allowed functions/constants/variables, and one working example per type, generated live from the enforced schema (`--schema json` for machine-readable output).

**JSON format** — always set `problem_count` to the number of problems on the worksheet. Two gates enforce coverage, and they are not the same gate:

- `verify.py` hard-fails unless every problem id 1..N has at least one check. This counts **problems**.
- `tests/check_answer_slots.py` hard-fails unless every id has **one entry per response the problem asks for** — every printed `\ansline`/`\ansblank`/`\answerline`, and every lettered `(a)`/`(b)`/`(c)` sub-part in the stem. This counts **answers**.

When a problem carries more than one entry, give each a `"slot"` — the name of the response it covers (`"AC"`, `"the ones digit"`, `"(b)"`). No check reads it; the Quick Answers bank prints it, so a grader can tell which value answers which question. Without it the bank joins values in array order, and a sheet asking for "AC and BD" printed `2. 2.83, 8.49` with BD first.

The second gate exists because the first was mistaken for it. "At least one check per problem" was read as "a partially-verified answer key can never slip through", and those are different promises: a problem printing three blanks satisfies the per-id rule with one entry. In a 300-case review, **172 shipped a printed answer that nothing verified** — often the very skill the problem was tagged with. If a problem asks the student to write the number word *and* the ones digit, that is two entries. If a blank is working space rather than an answer, print it with `\scratchblank` and it is not counted:
```json
{
  "topic": "derivatives and trig",
  "problem_count": 17,
  "problems": [
    {"id": 1, "type": "solve",  "expr": "x**2 - 5*x + 6",      "expected": [2, 3]},
    {"id": 2, "type": "factor", "expr": "x**2 - 7*x + 12",     "expected": "(x-3)*(x-4)"},
    {"id": 3, "type": "eval",   "expr": "(x-1)*(x+2)", "at": {"x": 0}, "expected": -2},
    {"id": 4, "type": "zeros",  "expr": "x*(x-3)**2",           "expected": [0, 3]},
    {"id": 5, "type": "expand", "expr": "(x+2)**2",             "expected": "x**2 + 4*x + 4"},
    {"id": 6, "type": "diff",   "expr": "x**3 - 4*x",           "expected": "3*x**2 - 4"},
    {"id": 7, "type": "integrate", "expr": "6*x**2",            "expected": "2*x**3"},
    {"id": 8, "type": "limit",  "expr": "sin(x)/x", "to": 0,    "expected": 1},
    {"id": 9, "type": "equiv",  "expr": "sin(2*x)",             "expected": "2*sin(x)*cos(x)"},
    {"id": 10, "type": "solve_interval", "expr": "2*sin(t) - 1", "var": "t",
               "interval": [0, 360], "unit": "deg", "expected": [30, 150]},
    {"id": 11, "type": "approx", "expr": "9*tan(35*pi/180)", "expected": 6.30, "tol": 0.01},
    {"id": 12, "type": "distance", "points": [[1, 2], [4, 6]], "expected": 5},
    {"id": 13, "type": "midpoint", "points": [[2, -3], [8, 7]], "expected": [5, 2]},
    {"id": 14, "type": "slope", "points": [[2, 1], [2, 9]], "expected": "undefined"},
    {"id": 15, "type": "polygon_area", "points": [[0, 0], [5, 0], [6, 4], [1, 3]], "expected": 17},
    {"id": 16, "type": "triangle", "given": {"a": 7, "b": 11, "C": 34},
               "solve_for": "c", "expected": 6.51},
    {"id": 17, "type": "manual", "desc": "Graph sketch — verify visually"}
  ]
}
```

**Type reference:**

| Type | Verifiable? | What it checks |
|---|---|---|
| `solve` | ✅ | Roots of expr=0 match expected list (optional `var`, default `x`) |
| `zeros` | ✅ | Zeros of expr match expected list (duplicates collapse) |
| `factor` | ✅ | Factored form is equivalent to expr |
| `expand` | ✅ | Expanded form is equivalent to expr |
| `eval` | ✅ | expr evaluated at given values matches expected |
| `diff` | ✅ | Derivative of expr matches expected (optional `order`) |
| `integrate` | ✅ | Expected antiderivative differentiates back to expr — omit the `+C` |
| `limit` | ✅ | Limit of expr as var → `to`; optional `dir`: `"+"`, `"-"`, `"+-"` (default) |
| `equiv` | ✅ | expr and expected are the same function (trig identities, simplification) |
| `solve_interval` | ✅ | Roots of expr=0 on `[a, b)`; `"unit": "deg"` for degree-mode trig equations |
| `approx` | ✅ | Numeric expr recomputed exactly, compared within `tol` (default: scale-aware — accepts what rounds to the written precision) — for rounded answers |
| `distance` | ✅ | Distance between two `points`; exact, or within `tol` if given |
| `midpoint` | ✅ | Midpoint of two `points`; expected is an `[x, y]` pair |
| `slope` | ✅ | Slope through two `points`; expected value or `"undefined"` for vertical |
| `polygon_area` | ✅ | Shoelace area of the ordered `points` (3+) — triangles, quads, composite grid figures |
| `triangle` | ✅ | Solves the triangle from 3 `given` values (sides `a/b/c`, angles `A/B/C`), checks `solve_for` within `tol`; degrees by default; accepts either triangle in the ambiguous SSA case |
| `system` | ✅ | `equations` (each `=0`), `vars`, `expected` `{var: value}` (all vars) or a list of solution dicts. Each listed solution must satisfy every equation; PASS only when the count matches SymPy's full solution set — MANUAL for infinite families |
| `series` | ✅ | `summation(term, var, from..to)` vs `expected`; finite or infinite (`"to": "oo"`), incl. geometric and Taylor (`factorial` allowed) |
| `inequality` | ✅ | Solution set of `expr relation 0` (`relation`: `<`, `<=`, `>`, `>=`) vs an interval spec `[lo, hi, openness]` (`openness`: `open`/`closed`/`loopen`/`hiopen`; `lo`/`hi` may be `"oo"`/`"-oo"`) |
| `stats` | ✅ | `measure` of a `data` list: `mean`/`median`/`mode`/`range`/`sum`/`variance`/`stdev`/`q1`/`q3`/`iqr` (school median-of-halves quartiles; non-unique mode → manual) |
| `probability` | ✅ | `favorable`/`total` as an exact fraction |
| `read_data` | ✅ | Read/compute from a chart or table whose `data` is in the JSON. Object data → `query` `value`/`total`/`max_value`/`min_value`/`max_key`/`min_key`/`difference` (with `key`); list data → `total`/`count`/`max_value`/`min_value`. The SAME `data` feeds the pgfplots chart, so figure and check share one source |
| `definite_integral` | ✅ | ∫ from `from` to `to` of `expr`. Uses SymPy's exact integral when available, else convergence-checked mpmath quadrature; returns MANUAL if numerics don't converge rather than trust a wrong value |
| `estimate` | ✅ | Rounds each numeric **operand** in `expr` (half-up) to `place` (`ten`/`hundred`/`thousand`/`whole`/`tenth`/`hundredth`), then evaluates — front-end "estimate by rounding". `probability` favorable/total is range-validated (0 ≤ fav ≤ total) |
| `compare` | ✅ | Order `values` (`order`: `asc`/`desc`) or state a `relation` (`<`/`>`/`=`) between the first two |
| `manual` | 👁 | Flagged for human review — never fails automatically |

**Reframe "understanding" topics as checkable tasks** (see `references/problem-library.md` → "Reframing…"): missing-number → `solve`, fact-family → `eval`, estimation → `estimate`, ordering → `compare`.

**A check must exercise the work the problem asks for.** No gate can enforce this — it is a relationship between the printed stem and the JSON that no static rule reads reliably, so it is on you. Two shipped failures show the shape:

- A problem gives `f(x) = (x²−5x−14)/(x−7)` for `x ≠ 7` and asks for the `c` that makes `f` continuous at 7. Its check was `solve(c − 9, c) == [9]` — it asserts that 9 solves `c − 9 = 0` and never touches the function. Green gate, response claiming "machine-verified with SymPy", nothing verified. Check the limit.
- A problem gives midpoint `M(3,5)` and endpoint `A(−1,2)` and asks for `B`. Its check was `midpoint([[−1,2],[7,8]]) == [3,5]` — the answer fed in as an input, a given verified as the output. It cannot fail, and the answer bank printed `6. 3, 5`, so a student with the correct `(7,8)` marks themselves wrong. **For an inverse item, compute the asked value.**

`tests/check_answer_slots.py` prints an advisory when a check's expected values are all already in the stem, but it is deliberately advisory: measured over 300 cases it is right about one time in seven.

**Error-analysis ("find and fix the mistake") is TWO responses, not one.** The *correction* is a value, so it takes an ordinary type — the planted wrong result is checkably wrong and the corrected one checkably right. The *diagnosis* ("name the error", "say what rule it breaks", "explain what he did wrong") is prose, so it takes a `manual` entry alongside. Declare both. Routing the whole item through an ordinary type leaves the diagnosis unchecked and, worse, makes the sheet claim it is fully machine-verified: in the 300-case review **202 cases** did exactly that, and many then stated "Nothing is flagged for manual review" in the delivered response, two paragraphs from an answer key printing a grading rubric for the explanation they had just called machine-checked. Deciding per *response* rather than per *problem* is what resolves this — the two rules below are not in tension once you stop asking which one the problem belongs to.

**Data charts:** render bar/line/pictogram charts with pgfplots (see `references/latex-templates.md`), sourcing the plotted values from the same `data` array the `read_data` check uses — never retype them. `solve_interval` on a transcendental equation now confirms *completeness* by mpmath root-enumeration (PASS when the key's roots match all numerically-found roots; MANUAL if counts differ)."

**Complex numbers:** `I` is available in expressions, so `eval` handles complex arithmetic (e.g. `(3+2*I)*(1-4*I)` expected `"11 - 10*I"`). For `solve`/`zeros`, non-real roots are no longer dropped silently — set `"domain": "complex"` to require the full root set (e.g. `x**4-1` → `[1, -1, "I", "-I"]`) or `"domain": "real"` to restrict to real roots.

For geometry, **state the givens and let the script compute**: pass raw coordinates to `distance`/`midpoint`/`slope`/`polygon_area` and raw triangle data to `triangle` rather than doing the formula yourself in `expr`. Angle convention: side `a` is opposite angle `A` (matches the figure templates).

Use `manual` for: graph sketches, sign charts, word problem setups, two-column proofs, constructions, Riemann sum tables, series convergence arguments, drawn or marked representations (circle it, shade it, plot it), a named misconception, and any explanation/reasoning answer — **per response**, so a problem whose (a) is a number and whose (b) is "explain why" gets one ordinary entry and one `manual` entry, not a choice between them.

A `manual` entry's `desc` is the rubric a human grader actually reads, so it must describe **the problem as printed**. Nothing binds it automatically: one reviewed case shipped a `desc` grading a scale-spacing argument about a student named "Priya" who appears nowhere in the worksheet — a rubric left over from an earlier draft, green through every gate. Re-read the `desc` against the stem before shipping.

**Optional review aid for `manual` content:** proofs and explanations can't be CAS-verified, but an independent LLM-judge pass can flag likely errors before a human reviews them. See `references/manual-review-aid.md`. This is a review aid, NOT a gate — a `manual` problem stays `manual`; never mark it verified on a judge's say-so.

**Expression syntax** — enforced by a strict allowlist in `verify.py`; anything outside it is rejected as a failure, never executed:
- Explicit operators only: `3*x` (not `3x`), `x**2` or `x^2` for powers
- Functions: `sin cos tan asin acos atan sec csc cot sinh cosh tanh log ln exp sqrt Abs floor ceiling`
- Constants: `pi`, `E` (Euler's number), `oo` (infinity)
- Variables: `x y z t u v w a b c h k m n r s theta phi` (pick from these when writing problems)

**Strict schema:** an unknown `type`, a misspelled field, or a missing required field is a hard failure (exit 1) — never a silent skip. If you need an unverifiable problem, declare it `manual` explicitly.

**Explicit `tol` is capped.** A `tol` wider than max(1% of |expected|, half a unit in the expected value's last written place) is rejected — an unbounded tolerance is a one-field bypass of the whole gate. For genuine estimation problems, add `"tol_reason": "<why>"` to acknowledge the widened tolerance: the run then passes with exit 2 and a visible `⚠` tally, never silently.

**If verification fails (exit 1):** fix the LaTeX answer key and re-run. Do not compile until the answer key is correct.

**Trust boundary of `approx`:** it confirms the *arithmetic of the formula you wrote* matches `expected` — it cannot confirm the formula is the right one for the stated problem. Keep the `approx` `expr` a faithful transcription of the problem's givens, and rely on the prose/figure/answer-key checkers below to bind the story to the math.

**Misconception traps (`"traps"`, universal on scalar-answer types):** declare the result a known wrong method yields:
```json
{"id": 11, "type": "approx", "expr": "9*sin(35*pi/180)", "expected": 5.16,
 "traps": [{"desc": "used cos instead of sin", "expr": "9*cos(35*pi/180)", "value": 7.37}]}
```
Verification computes each trap `expr` and **fails unless the problem's own comparison rejects it** — a trap the check would accept means the problem cannot distinguish the error it targets: change the givens. The optional `value` (the wrong number printed in an error-analysis stem) must round-match its own `expr`, so the planted number is derived, never hand-typed; it then counts as a JSON given for the prose checker. The `desc`↔`expr` correspondence is yours to keep faithful — the same trust boundary as `approx` above. Allowed only on types with a single comparable answer (`approx eval triangle distance slope polygon_area stats probability limit series definite_integral estimate read_data`); `--schema` documents the shape.

### 4b. Render figures from the verified JSON

Immediately after `run_verify.sh` succeeds, render the figures **from the same JSON**:

```bash
python3 "$SKILL_DIR/scripts/render_figures.py" /tmp/verify_TOPIC_DATE.json
# → /tmp/figs_TOPIC_DATE.tex, one \probfig{N} macro per figured problem
```

This is the `read_data` chart rule applied to geometry: the `given` dict the verifier
checks is what places every vertex, so the drawing cannot disagree with the answer key.
Figures are to scale (longest side ≈ 4.5cm), label **only** given values plus `?` on
`solve_for`, mark a given 90° angle with a square instead of an arc, and render the
ambiguous SSA case as the two-apex swing figure — both apexes computed, not retyped.

- Every `type: "triangle"` problem renders automatically from its own `given` dict.
- Right-triangle setups on `approx` and `eval` problems opt in with a `"figure"` object:
  `{"kind": "right_triangle", "given": {"b": 9, "A": 35}, "solve_for": "a", "unknown": "x"}`
  (two of `a/b/c/A/B`; the right angle at `C` is implied). Every figure value must
  appear among the numbers the problem's own check used — a literal in `expr`, or one
  of the `at` values on `eval` (the write-the-ratio shape: `"expr": "a/b"` with
  `"at": {"a": 8, "b": 15}`, figure `"given": {"a": 8, "b": 15}`, `"solve_for": "A"`,
  `"unknown": "A"` to mark the asked-about angle) — verification hard-fails otherwise,
  so the figure can only show numbers the arithmetic check actually used. Other problem
  types cannot carry a figure: they have no bindable single answer, and verification
  rejects them with the rewrite (verify as `approx`/`eval`, or drop the figure).
- In the worksheet: `\input{/tmp/figs_TOPIC_DATE.tex}` right after `\begin{document}`,
  then place `\probfig{N}` with problem N inside its minipage (figure-placement rules
  in `references/latex-templates.md`), keeping the work-space `\vspace` outside.
- An impossible figure refuses to render (exit 1) — fix the JSON, don't fight the tool.
- **Re-run this whenever the JSON changes.** A stale figs file is caught by
  `check_prose_consistency.py --figs` in step 4c.

`build.sh` (step 5) runs this render automatically when the JSON has figured problems and passes `--figs` to the checkers; run it by hand only when iterating on the `.tex` outside the driver.

### 4c. Render effort markers (quiz points / difficulty stars)

For timed quizzes (and practice sheets on request), render the per-problem effort
markers **from the same JSON** — generated, never hand-written:

```bash
python3 "$SKILL_DIR/scripts/render_meta.py" /tmp/verify_TOPIC_DATE.json
# → /tmp/meta_TOPIC_DATE.tex — \probpts{N} "(D pts)", \probmeta{N} stars, computed \totalpoints
```

`\input` the meta file right after `\begin{document}` and place the marker at the **end
of each stem, inside the problem's unbreakable block** — all problems or none, ONE mode
per document (points XOR stars). Never hand-type `\bigstar` or "(N pts)": the literal
forms are banned by `check_prose_consistency.py`, which also fails swapped, duplicated,
missing, or unresolved markers (`--meta`; a stale file after a JSON edit is caught the
same way — re-run this renderer). The renderer is the one place difficulty tags become
gating: every problem needs an integer difficulty 1–5 or it refuses to render, naming
the offending ids. `\totalpoints` is computed — never type the sum yourself.
`build.sh` runs this automatically when the sheet uses markers or every problem is
tagged, and passes `--meta` to the checker.

### 5. Run the gate chain and compile — one command

```bash
bash "$SKILL_DIR/scripts/build.sh" /tmp/verify_TOPIC_DATE.json
```

That single command replaces what used to be nine separate steps. It discovers `ws_`/`ak_`/`ss_TOPIC_DATE.tex` and `verify_ss_TOPIC_DATE.json` next to the JSON (student-name prefixes like `leo_ws_` and tier tokens `wsS_`/`wsC_`/`wsX_` included), then runs, fail-fast:

1. `run_verify.sh` on the worksheet JSON, then the study-guide JSON
2. `check_ss_coverage.py` — every worksheet `"skill"` has a tagged study-guide entry (zero/partial worksheet tagging fails)
3. `check_facet_coverage.py` — every worksheet facet must have a study-guide worked example tagged with it, and a declared `"subtitle"` must appear verbatim in the worksheet title block (no-op for sheets without a facet plan)
4. figure rendering (when shipped and the JSON has figure/triangle problems)
5. effort-marker rendering (`render_meta.py`, when the sheet uses `\probmeta`/`\probpts` or every problem is difficulty-tagged)
6. quick-answer bank regeneration (`render_quick_answers.py` on the answer key — every build, with the two preflight teaching failures)
7. `check_layout.py` on the worksheet (figure scope + work space + answer location)
8. `check_answer_line.py` on the worksheet (`answer_unit` ↔ `\answerline`)
9. `compile.sh` for all three documents (nothing compiles after a failed gate). Each compile enforces a **page budget** read from the engine's own `Output written ... (N pages` log line (`check_log.py --max-pages`): the study guide is hard-capped at **2 pages** (its documented cap, above), and the worksheet (**8 pages**) and answer key (**6 pages**) get sanity ceilings sized from the real artifacts — the largest real 12-problem worksheet ran 7 pages with figures, so anything past the ceiling is a layout accident, not a bigger worksheet. Over budget: cut optional sections, tighten workspace, or split the sheet into two
10. `check_answer_key.py` binding `ak_` and `ss_` to their verified JSONs (values and units; for `ss_`: pairing — every examplebox is followed by its tryitbox — and role/position agreement, then per-box value binding)
11. `check_study_guide.py` — every worked example opens with a `\step` strategy line before any computation
12. `check_prose_consistency.py` on the worksheet AND the study guide (`--figs`/`--meta` passed automatically; examplebox prose givens are bound to the ss JSON; intermediate values that equal a subexpression of the entry's expr at printed precision are auto-matched; story numbers unused by the computation are expected flags)

It ends with a gate-summary table and ONE verdict line. Exit 0 = all green with three PDF paths printed; exit 1 = a gate failed (named — fix and re-run); exit 2 = green with manual-review items. **Missing `ak_`/`ss_` documents are failures, not skips** — the skill mandates three documents (`--worksheet-only` exists for the rare single-document request). Default output directory is `~/Documents/Worksheets/` (`--outdir` to override; see the Prerequisites note about headless environments).

Why the checkers exist (`build.sh` runs them for you):

- `check_answer_key.py` binds **per problem**: it segments the key (`\problem{...}`, one enumerate `\item` per problem, or one `examplebox` per worked example), requires the segment count to equal `problem_count`, and fails unless every verified value appears in **its own problem's** `\boxed{}`/`\ans{}` at the printed precision — `4.52` never satisfies a verified `4.51`, while `5`, `5.0` and `5.00` are the same answer. A swapped key, a wrong boxed value (even with the correct number in the worked steps beside it), or an unsegmentable key all hard-fail; answer-bank keys degrade to a loud whole-document `⚠` check. **Best practice:** render each boxed final answer *from* the JSON `expected` string rather than re-typing it, so the printed answer cannot drift from the verified value by construction.
- `check_prose_consistency.py` checks prose numbers and **figure-label numbers** against the JSON givens — a to-scale triangle labeled with a wrong side is flagged — and hard-stops on effort-marker faults (unresolved/swapped/missing `\probmeta`/`\probpts`, hand-typed stars or "(N pts)"). On the study guide it parses per box, so a worked example whose prose says `c = 12` while the verified expr computes with 10 is caught.
- `check_ss_coverage.py` requires a tagged study-guide entry for every worksheet `"skill"` — a guide that skips a tested skill fails before anything renders.
- `check_study_guide.py` enforces the worked-example shape: ≥2 `\step` lines per examplebox, the first prose-first (the strategy slot), and a boxed final answer for machine-verified examples. It guarantees the slot exists; the quality of the strategy sentence stays with you.
- `check_answer_line.py` binds declared `answer_unit`s to the sheet's `\answerline`s, both directions (step 3).
- `check_layout.py` enforces the figure-scope, work-space, and answer-location rules from step 3.
- `--figs` splices the rendered `\probfig{N}` bodies back into the text so `check_prose_consistency.py` and `check_layout.py` see the figures the student sees; without it, a sheet using `\probfig` exits 2 (an unchecked figure must never read as a pass). A **stale** figs file rendered before a JSON edit is caught the same way — re-run step 4b.

### 6. Deliver

Deliver all three PDFs however your agent makes files available to the user, matching the channel the request came from:

- **Local CLI / IDE agents** — the PDFs are already on the user's machine: report the three output paths clearly. If your agent has a file-send or preview capability, use it.
- **Chat-connected agents** — if the request arrived over a messaging channel and your agent can attach files, send the PDFs back on that channel; otherwise report where they are so the user can retrieve them.
- **Sandboxed / remote agents** — commit or export the PDFs so the user can retrieve them, and report where they are.

Suggested send order: skills summary first (study guide), then worksheet, then answer key.

**Printing**: Do NOT print unless explicitly asked. If asked, print worksheet + skills summary (not answer key, unless requested). Use `lpr -P <printer_name>` where available.

## Quality Checklist

Before compiling, verify each problem:
- [ ] Mathematically correct (you checked the solution)
- [ ] Unambiguous problem statement
- [ ] Appropriate difficulty for the student's level
- [ ] Sufficient work space
- [ ] Diagrams/graphs/tables included where needed
- [ ] Facets tagged and interleaved after the warm-up third (verify.py flags same-facet runs > 3)

## File Naming

```
ws_algebra2_factoring_2026-02-22.pdf   ← worksheet
ak_algebra2_factoring_2026-02-22.pdf   ← answer key
ss_algebra2_factoring_2026-02-22.pdf   ← skills summary / study guide
```

Prefix with student name when known: `leo_ws_...`, `leo_ak_...`, `leo_ss_...`

## Debugging individual gates

`build.sh` is the normal path — these are the underlying commands for isolating a single failing gate. They are the same programs `build.sh` runs; using them does NOT discharge the gate chain (finish with a green `build.sh` run before delivering):

```bash
bash "$SKILL_DIR/scripts/run_verify.sh" /tmp/verify_TOPIC_DATE.json          # 0 pass · 1 fail · 2 manual-review
bash "$SKILL_DIR/scripts/run_verify.sh" /tmp/verify_ss_TOPIC_DATE.json
python3 "$SKILL_DIR/tests/check_facet_coverage.py" /tmp/ws_TOPIC_DATE.tex /tmp/verify_TOPIC_DATE.json /tmp/verify_ss_TOPIC_DATE.json
python3 "$SKILL_DIR/tests/check_layout.py" /tmp/ws_TOPIC_DATE.tex            # figure scope + work space + answer location
python3 "$SKILL_DIR/tests/check_ss_coverage.py" /tmp/verify_TOPIC_DATE.json /tmp/verify_ss_TOPIC_DATE.json
python3 "$SKILL_DIR/tests/check_answer_line.py" /tmp/ws_TOPIC_DATE.tex /tmp/verify_TOPIC_DATE.json
python3 "$SKILL_DIR/tests/check_answer_key.py" /tmp/ak_TOPIC_DATE.tex /tmp/verify_TOPIC_DATE.json
python3 "$SKILL_DIR/tests/check_answer_key.py" /tmp/ss_TOPIC_DATE.tex /tmp/verify_ss_TOPIC_DATE.json
python3 "$SKILL_DIR/tests/check_study_guide.py" /tmp/ss_TOPIC_DATE.tex /tmp/verify_ss_TOPIC_DATE.json
python3 "$SKILL_DIR/tests/check_prose_consistency.py" /tmp/ws_TOPIC_DATE.tex /tmp/verify_TOPIC_DATE.json
python3 "$SKILL_DIR/tests/check_prose_consistency.py" /tmp/ss_TOPIC_DATE.tex /tmp/verify_ss_TOPIC_DATE.json
bash "$SKILL_DIR/scripts/compile.sh" /tmp/ws_TOPIC_DATE.tex ~/Documents/Worksheets/   # also ak_/ss_
```

## Troubleshooting

| Problem | Fix |
|---|---|
| `tectonic` not found | `brew install tectonic`, or rely on the pdflatex fallback (see Prerequisites) |
| pdflatex: `.sty` not found (enumitem, mdframed, …) | `apt install texlive-latex-extra` (pdflatex doesn't auto-download packages) |
| `worksheet-preamble.tex` not found | Compile via `compile.sh`/`build.sh` — they stage `templates/*.tex` beside your `.tex`. Don't invoke the engine directly |
| `sympy is not installed` but you installed it | You have several pythons and pip fed a different one — run the exact `<python> -m pip install sympy` command the error prints, or set `MWS_PYTHON_CANDIDATES` |
| Which JSON fields does type X take? | `python3 "$SKILL_DIR/scripts/verify.py" --schema` (always current — generated from the enforced schema) |
| Slow first compile | Downloading packages from CTAN — wait 30–60s, faster after |
| LaTeX error on line N | Check paired `$...$`, matching `\begin{}/\end{}` |
| Compile blocked: `Overfull \hbox (Npt too wide)` | Text physically overflows the printed page — shorten the line, allow a break point, or scale the figure. The log gate (`scripts/check_log.py`) blocks PDFs that would ship with off-page text; `OVERFULL_PT=5` relaxes the threshold if the overhang is verified harmless |
| Compile blocked: undefined references | A `\ref` points at a missing or typo'd `\label` — the PDF would print `??` where the number belongs. Fix the pair and recompile |
| Compile blocked: page budget exceeded | The document overran its cap (ss 2 · ws 8 · ak 6 pages, from the log's `Output written ... (N pages` line). Cut optional sections (watch-out box, vocabulary), tighten workspace, or split the sheet into two — never bypass the cap by compiling the engine directly |
| pgfplots not rendering | Ensure `\pgfplotsset{compat=1.18}` is in preamble |
| PDF not created | Read full tectonic output for the specific error |
