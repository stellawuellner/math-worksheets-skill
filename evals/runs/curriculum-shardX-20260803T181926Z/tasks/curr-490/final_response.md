# Average Value, Accumulated Change, and Motion — AP Calculus AB/BC

Three PDFs are ready.

**Study guide (2 pages)** — four sections, each with a rule box, a two-step
worked example, and a try-it whose answer is printed upside down inside the box:

1. average value of a function — $\frac{1}{b-a}\int_a^b f$, and why the
   division is what turns area back into a height
2. accumulated change from a rate — $Q(b) = Q(a) + \int_a^b r$, including the
   net-rate case when something flows in and out at once
3. net displacement from velocity — signed, so backward motion cancels
4. total distance — $\int |v|$, found by solving $v = 0$ and splitting

A watch-out box closes with the distinction the whole set turns on: average
velocity is displacement over time, average speed is total distance over time,
and they agree only when the velocity never changes sign.

**Worksheet (6 pages, 10 problems)** — the point of the sheet is that the
integral you set up depends on what is asked, not on what is given. Problems 1
and 2 are a short warm-up (one average value, one accumulated amount), and after
that the four ideas rotate so no two adjacent problems want the same setup.
Problems 3 and 4 deliberately give the *same* velocity function and ask
different questions — net displacement (−9 m) then total distance (23 m) — which
is the cleanest way to see that the two are not the same computation. Later
problems combine more than one idea in a single question: fuel remaining
(problem 6) needs an accumulated change and a starting amount; problem 7 asks
for rest times, total distance, and then average *speed*; problem 9 needs a net
rate before anything can be integrated. The synthesis challenge (problem 10)
runs all four ideas on one particle and then asks the student to explain why two
of the answers disagree. Work space runs 6–9 cm per problem.

**Answer key (3 pages)** — quick-answer bank at the top, a generated Curriculum
section, then a stepped solution for every problem. Step 1 always names *which*
integral and why, because choosing the setup is the assessed skill. Units are
carried through and appear in the boxed answers wherever the answer has one.

**Verification.** All 10 problems were machine-checked with SymPy — 18 checks in
total, since several problems carry multiple parts. 17 passed automatically:
every definite integral (including the absolute-value integrals for total
distance) was recomputed, the two "amount at the end" answers were checked as
equations, the rest times were solved, and the average-speed arithmetic was
recomputed to three decimals.

**Flagged for manual review:** one item — problem 10(e), the short paragraph
explaining why average velocity and average speed differ here. That is genuinely
open writing, so it is labelled `manual` rather than claimed as verified. The key
gives the numbers (average speed $23/9 \approx 2.556$ vs average velocity $1$)
and says what to accept.

Standard: FUN-6 throughout. Difficulty ramps 1 → 5 across the sheet.
