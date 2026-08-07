# Solving AAS and ASA triangles with the law of sines (Precalculus)

Three PDFs are ready.

**Study guide (`ss_lawsines_curr426.pdf`, 2 pages)** — four sections, each a rule
box, a worked example whose first step names *why* that route applies, and a
try-it with the answer upside down inside the box: the angle sum and the
side–angle pairing convention; AAS, where the known side already has its partner
angle; ASA, where it does not and the third angle must come first; and the
surveying baseline, which is always ASA in disguise.

**Worksheet (`ws_lawsines_curr426.pdf`, 6 pages)** — 10 problems. **Every problem
carries its own to-scale triangle**, generated from the same verified data the
answer key uses, so the picture cannot disagree with the answer: each figure
labels only the given values and marks the unknown with a question mark. That is
the visual model this format asks for, and it is connected to notation by the
$a$-opposite-$A$ convention stated in the directions and used in every figure.
The last three problems are surveying contexts with metre units — two towers, a
footpath, two fire lookouts. Difficulty ramps 1 to 5.

**Answer key (`ak_lawsines_curr426.pdf`, 3 pages)** — worked solutions that name
which pairing is being used and why the third angle is or is not needed, plus a
sanity check on two problems (largest side faces largest angle). Two problems
print a "common wrong answer" line naming the misconception the numbers were
chosen to expose. There is also a Quick Answers bank and a generated Curriculum
section (HSG-SRT.D.10, HSG-SRT.D.11).

## What is verified, honestly

The sheet asks for **12 responses across the 10 problems**.

- **10 are machine-checked** by SymPy — one per problem. Each is checked by
  solving the whole triangle from its three given values, not by re-running the
  formula I wrote, so a mis-paired side would fail. The same `given` data drives
  the printed figures, which is why the drawings are guaranteed consistent with
  the answers.
- **2 are instructor-judged** and marked `---` in the Quick Answers bank:
  problem 5(b), explaining why two angles and one side determine the triangle,
  and problem 10(b), explaining why this data gives exactly one triangle while
  two sides and a non-included angle may not. Both are conceptual prose. The key
  prints a rubric for each; 10(b) requires the inverse sine and its two candidate
  angles to be named, not just an assertion that this case is simpler.

That matches the key's own "What is verified" note. Nothing is marked
`[unchecked]`.

Two declared misconception traps (problems 2 and 3) were recomputed and confirmed
to land on values the problems' own checks reject: inverting the ratio, and
pairing a side with an adjacent angle rather than the opposite one.
