Three PDFs are ready for an Algebra 1 student on arithmetic sequences as linear
functions, focused on finding and fixing off-by-one errors in sequence indexing.

- **Worksheet** (8 problems, `ws_seqindex_curr274.pdf`, 4 pages) — seven of the
  eight problems are find-and-fix items, each carrying a real indexing slip.
  Rosa computes $a_{10} = 6 + 10(5) = 56$ instead of 51 (one step too many);
  Theo reads the constant of $a_n = 4n + 7$ as the first term and says 7 when
  $a_1 = 11$; Milo counts terms from the 7th to the 23rd by subtracting and gets
  16 instead of 17; a student solves $5 + 6n = 89$ and lands on term 14 rather
  than 15 — a *clean whole number*, which is exactly why that error survives;
  Priya sums twelve terms using $a_1 + nd$ as the last term and gets 408 instead
  of 378; Dana writes $3, 10, 17, 24, \ldots$ as $a_n = 7n + 3$ and reports
  $a_{20} = 143$ when the correct linear form $a_n = 7n - 4$ gives 136; and the
  final computational item mixes the two counting errors — the sum of $a_5$
  through $a_{20}$, where a classmate averages the correct end terms but
  multiplies by $20 - 5$ and gets 735 instead of 784. Problem 8 is an open
  explanation. Work space runs 5–7.5 cm per problem.
- **Answer key** (`ak_seqindex_curr274.pdf`, 3 pages) — four numbered steps per
  problem: name the slip in words, redo the work correctly, box the answer, then
  run an *independent* check — the $n = 1$ test, substitution back into the
  sequence, the second sum formula, a three-term list countable on fingers, or
  the whole-sums subtraction $820 - 36 = 784$. It carries the generated
  quick-answer bank and the generated "Common wrong answers" block (56, 7, 16,
  14, 408, 143, 735), plus a model answer and an explicit full-credit checklist
  for the open item.
- **Study guide** (2 pages, `ss_seqindex_curr274.pdf`) — three skills matching
  the worksheet tags: count steps rather than terms (with the $n = 1$ test as the
  self-check), the line behind the sequence ($a_n = dn + b$ with $b = a_1 - d$,
  and why the constant is the value at $n = 0$), and how many terms are in a sum
  ($q - p + 1$). Each skill has a rule box, a two-step worked example and an
  upside-down try-it, plus a watch-out box on why an off-by-one index produces a
  believable number.

**Verification.** 7 of the 8 worksheet problems are machine-checked with SymPy:
five `eval` computations (including the term count $q - p + 1$ and the linear
form $dn + (a - d)$), a `solve` for the term number, and two `series` sums — one
over the first 12 terms, one over the index range 5 to 20. Problem 4 carries two
entries under one id so that both the corrected equation and its solution are
checked. All 6 study-guide results are machine-checked. Problem 8 is a genuinely
open explanation and is declared `{"type": "manual"}`; the build exits 2 with one
manual-review item, and the problem is nowhere described as machine-verified.

Seven planted wrong results are declared misconception traps (56, 7, 16, 14, 408,
143, 735). The verifier proved each one distinguishably wrong and derived from
the stated wrong method rather than typed by hand.

**Standards.** Every problem is tagged `HSF-BF.A.2, HSF-LE.A.2`, copied verbatim
from `references/standards-map.md` ("Sequences & series (explicit/recursive)"),
which covers the task's `HSF-BF.A / HSF-LE.A` reference. No code was invented.

**Gate-log note.** Worksheet prose matched 30 of 35 numbers. The flags are the
printed sequence terms in problem 6 ($3, 10, 17, 24$ — derived from the tagged
givens $a_1 = 3$, $d = 7$ rather than listed literally) and the "$n = 1$" in the
test instruction. The study-guide flags are all intermediate values inside worked
examples (90, 47, 49, 63) and the printed opening terms of each example's
sequence. No computed final value is unbound.
