# Comparing Distributions and Compound Events (Grade 6–7)

Three PDFs are ready.

- **Worksheet** (`ws_distprob_curr200.pdf`, 6 pages) — 12 problems in an
  interleaved-synthesis format. Two dot plots on a **shared scale** (Team Alpha
  and Team Bravo, eight quiz scores each) sit above the problem list, with the
  raw ordered lists printed beside them, plus a bar graph of after-school club
  sign-ups. The two teams were chosen so their medians are identical (15.5) and
  their spreads are not (range 9 vs 19, IQR 4 vs 9) — center alone cannot tell
  them apart, which is the point the sheet is built around. The chance devices
  (a 12-marble bag, an 8-section spinner, a number cube) are listed once so
  every probability problem draws on the same declared sample spaces.
  Problems 1–4 are the blocked warm-up (median, median, range, range); after
  that the four methods rotate with no same-method run longer than two:
  simple probability, IQR, an independent compound event, the mean, a
  without-replacement compound event, a read-the-graph probability, an
  "at least one" complement problem, and a synthesis challenge that compares
  the two distributions and then draws one score from each list.
- **Answer key** (`ak_distprob_curr200.pdf`, 5 pages) — the generated
  quick-answer bank, then a full solution per problem: which measure the
  question calls for and why, the quartile split written out, and for every
  compound event an explicit statement of whether the first stage changes the
  second. Four problems carry a named common wrong answer (15 for reporting one
  middle value, 14 for using the maximum as $Q_3$, 19.43 for dividing by 7, and
  3/4 for adding the two single-spin probabilities instead of using the
  complement).
- **Study guide** (`ss_distprob_curr200.pdf`, 2 pages) — four sections matching
  the four worksheet skills (comparing centers, comparing spreads, single-event
  probability, compound-event probability). Each has a rule box, a worked
  example whose first step says why that method applies, and a try-it with the
  answer upside down inside the box. The compound-event box names all three
  cases a student must discriminate: independent, dependent (no replacement),
  and "at least one" via the complement.

## Verification

14 of the 15 checks are machine-verified with SymPy: 7 `stats` checks
(median ×2, range ×2, IQR ×2, mean) computed from the same two data arrays that
draw the dot plots, 6 `probability` checks as exact fractions (simple,
independent compound, dependent compound, complement, and the two-list
synthesis draw), and 1 `read_data` total bound to the same array that draws the
club bar graph. Problems 10 and 12 carry more than one verify entry under one
problem id.

One item is labelled for manual review, and the key says so at the point of
use:

- problem 12(b) — "the two teams have the same median; which is more
  consistent, using both IQRs and both ranges?" The IQR it rests on (4) and the
  compound probability in part (c) are machine-checked; the written comparison
  is not.

It is encoded as `{"type": "manual", ...}` rather than claimed as verified,
which is why the build exits 2. All 8 study-guide items (4 worked examples +
4 try-its) are fully machine-verified, and each of the four worksheet facets
has a matching worked example.

Four misconception traps are declared and machine-proved distinguishable from
the correct answers; the key prints each as a named wrong answer.

**Standards used:** `6.SP.B.5` for the center and spread measures (row
"Mean/median/mode/range, data distributions"), `6.SP.A` for the written
variability comparison (row "Statistical questions & variability"),
`7.SP.C.7` for single-event probability (row "Simple/theoretical probability"),
and `7.SP.C.8` for the compound events (row "Compound events, tree diagrams") —
all taken verbatim from `references/standards-map.md`.

## Build

All 21 gates green on the second attempt (exit 2 for the one declared manual
item). The first build failed one gate, `answer-key-ak`, and the cause is worth
recording because it is a checker behaviour rather than a wrong answer: in a
problem segment holding **two** boxed answers, `check_answer_key.py`
concatenates the box contents with a space before scanning them, and its
mixed-number rule then read `40 \dfrac{3}{8}` as the single value 40.375, so
neither 40 nor 3/8 was found. Printing the second box as
`\ans{P = \dfrac{3}{8}}` separates the integer from the fraction and both
values bind. Page counts: worksheet 6 (budget 6), answer key 5 (budget 6),
study guide 2 against its hard 2-page cap.
