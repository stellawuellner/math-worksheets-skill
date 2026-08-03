# Diagnosing Swapped Input–Output and Function-Notation Errors (Grade 8 / Pre-Algebra)

Three PDFs are ready for an eighth-grade or pre-algebra student, built entirely
around one idea: almost every function-notation mistake is a number put in the
wrong slot.

- **Worksheet (8 problems).** Problem 1 evaluates $f(3)$; problem 2 asks for the
  input that makes $f(x) = 19$ — the same rule run in the opposite direction, so
  the two questions can be contrasted. Four problems are find-and-fix items with
  a named student and their actual work: Priya reads a function table backwards,
  Jo writes $f(2+3) = f(2)+f(3)$, Kim computes $C(28)$ when the \$28 is money (an
  output), and Marcus evaluates $h(12)$ when 12 was the target output. Problem 6
  makes Theo compare two functions properly — at the same input. Problem 8 asks
  the student to write the rule they would give a classmate for telling an
  evaluate question from a solve question, and to show it working on $f(3)$ and
  $f(x) = 3$.
- **Answer key.** Every solution names the swap in words before it does any
  algebra, checks solved inputs by evaluating forwards, and says what a wrong
  answer would have meant. Problem 8 carries a model answer plus explicit
  accept/reject guidance for the grader. The generated quick-answer bank sits
  directly under the title block, followed by the **Common wrong answers** block.
- **Study guide (2 pages).** Three sections: what $f(a)$ names (and why $f(\ )$
  is not multiplication), the one-question test for evaluate vs solve, and how to
  read a function table in either direction. Each has a rule box, a worked
  example that opens with the decision, and a try-it with the answer inverted
  inside the box.

## Verification

**7 of 8** worksheet problems were machine-checked with SymPy. Problem 8 asks the
student to write a rule in their own words, so it is declared
`{"type": "manual"}` rather than claimed as verified — the build exits 2 and says
so, which is the correct outcome for an open response, not a failure. All **6**
study-guide boxes (3 worked examples + 3 try-its) are machine-verified.

**Seven misconception traps are declared and machine-checked**, one for every
planted wrong result plus a second reading of Jo's error: 2 (solving when you
should substitute), 71 (substituting an output), 4 (reading the table backwards),
10 (splitting $f(2+3)$ additively), 21 (multiplying the two outputs), 73
($C(28)$), and $-42$ ($h(12)$). Verification proves each of those values is one
the problem's own check rejects, so every find-and-fix item genuinely
discriminates the error it targets; the key prints them all in its "Common wrong
answers" block so a wrong paper names its own misconception. Problem 6 is a
`compare` item, a type the trap schema does not cover, and problem 8 is `manual`
— those are the only two without traps.

Standards are tagged `8.F.A.1–8.F.B.5` exactly as `references/standards-map.md`
writes it.

Gate verdict: **BUILD PASSED — 1 verification run flagged manual-review items
(exit 2)**, on the first attempt; every other gate green. The answer key
`\input`s the quick-answer bank plainly, with no `\raggedright` and no
`\emergencystretch`, and the seven-line "Common wrong answers" block compiles
with no overfull box.
