# Find-the-mistake set: indexes, ratios and convergence

Three PDFs for your Algebra 2 student, all on **diagnosing index, common-ratio and
convergence errors** in sequences, series and binomial expansions:

- **`ws_seqerr_curr394.pdf`** — the student worksheet, 8 problems, 4 pages.
- **`ak_seqerr_curr394.pdf`** — the full step-by-step answer key, 4 pages.
- **`ss_seqerr_curr394.pdf`** — a 2-page study guide.

## Every problem quotes a real wrong answer

This is an error-analysis sheet, so each problem starts from a value someone actually got and
asks for the correct one:

| # | The quoted error | What it tests |
|---|---|---|
| 1 | fifth term of $a_n = 4n+3$ given as $19$ | counting from $n = 0$ |
| 2 | $\sum_{k=1}^{4}(2k+1)$ given as $25$ | an extra $k = 0$ term |
| 3 | common ratio of $5, 15, 45$ given as $10$ | subtracting instead of dividing |
| 4 | third term of $(x+2)^4$ given coefficient $32$ | index $k=2$ versus $k=3$ |
| 5 | $3 + 6 + 12 + \cdots$ summed as $-3$ | the convergence condition |
| 6 | first $20$ terms of $5n-2$ summed as $1008$ | 21 terms instead of 20 |
| 7 | coefficient of $x^2$ in $(2x+3)^5$ given as $540$ | not squaring the $2$ |
| 8 | (synthesis) ratio, first term and six-term sum from two given terms | — |

Problems 1 and 5 are the two full find-and-fix items: the student produces the correct value
*and* writes the diagnosis. The rest name the faulty move in the stem and ask for the
correction, which keeps the sheet moving.

## The planted wrong answers are machine-checked

Every quoted wrong value is declared as a misconception trap, recomputed by the verifier, and
confirmed to be *distinguishably* wrong — a trap the problem's own check would accept is
rejected as a bad problem design. Seven traps are declared (problems 1, 2, 3, 4, 5, 6, 7),
and the answer key prints them in a **Common wrong answers** block, so a wrong answer on the
page tells you which misconception the student is carrying.

## What was verified, and what was not

The key's generated note says it exactly: **12 of the 14 answers are machine-checked with
SymPy; 2 are instructor-judged.**

- **Machine-checked (12):** every corrected value, both series sums (including the infinite
  one), the full expansion of $(x+2)^4$, both binomial coefficients, and all three parts of
  the synthesis problem were recomputed independently.
- **Instructor-judged (2):** the written diagnoses in **1(b)** ("explain the error that
  produced 19") and **5(a)** ("why is $-3$ meaningless here"). These are prose and cannot be
  machine-graded; each is marked `---` in the Quick Answers bank, and the key states what a
  full-credit response must contain — for 1(b), naming the starting index and which $n$ the
  fifth term uses; "they used the wrong number" is explicitly not enough.

## Study guide

Three sections, each with a rule box, a worked example whose first step says why the method
applies, and a try-it with the answer upside down inside the box: reading an index, common
ratio and geometric sums (with the convergence condition stated as a condition, not a
footnote), and binomial terms by index. A watch-out box carries the $3 + 6 + 12 + \cdots$
non-convergent case explicitly. All 9 of its worked answers are machine-verified.
