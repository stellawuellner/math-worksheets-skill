# Triangle Congruence: Solving for Corresponding Parts — High School Geometry

Three PDFs are ready:

- **Worksheet** (`ws_congruence_curr313.pdf`, 4 pages) — 8 problems. The directions
  state the one idea the whole sheet runs on (a congruence statement is read *in
  order*, and CPCTC turns matched parts into an equation), followed by a
  **value-free reference figure** showing two triangles labelled $A,B,C$ and
  $D,E,F$ — deliberately carrying no measurements, so no student can read a
  neighbouring problem's numbers off it. Each problem states its own givens and
  units. Work space is 5–6 cm per single-part problem and 4–5.5 cm per part.
- **Answer key** (`ak_congruence_curr313.pdf`, 2 pages) — quick-answer bank, then
  for every problem: which letters correspond and why, the CPCTC equation that
  follows, each algebra step, and a substitution check where one exists. Problem 7
  includes a complete model two-column proof; problem 8 includes a model
  explanation of the correspondence error.
- **Study guide** (`ss_congruence_curr313.pdf`, 2 pages) — three sections
  (corresponding sides, corresponding angles, reading the correspondence
  correctly), each with a rule box, a two-step worked example and a try-it, plus a
  watch-out box on the most common lost mark: solving for $x$ and stopping when the
  question asked for a measure.

## Problem set

| # | Task | Skill |
|---|---|---|
| 1 | $AB = 3x+2$, $DE = 17$ | corresponding sides |
| 2 | $m\angle P = 4y-10$, $m\angle S = 50^\circ$ | corresponding angles |
| 3 | Both sides algebraic: $2x+7 = 4x-9$ | corresponding sides |
| 4 | Angle sum first, then carry $\angle C$ across to $\angle F$ | corresponding angles |
| 5 | Two-part: solve, then report $m\angle R$ in degrees | corresponding angles |
| 6 | Bridge truss, two-part: solve, then report $AC$ in metres | corresponding sides |
| 7 | Two-column SAS proof, then use the congruence it establishes | correspondence |
| 8 | Error analysis on $\triangle ABC \cong \triangle DFE$ | correspondence |

Difficulty ramps 1 → 5. Problem 4 is the one that requires the angle sum before
CPCTC applies; problem 7 is the only one where the congruence must be *proved*
before it can be used, which is the real high-school version of this skill.

## Verification

**12 checks over 8 problems: 10 machine-verified, 2 manual.** Every CPCTC equation
is solved independently by SymPy, and the two problems that ask for a measure
rather than a variable carry a second `eval` check of the substituted value
($m\angle R = 22$ degrees, $AC = 25$ m) — with those units **declared in the JSON
and gate-bound** to the sheet's `\answerline` and the key's boxed answer, so a
metres answer cannot drift to another unit.

The 2 manual items are the genuinely open ones, declared `{"type": "manual"}`:
problem 7(a), the two-column proof, and problem 8(a), the explanation of why the
correspondence names $\overline{DF}$ rather than $\overline{DE}$. No CAS can grade
a proof or an explanation, so neither is claimed as verified; the build reports
them and exits 2, which is the correct outcome. Both still get a full model answer
in the key.

**Figures:** no problem carries a valued figure. Triangle figures on this sheet
would have to be hand-drawn (the shipped renderer covers right triangles from a
`triangle`/`approx`/`eval` given-dict, which these congruence pairs are not), and
a hand-drawn figure with numbers is exactly the retyping drift the pipeline
forbids. The value-free reference figure carries the labelling convention instead,
and every measurement lives in the problem text where the checkers can bind it.

Standard `HSG-CO.A–HSG-CO.D` (congruence: transformations, triangle congruence,
proofs) on every problem, taken verbatim from `references/standards-map.md`; the
task's `HSG-CO.B / HSG-CO.C` sits inside that row's range.

Gate verdict: **BUILD PASSED — all gates green, 2 manual-review items (exit 2)**.
