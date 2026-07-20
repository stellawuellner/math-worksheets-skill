---
name: math-worksheets
description: Generate professional math practice worksheets and full answer keys as PDFs. Compiles LaTeX to PDF using tectonic (free, no account needed). Supports any math topic from elementary through AP Calculus BC (Pre-Algebra, Algebra 1/2, Geometry, Pre-Calc, Calculus AB/BC — limits, derivatives, integrals, series). Handles coordinate plane grids, geometric figures, tables, and multi-part problems. Use when a user asks for a math worksheet, practice problems, homework help sheet, or answer key for any K-12 math topic including calculus.
---

# Math Worksheet Generator

Generate a student worksheet PDF + full step-by-step answer key PDF for any math topic from elementary through AP Calculus BC. Compiles LaTeX with `tectonic` (no TeX installation required — it auto-downloads packages).

This skill is **agent-agnostic**: it works in any agent harness that can read files and run shell commands (OpenClaw, Claude Code, Gemini, Codex, etc.). Platform-specific steps below are always optional with a portable fallback.

Throughout this document, `$SKILL_DIR` means the directory containing this SKILL.md. Resolve it once at the start (e.g. `SKILL_DIR=/path/to/math-worksheets`) — do not rely on `$0`, which is only meaningful inside a script.

## Model Selection (Automatic, Best-Effort)

Reasoning models (o1, o3, DeepSeek R1, Gemini DeepThink) work through math step-by-step and make significantly fewer errors than standard models. This skill tries to detect the best available model and delegate problem generation to it. **Every branch degrades gracefully** — if detection or delegation isn't possible on the current platform, generate the problems yourself; the SymPy verification gate (Step 4) catches most errors regardless.

Rankings are bundled in `references/model-rankings.json` (human-readable notes in `references/model-rankings.md`) and updated with each skill release. Detection is fully local — no network calls.

**Step 0 — run model detection before anything else:**

```bash
result=$(bash "$SKILL_DIR/scripts/check_reasoning_model.sh")
status=$(echo "$result" | awk '{print $1}')   # FOUND_REASONING, FOUND_STRONG, or NONE
model_alias=$(echo "$result" | awk '{print $2}')
model_full=$(echo "$result" | awk '{print $3}')
```

The script inspects the host agent's config files (OpenClaw, Claude Code, Gemini, Codex) plus common `*_MODEL` environment variables. If the script can't run (no bash, no python3), skip detection and treat the status as `NONE`.

**How to delegate depends on the platform** — use whichever mechanism the current harness provides:

- **OpenClaw**: `sessions_spawn(task="<generation prompt>", model=model_alias)`
- **Claude Code**: spawn a subagent via the Agent/Task tool, passing the model override if the detected model is available to the harness; otherwise generate inline.
- **Gemini / Codex / other agents**: per-task model switching is generally not available — generate the problems inline with the current model.
- **No subagent support at all**: generate inline. This is always acceptable.

Then branch on the status:

**`FOUND_REASONING`** (o3, o1, DeepThink, DeepSeek R1) — best case. Delegate problem generation to it (or, if the current model *is* the reasoning model, just proceed). No warning needed.

**`FOUND_STRONG`** (Claude Opus) — excellent quality, use it without alarming the user. Optionally add a quiet note: *"Using Opus — solid math accuracy and excellent LaTeX. For the hardest Algebra 2 problems, a reasoning model (DeepThink/o1) would be marginally better."*

**`NONE`** — standard model only; proceed but surface a clear recommendation:
```
⚠️ No reasoning model or Opus detected. Worksheet generated with [current model].
For best accuracy, especially on multi-step problems, configure one of:
  • Gemini 2.5 Pro DeepThink  — google.generativeai.com (free tier available)
  • o1 / o3                   — platform.openai.com
  • DeepSeek R1               — platform.deepseek.com (very affordable)
  • Claude Opus               — console.anthropic.com
SymPy verification will catch most errors regardless.
```

| Status | Model examples | Action |
|---|---|---|
| `FOUND_REASONING` | DeepThink, o1, o3, R1 | Use it silently, no warning |
| `FOUND_STRONG` | Claude Opus 4.x | Use it silently, optional quiet note |
| `NONE` | Sonnet, Flash, GPT-4o | Use current model + show recommendation |

## Prerequisites

**tectonic** (LaTeX compiler — auto-downloads packages on demand). Install with whichever is available:

```bash
brew install tectonic       # macOS or Linux with Homebrew
cargo install tectonic      # any platform with Rust
sudo apt install tectonic   # Debian/Ubuntu (recent releases)
# or download a release binary: https://github.com/tectonic-typesetting/tectonic/releases
```

**python3 + sympy** for answer verification: `pip3 install sympy`

Output directory (create if needed): `~/Documents/Worksheets/`. In headless or sandboxed environments where the user won't browse `~/Documents`, use `./worksheets/` inside the workspace instead and report the paths.

## Workflow

### 1. Gather requirements

Ask (or infer from context):
- **Student**: name, grade, course (e.g. "8th grade, Pre-Algebra")
- **Topic**: e.g. "factoring trinomials", "solving two-step equations"
- **Problem count**: default 10 if not specified
- **Format preference**: timed quiz, homework practice, mixed difficulty, or topic drill

**Photo input shortcut**: If the user sends a photo of homework or a textbook page, read the image with whatever vision capability the platform provides (e.g. OpenClaw's `image` tool, or reading the image file directly in Claude Code / Gemini / Codex) to extract problem types, format, and difficulty — then mirror that style exactly.

### 2. Design problems

Design problems appropriate to the student's level. Increase difficulty gradually across the set. Every problem must be mathematically correct — verify your own solutions.

See `references/problem-library.md` for topic-specific problem type menus.

### 3. Write LaTeX source

Write **three** `.tex` files to `/tmp/`:
- `ws_TOPIC_DATE.tex` — student worksheet (blank work areas)
- `ak_TOPIC_DATE.tex` — answer key (full step-by-step solutions)
- `ss_TOPIC_DATE.tex` — skills summary / study guide (cheat sheet)

The **skills summary** is a 1–2 page reference card the student can use while working through the worksheet or when studying. It contains:
- One section per distinct skill tested (2–5 sections typical)
- A **formula/rule box** (blue) per skill — the key facts and formulas
- A **mini worked example** (green) per skill — brief pattern demonstration, simpler than worksheet problems
- An optional **watch-out box** (orange) — common mistakes worth flagging
- Optional **key vocabulary** section at the bottom

See `references/latex-templates.md` → "Skills Summary / Study Guide Template" for the full shell and box macros.

See `references/latex-templates.md` for document templates, coordinate planes, tables, geometric figures, and answer key patterns.

**Required packages** (include in every document):
```latex
\usepackage[margin=1in, top=0.75in, bottom=0.75in]{geometry}
\usepackage{amsmath, amssymb}
\usepackage{tikz, pgfplots}
\usepackage{enumitem, fancyhdr, multicol, array, booktabs}
\pgfplotsset{compat=1.18}
\usetikzlibrary{calc, angles, quotes}
```

**Work space defaults**: `\vspace{5cm}` per problem; `8cm` for multi-step; `10cm+` for graphs.

### 4. Write and run the verification file

Before compiling, write `/tmp/verify_TOPIC_DATE.json` — a structured data file describing each problem and its expected answer. The bundled `scripts/verify.py` evaluates this using SymPy. No generated code is ever executed.

```bash
bash "$SKILL_DIR/scripts/run_verify.sh" /tmp/verify_TOPIC_DATE.json
```

**JSON format:**
```json
{
  "topic": "derivatives and trig",
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
| `approx` | ✅ | Numeric expr recomputed exactly, compared within `tol` (default 0.01) — for rounded answers |
| `distance` | ✅ | Distance between two `points`; exact, or within `tol` if given |
| `midpoint` | ✅ | Midpoint of two `points`; expected is an `[x, y]` pair |
| `slope` | ✅ | Slope through two `points`; expected value or `"undefined"` for vertical |
| `polygon_area` | ✅ | Shoelace area of the ordered `points` (3+) — triangles, quads, composite grid figures |
| `triangle` | ✅ | Solves the triangle from 3 `given` values (sides `a/b/c`, angles `A/B/C`), checks `solve_for` within `tol`; degrees by default; accepts either triangle in the ambiguous SSA case |
| `manual` | 👁 | Flagged for human review — never fails automatically |

For geometry, **state the givens and let the script compute**: pass raw coordinates to `distance`/`midpoint`/`slope`/`polygon_area` and raw triangle data to `triangle` rather than doing the formula yourself in `expr`. Angle convention: side `a` is opposite angle `A` (matches the figure templates).

Use `manual` for: graph sketches, sign charts, word problem setups, two-column proofs, constructions, Riemann sum tables, series convergence arguments.

**Expression syntax** — enforced by a strict allowlist in `verify.py`; anything outside it is rejected as a failure, never executed:
- Explicit operators only: `3*x` (not `3x`), `x**2` or `x^2` for powers
- Functions: `sin cos tan asin acos atan sec csc cot sinh cosh tanh log ln exp sqrt Abs floor ceiling`
- Constants: `pi`, `E` (Euler's number), `oo` (infinity)
- Variables: `x y z t u v w a b c h k m n r s theta phi` (pick from these when writing problems)

**Strict schema:** an unknown `type`, a misspelled field, or a missing required field is a hard failure (exit 1) — never a silent skip. If you need an unverifiable problem, declare it `manual` explicitly.

**If verification fails (exit 1):** fix the LaTeX answer key and re-run. Do not compile until the answer key is correct.

### 5. Compile

```bash
bash "$SKILL_DIR/scripts/compile.sh" /tmp/ws_TOPIC_DATE.tex ~/Documents/Worksheets/
bash "$SKILL_DIR/scripts/compile.sh" /tmp/ak_TOPIC_DATE.tex ~/Documents/Worksheets/
bash "$SKILL_DIR/scripts/compile.sh" /tmp/ss_TOPIC_DATE.tex ~/Documents/Worksheets/
```

### 6. Deliver

Deliver all three PDFs however the current platform delivers files, matching the channel the request came from:

- **Chat-connected agents (e.g. OpenClaw)** — send back on the originating channel:
  - Telegram → `message` tool with `filePath` (copy to the outbound media dir, e.g. `~/.openclaw/media/outbound/`, first)
  - iMessage/SMS → `imsg` skill
  - Email → `gog` skill (all three as attachments)
- **CLI / IDE agents (Claude Code, Gemini, Codex)** — the PDFs are already on the user's machine: report the three output paths clearly. If the harness has a file-sending or preview tool, use it.
- **Sandboxed / remote agents** — commit or export the PDFs so the user can actually retrieve them, and report where they are.

Suggested send order: skills summary first (study guide), then worksheet, then answer key.

**Printing**: Do NOT print unless explicitly asked. If asked, print worksheet + skills summary (not answer key, unless requested). Use `lpr -P <printer_name>`.

## Quality Checklist

Before compiling, verify each problem:
- [ ] Mathematically correct (you checked the solution)
- [ ] Unambiguous problem statement
- [ ] Appropriate difficulty for the student's level
- [ ] Sufficient work space
- [ ] Diagrams/graphs/tables included where needed
- [ ] Problems vary across the set (not all the same sub-type)

## File Naming

```
ws_algebra2_factoring_2026-02-22.pdf   ← worksheet
ak_algebra2_factoring_2026-02-22.pdf   ← answer key
ss_algebra2_factoring_2026-02-22.pdf   ← skills summary / study guide
```

Prefix with student name when known: `leo_ws_...`, `leo_ak_...`, `leo_ss_...`

## Troubleshooting

| Problem | Fix |
|---|---|
| `tectonic` not found | `brew install tectonic` |
| Slow first compile | Downloading packages from CTAN — wait 30–60s, faster after |
| LaTeX error on line N | Check paired `$...$`, matching `\begin{}/\end{}` |
| pgfplots not rendering | Ensure `\pgfplotsset{compat=1.18}` is in preamble |
| PDF not created | Read full tectonic output for the specific error |
