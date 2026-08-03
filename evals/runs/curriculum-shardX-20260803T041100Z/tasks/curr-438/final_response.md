# Conditional and Independent-Event Probabilities — three PDFs

**Worksheet** (`ws_condprob_curr438.pdf`, 10 problems, ~4 pages). A single
two-way survey table (200 students, bus riding vs. playing a sport) sits with the
directions and is used by problems 1, 2, 3 and 6, so no problem carries a figure
another problem could be read against. Four planned facets, interleaved (longest
same-facet run: 3):

- **conditional-from-table** (1, 2, 6) — $P(\text{sport}\mid\text{bus}) = 3/5$, the reversed $P(\text{bus}\mid\text{sport}) = 2/5$ with an explanation of why the same 48-student cell gives different answers, and $P(\text{bus}\mid\text{no sport}) = 2/5$
- **multiplication-rule** (4, 5, 8) — two chips passing independently ($0.98^2$), two red pens drawn *without* replacement ($5/33$, with the conditional second factor named), and a two-line factory problem ending in the total defect rate $0.032$
- **independence-test** (3, 7) — the table test ($0.6 \times 0.4 = 0.24$, independent) and a numeric case that fails the test ($0.4 \times 0.5 = 0.2 \ne 0.25$, dependent)
- **binomial-independence** (9, 10) — expand $(a+b)^3$ and interpret the $3a^2b$ term, then compute $P(\text{exactly 2 of 3}) = 0.384$ with an **open explanation** of the independence assumption

Difficulty ramps 1 → 5, and the bloom mix is 1 recall / 7 apply / 6 analyze /
1 justify. Multi-part problems carry a separate answer blank per part; the open
explanation is marked `\noansline` because the written argument is the answer.

**Answer key** (`ak_condprob_curr438.pdf`). Every solution names the reasoning
before the arithmetic — conditioning shrinks the sample space to a row or column;
without replacement makes the second factor conditional; a coefficient of 3 counts
arrangements, not probability — and checks the result (the $3.2\%$ overall defect
rate must lie between $2\%$ and $5\%$). The quick-answer bank prints the three
declared traps: 1.96 (added instead of multiplying), 0.17 (treated dependent
draws as independent), 0.128 (dropped the arrangement coefficient).

**Study guide** (`ss_condprob_curr438.pdf`, 2 pages). Four sections matching the
four facets, each with a rule box, a two-step worked example and a try-it. The
binomial section's rule box carries the $(a+b)^3$ expansion and reads each term as
an outcome count.

## Verification

Of the 15 worksheet verification entries, **14 are machine-verified** with SymPy
(`probability` as exact fractions, `eval`, `expand` for the binomial expansion)
and **1 is `manual`** — problem 10(b) is a genuinely open explanation of the
independence assumption and is labelled as such, so the build exits 2 with that
item listed. All 8 study-guide results are machine-verified. The three declared
traps were proved distinguishably wrong; every other gate is green, including
facet coverage, subtitle binding and per-problem answer binding.

Standards: `HSS-CP.A–HSS-CP.B` from `references/standards-map.md` (row
"Conditional probability & rules") for the 14 conditional/independence entries,
and `HSA-APR.C.5` (row "Binomial theorem & Pascal's triangle") for the
$(a+b)^3$ expansion. The task's `standard_refs` also lists `HSN-VM` (matrices and
vectors), which no problem on this sheet exercises, so no problem is tagged with
it.

**First-attempt gate failure (for the record):** `compile-ss` failed once on an
overfull hbox in the study guide — the line "…probability $0.7$. Find
$P(\text{exactly 2 made})$." would not break inside the math, so it ran 13 pt off
the box. Rewording the prompt in words fixed it; nothing else changed.
