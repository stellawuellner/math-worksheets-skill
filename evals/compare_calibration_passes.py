#!/usr/bin/env python3
"""pass2_harness.py — compare a second calibration judging pass against the
sealed manifest and against pass 1.

Usage: pass2_harness.py <verdicts_dir> [--pass1 <verdicts_dir>]

Deliberately in the SCRATCHPAD, not the repo, while judging is live: nothing
the judge could read may change mid-pass. It moves into the repo with the
pass-2 analysis, after the verdicts land.

What it computes mechanically:
  - judge-model census (the single-instrument requirement, checked first)
  - accept/reject per case, agreement vs pass 1, mean score deltas
  - v2 transcription compliance: does each verdict carry the mandatory
    bank rows, a "ramp:" line, and a manual-rubric + grader-decision line?
    (These are NEW in the updated rubric; pass 1 predates them, so pass-1
    compliance ~0 is expected and is the baseline.)
  - for every SEEDED case: the verdict, and every hard-failure/error text,
    printed BESIDE the manifest's planted location

What it refuses to compute: detection. The first calibration's scorer matched
keywords and reported 0/15 when the truth was 3/15 — the judge described
defects concretely, not in the seeder's vocabulary. Detection is decided by
READING each citation against the manifest location, so this prints the
pairings and a human (or the agent, carefully) adjudicates each one.
"""
import json
import os
import sys

ROOT = "/home/user/math-worksheets-skill"
MANIFEST = os.path.join(ROOT, "evals", "analysis",
                        "curriculum-shardX-20260808T033421Z",
                        "seed-manifest.json")
PASS1 = os.path.join(ROOT, "evals", "runs",
                     "curriculum-shardX-20260808T033421Z", "verdicts")


def load_verdicts(d):
    out = {}
    for f in sorted(os.listdir(d)):
        if f.endswith(".json"):
            v = json.load(open(os.path.join(d, f)))
            out[v["task_id"]] = v
    return out


def transcription_compliance(v):
    text = " ".join(v.get("artifact_findings", []))
    return {
        "bank_rows": "bank row" in text,
        "ramp": "ramp:" in text,
        "manual_rubric": ("manual rubric" in text
                          and ("grader decision" in text or "<none>" in text)),
    }


def main():
    p2_dir = sys.argv[1]
    p1_dir = sys.argv[sys.argv.index("--pass1") + 1] if "--pass1" in sys.argv else PASS1
    man = json.load(open(MANIFEST))
    # manifest keys: "task", "defect" ("control" for the untouched sheets),
    # "where" for the planted location
    entries = {e["task"]: e for e in man["entries"]}
    seeded = {t: e for t, e in entries.items() if e["defect"] != "control"}
    p1 = load_verdicts(p1_dir)
    p2 = load_verdicts(p2_dir)

    print(f"pass-2 verdicts: {len(p2)}   pass-1: {len(p1)}   "
          f"manifest: {len(seeded)} seeded + {len(entries) - len(seeded)} controls")

    models = {}
    for v in p2.values():
        m = v.get("judge", {}).get("model", "?")
        models[m] = models.get(m, 0) + 1
    print(f"judge models: {models}"
          + ("   <-- MIXED: per-class rates are estimates" if len(models) > 1
             else "   (single instrument ok)"))

    agree = mixed = 0
    diffs = []
    for tid, v in sorted(p2.items()):
        w1 = p1.get(tid, {}).get("verdict")
        w2 = v.get("verdict")
        if w1 == w2:
            agree += 1
        else:
            diffs.append((tid, w1, w2))
        s1 = p1.get(tid, {}).get("total_score")
        s2 = v.get("total_score")
        if isinstance(s1, int) and isinstance(s2, int):
            mixed += abs(s1 - s2)
    n = len(p2)
    print(f"\nverdict agreement vs pass 1: {agree}/{n} "
          f"({100 * agree / n:.0f}%)   mean |score delta|: {mixed / n:.2f}")
    for tid, a, b in diffs:
        print(f"  flip {tid}: pass1={a} pass2={b}")

    comp = {k: 0 for k in ("bank_rows", "ramp", "manual_rubric")}
    for v in p2.values():
        for k, ok in transcription_compliance(v).items():
            comp[k] += ok
    print(f"\ntranscription compliance (of {n}): {comp}")
    if comp["ramp"] < n or comp["manual_rubric"] < n:
        print("  NOTE: a verdict skipping a mandatory transcription is itself"
              " a finding about the judge — list them:")
        for tid, v in sorted(p2.items()):
            c = transcription_compliance(v)
            missing = [k for k, ok in c.items() if not ok]
            if missing:
                print(f"    {tid}: missing {missing}")

    print("\n" + "=" * 72)
    print("SEEDED CASES — adjudicate each citation against the manifest.")
    print("A rejection is NOT a detection unless it cites the planted defect.")
    print("=" * 72)
    by_class = {}
    for tid, entry in sorted(seeded.items()):
        v = p2.get(tid)
        if v is None:
            print(f"\n--- {tid}  [{entry['defect']}]  NO PASS-2 VERDICT")
            continue
        by_class.setdefault(entry["defect"], []).append(tid)
        print(f"\n--- {tid}  [{entry['defect']}]  pass2={v['verdict']} "
              f"({v.get('total_score')}/32)   planted: {entry.get('where','?')[:160]}")
        cited = (v.get("hard_failures", [])
                 + [e.get("description", str(e)) if isinstance(e, dict) else str(e)
                    for e in v.get("errors", [])])
        for c in cited[:6]:
            print(f"      cites: {str(c)[:200]}")
        if not cited:
            print("      cites: (nothing)")

    print("\n" + "=" * 72)
    print("CONTROLS — any rejection here needs the curr-082 treatment:")
    print("verify each citation against the artifacts before calling it real.")
    print("=" * 72)
    controls = [t for t in p2 if t not in seeded]
    for tid in sorted(controls):
        v = p2[tid]
        mark = "  <-- REJECTED, ADJUDICATE" if v["verdict"] != "ACCEPT" else ""
        print(f"  {tid}: {v['verdict']} ({v.get('total_score')}/32){mark}")
        if v["verdict"] != "ACCEPT":
            for c in v.get("hard_failures", [])[:3]:
                print(f"      cites: {str(c)[:200]}")


if __name__ == "__main__":
    main()
