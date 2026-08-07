Here are the three PDFs for the Grade 7 "write the inequality" concept practice.

- **Worksheet** (`ws_ineq_from_words_curr181.pdf`) — 10 verbal constraints, each
  naming its unknown, each asking for the inequality and its solution. The whole
  sheet turns on one distinction: does the limit itself count? So it alternates
  **at most / at least** items (a 450 kg lift, a 36-point pass mark, a 60 km
  badge) with **fewer than / more than** items (a film for over-12s, a parcel
  under 20 kg, fewer than 24 players in six teams), and then adds a starting
  amount (taxi start fee, bookends on a shelf, water already in a pool, a
  driver's fee on a bus tour).
  Two problems carry a **test-value table** — try the boundary and one number
  either side, mark which the situation allows — because that table is exactly
  what tells ≤ apart from <, and it is the model the directions teach.
- **Answer key** (`ak_ineq_from_words_curr181.pdf`) — Quick Answers bank
  (solutions printed as intervals for fast grading), generated Curriculum
  section (7.EE.B.4, difficulty 1–5), and solutions that name the phrase, choose
  the sign because of it, and only then solve. Where a table was used, the key
  reads the table back: 18 boxes weigh exactly 450 kg and are allowed, 19 weigh
  475 kg and are not.
- **Study guide** (`ss_ineq_from_words_curr181.pdf`) — three sections (boundary
  included, boundary excluded, limits with a starting amount), each with the
  signal phrases, the test-value check, a two-step worked example and a try-it
  with the answer upside down inside the box; plus a watch-out that an
  inequality's solution set can contain numbers the situation cannot use.

**What is verified.** The sheet asks for 14 responses. **10 are machine-checked**
with SymPy: each solution set is recomputed with `solveset` over the reals from
the inequality itself and compared with the declared interval, so a wrong
boundary *or a wrong strictness* fails. **4 are instructor-judged** — the three
"write the inequality" responses on problems 4, 9 and 10, and the closing
explanation on 10(c) about why not every number in the solution set is a
possible group size. Those are genuinely open (several arrangements of the same
inequality are correct), so each carries a rubric in the key naming the
acceptable forms and the specific wrong ones, and the bank marks them `---`.
All six study-guide checks are machine-verified.
