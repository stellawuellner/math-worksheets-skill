Here are three PDFs on reading and writing teen numerals and number words — a
10-problem fluency worksheet, a full step-by-step answer key, and a two-page
study guide.

**Worksheet** (`ws_teenwords_curr032.pdf`, 3 pages). Ten problems, no two built
on the same skeleton, ramping from a single word-to-numeral translation to
checking someone else's work:

- Problems 1, 2, 5: write the numeral for a spoken word — *thirteen*,
  *seventeen*, and then *eleven*, which is harder because the word never says
  its ones part out loud.
- Problems 3 and 7: go the other way from the numerals 15 and 12 — first how
  many ones, then the number word itself.
- Problems 4 and 6: the ten-and-ones structure directly (16, and *eighteen*
  written as a numeral and then split).
- Problem 8: write the numerals for *fourteen* and *nineteen*, then compare
  them.
- Problem 9: Ravi wrote *fifteen* as 51. The child writes the correct numeral
  and explains the swap. That wrong answer, 51, is not a made-up number — it is
  declared as a misconception trap and the system recomputed it from the
  mistaken method, so the key can tell you what a child who writes 51 was
  thinking.
- Problem 10: three number words ordered least to greatest as numerals.

A word bank sits in the directions, and best-attempt spelling is explicitly
accepted so a first-grader is not blocked by orthography.

**Answer key** (`ak_teenwords_curr032.pdf`, 3 pages). Every problem restated
and worked, always through the same idea — the word says the ones piece first,
the numeral writes the ten first. Quick Answers and a Curriculum block (1.NBT)
sit at the top.

**Study guide** (`ss_teenwords_curr032.pdf`, 2 pages). Four sections: word to
numeral, numeral to word, finding the ones in a teen numeral, and comparing two
teen numerals. Each has a rule box (including the word bank and the three words
that must simply be learned — eleven, twelve, thirteen), a worked example, and
a try-it with the answer upside down inside the box.

**How much of this is machine-checked.** 7 of the 10 problems are fully verified
with SymPy: every numeral written from a word was checked as ten plus its ones
(10 + 3 = 13, 10 + 7 = 17, 10 + 1 = 11, 10 + 8 = 18, 10 + 4 = 14, 10 + 9 = 19,
10 + 5 = 15), every ones count as the numeral minus ten, both comparison
symbols, and the final ordering. The remaining 3 responses are open: writing
the word *fifteen* (problem 3b), writing the word *twelve* (problem 7b), and
explaining Ravi's swap (problem 9b). A spelled word is prose, not a computed
value, so those are flagged rather than claimed — the Quick Answers strip prints
`---`, the "What is verified" note names problems 3, 7 and 9, and the key gives
a rubric for each, including which near-misses earn half credit. Every numeric
half of those three problems is machine-checked.
