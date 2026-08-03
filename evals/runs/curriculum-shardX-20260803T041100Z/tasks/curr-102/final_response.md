# Powers of Ten and Place-Value Relationships — Grades 4–5

Three PDFs are ready:

- **Study guide** (`ss_powersoften_curr102.pdf`, 2 pages) — read this first.
- **Worksheet** (`ws_powersoften_curr102.pdf`, 5 pages, 12 problems).
- **Answer key** (`ak_powersoften_curr102.pdf`, 3 pages) — full place-value reasoning, not just results.

## What the worksheet does

Every problem is the same fact used a different way: *each place is worth ten
times the place to its right*. The sheet rotates through four uses of it, one
after another, so the student has to decide which one a problem calls for
instead of repeating a procedure twelve times:

- **Digit-value relationships** (1, 4, 8): how many times as much is one digit
  worth as another. Problem 4 runs it the other direction with decimals
  ($0.08$ against $0.8$), and problem 8 is the trap version — the two 5s in
  55500 are *two* places apart, so the answer is 100, not 10.
- **Powers of ten in exponent form** (2, 6, 11): what $10^3$ means, writing
  60000 as $6 \times 10^4$, and reading expanded form
  $3\times10^4 + 7\times10^2 + 5$ back into standard form — where the missing
  thousands and tens places are the whole point.
- **Shifting digits by 10, 100, 1000** (3, 7, 10): a whole number times 100, a
  decimal times 1000, and a division by 100. The key insists on "the digits
  move $n$ places" rather than "add $n$ zeros", because the zero rule breaks the
  moment a decimal appears.
- **Rounding to a place to estimate** (5, 9, 12): rounding *is* rounding to a
  power of ten. Problem 12 closes the sheet by rounding a divisor to the nearest
  ten so that $8120 \div 40$ becomes a shift plus a basic fact, then asks
  whether the estimate lands high or low and why.

A value-free place-value chart is printed with the directions as the shared
reference; no problem carries its own figure, so nothing on the page can be
mistaken for another problem's givens. Difficulty ramps 1 → 5 and the four
facets are fully interleaved after the opening pair.

## What was verified

**All 12 problems were machine-verified with SymPy** — nothing is flagged for
manual review, and every boxed answer in the key was bound back to the
recomputed value. Six misconception traps were declared and machine-checked as
distinguishably wrong; they print in the key's "Common wrong answers" block:

- rounding to the nearest hundred when asked for the nearest thousand (8100 for 8000),
- "one place left is ten times" applied to digits two places apart (10 for 100),
- rounding 2905 up to 3000 by reading the ones digit instead of the tens digit,
- multiplying by 100 where the problem divides (450000 for 45),
- dropping the empty places in expanded form (375 for 30705),
- rounding the divisor 39 down to 30 instead of to the nearest ten.

Problem 12(c) also asks for a one-sentence explanation; the key gives a model
answer and states what to accept. The value on every answer line is the
machine-checked one.

## Standards tags

All twelve problems carry a code from `references/standards-map.md`. Four keep
the codes they already had — `5.NBT.B.7 / 6.NS.B.3` for the two decimal-shift
problems, `2.NBT.B.5 / 3.NBT.A.2 / 4.NBT.B.4` for the two multi-digit
estimation problems. The other eight (1, 2, 3, 6, 8, 10, 11, 12) are tagged
**`4.NBT.A.1–A.3 / 5.NBT.A.1–A.2`**, verbatim from the map's "Place value &
powers of ten (gr 4–5)" row, which is exactly what they exercise: a digit
worth ten times the digit to its right, powers of ten in exponent form,
shifting digits by 10/100/1000, expanded form written with powers of ten, and
rounding to a named place. The earlier build left those eight untagged because
that row did not yet exist in the map. Everything else (difficulty, Bloom
level, skill, facet) was already tagged on all twelve.

## Study guide

Two pages, four sections matching the four facets, opening with the place-value
chart and the one rule that generates all of it. Each section has a rule box, a
worked example whose first step says *why* that method applies, and a try-it
with the answer printed upside down inside the box. It closes with the two
errors this topic produces most: answering "ten times" without counting how many
places apart the digits are, and rounding by the wrong digit.

## Gate chain

`build.sh` finished **BUILD PASSED — all gates green** (exit 0): template
shells, both verification files, skill and facet coverage, subtitle binding,
layout and work space, three compiles inside their page budgets (5 / 3 / 2
pages), per-problem answer-key binding, study-guide structure, and prose
consistency.

One gate failed on the first attempt: `verify-ws` rejected problem 5's declared
trap, because rounding $4780 + 3240$ to the nearest hundred and to the nearest
thousand both give 8000 — the problem could not distinguish the error it
claimed to target. The givens were changed to $4780 + 3260$, where the two
roundings give 8000 and 8100, and the trap became meaningful. That is the gate
doing exactly what it exists for.
