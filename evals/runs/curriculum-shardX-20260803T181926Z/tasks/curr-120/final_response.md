# Factor detective: factors, multiples, primes and patterns — three PDFs

Here is a 12-problem set for grades 4–5 on using how a number is *built* — its
factors — to crack divisibility and pattern puzzles.

**What is in each document**

- **Worksheet** (`ws_factorpuzzles_curr120.pdf`, 5 pages). Twelve puzzles that
  rotate between four tools: *factor pairs and primes*, *divisibility rules*
  (including the digit-sum test for 3), *multiples and first common multiples*,
  and *number patterns*. The first two problems are a short warm-up; after that
  the tools are interleaved, so the child has to decide which one a puzzle
  needs. Highlights: "Ari says 51 is prime — show it is not"; a riddle (a
  number in the thirties divisible by 3 and 4); two bells ringing every 8 and
  12 minutes; "Ravi says 91 must be prime because it is odd"; and a challenge
  about a number with exactly three factors whose middle factor is 7. Numbers
  stay in the grade 4–5 range and every problem has room to show a factor pair,
  a digit sum, or a skip-count.
- **Answer key** (`ak_factorpuzzles_curr120.pdf`, 3 pages). Answers at a glance,
  then a step-by-step solution for each puzzle written the way a child works —
  skip-counts spelled out, factor trees described — with the final answer boxed
  and a "listen for" note naming the usual wrong answer (35 for the 8th term,
  from counting eight jumps instead of seven; 96 for the bells, from
  multiplying 8 by 12 instead of finding the *first* common multiple).
- **Study guide** (`ss_factorpuzzles_curr120.pdf`, 2 pages). Four short
  sections — factor pairs and primes, divisibility rules, multiples and first
  common multiples, number patterns — each with the rule, a worked example
  that opens by saying why that method is the quick one, and a try-it whose
  answer is printed upside down inside the box.

**What was verified**

All 14 machine-checkable answers were recomputed with SymPy before compiling:
every factor-pair partner, both digit sums, the prime factorisation of 60, both
first-common-multiple problems (checked twice each — once as a multiple of each
starting number), the pattern term, the riddle answer, and the comparison in
problem 4. The key was then bound problem-by-problem to those values, and the
"minutes" unit on problem 10 is verified on both the sheet and the key.

**Flagged for manual review (2 items)**

- Problem 11(b) — explaining why "odd" does not mean "prime", and how far you
  have to test for factors. The factor pair $91 = 7 \times 13$ is verified; the
  explanation is a written answer, with a model in the key.
- Problem 12(b) — explaining why a number with exactly three factors must be a
  prime times itself. The answer 49 is verified; the reasoning is the written
  half, and the key gives a model argument plus two examples (4 and 25) to test
  it against.

Suggested order: study guide first, then the worksheet, then the answer key.
