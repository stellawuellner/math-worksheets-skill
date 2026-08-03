Here are three PDFs on writing exponential growth and decay models from data.

**Worksheet (6 pages, 10 problems).** Every problem ends with a model of the
form $y = a\cdot b^t$ written from real data, and the three ways that data
arrives are interleaved across the sheet:

- **From a table** (problems 1, 2, 5, 9): divide consecutive values, confirm the
  ratio is constant, and read the initial amount off the $t = 0$ row. Contexts
  are a bacteria culture, a drug in the bloodstream, a bouncing ball, and a
  crowdfunding total. Problem 9 makes the linear-versus-exponential decision
  explicit — the differences are not constant, the ratios are.
- **From a percent rate** (3, 4, 7): a 3 percent yearly population increase, a
  15 percent annual depreciation, a 22 percent weekly algae treatment. Each asks
  the student to check the factor by computing one period before trusting it.
- **From two readings** (6, 8, 10): the factor has been applied more than once,
  so the ratio has to be un-powered. Problem 10 is the challenge — neither
  reading is at $t = 0$, so the initial value must be recovered by working
  backwards.

Each problem states its units (milligrams, centimetres, square metres, dollars,
residents), and every problem asks for a prediction from the student's own
model, so a wrong factor shows up immediately.

**Answer key (4 pages).** Every problem is worked in steps: how the factor was
obtained, what $a$ and $b$ mean in that context, then the prediction and the
boxed answer with its unit. Notes at the end of each solution cover the
interpretation a parent can ask about — why a negative root is rejected, why
"add 3 percent ten times" undershoots, why dividing the earlier value by the
later one inverts decay into growth. The quick-answer bank at the top lists the
three declared misconception traps with the wrong number each one produces
(10400, 480, 3300), so a wrong answer can be diagnosed rather than just marked.

**Study guide (2 pages).** Three sections, one for each way of getting the
factor, each with a rule box, a worked example, and a try-it problem whose
answer is printed upside down inside the box. A closing watch-out box covers the
two errors that account for most lost marks here.

**Verification.** All 21 machine-checkable quantities across the 10 problems
were recomputed with SymPy — every growth or decay factor and every prediction —
and all 6 study-guide boxes were checked the same way. Nothing on either
document is left for manual review. The three declared traps were also checked
to confirm each wrong method lands on a number the problem's own check rejects.

Standard tagged: HSF-LE.A.2. Difficulty ramps 1 to 5 across the sheet.
