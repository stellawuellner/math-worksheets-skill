# v3.6.0 — Answer-key redesign, lean downloads, 95% coverage

> The annotated tag `v3.6.0` carries these same notes. This file exists so
> cutting the GitHub Release is copy-paste: *Releases → Draft a new release →
> choose tag `v3.6.0` → paste this body.* (The automation that prepared this
> release can push branches but not tags — the tag push is the one manual
> step, from any full-access checkout: `git push origin v3.6.0`.)

Since v2.0.0 — the previous release — this project became a different system.
Newest first:

## Answer keys (v3.6)
- Reading order: header → **Quick Answers** → worked solutions → a **final
  page of the key's own** for the verification + curriculum summary and the
  common-wrong-answers table (emitted via `\AtEndDocument`; no author change,
  every existing key picks it up on rebuild).
- Hand-judged answers are marked **`$\spadesuit$`** instead of an em dash; the
  summary page's legend explains the mark. The eval harness recognises both
  generations, because the retained corpus is a history.
- Keys breathe: rubber inter-problem space, `\raggedbottom`, flexible
  `\parskip`. Worksheets stay measured — work space there is a promise the
  page budget charges for.

## Packaging (v3.6)
- **Download ZIP / release tarballs are ~2 MB** (skill only, ~230 files); the
  286 MB eval corpus stays in clones via `.gitattributes` `export-ignore`.
  README's *Get the skill* section has the sparse-checkout recipe.
- Sample images regenerated from a fresh gate-passing build.

## Quality system (v3.3–v3.5)
- Coverage **92% → 95%** with an enforced floor of 93; four suites that were
  silently skipping in CI now run where TeX exists, guarded by a wiring test.
- **Version contract enforced**: sympy ≥ 1.12 floor + measured-baseline stamp
  (1.14.0) in every report; pgfplots ≥ 1.18 guarded with an actionable error;
  a scheduled CAS canary tests the newest sympy weekly.
- Study guides rebuilt on learning-science results: mandatory strategy step,
  retrieval try-its, self-explanation (`\why`) and fading (`\fadestep`)
  macros, declared page budgets (1–6), `--study-guide-only` builds.
- **Eval instrument calibrated with seeded defects**: 3/15 detection, 1/10
  false hard failure on clean controls, 68% inter-pass agreement — and the
  rubric now transcribes the two classes the judge proved blind to.
  Calibration runs refuse mixed judge models.
- New advisory lint for stems requesting a formula nothing verifies
  (20/20 on the corpus when measured).
- `\ans` fixed to work in text mode in study guides; `\spadesuit`-era bank
  cross-checks; LaTeX-injection escaping pinned per character.

Full changelog: [README.md#changelog](../README.md#changelog)
