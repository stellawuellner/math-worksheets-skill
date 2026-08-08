#!/usr/bin/env python3
"""seed_defects.py — build a calibration run by planting KNOWN defects.

Usage:
  seed_defects.py --source RUN_ID --run NEW_RUN_ID TASK[:DEFECT] ... [--dry-run]
  seed_defects.py --list

WHAT THIS MEASURES, AND WHY IT NEEDS ITS OWN RUN

A judge that scores every worksheet 4/5 is indistinguishable from a judge that
reads nothing, and the 300-case runs cannot tell the two apart: nobody knows
the true defect count, so a low fault rate reads equally as "the sheets are
good" and as "the judge is blind". Seeding fixes the denominator. Take sheets
that are known-clean, plant exactly one catalogued defect in some of them,
leave the rest untouched, and hand the mixture over blind. Then a detection
rate means something, and so does a false-positive rate — which is why the
CONTROLS are not padding. A judge that flags every sheet scores 100% detection
on a seeded-only set.

THE ADMISSION RULE: A SEEDED CASE MUST STILL PASS EVERY GATE

Each seeded case is rebuilt through the full build.sh chain and is admitted
only if the chain stays GREEN. That is not a convenience — it is the
definition of what this run is for. A defect a gate catches is already
handled; measuring the judge on it says nothing about the territory the judge
exists to cover. So a transform that trips a gate is DROPPED from the run and
reported as `gated`, and that outcome is itself a result worth reading: it
says the gate covers that class, and the catalogue entry should retire.

This is the adversarial twin of repair_artifacts.py and deliberately shares its
shape: deterministic transforms over stored artifacts, then the same gate chain
the original had to meet. The difference is only the direction of the change
and the sign of the expected verdict.

THE MANIFEST IS SEALED OUTSIDE THE RUN

evals/runs/<id>/ is what the judge reads. The answer key to this test therefore
goes to evals/analysis/<id>/SEALED-MANIFEST.md, following the precedent set
when FINDINGS.md and COMPARISON.md were moved out of the run-2 packet: a blind
test stops being blind the moment its answers ship beside it.
"""
import argparse
import json
import os
import random
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, "evals", "runs")
ANALYSIS = os.path.join(ROOT, "evals", "analysis")
# NEUTRALLY NAMED, and that is load-bearing: build.sh echoes its working paths
# into gate_log.txt, which ships to the judge — 35 mentions per log. The first
# staging dir was /tmp/seed_defects, and one grep over the first recorded run
# found the harness's own name on every page of the packet. A judge who reads
# "seed_defects" in a gate log knows planted defects exist and hunts for them,
# which corrupts the false-positive half of the calibration — the controls
# only measure a judge behaving normally. evalbuild3 follows the evalbuild2
# naming the genuine runs used, so the logs are indistinguishable.
WORK = os.path.join("/tmp", "evalbuild3")

# The seed is FIXED and recorded. Every choice this script makes at random —
# which step to corrupt, which manual entry to blank — must replay exactly, or
# the manifest describes a run that no longer exists.
SEED = 20260807


# ── The catalogue ───────────────────────────────────────────────────────────
# Every entry is a defect the 300-case review actually found, restricted to
# ones no gate reads. Each transform returns (new_text, where) with where=None
# when it did not apply, so a case that cannot carry its assigned defect is
# skipped loudly rather than shipped unseeded and counted as seeded.

def seed_worked_step_error(tex, rng):
    r"""Corrupt one number in a worked step; leave the boxed answer correct.

    check_answer_key binds the \ans{} BOX to the verified JSON. Nothing reads
    the align* lines above it, so a step can contradict the answer it derives
    and every gate stays green. This is the defect with the sharpest real-world
    cost in the whole catalogue: the box is right, so a student checking only
    the answer sees nothing, while a parent working through the derivation to
    explain it hits arithmetic that does not close.
    """
    blocks = list(re.finditer(r"\\begin\{align\*\}(.*?)\\end\{align\*\}",
                              tex, re.S))
    for m in rng.sample(blocks, len(blocks)):
        body = m.group(1)
        # Only touch an intermediate line: corrupting the last line would
        # contradict the box directly, which is a different (louder) defect.
        lines = body.split(r"\\")
        if len(lines) < 2:
            continue
        idx = 0
        nums = list(re.finditer(r"(?<![\d.])\d+(?![\d.])", lines[idx]))
        # Skip an exponent or a lone 1/2: changing those reads as a typo in
        # notation rather than an arithmetic slip a reader would try to follow.
        nums = [n for n in nums if lines[idx][max(0, n.start() - 1)] != "^"]
        if not nums:
            continue
        n = rng.choice(nums)
        old = n.group()
        # Never land on 0: a vanished term reads as a deliberate cancellation
        # rather than the slip in arithmetic this is meant to plant.
        shifted = int(old) + rng.choice([-2, -1, 1, 2])
        new = str(shifted if shifted != 0 else int(old) + 3)
        lines[idx] = lines[idx][:n.start()] + new + lines[idx][n.end():]
        newbody = r"\\".join(lines)
        return (tex[:m.start(1)] + newbody + tex[m.end(1):],
                f"align* step 1: {old} -> {new}")
    return (tex, None)


def seed_ramp_inversion(data, rng):
    """Reverse the declared difficulty ramp so the sheet starts hardest.

    The ramp report is exit-neutral by design (a spiral-review sheet is
    legitimately unsorted), so nothing fails. A teacher handing this out finds
    the class stalls on problem 1.
    """
    # Per problem ID, not per entry. A multi-response problem has several
    # entries sharing one id, and render_meta.py hard-fails on "conflicting
    # across entries" — a difficulty tag is student-visible through \probmeta,
    # so it cannot be two things at once. Assigning positionally over the entry
    # list gave two entries of id 4 different values and the gate stopped the
    # build, correctly. The defect being planted is a bad RAMP, not an
    # inconsistent tag.
    by_id = {}
    for p in data.get("problems", []):
        if isinstance(p, dict) and isinstance(p.get("difficulty"), int):
            by_id.setdefault(p["id"], []).append(p)
    ids = sorted(by_id)
    if len(ids) < 4:
        return (data, None)
    before = [by_id[i][0]["difficulty"] for i in ids]
    after = sorted(before, reverse=True)
    if after == before:
        return (data, None)          # already descending: nothing to invert
    for i, v in zip(ids, after):
        for p in by_id[i]:
            p["difficulty"] = v
    return (data, f"difficulty by id {before} -> {after}")


def seed_vague_rubric(data, rng):
    """Replace a manual desc with a rubric that grades nothing in particular.

    The stale-rubric lint fires on a desc naming a person or thing absent from
    the problem — a rubric left over from another draft. It does not, and
    should not, fire on vacuity: "Grade the explanation" names nothing wrong.
    But it tells a grader nothing either, and a manual entry's desc IS the
    grading criterion, so this is a silent hole in the only part of the sheet
    a machine never checks.
    """
    manuals = [p for p in data.get("problems", [])
               if isinstance(p, dict) and "expected" not in p
               and isinstance(p.get("desc"), str) and len(p["desc"]) > 60]
    if not manuals:
        return (data, None)
    p = rng.choice(manuals)
    before = p["desc"]
    p["desc"] = "Grade the student's explanation."
    return (data, f"manual id {p.get('id')}: {before[:70]!r} -> vague")


def seed_control(tex_or_data, rng):
    """No change. The false-positive denominator."""
    return (tex_or_data, "unmodified control")


CATALOGUE = {
    "worked-step-error": {
        "target": "answer_key.tex", "fn": seed_worked_step_error,
        "why_ungated": "check_answer_key binds the \\ans{} box, never the "
                       "worked steps above it",
        "expect": "the judge should find the derivation contradicts its own "
                  "boxed answer"},
    "ramp-inversion": {
        "target": "verify.json", "fn": seed_ramp_inversion,
        "why_ungated": "the difficulty-ramp report is exit-neutral — an "
                       "unsorted spiral-review sheet is legitimate",
        "expect": "the judge should notice the sheet opens at its hardest"},
    "vague-rubric": {
        "target": "verify.json", "fn": seed_vague_rubric,
        "why_ungated": "the stale-rubric lint fires on a wrong eponym, not on "
                       "a desc that names nothing at all",
        "expect": "the judge should notice a manual item whose rubric gives a "
                  "grader no criterion"},
    "control": {
        "target": None, "fn": seed_control,
        "why_ungated": "nothing was changed",
        "expect": "the judge should report no fault — this is the "
                  "false-positive denominator"},
}

DOCS = {"worksheet": "ws", "answer_key": "ak", "study_guide": "ss"}


def apply_defect(src, dst_stage, stem, defect, rng):
    """Stage one case into dst_stage, seeded. Returns `where` or None."""
    where = None
    spec = CATALOGUE[defect]
    data = json.load(open(os.path.join(src, "verify.json"), encoding="utf-8"))

    if spec["target"] == "verify.json":
        data, where = spec["fn"](data, rng)
        if where is None:
            return None
    json.dump(data, open(f"{dst_stage}/verify_{stem}.json", "w",
                         encoding="utf-8"), indent=2)
    ss = os.path.join(src, "verify_study_guide.json")
    if os.path.isfile(ss):
        shutil.copy(ss, f"{dst_stage}/verify_ss_{stem}.json")

    for doc, role in DOCS.items():
        p = os.path.join(src, f"{doc}.tex")
        if not os.path.isfile(p):
            return None
        tex = open(p, encoding="utf-8").read()
        if spec["target"] == f"{doc}.tex":
            tex, where = spec["fn"](tex, rng)
            if where is None:
                return None
        # Same companion-input rewrite repair_artifacts.py does: build.sh
        # regenerates qa_/figs_/meta_ under the CURRENT stem, so a document
        # rebuilt under a new stem must \input the new names.
        for pre in ("qa", "figs", "meta"):
            tex = re.sub(r"\\input\{" + pre + r"_[^}]*\}",
                         f"\\\\input{{{pre}_{stem}}}", tex)
        open(f"{dst_stage}/{role}_{stem}.tex", "w", encoding="utf-8").write(tex)
    return where or "unmodified control"


def record_case(run_id, tid, stage, src):
    """Record one green-built case into evals/runs/<run_id>/ via run_eval.py.

    Same invocation repair_artifacts.py uses — record derives every artifact
    from the stage directory's stem and refuses partial results, so a case
    either lands whole or not at all. The delivery response is carried over
    from the source unchanged: it is the message the generator actually wrote
    for these artifacts, and the transforms leave everything it describes
    (problem counts, files, coverage) true.
    """
    resp = os.path.join(src, "final_response.md")
    staged = os.path.join(stage, "final_response.md")
    if os.path.isfile(resp):
        shutil.copy(resp, staged)
    cmd = ["python3", os.path.join(ROOT, "evals", "run_eval.py"), "record",
           tid, "--run", run_id, "--from", stage,
           "--generator-model", "claude-fable-5"]
    if os.path.isfile(staged):
        cmd += ["--response-file", staged]
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    return (r.returncode == 0,
            (r.stdout + r.stderr).strip().splitlines()[-1][:160] if
            (r.stdout or r.stderr) else "")


def copy_packet(source_run, run_id, n_tasks):
    """Copy the judging brief and rubrics from a prior run, counts fixed up.

    The packet must read exactly like the source run's: a brief that mentioned
    seeding, calibration, or a changed procedure would unblind the test, and a
    rubric that drifted from the one the baseline was scored under would
    confound the sensitivity measurement with a rubric change — the exact
    mistake the run-1/run-2 comparison already has to disclose.
    """
    src = os.path.join(RUNS, source_run)
    dst = os.path.join(RUNS, run_id)
    for name in ("JUDGING.md", "rubric.md", "rubric-v2.md",
                 "JUDGING-V2-ADDENDUM.md", "standards-map.md"):
        p = os.path.join(src, name)
        if not os.path.isfile(p):
            continue
        text = open(p, encoding="utf-8").read()
        text = text.replace(source_run, run_id)
        text = text.replace("— 300 of them", f"— {n_tasks} of them")
        open(os.path.join(dst, name), "w", encoding="utf-8").write(text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true",
                    help="print the defect catalogue and exit")
    ap.add_argument("--source", help="run id to draw clean cases from")
    ap.add_argument("--run", help="new run id to write")
    ap.add_argument("--record-run",
                    help="an evals/runs/<id> already created by run_eval.py "
                         "start: record each green-built case into it and "
                         "copy the source run's judging packet. The run dir "
                         "carries NO trace of which cases are seeded — that "
                         "mapping goes only to the sealed manifest")
    ap.add_argument("--dry-run", action="store_true",
                    help="stage and seed, but do not build or record")
    ap.add_argument("tasks", nargs="*",
                    help="TASK_ID:DEFECT (defect defaults to 'control')")
    a = ap.parse_args()

    if a.list:
        for name, spec in CATALOGUE.items():
            print(f"{name}\n  target      : {spec['target'] or '(none)'}\n"
                  f"  ungated because: {spec['why_ungated']}\n"
                  f"  expected    : {spec['expect']}\n")
        return 0
    if not (a.source and a.run and a.tasks):
        ap.error("--source, --run and at least one task are required")

    src_run = os.path.join(RUNS, a.source)
    if not os.path.isfile(os.path.join(src_run, "run.json")):
        print(f"error: not a run: {src_run}", file=sys.stderr)
        return 2

    rng = random.Random(SEED)
    manifest, gated, skipped = [], [], []
    for spec in a.tasks:
        tid, _, defect = spec.partition(":")
        defect = defect or "control"
        if defect not in CATALOGUE:
            print(f"error: unknown defect {defect!r} (see --list)",
                  file=sys.stderr)
            return 2
        src = os.path.join(src_run, "tasks", tid)
        if not os.path.isfile(os.path.join(src, "verify.json")):
            skipped.append((tid, defect, "no stored verify.json"))
            print(f"  · {tid}: no stored verify.json", flush=True)
            continue

        stem = f"c_{tid.replace('-', '')}"
        stage = os.path.join(WORK, tid)
        shutil.rmtree(stage, ignore_errors=True)
        os.makedirs(stage)
        where = apply_defect(src, stage, stem, defect, rng)
        if where is None:
            skipped.append((tid, defect, "this case cannot carry that defect"))
            print(f"  · {tid}: cannot carry {defect}", flush=True)
            continue
        if a.dry_run:
            print(f"  ✅ {tid}: {defect} — {where} (dry run)", flush=True)
            manifest.append(dict(task=tid, defect=defect, where=where,
                                 built=False))
            continue

        log = os.path.join(stage, "gate_log.txt")
        with open(log, "w") as fh:
            r = subprocess.run(
                ["bash", os.path.join(ROOT, "scripts", "build.sh"),
                 f"{stage}/verify_{stem}.json", "--outdir", stage],
                stdout=fh, stderr=subprocess.STDOUT, cwd=ROOT)
        # 2 is "manual-review items present", which is a pass with honest
        # encoding — the same reading repair_artifacts.py uses.
        if r.returncode not in (0, 2):
            # THE ADMISSION RULE. A gate caught it, so it is not calibration
            # material: measuring the judge on a defect the chain already
            # stops tells us nothing about the uncovered territory.
            gated.append((tid, defect, f"build exit {r.returncode}"))
            print(f"  ⛔ {tid}: {defect} tripped a gate (exit "
                  f"{r.returncode}) — DROPPED, see {log}", flush=True)
            continue
        if a.record_run:
            ok, line = record_case(a.record_run, tid, stage, src)
            if not ok:
                # A case that built green but cannot be recorded is a harness
                # fault, not a judged case — it must not silently shrink the
                # denominator the manifest claims.
                gated.append((tid, defect, f"record failed: {line}"))
                print(f"  ❌ {tid}: {defect} built but did not record — "
                      f"{line}", flush=True)
                continue
        manifest.append(dict(task=tid, defect=defect, where=where, built=True,
                             build_exit=r.returncode, stage=stage))
        print(f"  ✅ {tid}: {defect} — {where}", flush=True)

    print(f"\nseeded {len([m for m in manifest if m['defect'] != 'control'])} "
          f"· controls {len([m for m in manifest if m['defect'] == 'control'])} "
          f"· gated-out {len(gated)} · skipped {len(skipped)}")
    if gated:
        print("\nDROPPED because a gate caught them — the gate covers this "
              "class, and the catalogue entry should retire:")
        for tid, d, why in gated:
            print(f"  ⛔ {tid}: {d} ({why})")
    if not a.dry_run and manifest and a.record_run:
        copy_packet(a.source, a.record_run, len(manifest))
        print(f"\njudging packet copied from {a.source} with counts fixed up")
    if not a.dry_run and manifest:
        os.makedirs(os.path.join(ANALYSIS, a.run), exist_ok=True)
        path = os.path.join(ANALYSIS, a.run, "seed-manifest.json")
        json.dump(dict(source_run=a.source, run=a.run, seed=SEED,
                       catalogue={k: v["expect"] for k, v in CATALOGUE.items()},
                       entries=manifest, gated_out=gated, skipped=skipped),
                  open(path, "w", encoding="utf-8"), indent=2)
        print(f"\nsealed manifest -> {os.path.relpath(path, ROOT)}")
        print("It is OUTSIDE evals/runs/ on purpose: a blind test stops being "
              "blind the moment its answers ship beside it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
