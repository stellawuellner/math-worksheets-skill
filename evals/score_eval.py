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

4. Take a quoted value on trust. A finding that says the key prints 36 is
   evidence only if 36 is printed somewhere in the artifacts. Every numeric and
   symbolic value quoted in a verdict is looked up in the extracted text and the
   verification JSON; the ones that are not there are listed. PDF extraction is
   lossy — `\\frac{3}{5}` comes out as "35" and radicals come out mangled — so a
   miss is reported for adjudication, never used to overturn a judgment.

5. Trust the judge to have opened the Quick Answers bank. A 300-case review
   found answer_key_quality scored 4/4 in 107 of 124 cases whose bank was
   defective. The bank is deterministic, so the harness regenerates it from
   verify.json (via scripts/render_quick_answers.render) and compares it to the
   bank the shipped answer_key.pdf prints; it also reruns the answer-slot gate
   (tests/check_answer_slots.py, version-stamped) and cross-checks standards
   codes against references/standards-map.md. Blocking bank/slot contradictions
   are ACCEPT-blocking exactly like the gate-chain contradiction; ambiguous
   extractions and all standards findings are flagged for adjudication instead
   ("a miss is a flag, not proof"). --skip-machine-checks disables this layer
   for harness debugging only.

Verdicts may additionally carry an OPTIONAL `scores_v2` block (plus
`hard_failures_v2`) scored under evals/curriculum-judge-rubric-v2.md. The
official verdict is computed from the v1 scores exactly as before; when
`scores_v2` is present a shadow v2 verdict is derived with the same arithmetic
and reported side by side. A verdict without `scores_v2` is complete — the v2
block is forward compatibility, not a new requirement.
"""
import argparse
import importlib.util
import json
import os
import re
import shutil
import statistics
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, "evals", "runs")
MIN_DIMENSION = 3
MIN_TOTAL = 27
MAX_TOTAL = 32


def _load_scoring_harness():
    """The claim audit lives with the rest of the harness; share it, don't fork it."""
    path = os.path.join(ROOT, "scripts", "score_eval_run.py")
    if not os.path.isfile(path):
        return None
    spec = importlib.util.spec_from_file_location("score_eval_run", path)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception:  # a broken sibling must not block scoring
        return None
    return module


HARNESS = _load_scoring_harness()
ARTIFACT_PDFS = ("worksheet.pdf", "answer_key.pdf", "study_guide.pdf")
ARTIFACT_JSON = ("verify.json", "verify_study_guide.json")


def artifact_text(task_dir):
    """Everything the judge was shown, as text, for looking values up in."""
    texts = []
    if shutil.which("pdftotext"):
        for name in ARTIFACT_PDFS:
            path = os.path.join(task_dir, name)
            if os.path.isfile(path):
                proc = subprocess.run(["pdftotext", "-layout", path, "-"],
                                      capture_output=True, text=True, errors="replace")
                if proc.returncode == 0:
                    texts.append(proc.stdout)
    for name in ARTIFACT_JSON:
        path = os.path.join(task_dir, name)
        if os.path.isfile(path):
            with open(path, encoding="utf-8", errors="replace") as fh:
                texts.append(fh.read())
    return texts


def audit_claims(task_dir, verdict):
    """Values this verdict quotes that no artifact contains."""
    if HARNESS is None or not os.path.isdir(task_dir):
        return []
    texts = artifact_text(task_dir)
    if not any(text.strip() for text in texts):
        return []
    index = HARNESS.artifact_value_index(texts)
    return HARNESS.audit_verdict_claims(verdict, index)


def _read_text(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def _pdf_text(path):
    if not (shutil.which("pdftotext") and os.path.isfile(path)):
        return ""
    proc = subprocess.run(["pdftotext", "-layout", path, "-"],
                          capture_output=True, text=True, errors="replace")
    return proc.stdout if proc.returncode == 0 else ""


def machine_cross_checks(task_dir, task, standards_map=None):
    """Deterministic bank/slot/standards facts about one task's artifacts.

    Computed at aggregate time because `record` predates these checks and the
    retained observations are frozen evidence. Returns None when the shared
    harness is unavailable — scoring proceeds, minus this layer, exactly as it
    did before the layer existed.
    """
    if HARNESS is None or not os.path.isdir(task_dir):
        return None
    checks = {"bank": None, "slot_gate": None, "standards": []}
    key_text = _pdf_text(os.path.join(task_dir, "answer_key.pdf"))
    verify_path = os.path.join(task_dir, "verify.json")
    verify_data = None
    if os.path.isfile(verify_path):
        try:
            with open(verify_path, encoding="utf-8") as fh:
                verify_data = json.load(fh)
        except (OSError, json.JSONDecodeError):
            verify_data = None
    ws_path = os.path.join(task_dir, "worksheet.tex")
    ws_tex = _read_text(ws_path) if os.path.isfile(ws_path) else ""
    level = ""
    ak_tex = _read_text(os.path.join(task_dir, "answer_key.tex"))
    if ak_tex:
        m = re.search(r"\\aktitleblock\{[^{}]*\}\{([^{}]*)\}", ak_tex)
        level = m.group(1).strip() if m else ""

    if key_text and verify_data is not None:
        checks["bank"] = HARNESS.audit_shipped_bank(
            key_text, verify_data, level, ws_tex)
    checks["slot_gate"] = HARNESS.run_slot_gate(
        ws_path if os.path.isfile(ws_path) else None,
        verify_path if os.path.isfile(verify_path) else None)
    codes = {}
    if verify_data is not None:
        for entry in verify_data.get("problems", []):
            if isinstance(entry, dict) and entry.get("standard"):
                codes.setdefault(str(entry["standard"]), "verify.json standard tag")
    for code in HARNESS.printed_curriculum_codes(key_text):
        codes.setdefault(code, "printed Curriculum block")
    checks["standards"] = HARNESS.standards_map_flags(
        codes, task.get("band"), standards_map)
    return checks


def shadow_v2_verdict(verdict, dims):
    """Derive the optional rubric-v2 shadow verdict from `scores_v2`.

    Returns (result, note). result is None when no scores_v2 block exists —
    which is fine — and note is a string when the block exists but is
    malformed, which is reported without invalidating the v1 verdict.
    """
    scores = verdict.get("scores_v2")
    if scores is None:
        return None, None
    if not isinstance(scores, dict):
        return None, "scores_v2 is not an object of dimension scores"
    bad = [k for k in dims if not isinstance(scores.get(k), int)
           or not 0 <= scores[k] <= 4]
    extra = [k for k in scores if k not in dims]
    if bad or extra:
        return None, ("scores_v2 "
                      + (f"missing/invalid {', '.join(bad)}" if bad else "")
                      + (f" unknown dimension {', '.join(extra)}" if extra else ""))
    hard = verdict.get("hard_failures_v2") or []
    total = sum(scores[k] for k in dims)
    derived = ("ACCEPT" if not hard and total >= MIN_TOTAL
               and all(scores[k] >= MIN_DIMENSION for k in dims) else "REJECT")
    return {"verdict": derived, "total": total, "scores": scores,
            "hard_failures": hard}, None


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
    p.add_argument("--skip-machine-checks", action="store_true",
                   help="skip the bank-diff/slot-gate/standards layer "
                        "(harness debugging only)")
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
    unsupported, adjudicate = [], []
    machine_flags, v2_notes = [], []
    machine_fire_counts = {}
    slot_gate_version = None
    run_machine_checks = HARNESS is not None and not a.skip_machine_checks
    standards_map = HARNESS.load_standards_map() if run_machine_checks else None
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

        # Does every value this verdict quotes exist in the artifacts it read?
        claims = audit_claims(os.path.join(d, "tasks", tid), v)
        for item in claims:
            unsupported.append({"task_id": tid, **item})
        if any(item["blocking"] for item in claims):
            adjudicate.append(tid)

        # ---- machine cross-checks: bank diff, slot gate, standards map ----
        checks = machine_cross_checks(os.path.join(d, "tasks", tid), task,
                                      standards_map) if run_machine_checks else None
        if checks:
            bank = checks.get("bank") or {}
            for item in bank.get("findings", []):
                key = item["type"] + ("" if item["blocking"] else " (flag)")
                machine_fire_counts[key] = machine_fire_counts.get(key, 0) + 1
                if not item["blocking"]:
                    machine_flags.append({"task_id": tid, "type": item["type"],
                                          "message": item["message"]})
            sg = checks.get("slot_gate") or {}
            if sg.get("gate_version"):
                slot_gate_version = sg["gate_version"]
            if sg.get("checked") and sg.get("exit_code") != 0:
                machine_fire_counts["answer_slot_gate_failed"] = \
                    machine_fire_counts.get("answer_slot_gate_failed", 0) + 1
            for item in checks.get("standards", []):
                machine_fire_counts[item["type"] + " (flag)"] = \
                    machine_fire_counts.get(item["type"] + " (flag)", 0) + 1
                machine_flags.append({"task_id": tid, "type": item["type"],
                                      "message": item["message"]})

        # ---- optional rubric-v2 shadow scoring (never affects the verdict) --
        shadow, v2_note = shadow_v2_verdict(v, dims)
        if v2_note:
            v2_notes.append(f"{tid}: {v2_note}")

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
            if checks:
                for item in (checks.get("bank") or {}).get("findings", []):
                    if item["blocking"]:
                        contradictions.append(
                            f"{tid}: judged ACCEPT, but the shipped Quick "
                            f"Answers bank contradicts the verification data "
                            f"— {item['type']}: {item['message']}")
                sg = checks.get("slot_gate") or {}
                if sg.get("checked") and sg.get("exit_code") != 0:
                    contradictions.append(
                        f"{tid}: judged ACCEPT, but the answer-slot gate "
                        f"fails (exit {sg['exit_code']}) under "
                        f"[{sg['gate_version']}]"
                        + (f" — first fault: {sg['faults'][0]}"
                           if sg.get("faults") else ""))
        rows.append({"task_id": tid, "generator_model": per_task_gen.get(tid, gen["model"]),
                     "band": task.get("band", "?"),
                     "domain": task.get("domain", "?"), "verdict": derived,
                     "total": total, "scores": scores, "hard_failures": hard,
                     "manual_items": v.get("manual_items_reviewed", 0),
                     "gate_passed": obs.get("gate_chain_passed"),
                     "latency": obs.get("latency_seconds"),
                     "v2": shadow})

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

    # ---- shadow rubric-v2 verdicts: reported beside v1, never instead of it
    v2_rows = [r for r in rows if r.get("v2")]
    if v2_rows:
        v2_accepted = [r for r in v2_rows if r["v2"]["verdict"] == "ACCEPT"]
        v1_accepted_sub = [r for r in v2_rows if r["verdict"] == "ACCEPT"]
        lines += ["## Shadow verdicts under rubric v2", "",
                  "The official verdict above is computed from the v1 scores,",
                  "unchanged. These verdicts also carry a `scores_v2` block",
                  "(evals/curriculum-judge-rubric-v2.md, behavioral anchors);",
                  "the same acceptance arithmetic applied to it gives a shadow",
                  "verdict, reported here side by side. Tasks without",
                  "`scores_v2` are complete verdicts and simply do not appear.",
                  "",
                  f"| Metric | v1 | v2 (shadow) |", "| --- | --- | --- |",
                  f"| Verdicts carrying scores_v2 | {len(v2_rows)} | {len(v2_rows)} |",
                  f"| Acceptance among them | {len(v1_accepted_sub)}/{len(v2_rows)} "
                  f"({pct(len(v1_accepted_sub), len(v2_rows))}) | "
                  f"{len(v2_accepted)}/{len(v2_rows)} "
                  f"({pct(len(v2_accepted), len(v2_rows))}) |",
                  f"| Mean total among them | "
                  f"{statistics.mean([r['total'] for r in v2_rows]):.1f}/{MAX_TOTAL} | "
                  f"{statistics.mean([r['v2']['total'] for r in v2_rows]):.1f}/{MAX_TOTAL} |",
                  "", "| Dimension | v1 mean | v2 mean |", "| --- | --- | --- |"]
        for k in dims:
            lines.append(
                f"| {k} | {statistics.mean([r['scores'][k] for r in v2_rows]):.2f} | "
                f"{statistics.mean([r['v2']['scores'][k] for r in v2_rows]):.2f} |")
        lines.append("")
        moved = [r for r in v2_rows if r["v2"]["verdict"] != r["verdict"]]
        if moved:
            lines += ["Verdicts that move under v2:", ""]
            lines += [f"- {r['task_id']}: v1 {r['verdict']} "
                      f"({r['total']}/{MAX_TOTAL}) → v2 {r['v2']['verdict']} "
                      f"({r['v2']['total']}/{MAX_TOTAL})"
                      + (f" — v2 hard failures: {'; '.join(r['v2']['hard_failures'])}"
                         if r["v2"]["hard_failures"] else "")
                      for r in moved] + [""]
    if v2_notes:
        lines += ["### scores_v2 notes (non-invalidating)", "",
                  "A malformed `scores_v2` block never invalidates the v1",
                  "verdict; it is simply not shadow-scored.", ""]
        lines += [f"- {n}" for n in v2_notes] + [""]

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
    if run_machine_checks:
        lines += ["## Machine cross-checks", "",
                  "Deterministic facts recomputed from the shipped artifacts at",
                  "scoring time: the Quick Answers bank regenerated from",
                  "verify.json vs the bank the answer key prints, the answer-slot",
                  "gate, and the standards map. Fire counts are over all judged",
                  "tasks; a large count on a pre-fix corpus is expected and is",
                  "part of the run-to-run comparison, not noise.", ""]
        if slot_gate_version:
            lines += [f"- answer-slot gate version: `{slot_gate_version}` — "
                      "compare counts only between runs scored under the same "
                      "gate version.", ""]
        if machine_fire_counts:
            lines += ["| Check | Fires |", "| --- | --- |"]
            for key in sorted(machine_fire_counts):
                lines.append(f"| {key} | {machine_fire_counts[key]} |")
            lines.append("")
        else:
            lines += ["No machine cross-check fired on any judged task.", ""]
        if machine_flags:
            lines += ["### Flagged for adjudication (machine cross-checks)", "",
                      "Extraction-ambiguous bank rows and all standards-map",
                      "findings. A flag is a request for a person to look, not a",
                      "verdict override.", "",
                      "| Task | Type | Detail |", "| --- | --- | --- |"]
            for item in machine_flags[:200]:
                detail = item["message"].replace("|", "\\|")
                lines.append(f"| {item['task_id']} | {item['type']} | {detail} |")
            lines.append("")
    if unsupported:
        lines += ["## Claims not found in the artifacts", "",
                  "Values a verdict quotes that appear nowhere in the extracted PDF",
                  "text or the verification JSON. A finding that recites a number the",
                  "artifact does not contain was not read off the artifact. Extraction",
                  "is lossy, so adjudicate these rather than counting them as errors;",
                  "the **blocking** ones are hard failures, where the recited value is",
                  "the whole basis for a rejection.", "",
                  "| Task | Field | Value | Blocking |", "| --- | --- | --- | --- |"]
        for item in unsupported:
            lines.append(f"| {item['task_id']} | {item['field']} | `{item['value']}` | "
                         f"{'**yes**' if item['blocking'] else 'no'} |")
        lines.append("")
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
    if unsupported:
        print(f"⚠️  {len(unsupported)} quoted value(s) in "
              f"{len({u['task_id'] for u in unsupported})} verdict(s) are not in the artifacts")
    if adjudicate:
        print(f"❌ {len(adjudicate)} verdict(s) rest on a hard failure citing a value the "
              f"artifact does not contain: {', '.join(sorted(adjudicate))}")
    if machine_fire_counts:
        print("⚠️  machine cross-checks fired: "
              + ", ".join(f"{k}={v}" for k, v in sorted(machine_fire_counts.items())))
    if v2_rows:
        print(f"ℹ️  shadow rubric-v2: {len(v2_accepted)}/{len(v2_rows)} ACCEPT "
              f"(v1 over the same verdicts: {len(v1_accepted_sub)}/{len(v2_rows)})")
    print(f"report: {os.path.relpath(out, ROOT)}")
    return 1 if contradictions or adjudicate else 0


if __name__ == "__main__":
    sys.exit(main())
