Here are the three PDFs for the Grade 7 find-and-fix set on data errors.

- **Worksheet** (`ws_bias_denom_curr199.pdf`) — 8 problems, six of them
  find-and-fix items showing a named student's written answer for the child to
  correct and diagnose. The errors are the two the focus names. **Mismatched
  denominators:** 5 red and 7 blue counters answered as 5/7; "not red" on a
  12-section spinner answered as 4/12; a class-of-30 question answered out of
  the 18 instrument players. **Counts that changed:** a green sweet eaten and
  the fraction left at 4/10; the card numbered 7 removed and "odd" left at
  10/20 — the sharp case, because the removed card was itself odd, so *both*
  numbers fall. **Biased samples:** homework times from the students who stayed
  late in the library, a cinema survey taken outside a cinema, and a closing
  club problem where only 40 of 250 members replied to an email.
- **Answer key** (`ak_bias_denom_curr199.pdf`) — Quick Answers bank, generated
  Curriculum section (7.SP.A, 7.SP.C.5, 7.SP.C.7, difficulty 1–5), and for each
  item the corrected value worked through *plus* a rubric for the diagnosis
  saying what a correct naming of the error must contain and what only earns
  half. Problem 3's rubric is explicit that spotting the total fell from 10 to 9
  is half the answer; the numerator fell too.
- **Study guide** (`ss_bias_denom_curr199.pdf`) — three sections: getting the
  denominator right, spotting a sample that was never random, and recounting
  both numbers after something is removed. Each has a rule with the tell-tale
  signs, a worked example, and a try-it with the answer upside down inside the
  box.

**Misconception traps.** Five planted wrong results are declared as machine-
checked traps (5/7, 4/10, 4/12, 10/20, 12/18). The build recomputes each wrong
method and confirms it produces a value the problem's own check *rejects* — so
none of the planted answers is accidentally also correct, which is the one way
an error-analysis item can quietly fail.

**What is verified — the key's note says "0 of 8 problems fully
machine-checked", and that needs reading carefully.** Every problem here asks
for two things: a corrected value and a written diagnosis. That is 17 responses.

- **8 are machine-checked** with SymPy: every corrected probability as an exact
  fraction from the declared counts, the sample mean, and the two population
  estimates. All eight passed, plus the five trap checks above.
- **9 are instructor-judged**: the diagnoses. Naming why a denominator was wrong
  or why a sample was not random is prose, and no checker can grade it — so each
  carries a rubric in the key rather than being quietly counted as verified.

So no problem is machine-checked *end to end*, because each one deliberately
ends in an explanation. Every number on the sheet is verified. All six
study-guide checks are machine-verified.
