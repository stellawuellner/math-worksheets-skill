Here are the three PDFs for the Grade 7 sampling-and-probability workshop.

- **Worksheet** (`ws_samples_prob_curr198.pdf`) — 10 applied problems, every one
  stating its givens and units plainly and carrying no decorative story detail.
  Three strands run through it: **simple probability models** (a bag, a spinner,
  a "not yellow" complement, a two-part spinner, a jar drawn with replacement),
  **scaling a random sample to a population** (50 students to 600, 80 light
  bulbs to a batch of 2000, and a capture–recapture fish estimate), and
  **judging whether a sample can be trusted** — a school survey given only to
  the basketball team, and two ways of picking 20 club members from 200. The
  basketball item is deliberate: the arithmetic works out to 704 students and
  the estimate is still worthless, which is the lesson.
- **Answer key** (`ak_samples_prob_curr198.pdf`) — Quick Answers bank,
  generated Curriculum section (7.SP.A, 7.SP.C.5 and 7.SP.C.7, difficulty 1–5),
  and worked solutions that write the fraction before reducing it and say why
  each scaling step is allowed. The expected-value solution is explicit that 40
  reds in 200 draws is a long-run expectation, not a promise.
- **Study guide** (`ss_samples_prob_curr198.pdf`) — three sections matching the
  three strands, each with a rule, a two-step worked example, and a try-it with
  the answer upside down inside the box; plus a watch-out that says to check how
  a sample was chosen *before* scaling it up.

**What is verified.** The sheet asks for 17 responses. **14 are machine-checked**
with SymPy — every probability computed as an exact fraction from the declared
favourable and total counts, every population estimate recomputed from the
sample counts, the expected number of reds recomputed from the probability, and
the fish estimate solved from the proportion 300/x = 9/60 rather than compared
against a typed number. **3 are instructor-judged**: whether the basketball-team
survey is a random sample (5a), which of the two club methods is random (8a),
and the assumption behind the fish estimate together with the direction of the
error if tagged fish are easier to catch (10c). Each carries a rubric in the key
saying what a correct response must contain, and the bank marks them `---`. All
six study-guide checks are machine-verified.
