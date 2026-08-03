# Counting a Set and Telling How Many — Kindergarten / Grade 1

Three PDFs are ready:

- **Study guide** (`ss_counting_curr002.pdf`, 2 pages) — read this with your child first.
- **Worksheet** (`ws_counting_curr002.pdf`, 4 pages, 10 problems).
- **Answer key** (`ak_counting_curr002.pdf`, 3 pages) — the reasoning for each one, plus what to listen for.

## What the worksheet does

Every one of the ten problems shows a set of objects and asks the same question
in the end — *how many are there?* — so the whole sheet stays on one-to-one
counting and cardinality. What changes is how hard the set is to keep track of:

- **Count a set and tell how many** (problems 1, 2, 3, 5, 8): a neat ten-frame
  first, then a scattered arrangement where a child must cross objects off to
  avoid double-counting, then a full ten-frame plus loose dots (counting *on*
  from ten instead of starting over), then uneven rows, then a full tray of 16.
- **Count two groups as one set** (4, 7, 9): ducks in two places, two colours of
  blocks, and finally three baskets — the hardest version, because the count has
  to run straight through all three without restarting.
- **Tell which set has more** (6, 10): two sets counted, then compared with
  $>$ or $<$. Problem 10 gives both jars the same full ten-frame so only the
  loose marbles can decide, which is the first taste of comparing teen numbers.

Difficulty ramps 1 → 4 and no two problems use the same picture skeleton. The
pictures are counting frames and rows rather than numerals, which is the point
at this age: the child produces the number, the sheet does not hand it over.

## What was verified

**All 10 problems were machine-verified with SymPy** — nothing is flagged for
manual review, and every boxed answer in the key was bound back to the
recomputed value. Four misconception traps were declared and machine-checked as
distinguishably wrong, and they print in the key's "Common wrong answers" block:

- touching one object twice (a set of 7 counted as 8),
- skipping the object set apart from the rest (9 counted as 8),
- counting only the bigger of two groups (9 answered as 5),
- stopping after two of three baskets (9 answered as 7).

That is the part worth reading before you grade: a wrong number here usually
names the counting error exactly.

## Standards and tagging

Codes come verbatim from the repository's `references/standards-map.md`:
`K.CC.A.1–K.CC.C.7` for the counting and comparing work (6 problems) and
`1.NBT` for the four that lean on ten as a unit (12, 13, 16, and the two-jar
comparison). Every problem also carries a difficulty, a Bloom level, and a skill
tag; the three-facet plan is declared in the verify JSON and its subtitle is
bound to the worksheet title.

## Study guide

Two pages, three sections that match the three skills: counting a set in order,
counting two groups without restarting, and comparing two finished counts. Each
has a rule box, a worked example whose first step says *why* the method is
chosen, and a try-it with the answer printed upside down inside the box. It
closes with the two warnings that matter most at this age — a spread-out set is
not automatically "more", and being asked "how many?" after counting should get
the last number said, not another count.

## Gate chain

`build.sh` finished **BUILD PASSED — all gates green** (exit 0): template
shells, both verification files, skill and facet coverage, subtitle binding,
layout and work space, three compiles inside their page budgets, per-problem
answer-key binding, study-guide structure, and prose consistency.

One gate failed on the first attempt: `template-ss` rejected a `\skillheading`
of 58 characters (the cap is 57) because the skill slug was repeated in the
heading text. The slug lives in the JSON, which is what the coverage gate reads,
so the headings were shortened to plain words. Nothing about the mathematics
changed.
