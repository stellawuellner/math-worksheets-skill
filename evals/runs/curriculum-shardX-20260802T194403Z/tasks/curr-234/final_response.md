# Diagnosing Swapped Input-Output and Function-Notation Errors (Grade 8 / Pre-Algebra)

Three PDFs are ready for an eighth-grade or pre-algebra student, built entirely
around one idea: almost every function-notation mistake is a number put in the
wrong slot.

- **Worksheet (4 pages, 8 problems).** Problem 1 evaluates `f(3)`; problem 2 asks
  for the input that makes `f(x) = 19` — the same rule run in the opposite
  direction, so the two questions can be contrasted. Four problems are
  find-and-fix items with a named student and their actual work: Priya reads a
  function table backwards, Jo writes `f(2+3) = f(2)+f(3)`, Kim computes `C(28)`
  when the \$28 is money (an output), and Marcus evaluates `h(12)` when 12 was
  the target output. Problem 6 makes Theo compare two functions properly — at the
  same input. Problem 8 asks the student to write the rule they would give a
  classmate for telling an evaluate question from a solve question, and to show
  it working on `f(3)` and `f(x) = 3`.
- **Answer key (2 pages).** Every solution names the swap in words before it does
  any algebra, checks solved inputs by evaluating forwards, and says what a
  wrong answer would have meant. Problem 8 carries a model answer plus explicit
  accept/reject guidance for the grader.
- **Study guide (2 pages).** Three sections: what `f(a)` names (and why `f( )` is
  not multiplication), the one-question test for evaluate vs solve, and how to
  read a function table in either direction. Each has a rule box, a worked
  example that opens with the decision, and a try-it with the answer inverted
  inside the box.

## Verification

**7 of 8** worksheet problems were machine-checked with SymPy. Problem 8 asks the
student to write a rule in their own words, so it is declared
`{"type": "manual"}` rather than claimed as verified — the build exits 2 and says
so, which is the correct outcome for an open response, not a failure. All **6**
study-guide boxes (3 worked examples + 3 try-its) are machine-verified.

**Six misconception traps are declared and machine-checked**, one for each
planted wrong result: 2 (solving when you should substitute), 71 (substituting an
output), 4 (reading the table backwards), 10 (splitting `f(2+3)`), 73 (`C(28)`),
and -42 (`h(12)`). Verification proves each of those values is one the problem's
own check rejects, so every find-and-fix item genuinely discriminates the error
it targets; the answer key prints them as a "common wrong answers" block for
grading. The full gate chain is green.
