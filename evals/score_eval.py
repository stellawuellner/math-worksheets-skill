#!/usr/bin/env python3
"""score_eval.py — aggregate an independent judge's verdicts into a run report.

Usage:
  score_eval.py [--run ID] [--allow-self-judging]

WHAT THIS REFUSES TO DO
1. Score a run judged by the model that generated it. The generator is recorded
   in run.json when the run starts; the judge names itself in every verdict. If
   they match, this exits without producing a report. A model grading its own
   homework produces a number, and the number is worthless — worse than absent,
   because it looks like evidence. --allow-self-judging exists for harness
   testing and stamps the report as unusable.

2. Take a verdict's own ACCEPT at face value. The rubric's acceptance rule is
   arithmetic — no hard failures, every dimension at least 3, total at least
   27 of 32 — so it is recomputed from the scores. A verdict claiming ACCEPT on
   a dimension of 2 is a judging error, and the report names it rather than
   averaging it in.

3. Ignore what the harness already knew. `record` measured things the judge was
   deliberately not shown: whether three PDFs exist, whether the printed problem
   count matches the task, whether the gate chain passed. An ACCEPT on a task
   with a missing PDF is not a disagreement about quality; it means the judge
   did not look. Those contradictions are reported separately from the scores.
"""
import argparse
import json
import os
import statistics
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, "evals", "runs")
MIN_DIMENSION = 3
MIN_TOTAL = 27
MAX_TOTAL = 32


def die(msg, code=2):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def load(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        die(f"cannot read {path}: {exc}")


def pct(n, d):
    return f"{100.0 * n / d:.1f}%" if d else "n/a"


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--run")
    p.add_argument("--allow-self-judging", action="store_true")
    a = p.parse_args(argv)

    if a.run:
        d = os.path.join(RUNS, a.run)
    else:
        runs = sorted(x for x in os.listdir(RUNS)
                      if os.path.isfile(os.path.join(RUNS, x, "run.json"))) \
            if os.path.isdir(RUNS) else []
        if not runs:
            die("no runs found")
        d = os.path.join(RUNS, runs[-1])
    if not os.path.isfile(os.path.join(d, "run.json")):
        die(f"not a run directory: {d}")
    run = load(os.path.join(d, "run.json"))
    suite = load(os.path.join(ROOT, run["suite_file"]))
    dims = list(suite["judge_protocol"]["quality_dimensions"])

    vdir = os.path.join(d, "verdicts")
    verdicts = {}
    for name in sorted(os.listdir(vdir)) if os.path.isdir(vdir) else []:
        if name.endswith(".json"):
            v = load(os.path.join(vdir, name))
            verdicts[v.get("task_id", name[:-5])] = v
    if not verdicts:
        die(f"no verdicts in {os.path.relpath(vdir, ROOT)} — the judge has not run yet")

    # ---- independence, before anything is counted
    gen = run["generator"]
    # A run may be authored by a fleet. Independence has to hold against every
    # model that actually made something, not just the run's default label —
    # otherwise one subagent on the judge's own model slips through.
    obs_dir = os.path.join(d, "observations")
    per_task_gen = {}
    for name in sorted(os.listdir(obs_dir)) if os.path.isdir(obs_dir) else []:
        o = load(os.path.join(obs_dir, name))
        per_task_gen[o["task_id"]] = o.get("generator", gen).get("model", gen["model"])
    gen_models = {m for m in per_task_gen.values() if m} or {gen["model"]}
    judges = {(v.get("judge", {}).get("agent", "?"), v.get("judge", {}).get("model", "?"))
              for v in verdicts.values()}
    clashes = [j for j in judges
               if j[1] and any(j[1].lower() == m.lower() for m in gen_models)]
    if clashes and not a.allow_self_judging:
        print("❌ refusing to score: the judge is the model that generated this run")
        for m in sorted(gen_models):
            print(f"   generator : {m}")
        for agent, model in sorted(clashes):
            print(f"   judge     : {agent} / {model}")
        print("\n   Have a different model judge these artifacts. The run directory is\n"
              "   self-contained — hand another agent the JUDGING.md brief and let it\n"
              "   write into verdicts/. Nothing needs regenerating.")
        return 1

    missing_verdicts = [t for t in run["task_ids"] if t not in verdicts]
    stray = [t for t in verdicts if t not in run["task_ids"]]

    rows, malformed, contradictions = [], [], []
    for tid in run["task_ids"]:
        v = verdicts.get(tid)
        if not v:
            continue
        scores = v.get("dimension_scores", {})
        bad = [k for k in dims if not isinstance(scores.get(k), int)
               or not 0 <= scores[k] <= 4]
        extra = [k for k in scores if k not in dims]
        if bad or extra:
            malformed.append(f"{tid}: "
                             + (f"missing/invalid {', '.join(bad)}" if bad else "")
                             + (f" unknown dimension {', '.join(extra)}" if extra else ""))
            continue
        total = sum(scores[k] for k in dims)
        hard = v.get("hard_failures") or []
        derived = ("ACCEPT" if not hard and total >= MIN_TOTAL
                   and all(scores[k] >= MIN_DIMENSION for k in dims) else "REJECT")
        claimed = (v.get("verdict") or "").upper()
        if claimed and claimed != derived:
            malformed.append(f"{tid}: verdict says {claimed} but the scores derive "
                             f"{derived} (total {total}/{MAX_TOTAL}, "
                             f"min dimension {min(scores[k] for k in dims)})")
        if v.get("total_score") is not None and v["total_score"] != total:
            malformed.append(f"{tid}: total_score {v['total_score']} does not match "
                             f"the sum of its dimensions ({total})")

        obs_path = os.path.join(d, "observations", f"{tid}.json")
        obs = load(obs_path) if os.path.isfile(obs_path) else {}
        task = load(os.path.join(d, "tasks", tid, "task.json"))
        if derived == "ACCEPT":
            # Things the judge could not see, that an ACCEPT cannot survive.
            for label, ok in (("a required PDF is missing",
                               all(obs.get("artifacts_present", {}).get(n, True)
                                   for n in ("worksheet.pdf", "answer_key.pdf",
                                             "study_guide.pdf"))),
                              ("the printed problem count does not match the task",
                               obs.get("problem_count_matches", True)),
                              ("the repository gate chain did not pass",
                               obs.get("gate_chain_passed", True))):
                if not ok:
                    contradictions.append(f"{tid}: judged ACCEPT, but {label}")
        rows.append({"task_id": tid, "generator_model": per_task_gen.get(tid, gen["model"]),
                     "band": task.get("band", "?"),
                     "domain": task.get("domain", "?"), "verdict": derived,
                     "total": total, "scores": scores, "hard_failures": hard,
                     "manual_items": v.get("manual_items_reviewed", 0),
                     "gate_passed": obs.get("gate_chain_passed"),
                     "latency": obs.get("latency_seconds")})

    judged = len(rows)
    accepted = [r for r in rows if r["verdict"] == "ACCEPT"]
    gate_passed = [r for r in rows if r["gate_passed"]]

    def by(key):
        groups = {}
        for r in rows:
            groups.setdefault(r[key], []).append(r)
        return {k: (sum(1 for r in v if r["verdict"] == "ACCEPT"), len(v))
                for k, v in sorted(groups.items())}

    lines = [f"# Eval report — `{run['run_id']}`", "",
             f"- suite: `{run['suite']}` shard {run['shard']}",
             f"- repo commit: `{run['repo_commit']}`",
             "- generator: " + ", ".join(f"**{m}**" for m in sorted(gen_models)),
             f"- judge: " + ", ".join(f"**{ag} / {mo}**" for ag, mo in sorted(judges)),
             f"- tasks in run: {len(run['task_ids'])} · judged: {judged}", ""]
    if a.allow_self_judging and clashes:
        lines += ["> **This report is not usable as evidence.** It was produced with",
                  "> `--allow-self-judging`: the generator and the judge are the same",
                  "> model, so the scores measure self-assessment, not quality.", ""]
    if missing_verdicts:
        lines += [f"> {len(missing_verdicts)} task(s) in this run have no verdict and are",
                  "> excluded below. Rates are over judged tasks, not over the run.", ""]

    lines += ["## Headline", "",
              "| Metric | Value |", "| --- | --- |",
              f"| Acceptance rate | **{pct(len(accepted), judged)}** "
              f"({len(accepted)}/{judged}) |",
              f"| Hard-gate pass rate | {pct(len(gate_passed), judged)} |",
              f"| Mean quality among gate passes | "
              f"{statistics.mean([r['total'] for r in gate_passed]):.1f}/{MAX_TOTAL} |"
              if gate_passed else "| Mean quality among gate passes | n/a |",
              f"| Manual items reviewed | {sum(r['manual_items'] for r in rows)} |", ""]

    if len(gen_models) > 1:
        lines += ["## Acceptance by generating model", "",
                  "The same tasks, different models driving the skill. Read this",
                  "alongside the band table — a model that is only weak on one band",
                  "is a different finding from one that is weak everywhere.", "",
                  "| Model | Accepted | Mean score |", "| --- | --- | --- |"]
        for m in sorted(gen_models):
            sub = [r for r in rows if r["generator_model"] == m]
            if not sub:
                continue
            ok = sum(1 for r in sub if r["verdict"] == "ACCEPT")
            lines.append(f"| {m} | {ok}/{len(sub)} ({pct(ok, len(sub))}) | "
                         f"{statistics.mean([r['total'] for r in sub]):.1f}/{MAX_TOTAL} |")
        lines.append("")
    else:
        lines += [f"_All tasks generated by `{sorted(gen_models)[0]}`. Re-run the same",
                  "task list under another model to compare; the report grows a",
                  "per-model table automatically once a run contains more than one._", ""]

    for label, key in (("band", "band"), ("domain", "domain")):
        lines += [f"## Acceptance by {label}", "", f"| {label.title()} | Accepted |",
                  "| --- | --- |"]
        for k, (ok, n) in by(key).items():
            lines.append(f"| {k} | {ok}/{n} ({pct(ok, n)}) |")
        lines.append("")

    weak = {k: statistics.mean([r["scores"][k] for r in rows]) for k in dims} if rows else {}
    lines += ["## Dimension means", "", "| Dimension | Mean |", "| --- | --- |"]
    for k, m in sorted(weak.items(), key=lambda kv: kv[1]):
        lines.append(f"| {k} | {m:.2f} |")
    lines.append("")

    fails = [r for r in rows if r["verdict"] == "REJECT"]
    if fails:
        lines += ["## Rejected", "", "| Task | Total | Hard failures |", "| --- | --- | --- |"]
        for r in fails:
            hf = "; ".join(r["hard_failures"]) if r["hard_failures"] else "scores below threshold"
            lines.append(f"| {r['task_id']} | {r['total']}/{MAX_TOTAL} | {hf} |")
        lines.append("")
    if malformed:
        lines += ["## Judging errors", "",
                  "Verdicts whose own arithmetic does not hold. Counted by their",
                  "recomputed value, not the one claimed.", ""]
        lines += [f"- {m}" for m in malformed] + [""]
    if contradictions:
        lines += ["## Contradicted by the harness", "",
                  "The judge was deliberately not shown these facts. An ACCEPT that",
                  "survives them means the artifacts were not actually inspected.", ""]
        lines += [f"- {c}" for c in contradictions] + [""]
    if stray:
        lines += ["## Stray verdicts", "",
                  "Verdicts for tasks that are not part of this run:", ""]
        lines += [f"- {s}" for s in stray] + [""]

    out = os.path.join(d, "report.md")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))

    print(f"acceptance {pct(len(accepted), judged)} ({len(accepted)}/{judged} judged)")
    if missing_verdicts:
        print(f"⚠️  {len(missing_verdicts)} task(s) unjudged and excluded")
    if malformed:
        print(f"⚠️  {len(malformed)} verdict(s) did not survive recomputation")
    if contradictions:
        print(f"❌ {len(contradictions)} ACCEPT(s) contradicted by mechanical facts")
    print(f"report: {os.path.relpath(out, ROOT)}")
    return 1 if contradictions else 0


if __name__ == "__main__":
    sys.exit(main())
