Three PDFs are ready for a second- or third-grade learner on the foundations of
division, focused on the mix-up that causes most early division errors: telling
**how many groups** apart from **how many are in each group**.

- **Worksheet** (8 problems, `ws_division_curr074.pdf`) — every problem is a
  sharing story where the two given numbers have different jobs. It opens with a
  matched pair on the same kind of stickers ($18$ into $3$ bags: how many *in
  each*? — then $20$ with $5$ *in each*: how many bags?), so the child sees that
  the same-looking numbers answer two different questions. Then come four
  find-and-fix items: Ravi calling the crackers-per-plate number the number of
  plates, Leo calling the number of pots the seeds in each pot, Rio's "$8$
  groups" caught by multiplying back, and a missing-factor equation
  ($\underline{\ \ } \times 8 = 48$) that forces the child to say which job the
  blank has. Problem 7 puts Jen's story and Ben's story side by side with the
  *same two numbers* and asks about Ben's rows only. The last problem asks the
  child to explain the "in each" test in their own words and then use it.
  Work space runs 5–8 cm, declared per problem with `workspace_cm`.
- **Answer key** (`ak_division_curr074.pdf`) — three to four numbered steps per
  problem, written the way a second-grader is taught: sort the numbers by their
  job, skip-count to divide, state the answer, then multiply back to check. Each
  find-and-fix solution also names *which* number was written back and shows what
  total the wrong answer would have needed ($4 \times 4 = 16$ crackers, $8 \times
  8 = 64$ markers), which is what makes the error visible without being told. It
  carries the generated quick-answer bank and a generated "Common wrong answers"
  block, plus a full model answer and a full-credit checklist for the open part.
- **Study guide** (2 pages, `ss_division_curr074.pdf`) — three sections matching
  the worksheet's skill tags: how many are in each group, how many groups, and
  check by multiplying back. Each has a rule box (including a dot picture of
  equal groups and the "in each" giveaway), a two-step worked example, and an
  upside-down try-it, plus a watch-out box on the single most useful habit here:
  the answer is never a number the story already gave you.

**Verification.** 8 of the 9 checks are machine-verified with SymPy: seven
`eval` division computations and one `solve` for the missing factor in
$g \times 8 = 48$. All six study-guide results are machine-verified too. **Seven
planted wrong answers are declared as misconception traps** — in every case the
trap expression is the *given number itself* (`g` or `s`), which is exactly this
misconception: repeating the group count where the group size was asked for, or
the reverse. The verifier proved each is distinguishably wrong, which is why the
numbers were chosen so the two never coincide (a story with $6$ groups of $6$
would be blind to the error it is meant to catch).

Part (a) of problem 8 is genuinely open — it asks the child to describe the test
in their own words — so it is declared `{"type": "manual"}`, the build exits 2
with exactly one manual-review item, and it is not claimed as verified anywhere.
Part (b) of the same problem is machine-checked.

**Standards.** `references/standards-map.md` has no row for 3.OA.A.2 (the meaning
of division) or 3.OA.A.4 (the unknown in a multiplication/division equation),
which are the two codes closest to this focus. Rather than invent a code, seven
problems are tagged with the row that genuinely covers them —
`3.OA.A.3 / 4.OA.A.2`, multiplication and division word problems — and the
missing-factor problem is tagged `3.OA.C.7` (multiply and divide facts). A row
for 3.OA.A.2–A.4 would be a real addition to the map. The grade level prints on
the answer key only.

**Gate log.** Every gate green; both prose-consistency checks matched 100% of the
printed numbers against the verified givens.
