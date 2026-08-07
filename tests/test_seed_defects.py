#!/usr/bin/env python3
"""test_seed_defects.py — the calibration seeder's transforms.

These pin the two properties that make a seeded run mean anything:

  1. A transform that cannot apply returns None, so a case that cannot carry
     its assigned defect is SKIPPED rather than shipped unseeded. Silently
     counting an unmodified sheet as seeded would deflate the judge's measured
     detection rate with sheets that have nothing to detect.
  2. A transform changes the defect and NOTHING else. The seeded corpus is
     compared against its source; any incidental edit shows up as a difference
     the judge might react to, and the manifest would attribute that reaction
     to the planted defect.

The gate-invisibility of each class is not asserted here — it is MEASURED, by
seed_defects.py running the real build chain and dropping anything a gate
catches. An assertion would only restate the catalogue's own claim.
"""
import copy
import json
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "evals"))
import seed_defects as S  # noqa: E402

FAILS = []


def check(name, cond, extra=""):
    print(f"  {'✅' if cond else '❌'} {name}" + (f" — {extra}" if extra else ""))
    if not cond:
        FAILS.append(name)


rng = random.Random(S.SEED)

# ── worked-step-error ───────────────────────────────────────────────────────
print("worked-step-error corrupts a step and leaves the box alone:")

AK = r"""\problem{Rewrite $y = x^2 + 6x + 5$ in vertex form.}
\textbf{Solution:} Half of $6$ is $3$.
\begin{align*}
  y &= (x^2 + 6x + 9) - 9 + 5 \\
    &= (x + 3)^2 - 4
\end{align*}
\ans{y = (x+3)^2 - 4}
"""

out, where = S.seed_worked_step_error(AK, random.Random(S.SEED))
check("it applies to an answer key with a worked derivation", where is not None)
check("the boxed answer is untouched", r"\ans{y = (x+3)^2 - 4}" in out)
check("the final align line is untouched", r"&= (x + 3)^2 - 4" in out)
check("exactly one line differs from the source",
      sum(a != b for a, b in zip(AK.split("\n"), out.split("\n"))) == 1,
      where)
check("the stem is untouched", r"$y = x^2 + 6x + 5$" in out)

# No align* block => nothing to corrupt => skip, never a silent pass-through.
out, where = S.seed_worked_step_error(
    r"\problem{Add.} \textbf{Solution:} Add them. \ans{7}",
    random.Random(S.SEED))
check("an answer key with no derivation is skipped, not shipped unseeded",
      where is None)

# A single-line align* has no INTERMEDIATE step; corrupting its only line
# would contradict the box directly, which is a different, louder defect.
out, where = S.seed_worked_step_error(
    "\\begin{align*}\n  y &= 4\n\\end{align*}\n\\ans{4}",
    random.Random(S.SEED))
check("a one-line derivation is skipped", where is None)

# ── ramp-inversion ──────────────────────────────────────────────────────────
print("\nramp-inversion reverses the ramp by problem id:")

DATA = {"problems": [
    {"id": 1, "type": "eval", "expr": "1+1", "expected": 2, "difficulty": 1},
    {"id": 2, "type": "eval", "expr": "2+2", "expected": 4, "difficulty": 2},
    {"id": 3, "type": "eval", "expr": "3+3", "expected": 6, "difficulty": 3},
    # id 4 carries TWO entries: render_meta.py hard-fails on a difficulty that
    # conflicts across entries, because the tag is student-visible. An earlier
    # version assigned positionally over the entry list and the gate stopped
    # the build — correctly, but on a harness bug rather than the defect.
    {"id": 4, "type": "eval", "expr": "4+4", "expected": 8, "difficulty": 4},
    {"id": 4, "type": "manual", "desc": "explain it", "difficulty": 4},
]}

out, where = S.seed_ramp_inversion(copy.deepcopy(DATA), rng)
got = {}
for p in out["problems"]:
    got.setdefault(p["id"], set()).add(p["difficulty"])
check("the ramp is reversed", [min(got[i]) for i in sorted(got)] == [4, 3, 2, 1],
      where)
check("every entry of one id keeps ONE difficulty",
      all(len(v) == 1 for v in got.values()))
check("nothing but difficulty changes",
      [p.get("expr") for p in out["problems"]]
      == [p.get("expr") for p in DATA["problems"]])

flat = {"problems": [{"id": i, "difficulty": 3} for i in range(1, 6)]}
_, where = S.seed_ramp_inversion(copy.deepcopy(flat), rng)
check("a flat ramp is skipped — inverting it changes nothing", where is None)

short = {"problems": [{"id": i, "difficulty": i} for i in (1, 2)]}
_, where = S.seed_ramp_inversion(copy.deepcopy(short), rng)
check("a sheet too short to have a ramp is skipped", where is None)

# ── vague-rubric ────────────────────────────────────────────────────────────
print("\nvague-rubric blanks a grading criterion without naming anything wrong:")

M = {"problems": [
    {"id": 1, "type": "eval", "expr": "1+1", "expected": 2},
    {"id": 2, "type": "manual", "desc": "Part (b): the student explains that "
     "doubling the radius quadruples the area, citing the squared factor."},
]}
out, where = S.seed_vague_rubric(copy.deepcopy(M), rng)
check("it replaces a substantive manual desc", where is not None, where)
check("the replacement names nothing from the problem",
      out["problems"][1]["desc"] == "Grade the student's explanation.")
check("the machine-checked entry is untouched",
      out["problems"][0] == M["problems"][0])

_, where = S.seed_vague_rubric(
    {"problems": [{"id": 1, "type": "eval", "expr": "1+1", "expected": 2}]}, rng)
check("a sheet with no manual entry is skipped", where is None)

_, where = S.seed_vague_rubric(
    {"problems": [{"id": 1, "type": "manual", "desc": "Explain."}]}, rng)
check("an already-terse desc is skipped — there is nothing to hollow out",
      where is None)

# ── control ─────────────────────────────────────────────────────────────────
print("\ncontrol changes nothing:")
out, where = S.seed_control(AK, rng)
check("the text is returned byte-identical", out == AK)
check("it still reports a location, so it appears in the manifest",
      where == "unmodified control")

# ── the catalogue is self-describing ────────────────────────────────────────
print("\nthe catalogue states, for every entry, why no gate reads it:")
for name, spec in S.CATALOGUE.items():
    check(f"{name} declares its ungated reason and expected detection",
          bool(spec.get("why_ungated")) and bool(spec.get("expect")))
check("control is present — without it a detection rate has no "
      "false-positive denominator", "control" in S.CATALOGUE)
check("the RNG seed is pinned, so the manifest describes a replayable run",
      isinstance(S.SEED, int))

print()
if FAILS:
    print(f"❌ {len(FAILS)} seeder test(s) failed: {FAILS}")
    sys.exit(1)
print("✅ All calibration-seeder tests passed")
